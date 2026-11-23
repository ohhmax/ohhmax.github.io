package com.max.hive;

import android.app.Activity;
import android.app.AlertDialog;
import android.content.Context;
import android.content.DialogInterface;
import android.content.Intent;
import android.content.SharedPreferences;
import android.content.pm.PackageManager;
import android.os.Build;
import android.os.Bundle;
import android.text.Editable;
import android.text.TextWatcher;
import android.view.LayoutInflater;
import android.view.View;
import android.view.ViewGroup;
import android.view.inputmethod.InputMethodManager;
import android.widget.AdapterView;
import android.widget.BaseAdapter;
import android.widget.EditText;
import android.widget.ImageButton;
import android.widget.ImageView;
import android.widget.LinearLayout;
import android.widget.ListView;
import android.widget.TextView;
import android.widget.Toast;

import java.util.ArrayList;
import java.util.Calendar;
import java.util.Collections;
import java.util.Comparator;
import java.util.HashMap;
import java.util.LinkedHashMap;
import java.util.Locale;
import java.util.List;
import java.util.Map;

public class MainActivity extends Activity implements View.OnClickListener, AdapterView.OnItemClickListener, SheetSyncService.SyncCallback, TextWatcher, DialogInterface.OnClickListener {

    public static final int TAB_OVERVIEW = 0;
    public static final int TAB_MESSAGES = 1;
    public static final int TAB_VISITS = 2;

    public static final int SORT_NEWEST = 0;
    public static final int SORT_OLDEST = 1;
    public static final int SORT_ACTIVITY = 2; // Most visits / Sender A-Z
    public static final int SORT_LOCATION = 3; // City/Country A-Z

    private static final String PREF_SORT_MODE = "pref_sort_mode";

    private TextView tvStatus;
    private ImageView ivStatusDot;
    private TextView tabOverview;
    private TextView tabMessages;
    private TextView tabVisits;
    private TextView tvEmpty;
    private ListView listView;
    private View layoutOverview;
    private TextView tvOverviewTodayVisits;
    private TextView tvOverviewMonthVisits;
    private TextView tvOverviewTotalVisits;
    private TextView tvOverviewTotalMessages;
    private TextView tvOverviewSharedCount;
    private TextView tvOverviewTopReferrerHighlight;
    private LinearLayout containerReferrers;
    private LinearLayout containerLocations;
    private LinearLayout containerDevices;

    private ImageButton btnSync;
    private ImageButton btnSettings;
    private ImageButton btnToggleSearch;
    private ImageButton btnSort;

    private LinearLayout layoutSearchBar;
    private EditText etSearch;
    private ImageButton btnClearSearch;
    private LinearLayout cardSetupRequired;

    private int currentTab = TAB_OVERVIEW;
    private int currentSortMode = SORT_NEWEST;
    private String currentSearchQuery = "";
    private boolean isLoadingMore = false;
    private boolean hasMoreItems = true;

    private final List<IngestionItem> allRawMessages = new ArrayList<IngestionItem>();
    private final List<IngestionItem> allRawVisits = new ArrayList<IngestionItem>();

    private final List<IngestionItem> displayMessages = new ArrayList<IngestionItem>();
    private final List<IngestionItem> displayVisits = new ArrayList<IngestionItem>();

    private MessageAdapter messageAdapter;
    private VisitAdapter visitAdapter;



    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        UiUtils.applySystemUiBars(this);
        setContentView(R.layout.activity_main);

        NotificationHelper.initChannels(this);

        if (Build.VERSION.SDK_INT >= 33) {
            if (checkSelfPermission("android.permission.POST_NOTIFICATIONS") != PackageManager.PERMISSION_GRANTED) {
                requestPermissions(new String[]{"android.permission.POST_NOTIFICATIONS"}, 101);
            }
        }

        SharedPreferences prefs = getSharedPreferences("max_hive_prefs", Context.MODE_PRIVATE);
        currentSortMode = prefs.getInt(PREF_SORT_MODE, SORT_NEWEST);

        tvStatus = findViewById(R.id.tvStatus);
        ivStatusDot = findViewById(R.id.ivStatusDot);
        tabOverview = findViewById(R.id.tabOverview);
        tabMessages = findViewById(R.id.tabMessages);
        tabVisits = findViewById(R.id.tabVisits);
        tvEmpty = findViewById(R.id.tvEmpty);
        listView = findViewById(R.id.listView);
        layoutOverview = findViewById(R.id.layoutOverview);

        tvOverviewTodayVisits = findViewById(R.id.tvOverviewTodayVisits);
        tvOverviewMonthVisits = findViewById(R.id.tvOverviewMonthVisits);
        tvOverviewTotalVisits = findViewById(R.id.tvOverviewTotalVisits);
        tvOverviewTotalMessages = findViewById(R.id.tvOverviewTotalMessages);
        tvOverviewSharedCount = findViewById(R.id.tvOverviewSharedCount);
        tvOverviewTopReferrerHighlight = findViewById(R.id.tvOverviewTopReferrerHighlight);
        containerReferrers = findViewById(R.id.containerReferrers);
        containerLocations = findViewById(R.id.containerLocations);
        containerDevices = findViewById(R.id.containerDevices);

        btnSync = findViewById(R.id.btnSync);
        btnSettings = findViewById(R.id.btnSettings);
        btnToggleSearch = findViewById(R.id.btnToggleSearch);
        btnSort = findViewById(R.id.btnSort);

        layoutSearchBar = findViewById(R.id.layoutSearchBar);
        etSearch = findViewById(R.id.etSearch);
        btnClearSearch = findViewById(R.id.btnClearSearch);
        cardSetupRequired = findViewById(R.id.cardSetupRequired);

        findViewById(R.id.btnOpenSetup).setOnClickListener(this);

        messageAdapter = new MessageAdapter(this, displayMessages);
        visitAdapter = new VisitAdapter(this, displayVisits);
        listView.setAdapter(messageAdapter);

        if (tabOverview != null) tabOverview.setOnClickListener(this);
        tabMessages.setOnClickListener(this);
        tabVisits.setOnClickListener(this);
        btnSync.setOnClickListener(this);
        btnSettings.setOnClickListener(this);
        btnToggleSearch.setOnClickListener(this);
        btnSort.setOnClickListener(this);
        btnClearSearch.setOnClickListener(this);
        listView.setOnItemClickListener(this);
        listView.setOnScrollListener(new android.widget.AbsListView.OnScrollListener() {
            @Override
            public void onScrollStateChanged(android.widget.AbsListView view, int scrollState) {}

            @Override
            public void onScroll(android.widget.AbsListView view, int firstVisibleItem, int visibleItemCount, int totalItemCount) {
                if (currentTab != TAB_OVERVIEW && totalItemCount > 0 && !isLoadingMore && hasMoreItems) {
                    if (firstVisibleItem + visibleItemCount >= totalItemCount - 2) {
                        loadMoreData();
                    }
                }
            }
        });

        etSearch.addTextChangedListener(this);

        switchTab(TAB_OVERVIEW);
        handleTabIntent(getIntent());

        try {
            Intent serviceIntent = new Intent(this, SheetSyncService.class);
            startService(serviceIntent);
        } catch (Throwable e) {}
    }

    @Override
    public void beforeTextChanged(CharSequence s, int start, int count, int after) {}

    @Override
    public void onTextChanged(CharSequence s, int start, int before, int count) {
        currentSearchQuery = s != null ? s.toString().trim() : "";
        if (btnClearSearch != null) {
            btnClearSearch.setVisibility(currentSearchQuery.isEmpty() ? View.GONE : View.VISIBLE);
        }
        applyFilterAndSort();
    }

    @Override
    public void afterTextChanged(Editable s) {}

    @Override
    protected void onNewIntent(Intent intent) {
        super.onNewIntent(intent);
        setIntent(intent);
        handleTabIntent(intent);
    }

    private void handleTabIntent(Intent intent) {
        if (intent != null) {
            String tab = intent.getStringExtra("tab");
            if ("visits".equals(tab)) {
                switchTab(TAB_VISITS);
            } else if ("messages".equals(tab)) {
                switchTab(TAB_MESSAGES);
            } else if ("overview".equals(tab)) {
                switchTab(TAB_OVERVIEW);
            }
        }
    }

    @Override
    protected void onResume() {
        super.onResume();
        UiUtils.applySystemUiBars(this);
        SheetSyncService.setAppForeground(true);

        checkConfigState();
        triggerSync(false);
    }

    @Override
    protected void onPause() {
        super.onPause();
        SheetSyncService.setAppForeground(false);
    }

    private void checkConfigState() {
        SharedPreferences prefs = getSharedPreferences("max_hive_prefs", Context.MODE_PRIVATE);
        String sheetUrl = prefs.getString(SheetSyncService.PREF_SHEET_URL, "").trim();
        String masterKey = prefs.getString(SheetSyncService.PREF_MASTER_KEY, "").trim();

        if (sheetUrl.isEmpty() || masterKey.isEmpty()) {
            cardSetupRequired.setVisibility(View.VISIBLE);
            tvStatus.setText("Setup Required");
            if (ivStatusDot != null) ivStatusDot.setVisibility(View.GONE);
        } else {
            cardSetupRequired.setVisibility(View.GONE);
            if (ivStatusDot != null) ivStatusDot.setVisibility(View.VISIBLE);
        }
    }

    @Override
    public void onClick(View v) {
        HapticHelper.performClick(v);
        int id = v.getId();
        if (id == R.id.tabOverview) {
            switchTab(TAB_OVERVIEW);
        } else if (id == R.id.tabMessages) {
            switchTab(TAB_MESSAGES);
        } else if (id == R.id.tabVisits) {
            switchTab(TAB_VISITS);
        } else if (id == R.id.btnSync) {
            triggerSync(true);
        } else if (id == R.id.btnSettings || id == R.id.btnOpenSetup) {
            Intent intent = new Intent(this, SettingsActivity.class);
            startActivity(intent);
        } else if (id == R.id.btnToggleSearch) {
            toggleSearchBar();
        } else if (id == R.id.btnSort) {
            showSortDialog();
        } else if (id == R.id.btnClearSearch) {
            etSearch.setText("");
        }
    }

    private void toggleSearchBar() {
        if (layoutSearchBar.getVisibility() == View.VISIBLE) {
            layoutSearchBar.setVisibility(View.GONE);
            etSearch.setText("");
            InputMethodManager imm = (InputMethodManager) getSystemService(Context.INPUT_METHOD_SERVICE);
            if (imm != null) imm.hideSoftInputFromWindow(etSearch.getWindowToken(), 0);
        } else {
            layoutSearchBar.setVisibility(View.VISIBLE);
            etSearch.requestFocus();
            InputMethodManager imm = (InputMethodManager) getSystemService(Context.INPUT_METHOD_SERVICE);
            if (imm != null) imm.showSoftInput(etSearch, InputMethodManager.SHOW_IMPLICIT);
        }
    }

    private void showSortDialog() {
        final String[] options = new String[] {
            "Newest First (Default)",
            "Oldest First",
            (currentTab == TAB_MESSAGES) ? "Sender Name (A-Z)" : "Most Visits (#)",
            "Location / City (A-Z)"
        };

        AlertDialog.Builder builder = new AlertDialog.Builder(this);
        builder.setTitle("Sort Items");
        builder.setSingleChoiceItems(options, currentSortMode, this);
        builder.setNegativeButton("Cancel", null);
        builder.show();
    }

    @Override
    public void onClick(DialogInterface dialog, int which) {
        currentSortMode = which;
        getSharedPreferences("max_hive_prefs", Context.MODE_PRIVATE)
            .edit()
            .putInt(PREF_SORT_MODE, currentSortMode)
            .apply();

        applyFilterAndSort();
        dialog.dismiss();
    }

    @Override
    public void onItemClick(AdapterView<?> parent, View view, int position, long id) {
        HapticHelper.performClick(view);
        if (currentTab == TAB_MESSAGES) {
            if (position >= 0 && position < displayMessages.size()) {
                IngestionItem item = displayMessages.get(position);
                DataRepository.putItem(item.id, item);
                Intent intent = new Intent(this, DetailActivity.class);
                intent.putExtra("item_id", item.id);
                intent.putExtra("item", item);
                startActivity(intent);
            }
        } else if (currentTab == TAB_VISITS) {
            if (position >= 0 && position < displayVisits.size()) {
                IngestionItem item = displayVisits.get(position);
                DataRepository.putItem(item.id, item);
                Intent intent = new Intent(this, DetailActivity.class);
                intent.putExtra("item_id", item.id);
                intent.putExtra("item", item);
                startActivity(intent);
            }
        }
    }

    private void loadMoreData() {
        if (isLoadingMore || !hasMoreItems || currentTab == TAB_OVERVIEW) return;
        isLoadingMore = true;
        int currentCount = (currentTab == TAB_MESSAGES) ? allRawMessages.size() : allRawVisits.size();

        SheetSyncService.fetchNextPage(this, currentCount, SheetSyncService.DEFAULT_PAGE_SIZE, new SheetSyncService.PageCallback() {
            @Override
            public void onPageLoaded(List<IngestionItem> newMessages, List<IngestionItem> newVisits, boolean hasMore) {
                isLoadingMore = false;
                hasMoreItems = hasMore;

                if (currentTab == TAB_MESSAGES && newMessages != null && !newMessages.isEmpty()) {
                    for (IngestionItem it : newMessages) {
                        boolean exists = false;
                        for (IngestionItem ex : allRawMessages) {
                            if (ex.id != null && ex.id.equals(it.id)) {
                                exists = true;
                                break;
                            }
                        }
                        if (!exists) {
                            allRawMessages.add(it);
                        }
                    }
                    applyFilterAndSort();
                } else if (currentTab == TAB_VISITS && newVisits != null && !newVisits.isEmpty()) {
                    for (IngestionItem it : newVisits) {
                        boolean exists = false;
                        for (IngestionItem ex : allRawVisits) {
                            if (ex.id != null && ex.id.equals(it.id)) {
                                exists = true;
                                break;
                            }
                        }
                        if (!exists) {
                            allRawVisits.add(it);
                        }
                    }
                    applyFilterAndSort();
                }
            }

            @Override
            public void onPageError(String error) {
                isLoadingMore = false;
            }
        });
    }

    private void switchTab(int tabIndex) {
        currentTab = tabIndex;
        hasMoreItems = true;
        isLoadingMore = false;
        if (tabOverview != null) {
            tabOverview.setBackgroundResource(tabIndex == TAB_OVERVIEW ? R.drawable.bg_tab_active : R.drawable.bg_tab_inactive);
            tabOverview.setTextColor(getColor(tabIndex == TAB_OVERVIEW ? R.color.tab_active_text : R.color.tab_inactive_text));
            tabOverview.setTypeface(null, tabIndex == TAB_OVERVIEW ? android.graphics.Typeface.BOLD : android.graphics.Typeface.NORMAL);
        }
        if (tabMessages != null) {
            tabMessages.setBackgroundResource(tabIndex == TAB_MESSAGES ? R.drawable.bg_tab_active : R.drawable.bg_tab_inactive);
            tabMessages.setTextColor(getColor(tabIndex == TAB_MESSAGES ? R.color.tab_active_text : R.color.tab_inactive_text));
            tabMessages.setTypeface(null, tabIndex == TAB_MESSAGES ? android.graphics.Typeface.BOLD : android.graphics.Typeface.NORMAL);
        }
        if (tabVisits != null) {
            tabVisits.setBackgroundResource(tabIndex == TAB_VISITS ? R.drawable.bg_tab_active : R.drawable.bg_tab_inactive);
            tabVisits.setTextColor(getColor(tabIndex == TAB_VISITS ? R.color.tab_active_text : R.color.tab_inactive_text));
            tabVisits.setTypeface(null, tabIndex == TAB_VISITS ? android.graphics.Typeface.BOLD : android.graphics.Typeface.NORMAL);
        }

        if (tabIndex == TAB_OVERVIEW) {
            if (layoutOverview != null) layoutOverview.setVisibility(View.VISIBLE);
            if (listView != null) listView.setVisibility(View.GONE);
            if (tvEmpty != null) tvEmpty.setVisibility(View.GONE);
            if (btnSort != null) btnSort.setVisibility(View.GONE);
            populateOverview();
        } else if (tabIndex == TAB_MESSAGES) {
            if (layoutOverview != null) layoutOverview.setVisibility(View.GONE);
            if (listView != null) {
                listView.setVisibility(View.VISIBLE);
                listView.setAdapter(messageAdapter);
            }
            if (btnSort != null) btnSort.setVisibility(View.VISIBLE);
            applyFilterAndSort();
        } else {
            if (layoutOverview != null) layoutOverview.setVisibility(View.GONE);
            if (listView != null) {
                listView.setVisibility(View.VISIBLE);
                listView.setAdapter(visitAdapter);
            }
            if (btnSort != null) btnSort.setVisibility(View.VISIBLE);
            applyFilterAndSort();
        }
    }

    private void applyFilterAndSort() {
        if (currentTab == TAB_OVERVIEW) {
            populateOverview();
            return;
        }

        if (currentTab == TAB_MESSAGES) {
            displayMessages.clear();
            for (IngestionItem it : allRawMessages) {
                if (it.matchesQuery(currentSearchQuery)) {
                    displayMessages.add(it);
                }
            }
            Collections.sort(displayMessages, new ItemComparator(currentSortMode, true));
            messageAdapter.notifyDataSetChanged();
        } else {
            displayVisits.clear();
            for (IngestionItem it : allRawVisits) {
                if (it.matchesQuery(currentSearchQuery)) {
                    displayVisits.add(it);
                }
            }
            Collections.sort(displayVisits, new ItemComparator(currentSortMode, false));
            visitAdapter.notifyDataSetChanged();
        }
        updateEmptyState();
    }

    private void populateOverview() {
        if (layoutOverview == null) return;

        Calendar cal = Calendar.getInstance();
        cal.set(Calendar.HOUR_OF_DAY, 0);
        cal.set(Calendar.MINUTE, 0);
        cal.set(Calendar.SECOND, 0);
        cal.set(Calendar.MILLISECOND, 0);
        long todayStart = cal.getTimeInMillis();

        cal.set(Calendar.DAY_OF_MONTH, 1);
        long monthStart = cal.getTimeInMillis();

        java.text.SimpleDateFormat sdfDay = new java.text.SimpleDateFormat("MM/dd/yyyy", Locale.US);
        String currentDayStr = sdfDay.format(new java.util.Date());

        java.text.SimpleDateFormat sdfMonth = new java.text.SimpleDateFormat("MM/yyyy", Locale.US);
        String currentMonthStr = sdfMonth.format(new java.util.Date());

        int todayCount = 0;
        int monthCount = 0;
        int sharedCount = 0;

        Map<String, Integer> referrerMap = new HashMap<String, Integer>();
        Map<String, Integer> locationMap = new HashMap<String, Integer>();
        Map<String, Integer> deviceMap = new HashMap<String, Integer>();

        for (IngestionItem v : allRawVisits) {
            long ts = v.timestamp;
            boolean isToday = (ts >= todayStart);
            boolean isMonth = (ts >= monthStart);

            if (!isToday && v.rowTimestamp != null && v.rowTimestamp.startsWith(currentDayStr)) {
                isToday = true;
            }
            if (!isMonth && v.rowTimestamp != null && v.rowTimestamp.contains("/" + currentMonthStr.substring(3))) {
                isMonth = true;
            }

            int count = Math.max(1, v.visitCount);
            if (isToday) todayCount += count;
            if (isMonth) monthCount += count;

            if (v.isSharedVisit()) {
                sharedCount += count;
                String ref = v.referredBy.trim();
                Integer prev = referrerMap.get(ref);
                referrerMap.put(ref, (prev != null ? prev : 0) + count);
            }

            String flag = v.getCountryFlag();
            String locName = v.city.isEmpty() ? (v.country.isEmpty() ? "Direct Visitors" : v.country) : (v.city + ", " + v.country);
            String locKey = (flag.isEmpty() ? "" : (flag + " ")) + locName;
            Integer prevLoc = locationMap.get(locKey);
            locationMap.put(locKey, (prevLoc != null ? prevLoc : 0) + count);

            String dev = v.device.isEmpty() ? "Desktop" : v.device;
            Integer prevDev = deviceMap.get(dev);
            deviceMap.put(dev, (prevDev != null ? prevDev : 0) + count);
        }

        if (tvOverviewTodayVisits != null) tvOverviewTodayVisits.setText(String.valueOf(todayCount));
        if (tvOverviewMonthVisits != null) tvOverviewMonthVisits.setText(String.valueOf(monthCount));

        long totalVisits = SheetSyncService.cachedTotalVisits > 0 ? SheetSyncService.cachedTotalVisits : allRawVisits.size();
        long totalInquiries = SheetSyncService.cachedTotalInquiries > 0 ? SheetSyncService.cachedTotalInquiries : allRawMessages.size();

        if (tvOverviewTotalVisits != null) tvOverviewTotalVisits.setText(formatCount(totalVisits));
        if (tvOverviewTotalMessages != null) tvOverviewTotalMessages.setText(formatCount(totalInquiries));
        if (tvOverviewSharedCount != null) tvOverviewSharedCount.setText(sharedCount + " Shared Visits");

        // 1. Sort referrers descending
        List<Map.Entry<String, Integer>> sortedReferrers = new ArrayList<Map.Entry<String, Integer>>(referrerMap.entrySet());
        Collections.sort(sortedReferrers, new Comparator<Map.Entry<String, Integer>>() {
            @Override
            public int compare(Map.Entry<String, Integer> o1, Map.Entry<String, Integer> o2) {
                return o2.getValue().compareTo(o1.getValue());
            }
        });

        if (containerReferrers != null) {
            containerReferrers.removeAllViews();
            if (sortedReferrers.isEmpty()) {
                if (tvOverviewTopReferrerHighlight != null) {
                    tvOverviewTopReferrerHighlight.setText("Top Referrer: No shared visits yet");
                }
                containerReferrers.addView(createOverviewRowText("No referral visits recorded. Share your portfolio link to track referrer IDs here."));
            } else {
                Map.Entry<String, Integer> top = sortedReferrers.get(0);
                if (tvOverviewTopReferrerHighlight != null) {
                    tvOverviewTopReferrerHighlight.setText("Top Referrer: " + top.getKey() + " (" + top.getValue() + " visits)");
                }

                int rank = 1;
                for (Map.Entry<String, Integer> entry : sortedReferrers) {
                    if (rank > 10) break;
                    containerReferrers.addView(createRankedRowView(rank, entry.getKey(), entry.getValue() + " visits", R.drawable.ic_share));
                    rank++;
                }
            }
        }

        // 2. Sort locations descending
        List<Map.Entry<String, Integer>> sortedLocations = new ArrayList<Map.Entry<String, Integer>>(locationMap.entrySet());
        Collections.sort(sortedLocations, new Comparator<Map.Entry<String, Integer>>() {
            @Override
            public int compare(Map.Entry<String, Integer> o1, Map.Entry<String, Integer> o2) {
                return o2.getValue().compareTo(o1.getValue());
            }
        });

        if (containerLocations != null) {
            containerLocations.removeAllViews();
            if (sortedLocations.isEmpty()) {
                containerLocations.addView(createOverviewRowText("Waiting for visitor telemetry..."));
            } else {
                int rank = 1;
                for (Map.Entry<String, Integer> entry : sortedLocations) {
                    if (rank > 8) break;
                    containerLocations.addView(createRankedRowView(rank, entry.getKey(), entry.getValue() + " visits", 0));
                    rank++;
                }
            }
        }

        // 3. Sort devices descending
        List<Map.Entry<String, Integer>> sortedDevices = new ArrayList<Map.Entry<String, Integer>>(deviceMap.entrySet());
        Collections.sort(sortedDevices, new Comparator<Map.Entry<String, Integer>>() {
            @Override
            public int compare(Map.Entry<String, Integer> o1, Map.Entry<String, Integer> o2) {
                return o2.getValue().compareTo(o1.getValue());
            }
        });

        if (containerDevices != null) {
            containerDevices.removeAllViews();
            if (sortedDevices.isEmpty()) {
                containerDevices.addView(createOverviewRowText("Waiting for device telemetry..."));
            } else {
                int rank = 1;
                for (Map.Entry<String, Integer> entry : sortedDevices) {
                    if (rank > 6) break;
                    containerDevices.addView(createRankedRowView(rank, entry.getKey(), entry.getValue() + " sessions", R.drawable.ic_device_android));
                    rank++;
                }
            }
        }
    }

    private View createRankedRowView(int rank, String title, String subtitle, int iconRes) {
        LinearLayout row = new LinearLayout(this);
        row.setOrientation(LinearLayout.HORIZONTAL);
        row.setGravity(android.view.Gravity.CENTER_VERTICAL);
        row.setPadding(0, UiUtils.dpToPx(this, 6), 0, UiUtils.dpToPx(this, 6));

        TextView tvRank = new TextView(this);
        tvRank.setText("#" + rank);
        tvRank.setTextSize(11);
        tvRank.setTypeface(null, android.graphics.Typeface.BOLD);
        tvRank.setTextColor(getColor(R.color.badge_text));
        tvRank.setBackgroundResource(R.drawable.bg_badge);
        tvRank.setPadding(UiUtils.dpToPx(this, 7), UiUtils.dpToPx(this, 2), UiUtils.dpToPx(this, 7), UiUtils.dpToPx(this, 2));
        row.addView(tvRank);

        if (iconRes != 0) {
            ImageView iv = new ImageView(this);
            iv.setImageResource(iconRes);
            LinearLayout.LayoutParams ivLp = new LinearLayout.LayoutParams(UiUtils.dpToPx(this, 14), UiUtils.dpToPx(this, 14));
            ivLp.setMarginStart(UiUtils.dpToPx(this, 8));
            iv.setLayoutParams(ivLp);
            row.addView(iv);
        }

        TextView tvTitle = new TextView(this);
        tvTitle.setText(title);
        tvTitle.setTextSize(13);
        tvTitle.setTextColor(getColor(R.color.text_primary));
        tvTitle.setSingleLine(true);
        tvTitle.setEllipsize(android.text.TextUtils.TruncateAt.END);
        LinearLayout.LayoutParams titleLp = new LinearLayout.LayoutParams(0, ViewGroup.LayoutParams.WRAP_CONTENT, 1f);
        titleLp.setMarginStart(UiUtils.dpToPx(this, 8));
        titleLp.setMarginEnd(UiUtils.dpToPx(this, 8));
        tvTitle.setLayoutParams(titleLp);
        row.addView(tvTitle);

        TextView tvSub = new TextView(this);
        tvSub.setText(subtitle);
        tvSub.setTextSize(11);
        tvSub.setTextColor(getColor(R.color.text_secondary));
        row.addView(tvSub);

        return row;
    }

    private TextView createOverviewRowText(String text) {
        TextView tv = new TextView(this);
        tv.setText(text);
        tv.setTextSize(12);
        tv.setTextColor(getColor(R.color.text_muted));
        tv.setPadding(0, UiUtils.dpToPx(this, 6), 0, UiUtils.dpToPx(this, 6));
        return tv;
    }

    private void triggerSync(boolean userClicked) {
        SharedPreferences prefs = getSharedPreferences("max_hive_prefs", Context.MODE_PRIVATE);
        String sheetUrl = prefs.getString(SheetSyncService.PREF_SHEET_URL, "").trim();
        String masterKey = prefs.getString(SheetSyncService.PREF_MASTER_KEY, "").trim();

        if (sheetUrl.isEmpty() || masterKey.isEmpty()) {
            checkConfigState();
            return;
        }

        btnSync.setEnabled(false);
        tvStatus.setText(R.string.status_syncing);

        SheetSyncService.syncSheetData(this, userClicked, this);
    }

    @Override
    public void onSyncComplete(List<IngestionItem> messages, List<IngestionItem> visits, int newItemsCount) {
        btnSync.setEnabled(true);
        isLoadingMore = false;
        hasMoreItems = true;
        tvStatus.setText(R.string.status_connected);
        if (ivStatusDot != null) ivStatusDot.setVisibility(View.VISIBLE);
        cardSetupRequired.setVisibility(View.GONE);

        allRawMessages.clear();
        allRawMessages.addAll(messages);
        allRawVisits.clear();
        allRawVisits.addAll(visits);

        long totalVisits = SheetSyncService.cachedTotalVisits > 0 ? SheetSyncService.cachedTotalVisits : visits.size();
        long totalInquiries = SheetSyncService.cachedTotalInquiries > 0 ? SheetSyncService.cachedTotalInquiries : messages.size();

        tabMessages.setText("Messages (" + formatCount(totalInquiries) + ")");
        tabVisits.setText("Visits (" + formatCount(totalVisits) + ")");

        applyFilterAndSort();

        if (newItemsCount > 0) {
            Toast.makeText(this, newItemsCount + " new updates", Toast.LENGTH_SHORT).show();
        }
    }

    @Override
    public void onSyncError(String error) {
        btnSync.setEnabled(true);
        if (error != null && error.contains("Setup Required")) {
            checkConfigState();
        } else {
            tvStatus.setText(error != null && !error.isEmpty() ? error : "Offline");
        }
    }

    public static String formatCount(long count) {
        if (count < 1000) return String.valueOf(count);
        if (count < 10000) return String.format(Locale.US, "%,d", count);
        if (count < 1000000) return String.format(Locale.US, "%.1fK", count / 1000.0);
        if (count < 1000000000L) return String.format(Locale.US, "%.1fM", count / 1000000.0);
        return String.format(Locale.US, "%.2fB", count / 1000000000.0);
    }

    private void updateEmptyState() {
        if (currentTab == TAB_OVERVIEW) {
            tvEmpty.setVisibility(View.GONE);
            return;
        }
        if (currentTab == TAB_MESSAGES) {
            if (!currentSearchQuery.isEmpty()) {
                tvEmpty.setText("No messages match \"" + currentSearchQuery + "\"");
            } else {
                tvEmpty.setText(R.string.empty_messages);
            }
            tvEmpty.setVisibility(displayMessages.isEmpty() ? View.VISIBLE : View.GONE);
        } else {
            if (!currentSearchQuery.isEmpty()) {
                tvEmpty.setText("No visits match \"" + currentSearchQuery + "\"");
            } else {
                tvEmpty.setText(R.string.empty_visits);
            }
            tvEmpty.setVisibility(displayVisits.isEmpty() ? View.VISIBLE : View.GONE);
        }
    }

    // Message List Adapter
    public static class MessageAdapter extends BaseAdapter {
        private final Context ctx;
        private final List<IngestionItem> list;

        public MessageAdapter(Context ctx, List<IngestionItem> list) {
            this.ctx = ctx;
            this.list = list;
        }

        @Override public int getCount() { return list.size(); }
        @Override public Object getItem(int position) { return list.get(position); }
        @Override public long getItemId(int position) { return position; }

        @Override
        public View getView(int position, View convertView, ViewGroup parent) {
            if (convertView == null) {
                convertView = LayoutInflater.from(ctx).inflate(R.layout.item_message, parent, false);
            }
            IngestionItem item = list.get(position);
            if (item == null) return convertView != null ? convertView : new View(ctx);
            item.ensureNonNull();

            ImageView ivDeviceIcon = convertView.findViewById(R.id.ivDeviceIcon);
            TextView tvSenderName = convertView.findViewById(R.id.tvSenderName);
            TextView tvCountryFlag = convertView.findViewById(R.id.tvCountryFlag);
            TextView tvTime = convertView.findViewById(R.id.tvTime);
            TextView tvSubject = convertView.findViewById(R.id.tvSubject);
            TextView tvAttachmentBadge = convertView.findViewById(R.id.tvAttachmentBadge);
            TextView tvMessagePreview = convertView.findViewById(R.id.tvMessagePreview);
            TextView tvContactInfo = convertView.findViewById(R.id.tvContactInfo);
            TextView tvDevice = convertView.findViewById(R.id.tvDevice);

            ivDeviceIcon.setImageResource(item.getDeviceIconResId());
            tvSenderName.setText(item.name != null && !item.name.isEmpty() ? item.name : "Portfolio Submitter");

            String flag = item.getCountryFlag();
            if (flag != null && !flag.isEmpty()) {
                tvCountryFlag.setText(flag);
                tvCountryFlag.setVisibility(View.VISIBLE);
            } else {
                tvCountryFlag.setVisibility(View.GONE);
            }

            tvTime.setText(item.rowTimestamp != null ? item.rowTimestamp : "");
            tvSubject.setText(item.subject != null && !item.subject.isEmpty() ? item.subject : "Direct Contact");

            if (item.hasAttachment && item.attachments != null && !item.attachments.isEmpty()) {
                tvAttachmentBadge.setVisibility(View.VISIBLE);
                if (item.attachments.size() > 1) {
                    tvAttachmentBadge.setText(item.attachments.size() + " Files");
                } else {
                    IngestionItem.AttachmentItem firstAtt = item.attachments.get(0);
                    if (firstAtt != null) {
                        firstAtt.ensureNonNull();
                        tvAttachmentBadge.setText(firstAtt.getFormattedSize());
                    } else {
                        tvAttachmentBadge.setText("File");
                    }
                }
            } else {
                tvAttachmentBadge.setVisibility(View.GONE);
            }

            tvMessagePreview.setText(item.message != null ? item.message : "");
            String contactStr = (item.email != null && !item.email.isEmpty()) ? item.email : ((item.phone != null && !item.phone.isEmpty()) ? item.phone : "No contact");
            tvContactInfo.setText(contactStr);
            tvDevice.setText(item.device != null ? item.device : "Device");

            return convertView;
        }
    }

    // Visit List Adapter
    public static class VisitAdapter extends BaseAdapter {
        private final Context ctx;
        private final List<IngestionItem> list;

        public VisitAdapter(Context ctx, List<IngestionItem> list) {
            this.ctx = ctx;
            this.list = list;
        }

        @Override public int getCount() { return list.size(); }
        @Override public Object getItem(int position) { return list.get(position); }
        @Override public long getItemId(int position) { return position; }

        @Override
        public View getView(int position, View convertView, ViewGroup parent) {
            if (convertView == null) {
                convertView = LayoutInflater.from(ctx).inflate(R.layout.item_visit, parent, false);
            }
            IngestionItem item = list.get(position);
            if (item == null) return convertView != null ? convertView : new View(ctx);
            item.ensureNonNull();

            ImageView ivDeviceIcon = convertView.findViewById(R.id.ivDeviceIcon);
            TextView tvLocation = convertView.findViewById(R.id.tvLocation);
            TextView tvVisitBadge = convertView.findViewById(R.id.tvVisitBadge);
            TextView tvDevice = convertView.findViewById(R.id.tvDevice);
            TextView tvBattery = convertView.findViewById(R.id.tvBattery);
            TextView tvNetwork = convertView.findViewById(R.id.tvNetwork);
            TextView tvTime = convertView.findViewById(R.id.tvTime);
            View layoutReferral = convertView.findViewById(R.id.layoutReferral);
            TextView tvReferralText = convertView.findViewById(R.id.tvReferralText);

            ivDeviceIcon.setImageResource(item.getDeviceIconResId());

            String flag = item.getCountryFlag();
            String flagPrefix = (flag != null && !flag.isEmpty()) ? (flag + " ") : "";
            String locName = (item.city != null && !item.city.isEmpty()) ? (item.city + ", " + (item.country != null ? item.country : "")) : ((item.country != null && !item.country.isEmpty()) ? item.country : "Site Visit");
            tvLocation.setText(flagPrefix + locName);

            String visitBadgeText = "#" + item.visitCount;
            tvVisitBadge.setText(visitBadgeText);

            if (item.isSharedVisit()) {
                if (layoutReferral != null) layoutReferral.setVisibility(View.VISIBLE);
                if (tvReferralText != null) tvReferralText.setText("Shared via " + (item.referredBy != null ? item.referredBy : ""));
            } else {
                if (layoutReferral != null) layoutReferral.setVisibility(View.GONE);
            }

            String devStr = item.device != null ? item.device : "Desktop";
            if (item.ram != null && !item.ram.isEmpty() && !item.ram.equals("N/A")) {
                devStr += " • " + item.ram;
            }
            tvDevice.setText(devStr);
            tvBattery.setText((item.battery != null && !item.battery.isEmpty()) ? item.battery : "N/A");
            String netStr = item.ip != null ? item.ip : "";
            if (item.network != null && !item.network.isEmpty() && !item.network.equals("N/A")) {
                netStr += " • " + item.network;
            }
            tvNetwork.setText(netStr);
            tvTime.setText(item.rowTimestamp != null ? item.rowTimestamp : "");

            return convertView;
        }
    }
}
