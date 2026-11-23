package com.max.hive;

import android.app.NotificationManager;
import android.app.Service;
import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Build;
import android.os.Handler;
import android.os.IBinder;
import android.os.Looper;
import org.json.JSONArray;
import org.json.JSONObject;
import java.io.BufferedReader;
import java.io.InputStreamReader;
import java.net.HttpURLConnection;
import java.net.URL;
import java.net.URLEncoder;
import java.util.ArrayList;
import java.util.Collections;
import java.util.HashSet;
import java.util.List;
import java.util.Set;

public class SheetSyncService extends Service {
    public static final String PREF_SHEET_URL = "pref_custom_sheet_url";
    public static final String PREF_MASTER_KEY = "pref_custom_master_key";
    public static final String LOCAL_FEED_URL = "http://10.0.0.111:7070/api/contact/feed";

    private static final String PREFS_NAME = "max_hive_prefs";
    private static final String KEY_SEEN_ROWS = "seen_ciphertexts";
    public static final int DEFAULT_PAGE_SIZE = 30;

    public interface SyncCallback {
        void onSyncComplete(List<IngestionItem> messages, List<IngestionItem> visits, int newItemsCount);
        void onSyncError(String error);
    }

    public interface PageCallback {
        void onPageLoaded(List<IngestionItem> newMessages, List<IngestionItem> newVisits, boolean hasMore);
        void onPageError(String error);
    }

    private static final List<IngestionItem> cachedMessages = new ArrayList<IngestionItem>();
    private static final List<IngestionItem> cachedVisits = new ArrayList<IngestionItem>();
    public static long cachedTotalVisitors = 0;
    public static long cachedTotalVisits = 0;
    public static long cachedTotalInquiries = 0;
    private static final List<SyncCallback> registeredCallbacks = new ArrayList<SyncCallback>();
    private static final Object SYNC_LOCK = new Object();

    private static boolean isSyncing = false;
    private static boolean isAppForeground = false;
    private static SheetSyncService instance;

    private Handler handler;
    private PollRunnable pollRunnable;

    public static void setAppForeground(boolean foreground) {
        isAppForeground = foreground;
        if (instance != null) {
            instance.handleForegroundChange(foreground);
        }
    }

    public void handleForegroundChange(boolean foreground) {
        if (!foreground) {
            try {
                stopForeground(true);
                NotificationManager nm = (NotificationManager) getSystemService(Context.NOTIFICATION_SERVICE);
                if (nm != null) {
                    nm.cancel(1001);
                }
            } catch (Throwable e) {}
        }
    }

    public static class PollRunnable implements Runnable {
        private final SheetSyncService service;

        public PollRunnable(SheetSyncService service) {
            this.service = service;
        }

        @Override
        public void run() {
            if (service != null && service.handler != null) {
                syncSheetData(service, false, null);
                long delayMs = isAppForeground ? 3500L : 30000L;
                service.handler.postDelayed(this, delayMs);
            }
        }
    }

    @Override
    public void onCreate() {
        super.onCreate();
        instance = this;
        NotificationHelper.initChannels(this);

        SharedPreferences prefs = getSharedPreferences(PREFS_NAME, Context.MODE_PRIVATE);
        boolean useForeground = prefs.getBoolean(SettingsActivity.PREF_FOREGROUND, false);
        if (useForeground && isAppForeground) {
            try {
                if (Build.VERSION.SDK_INT >= 34) {
                    startForeground(1001, NotificationHelper.buildForegroundNotification(this), android.content.pm.ServiceInfo.FOREGROUND_SERVICE_TYPE_DATA_SYNC);
                } else {
                    startForeground(1001, NotificationHelper.buildForegroundNotification(this));
                }
            } catch (Throwable e) {}
        }

        handler = new Handler(Looper.getMainLooper());
        pollRunnable = new PollRunnable(this);
        handler.post(pollRunnable);
    }

    @Override
    public int onStartCommand(Intent intent, int flags, int startId) {
        return START_STICKY;
    }

    @Override
    public IBinder onBind(Intent intent) {
        return null;
    }

    @Override
    public void onDestroy() {
        if (handler != null && pollRunnable != null) {
            handler.removeCallbacks(pollRunnable);
        }
        if (instance == this) {
            instance = null;
        }
        super.onDestroy();
    }

    public static void registerCallback(SyncCallback callback) {
        synchronized (registeredCallbacks) {
            if (callback != null && !registeredCallbacks.contains(callback)) {
                registeredCallbacks.add(callback);
                if (!cachedMessages.isEmpty() || !cachedVisits.isEmpty()) {
                    callback.onSyncComplete(new ArrayList<>(cachedMessages), new ArrayList<>(cachedVisits), 0);
                }
            }
        }
    }

    public static void unregisterCallback(SyncCallback callback) {
        synchronized (registeredCallbacks) {
            if (callback != null) {
                registeredCallbacks.remove(callback);
            }
        }
    }

    public static class NotifyCompleteRunnable implements Runnable {
        private final List<SyncCallback> callbacks;
        private final List<IngestionItem> messages;
        private final List<IngestionItem> visits;
        private final int newCount;

        public NotifyCompleteRunnable(List<SyncCallback> callbacks, List<IngestionItem> messages, List<IngestionItem> visits, int newCount) {
            this.callbacks = callbacks;
            this.messages = messages;
            this.visits = visits;
            this.newCount = newCount;
        }

        @Override
        public void run() {
            for (SyncCallback cb : callbacks) {
                if (cb != null) {
                    cb.onSyncComplete(messages, visits, newCount);
                }
            }
        }
    }

    public static class NotifyErrorRunnable implements Runnable {
        private final List<SyncCallback> callbacks;
        private final String error;

        public NotifyErrorRunnable(List<SyncCallback> callbacks, String error) {
            this.callbacks = callbacks;
            this.error = error;
        }

        @Override
        public void run() {
            for (SyncCallback cb : callbacks) {
                if (cb != null) {
                    cb.onSyncError(error);
                }
            }
        }
    }

    public static class SyncWorkerRunnable implements Runnable {
        private final Context context;
        private final int offset;
        private final int limit;
        private final PageCallback pageCallback;

        public SyncWorkerRunnable(Context context) {
            this(context, 0, DEFAULT_PAGE_SIZE, null);
        }

        public SyncWorkerRunnable(Context context, int offset, int limit, PageCallback pageCallback) {
            this.context = context;
            this.offset = offset;
            this.limit = limit;
            this.pageCallback = pageCallback;
        }

        @Override
        public void run() {
            List<SyncCallback> callbacksToNotify;
            try {
                SharedPreferences prefs = context.getSharedPreferences(PREFS_NAME, Context.MODE_PRIVATE);
                String sheetUrl = prefs.getString(PREF_SHEET_URL, "").trim();
                String masterKey = prefs.getString(PREF_MASTER_KEY, "").trim();

                if (sheetUrl.isEmpty() || masterKey.isEmpty()) {
                    if (pageCallback != null) {
                        new Handler(Looper.getMainLooper()).post(new Runnable() {
                            @Override public void run() {
                                pageCallback.onPageError("Setup Required: Configure Sheet URL & Master Key in Settings");
                            }
                        });
                    } else {
                        synchronized (registeredCallbacks) {
                            callbacksToNotify = new ArrayList<SyncCallback>(registeredCallbacks);
                        }
                        new Handler(Looper.getMainLooper()).post(
                            new NotifyErrorRunnable(callbacksToNotify, "Setup Required: Configure Sheet URL & Master Key in Settings")
                        );
                    }
                    synchronized (SYNC_LOCK) {
                        isSyncing = false;
                    }
                    return;
                }

                Set<String> seenSet = new HashSet<String>(prefs.getStringSet(KEY_SEEN_ROWS, new HashSet<String>()));
                boolean isFirstRun = seenSet.isEmpty();

                List<IngestionItem> messages = new ArrayList<IngestionItem>();
                List<IngestionItem> visits = new ArrayList<IngestionItem>();
                int newCount = 0;
                int notifIdCounter = 100;

                // -------------------------------------------------------------
                // 1. FAST LOCAL FEED (Sub-50ms Instant Sync on LAN / ADB Reverse)
                // -------------------------------------------------------------
                String[] localFeedEndpoints = new String[] {
                    "http://10.0.2.2:7070/api/contact/feed",
                    "http://127.0.0.1:7070/api/contact/feed",
                    "http://10.0.0.111:7070/api/contact/feed",
                    "http://10.0.2.2:7071/api/contact/feed",
                    "http://127.0.0.1:7071/api/contact/feed",
                    "http://10.0.0.111:7071/api/contact/feed"
                };

                boolean localConsumed = false;
                for (String feedEndpoint : localFeedEndpoints) {
                    try {
                        String fullFeedUrl = feedEndpoint + "?limit=" + limit + "&offset=" + offset;
                        URL localUrl = new URL(fullFeedUrl);
                        HttpURLConnection localConn = (HttpURLConnection) localUrl.openConnection();
                        localConn.setConnectTimeout(800);
                        localConn.setReadTimeout(800);
                        localConn.setRequestMethod("GET");

                        if (localConn.getResponseCode() == 200) {
                            java.io.InputStream inStream = localConn.getInputStream();
                            String lJsonText = readStreamSafely(inStream, 2 * 1024 * 1024);
                            inStream.close();

                            JSONObject lJson = new JSONObject(lJsonText);
                            cachedTotalVisitors = lJson.optLong("totalVisitors", 0);
                            cachedTotalVisits = lJson.optLong("totalVisits", 0);
                            cachedTotalInquiries = lJson.optLong("totalInquiries", 0);
                            DataRepository.setTotalCounts(cachedTotalInquiries, cachedTotalVisits);

                            JSONArray lInquiries = lJson.optJSONArray("inquiries");
                            if (lInquiries != null) {
                                for (int i = 0; i < lInquiries.length(); i++) {
                                    JSONObject inq = lInquiries.getJSONObject(i);
                                    String inqId = inq.optString("id", "inq_" + (offset + i));

                                    String name = "";
                                    if (inq.has("sender") && inq.optJSONObject("sender") != null) {
                                        JSONObject s = inq.getJSONObject("sender");
                                        name = s.optString("name", s.optString("fullName", ""));
                                    }
                                    if (name.isEmpty()) {
                                        name = inq.optString("name", inq.optString("fullName", inq.optString("senderName", "")));
                                    }
                                    if (name.isEmpty() || name.equalsIgnoreCase("Anonymous") || name.equalsIgnoreCase("Anonymous Submitter")) {
                                        String em = inq.optString("email", "");
                                        name = (!em.isEmpty() && em.contains("@")) ? em.substring(0, em.indexOf("@")) : "Portfolio Submitter";
                                    }

                                    IngestionItem item = new IngestionItem();
                                    item.type = "CONTACT_SUBMISSION";
                                    item.id = inqId;
                                    long ts = inq.optLong("timestamp", System.currentTimeMillis());
                                    item.timestamp = ts;
                                    item.visitorId = inq.optString("visitorId", "");
                                    item.referredBy = IngestionItem.cleanText(inq.optString("referredBy", inq.optString("sharedBy", "")));
                                    item.rowTimestamp = new java.text.SimpleDateFormat("MM/dd/yyyy HH:mm:ss", java.util.Locale.US).format(new java.util.Date(ts));
                                    item.name = name;
                                    item.email = inq.optString("email", "");
                                    item.phone = inq.optString("phone", "");
                                    item.subject = inq.optString("subject", "Direct Inquiry");
                                    item.message = inq.optString("message", "");
                                    item.device = inq.optString("device", "Desktop");
                                    item.city = inq.optString("city", "");
                                    item.country = inq.optString("country", "");
                                    item.ip = inq.optString("ip", "");
                                    item.os = inq.optString("os", "");
                                    item.browser = inq.optString("browser", "");

                                    JSONArray atts = inq.optJSONArray("attachments");
                                    if (atts != null && atts.length() > 0) {
                                        item.hasAttachment = true;
                                        for (int a = 0; a < atts.length(); a++) {
                                            JSONObject attObj = atts.getJSONObject(a);
                                            IngestionItem.AttachmentItem att = new IngestionItem.AttachmentItem();
                                            att.name = attObj.optString("name", "Attachment_" + (a + 1));
                                            att.type = attObj.optString("type", "application/octet-stream");
                                            att.size = attObj.optLong("size", 0);
                                            att.dataUri = attObj.optString("data", attObj.optString("preview", ""));
                                            att.downloadUrl = attObj.optString("downloadUrl", attObj.optString("url", ""));
                                            att.fileId = attObj.optString("id", "");
                                            item.attachments.add(att);
                                        }
                                    }

                                    boolean isNew = !seenSet.contains(inqId);
                                    if (isNew) {
                                        seenSet.add(inqId);
                                        if (!isFirstRun && newCount < 3 && offset == 0) {
                                            newCount++;
                                            NotificationHelper.notifyMessage(context, item, notifIdCounter++);
                                        }
                                    }
                                    messages.add(item);
                                }
                            }

                            JSONArray lVisitors = lJson.optJSONArray("visitors");
                            if (lVisitors != null) {
                                for (int i = 0; i < lVisitors.length(); i++) {
                                    JSONObject vis = lVisitors.getJSONObject(i);
                                    String visId = vis.optString("id", "vis_" + (offset + i));
                                    long ts = vis.optLong("lastSeen", vis.optLong("timestamp", System.currentTimeMillis()));
                                    String eventKey = vis.optString("lastEventId", visId + "_" + ts);

                                    IngestionItem item = new IngestionItem();
                                    item.type = "VISITOR_ALERT";
                                    item.id = eventKey;
                                    item.visitorId = visId;
                                    item.timestamp = ts;
                                    item.rowTimestamp = new java.text.SimpleDateFormat("MM/dd/yyyy HH:mm:ss", java.util.Locale.US).format(new java.util.Date(ts));
                                    item.city = vis.optString("city", "");
                                    item.country = vis.optString("country", "");
                                    item.device = vis.optString("device", "Desktop");
                                    item.visitCount = vis.optInt("visits", 1);

                                    String ref = vis.optString("referredBy", vis.optString("sharedBy", ""));
                                    if (ref.isEmpty() && vis.has("telemetry") && vis.optJSONObject("telemetry") != null) {
                                        JSONObject t = vis.getJSONObject("telemetry");
                                        ref = t.optString("referredBy", t.optString("sharedBy", ""));
                                    }
                                    if (ref.equalsIgnoreCase("None") || ref.equalsIgnoreCase("null")) {
                                        ref = "";
                                    }
                                    item.referredBy = IngestionItem.cleanText(ref);

                                    boolean isNew = !seenSet.contains(eventKey);
                                    if (isNew) {
                                        seenSet.add(eventKey);
                                        if (!isFirstRun && newCount < 3 && offset == 0) {
                                            newCount++;
                                            NotificationHelper.notifyVisit(context, item, notifIdCounter++);
                                        }
                                    }
                                    visits.add(item);
                                }
                            }
                            localConn.disconnect();
                            localConsumed = true;
                            break;
                        }
                        localConn.disconnect();
                    } catch (Exception localErr) {}
                }

                // -------------------------------------------------------------
                // 2. PAGINATED GOOGLE SHEET GVIZ SQL ENGINE (5-15KB Bandwidth)
                // -------------------------------------------------------------
                if (!localConsumed) {
                    String targetBase = sheetUrl;
                    if (targetBase.contains("docs.google.com/spreadsheets") && !targetBase.contains("gviz/tq")) {
                        int editIdx = targetBase.indexOf("/edit");
                        if (editIdx > 0) {
                            targetBase = targetBase.substring(0, editIdx) + "/gviz/tq?tqx=out:csv";
                        } else {
                            targetBase = targetBase.replaceAll("/+$", "") + "/gviz/tq?tqx=out:csv";
                        }
                    }

                    // A. Fetch total count in 5 bytes on initial sync
                    if (offset == 0) {
                        try {
                            String countQuery = "select count(A) label count(A) ''";
                            String countUrl = targetBase + (targetBase.contains("?") ? "&" : "?")
                                + "tq=" + URLEncoder.encode(countQuery, "UTF-8")
                                + "&nocache=" + System.currentTimeMillis();
                            URL cUrl = new URL(countUrl);
                            HttpURLConnection cConn = (HttpURLConnection) cUrl.openConnection();
                            cConn.setConnectTimeout(2500);
                            cConn.setReadTimeout(2500);
                            if (cConn.getResponseCode() == 200) {
                                java.io.InputStream cIn = cConn.getInputStream();
                                String countStr = readStreamSafely(cIn, 1024);
                                cIn.close();
                                if (countStr != null) {
                                    countStr = countStr.replace("\"", "").trim();
                                    long totalRows = Long.parseLong(countStr);
                                    if (totalRows > 0) {
                                        cachedTotalVisits = totalRows;
                                        cachedTotalInquiries = totalRows;
                                        DataRepository.setTotalCounts(totalRows, totalRows);
                                    }
                                }
                            }
                            cConn.disconnect();
                        } catch (Throwable countErr) {}
                    }

                    // B. Fetch paginated slice using GViz SQL (order by A desc limit N offset M)
                    String pageQuery = "select * order by A desc limit " + limit + " offset " + offset;
                    String pageUrlStr = targetBase + (targetBase.contains("?") ? "&" : "?")
                        + "tq=" + URLEncoder.encode(pageQuery, "UTF-8")
                        + "&nocache=" + System.currentTimeMillis();

                    List<String> sheetUrlsToTry = new ArrayList<String>();
                    sheetUrlsToTry.add(pageUrlStr);
                    sheetUrlsToTry.add("http://10.0.2.2:7070/api/sheet/live-csv?tq=" + URLEncoder.encode(pageQuery, "UTF-8") + "&limit=" + limit + "&offset=" + offset);
                    sheetUrlsToTry.add("http://127.0.0.1:7070/api/sheet/live-csv?tq=" + URLEncoder.encode(pageQuery, "UTF-8") + "&limit=" + limit + "&offset=" + offset);
                    sheetUrlsToTry.add("http://10.0.0.111:7070/api/sheet/live-csv?tq=" + URLEncoder.encode(pageQuery, "UTF-8") + "&limit=" + limit + "&offset=" + offset);

                    List<String[]> rows = new ArrayList<String[]>();
                    Throwable lastNetworkEx = null;

                    for (String tryUrl : sheetUrlsToTry) {
                        HttpURLConnection conn = null;
                        try {
                            URL url = new URL(tryUrl);
                            conn = (HttpURLConnection) url.openConnection();
                            conn.setConnectTimeout(4000);
                            conn.setReadTimeout(4000);
                            conn.setRequestMethod("GET");
                            conn.setRequestProperty("User-Agent", "MaxHive-Android/2.5");
                            conn.setRequestProperty("Cache-Control", "no-cache, no-store");

                            int code = conn.getResponseCode();
                            if (code == 200) {
                                java.io.InputStream inStream = conn.getInputStream();
                                String csvText = readStreamSafely(inStream, 2 * 1024 * 1024);
                                inStream.close();
                                String[] lines = csvText.split("\r?\n");
                                for (String line : lines) {
                                    line = line.trim();
                                    if (line.isEmpty()) continue;
                                    String[] parts = parseCsvLine(line);
                                    if (parts.length >= 2) {
                                        rows.add(parts);
                                    }
                                }
                                break;
                            }
                        } catch (Throwable ex) {
                            lastNetworkEx = ex;
                        } finally {
                            if (conn != null) conn.disconnect();
                        }
                    }

                    if (rows.isEmpty() && lastNetworkEx != null && messages.isEmpty() && visits.isEmpty()) {
                        throw (lastNetworkEx instanceof Exception) ? (Exception) lastNetworkEx : new Exception(lastNetworkEx.getMessage());
                    }

                    // Process rows (Row 0 is column headers)
                    for (int i = 1; i < rows.size(); i++) {
                        String[] row = rows.get(i);
                        String timestamp = row[0].replace("\"", "").trim();

                        String ciphertext = null;
                        for (int c = 1; c < row.length; c++) {
                            String colVal = row[c].replace("\"", "").trim();
                            if (colVal.startsWith("MAXASYM1:") || colVal.startsWith("MAXENC1:")) {
                                ciphertext = colVal;
                                break;
                            }
                        }

                        IngestionItem item = null;
                        if (ciphertext != null) {
                            String decryptedJson = CryptoEngine.decryptPayload(ciphertext, masterKey);
                            if (decryptedJson != null) {
                                item = IngestionItem.fromJson(timestamp, ciphertext, decryptedJson);
                            }
                        } else if (row.length >= 2) {
                            String col1 = row[1].replace("\"", "").trim();
                            if (!col1.isEmpty() && !col1.equalsIgnoreCase("Timestamp") && !col1.equalsIgnoreCase("M1")) {
                                item = new IngestionItem();
                                item.type = "CONTACT_SUBMISSION";
                                item.id = "gform_" + (offset + i) + "_" + Math.abs(col1.hashCode());
                                item.rowTimestamp = timestamp;
                                item.rawCiphertext = "";
                                item.timestamp = System.currentTimeMillis();
                                item.name = IngestionItem.cleanText(col1);
                                if (row.length > 2) item.email = IngestionItem.cleanText(row[2].replace("\"", "").trim());
                                if (row.length > 3) item.phone = IngestionItem.cleanText(row[3].replace("\"", "").trim());
                                if (row.length > 4) item.subject = IngestionItem.cleanText(row[4].replace("\"", "").trim());
                                else item.subject = "Google Form Message";
                                if (row.length > 5) item.message = IngestionItem.cleanText(row[5].replace("\"", "").trim());
                                else item.message = item.name;
                                item.device = "Google Form";
                            }
                        }

                        if (item != null) {
                            String rowKey = ciphertext != null ? ciphertext : item.id;
                            boolean isNew = !seenSet.contains(rowKey);
                            if (isNew) {
                                seenSet.add(rowKey);
                                if (!isFirstRun && newCount < 3 && offset == 0) {
                                    newCount++;
                                    if ("CONTACT_SUBMISSION".equals(item.type)) {
                                        NotificationHelper.notifyMessage(context, item, notifIdCounter++);
                                    } else if ("VISITOR_ALERT".equals(item.type)) {
                                        NotificationHelper.notifyVisit(context, item, notifIdCounter++);
                                    }
                                }
                            }

                            if ("CONTACT_SUBMISSION".equals(item.type)) {
                                messages.add(item);
                            } else if ("VISITOR_ALERT".equals(item.type)) {
                                visits.add(item);
                            }
                        }
                    }
                }

                // Persist seen row fingerprints
                prefs.edit().putStringSet(KEY_SEEN_ROWS, seenSet).apply();

                // If offset == 0, replace repository; if offset > 0, append to repository
                if (offset == 0) {
                    DataRepository.updateData(messages, visits);
                    synchronized (cachedMessages) {
                        cachedMessages.clear();
                        cachedMessages.addAll(messages);
                    }
                    synchronized (cachedVisits) {
                        cachedVisits.clear();
                        cachedVisits.addAll(visits);
                    }
                } else {
                    DataRepository.appendMessages(messages);
                    DataRepository.appendVisits(visits);
                }

                final boolean hasMore = (messages.size() + visits.size()) >= (limit - 5);

                if (pageCallback != null) {
                    final List<IngestionItem> pMsgs = messages;
                    final List<IngestionItem> pVis = visits;
                    new Handler(Looper.getMainLooper()).post(new Runnable() {
                        @Override public void run() {
                            pageCallback.onPageLoaded(pMsgs, pVis, hasMore);
                        }
                    });
                } else {
                    synchronized (registeredCallbacks) {
                        callbacksToNotify = new ArrayList<SyncCallback>(registeredCallbacks);
                    }
                    final int nCnt = newCount;
                    new Handler(Looper.getMainLooper()).post(
                        new NotifyCompleteRunnable(callbacksToNotify, DataRepository.getMessages(), DataRepository.getVisits(), nCnt)
                    );
                }

            } catch (Throwable e) {
                android.util.Log.e("MaxHive", "Sync error: " + e.getMessage(), e);
                final String err = e.getMessage() != null ? e.getMessage() : "Sync failed";

                if (pageCallback != null) {
                    new Handler(Looper.getMainLooper()).post(new Runnable() {
                        @Override public void run() {
                            pageCallback.onPageError(err);
                        }
                    });
                } else {
                    synchronized (registeredCallbacks) {
                        callbacksToNotify = new ArrayList<SyncCallback>(registeredCallbacks);
                    }
                    new Handler(Looper.getMainLooper()).post(
                        new NotifyErrorRunnable(callbacksToNotify, err)
                    );
                }
            } finally {
                synchronized (SYNC_LOCK) {
                    isSyncing = false;
                }
            }
        }
    }

    public static void syncSheetData(final Context context, boolean force, final SyncCallback callback) {
        if (context == null) return;

        if (callback != null) {
            registerCallback(callback);
        }

        synchronized (SYNC_LOCK) {
            if (isSyncing && !force) {
                return;
            }
            isSyncing = true;
        }

        new Thread(new SyncWorkerRunnable(context.getApplicationContext(), 0, DEFAULT_PAGE_SIZE, null)).start();
    }

    public static void fetchNextPage(final Context context, int offset, int limit, final PageCallback callback) {
        if (context == null) return;
        new Thread(new SyncWorkerRunnable(context.getApplicationContext(), offset, limit, callback)).start();
    }

    private static String readStreamSafely(java.io.InputStream is, int maxBytes) throws java.io.IOException {
        if (is == null) return "";
        java.io.ByteArrayOutputStream baos = new java.io.ByteArrayOutputStream();
        byte[] buffer = new byte[8192];
        int bytesRead;
        int total = 0;
        while ((bytesRead = is.read(buffer)) != -1) {
            baos.write(buffer, 0, bytesRead);
            total += bytesRead;
            if (total >= maxBytes) {
                break;
            }
        }
        return baos.toString("UTF-8");
    }

    private static String[] parseCsvLine(String line) {
        List<String> tokens = new ArrayList<String>();
        StringBuilder sb = new StringBuilder();
        boolean inQuotes = false;

        for (int i = 0; i < line.length(); i++) {
            char c = line.charAt(i);
            if (c == '\"') {
                inQuotes = !inQuotes;
            } else if (c == ',' && !inQuotes) {
                tokens.add(sb.toString().trim());
                sb.setLength(0);
            } else {
                sb.append(c);
            }
        }
        tokens.add(sb.toString().trim());
        return tokens.toArray(new String[0]);
    }
}
