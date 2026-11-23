package com.max.hive;

import android.app.Activity;
import android.content.ActivityNotFoundException;
import android.content.ClipData;
import android.content.ClipboardManager;
import android.content.Context;
import android.content.Intent;
import android.graphics.Bitmap;
import android.graphics.BitmapFactory;
import android.net.Uri;
import android.os.Bundle;
import android.util.Base64;
import android.view.LayoutInflater;
import android.view.View;
import android.widget.Button;
import android.widget.ImageButton;
import android.widget.ImageView;
import android.widget.LinearLayout;
import android.widget.ProgressBar;
import android.widget.TextView;
import android.widget.Toast;

import java.io.File;
import java.io.FileOutputStream;
import java.io.InputStream;
import java.net.HttpURLConnection;
import java.net.URL;
import java.util.ArrayList;
import java.util.List;
import java.util.Locale;

public class DetailActivity extends Activity implements View.OnClickListener, View.OnLongClickListener {

    private IngestionItem item;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        UiUtils.applySystemUiBars(this);
        setContentView(R.layout.activity_detail);

        handleIntent(getIntent());
    }

    @Override
    protected void onNewIntent(Intent intent) {
        super.onNewIntent(intent);
        setIntent(intent);
        handleIntent(intent);
    }

    private void handleIntent(Intent intent) {
        if (intent == null) {
            finish();
            return;
        }

        String itemId = intent.getStringExtra("item_id");
        if (itemId != null && !itemId.isEmpty()) {
            item = DataRepository.getItem(itemId);
        }

        if (item == null) {
            try {
                item = (IngestionItem) intent.getSerializableExtra("item");
            } catch (Throwable e) {}
        }

        // Reconstruct from robust primitive extras (cold-start & IPC safe)
        if (item == null && (intent.hasExtra("extra_name") || intent.hasExtra("extra_message") || intent.hasExtra("extra_id"))) {
            item = new IngestionItem();
            item.id = intent.getStringExtra("extra_id");
            item.type = intent.getStringExtra("extra_type");
            item.name = intent.getStringExtra("extra_name");
            item.email = intent.getStringExtra("extra_email");
            item.phone = intent.getStringExtra("extra_phone");
            item.subject = intent.getStringExtra("extra_subject");
            item.message = intent.getStringExtra("extra_message");
            item.city = intent.getStringExtra("extra_city");
            item.country = intent.getStringExtra("extra_country");
            item.device = intent.getStringExtra("extra_device");
            item.ip = intent.getStringExtra("extra_ip");
            item.rowTimestamp = intent.getStringExtra("extra_timestamp");
            item.visitCount = intent.getIntExtra("extra_visit_count", 1);
            item.visitorId = intent.getStringExtra("extra_visitor_id");
            item.hasAttachment = intent.getBooleanExtra("extra_has_attachment", false);
            item.attachmentName = intent.getStringExtra("extra_attachment_name");
            item.ram = intent.getStringExtra("extra_ram");
            item.cores = intent.getStringExtra("extra_cores");
            item.gpu = intent.getStringExtra("extra_gpu");
            item.screen = intent.getStringExtra("extra_screen");
            item.timezone = intent.getStringExtra("extra_timezone");
            if (item.name == null || item.name.isEmpty()) item.name = "Portfolio Submitter";
            if (item.type == null) item.type = "CONTACT_SUBMISSION";
            if (item.rowTimestamp == null) item.rowTimestamp = "Just now";
        }

        if (item == null) {
            Toast.makeText(this, "Message details unavailable", Toast.LENGTH_SHORT).show();
            finish();
            return;
        }

        item.ensureNonNull();
        bindViews();
    }

    private static boolean isBlank(String s) {
        return s == null || s.trim().isEmpty();
    }

    private static String safeStr(String s, String def) {
        return (s != null && !s.trim().isEmpty()) ? s.trim() : def;
    }

    private void bindViews() {
        ImageButton btnBack = findViewById(R.id.btnBack);
        ImageButton btnShare = findViewById(R.id.btnShare);
        btnBack.setOnClickListener(this);
        btnShare.setOnClickListener(this);

        TextView tvTitle = findViewById(R.id.tvDetailTitle);
        ImageView ivDevice = findViewById(R.id.ivDetailDevice);
        TextView tvName = findViewById(R.id.tvDetailName);
        TextView tvFlag = findViewById(R.id.tvDetailFlag);
        TextView tvEmail = findViewById(R.id.tvDetailEmail);
        TextView tvPhone = findViewById(R.id.tvDetailPhone);
        TextView tvTimestamp = findViewById(R.id.tvDetailTimestamp);
        TextView tvSubject = findViewById(R.id.tvDetailSubject);
        TextView tvMessage = findViewById(R.id.tvDetailMessage);
        TextView tvTelemetry = findViewById(R.id.tvDetailTelemetry);

        Button btnCall = findViewById(R.id.btnCall);
        Button btnWhatsApp = findViewById(R.id.btnWhatsApp);
        Button btnEmail = findViewById(R.id.btnEmail);

        item.ensureNonNull();
        boolean isVisit = "VISITOR_ALERT".equals(item.type);
        tvTitle.setText(isVisit ? "Visit Details" : "Message Details");

        ivDevice.setImageResource(item.getDeviceIconResId());

        String flag = item.getCountryFlag();
        if (!isBlank(flag)) {
            tvFlag.setText(flag);
            tvFlag.setVisibility(View.VISIBLE);
        } else {
            tvFlag.setVisibility(View.GONE);
        }

        if (isVisit) {
            String loc = isBlank(item.city) ? (isBlank(item.country) ? "Unknown Location" : item.country) : (item.city + ", " + safeStr(item.country, ""));
            tvName.setText(loc);
            tvEmail.setText("Visitor ID: #" + safeStr(item.visitorId, "Unknown"));
            String visitText = "Visit Count: #" + item.visitCount;
            if (!isBlank(item.referredBy)) {
                visitText += " | Referred by: " + item.referredBy;
            }
            tvPhone.setText(visitText);
            btnCall.setVisibility(View.GONE);
            btnWhatsApp.setVisibility(View.GONE);
            btnEmail.setVisibility(View.GONE);
        } else {
            tvName.setText(safeStr(item.name, "Portfolio Submitter"));
            tvEmail.setText(safeStr(item.email, "No email provided"));
            tvPhone.setText(safeStr(item.phone, "No phone provided"));
        }

        tvTimestamp.setText("Received: " + safeStr(item.rowTimestamp, "Just now"));
        tvSubject.setText(safeStr(item.subject, "Direct Contact"));
        tvMessage.setText(safeStr(item.message, "(No message text)"));

        tvMessage.setOnLongClickListener(this);

        // Call Action
        if (item.phone != null && !item.phone.trim().isEmpty() && !item.phone.contains("Not Provided") && !item.phone.contains("No phone")) {
            btnCall.setEnabled(true);
            btnCall.setOnClickListener(this);
        } else {
            btnCall.setEnabled(false);
            btnCall.setAlpha(0.4f);
        }

        // WhatsApp Action
        if (item.phone != null && !item.phone.trim().isEmpty() && !item.phone.contains("Not Provided") && !item.phone.contains("No phone")) {
            btnWhatsApp.setEnabled(true);
            btnWhatsApp.setOnClickListener(this);
        } else {
            btnWhatsApp.setEnabled(false);
            btnWhatsApp.setAlpha(0.4f);
        }

        // Email Action
        if (item.email != null && item.email.contains("@")) {
            btnEmail.setEnabled(true);
            btnEmail.setOnClickListener(this);
        } else {
            btnEmail.setEnabled(false);
            btnEmail.setAlpha(0.4f);
        }

        // Multi-Attachment Section
        LinearLayout cardAttachmentSection = findViewById(R.id.cardAttachmentSection);
        LinearLayout containerAttachments = findViewById(R.id.containerAttachments);
        containerAttachments.removeAllViews();

        if (item.hasAttachment && !item.attachments.isEmpty()) {
            cardAttachmentSection.setVisibility(View.VISIBLE);
            LayoutInflater inflater = LayoutInflater.from(this);

            for (final IngestionItem.AttachmentItem att : item.attachments) {
                renderAttachmentCard(inflater, containerAttachments, att);
            }
        } else if (item.hasAttachment && item.attachmentDataUri != null && !item.attachmentDataUri.isEmpty()) {
            // Backward compatibility fallback for single attachment
            cardAttachmentSection.setVisibility(View.VISIBLE);
            LayoutInflater inflater = LayoutInflater.from(this);

            final IngestionItem.AttachmentItem att = new IngestionItem.AttachmentItem();
            att.name = item.attachmentName.isEmpty() ? "Attachment" : item.attachmentName;
            att.dataUri = item.attachmentDataUri;
            att.type = "image/jpeg";
            renderAttachmentCard(inflater, containerAttachments, att);
        } else {
            cardAttachmentSection.setVisibility(View.GONE);
        }

        // Expanded Deep Telemetry & Hardware Specifications
        StringBuilder sb = new StringBuilder();
        if (!item.ip.isEmpty()) sb.append("IP Address: ").append(item.ip).append("\n");
        if (!item.city.isEmpty() || !item.country.isEmpty()) sb.append("Location: ").append(item.city).append(", ").append(item.country).append("\n");
        if (!item.device.isEmpty()) sb.append("Device Hardware: ").append(item.device).append("\n");
        if (!item.os.isEmpty()) sb.append("Operating System: ").append(item.os).append("\n");
        if (!item.browser.isEmpty()) sb.append("Browser Engine: ").append(item.browser).append("\n");
        if (!item.cores.isEmpty() && !item.cores.equals("N/A")) sb.append("CPU Cores: ").append(item.cores).append("\n");
        if (!item.ram.isEmpty() && !item.ram.equals("N/A")) sb.append("System RAM: ").append(item.ram).append("\n");
        if (!item.gpu.isEmpty() && !item.gpu.equals("N/A")) sb.append("Graphics (GPU): ").append(item.gpu).append("\n");
        if (!item.screen.isEmpty() && !item.screen.equals("N/A")) sb.append("Display Resolution: ").append(item.screen).append("\n");
        if (!item.battery.isEmpty() && !item.battery.equals("N/A")) sb.append("Battery Status: ").append(item.battery).append("\n");
        if (!item.network.isEmpty() && !item.network.equals("N/A")) sb.append("Network Link: ").append(item.network).append("\n");
        if (!item.isp.isEmpty() && !item.isp.equals("N/A")) sb.append("Internet Provider (ISP): ").append(item.isp).append("\n");
        if (!item.timezone.isEmpty() && !item.timezone.equals("N/A")) sb.append("System Timezone: ").append(item.timezone).append("\n");
        if (item.visitCount > 0) sb.append("Lifetime Visits: ").append(item.visitCount);

        tvTelemetry.setText(sb.toString().trim());
    }

    private void renderAttachmentCard(LayoutInflater inflater, LinearLayout container, final IngestionItem.AttachmentItem att) {
        final View card = inflater.inflate(R.layout.item_attachment_card, container, false);
        ImageView ivIcon = card.findViewById(R.id.ivAttachmentIcon);
        TextView tvNameAtt = card.findViewById(R.id.tvAttachmentName);
        TextView tvMeta = card.findViewById(R.id.tvAttachmentMeta);
        final ImageView ivPreview = card.findViewById(R.id.ivAttachmentPreview);
        final Button btnAction = card.findViewById(R.id.btnAttachmentAction);
        final ProgressBar pbDownload = card.findViewById(R.id.pbAttachmentDownload);
        final TextView tvProgress = card.findViewById(R.id.tvAttachmentProgress);

        if (att == null) return;
        att.ensureNonNull();
        ivIcon.setImageResource(att.getIconResId());
        tvNameAtt.setText(safeStr(att.name, "Attachment"));
        tvMeta.setText(safeStr(att.type, "File") + " | " + att.getFormattedSize());

        // High-fidelity image preview from local disk or base64 dataUri
        loadAttachmentPreview(att, ivPreview);

        // Check if file is already on device or can be decoded directly
        final File existingFile = getExistingAttachmentFile(att);
        final boolean isReadyLocally = (existingFile != null && existingFile.exists()) ||
                (att.dataUri != null && att.dataUri.contains(","));

        if (isReadyLocally) {
            btnAction.setText("OPEN WITH");
        } else {
            btnAction.setText("DOWNLOAD");
        }

        final View.OnClickListener triggerOpenOrDownload = new View.OnClickListener() {
            @Override
            public void onClick(View v) {
                HapticHelper.performClick(v);
                File checkFile = getExistingAttachmentFile(att);
                if ((checkFile != null && checkFile.exists()) || (att.dataUri != null && att.dataUri.contains(","))) {
                    openWithNativeChooser(att);
                } else {
                    startAttachmentDownload(att, btnAction, pbDownload, tvProgress, ivPreview);
                }
            }
        };

        btnAction.setOnClickListener(triggerOpenOrDownload);
        card.setOnClickListener(triggerOpenOrDownload);
        ivPreview.setOnClickListener(triggerOpenOrDownload);

        container.addView(card);
    }

    private void loadAttachmentPreview(final IngestionItem.AttachmentItem att, final ImageView ivPreview) {
        if (!att.isImage() || ivPreview == null) return;
        Bitmap bmp = null;
        try {
            File existingFile = getExistingAttachmentFile(att);
            if (existingFile != null && existingFile.exists()) {
                BitmapFactory.Options opts = new BitmapFactory.Options();
                opts.inJustDecodeBounds = true;
                BitmapFactory.decodeFile(existingFile.getAbsolutePath(), opts);
                opts.inSampleSize = calculateInSampleSize(opts, 1200, 1200);
                opts.inJustDecodeBounds = false;
                bmp = BitmapFactory.decodeFile(existingFile.getAbsolutePath(), opts);
            }
        } catch (Throwable ignored) {}

        if (bmp == null && att.dataUri != null && att.dataUri.contains(",")) {
            try {
                String b64 = att.dataUri.substring(att.dataUri.indexOf(",") + 1);
                byte[] decoded = Base64.decode(b64, Base64.DEFAULT);
                BitmapFactory.Options opts = new BitmapFactory.Options();
                opts.inJustDecodeBounds = true;
                BitmapFactory.decodeByteArray(decoded, 0, decoded.length, opts);
                opts.inSampleSize = calculateInSampleSize(opts, 1200, 1200);
                opts.inJustDecodeBounds = false;
                bmp = BitmapFactory.decodeByteArray(decoded, 0, decoded.length, opts);
            } catch (Throwable ignored) {}
        }

        if (bmp != null) {
            ivPreview.setImageBitmap(bmp);
            ivPreview.setVisibility(View.VISIBLE);
        }
    }

    private File getAttachmentTargetFile(IngestionItem.AttachmentItem att) {
        String cleanName = att.name != null ? att.name.replaceAll("[^a-zA-Z0-9._-]", "_") : "";
        if (cleanName.isEmpty()) {
            cleanName = (att.fileId != null && !att.fileId.isEmpty()) ? att.fileId : ("att_" + System.currentTimeMillis());
        }

        File extDownloads = getExternalFilesDir("downloads");
        if (extDownloads != null) {
            return new File(extDownloads, cleanName);
        }
        File cacheDir = new File(getCacheDir(), "attachments");
        if (!cacheDir.exists()) cacheDir.mkdirs();
        return new File(cacheDir, cleanName);
    }

    private File getExistingAttachmentFile(IngestionItem.AttachmentItem att) {
        String cleanName = att.name != null ? att.name.replaceAll("[^a-zA-Z0-9._-]", "_") : "";
        if (cleanName.isEmpty()) return null;

        File extDownloads = getExternalFilesDir("downloads");
        if (extDownloads != null) {
            File f = new File(extDownloads, cleanName);
            if (f.exists()) return f;
        }

        File cacheAtts = new File(getCacheDir(), "attachments");
        File fCacheAtts = new File(cacheAtts, cleanName);
        if (fCacheAtts.exists()) return fCacheAtts;

        File fCache = new File(getCacheDir(), cleanName);
        if (fCache.exists()) return fCache;

        return null;
    }

    private void openWithNativeChooser(IngestionItem.AttachmentItem att) {
        try {
            File file = getExistingAttachmentFile(att);

            // If not yet written to disk but inline base64 exists, write it out now
            if ((file == null || !file.exists()) && att.dataUri != null && att.dataUri.contains(",")) {
                file = getAttachmentTargetFile(att);
                if (file.getParentFile() != null && !file.getParentFile().exists()) {
                    file.getParentFile().mkdirs();
                }
                String b64 = att.dataUri.substring(att.dataUri.indexOf(",") + 1);
                byte[] decoded = Base64.decode(b64, Base64.DEFAULT);
                FileOutputStream fos = new FileOutputStream(file);
                fos.write(decoded);
                fos.flush();
                fos.close();
            }

            if (file == null || !file.exists()) {
                Toast.makeText(this, "File not downloaded yet. Please tap DOWNLOAD.", Toast.LENGTH_SHORT).show();
                return;
            }

            Uri contentUri = GenericFileProvider.getUriForFile(this, file);
            String mime = att.type;
            if (mime == null || mime.isEmpty() || "*/*".equals(mime)) {
                mime = getContentResolver().getType(contentUri);
            }
            if (mime == null) mime = "*/*";

            Intent viewIntent = new Intent(Intent.ACTION_VIEW);
            viewIntent.setDataAndType(contentUri, mime);
            viewIntent.addFlags(Intent.FLAG_GRANT_READ_URI_PERMISSION);
            viewIntent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK);

            Intent chooser = Intent.createChooser(viewIntent, "Open with");
            startActivity(chooser);
        } catch (ActivityNotFoundException e) {
            Toast.makeText(this, "No application found on device to open this file format.", Toast.LENGTH_LONG).show();
        } catch (Throwable t) {
            Toast.makeText(this, "Open error: " + t.getMessage(), Toast.LENGTH_SHORT).show();
        }
    }

    private void startAttachmentDownload(final IngestionItem.AttachmentItem att, final Button btnAction, final ProgressBar pbDownload, final TextView tvProgress, final ImageView ivPreview) {
        if (att.downloadUrl == null || att.downloadUrl.isEmpty()) {
            Toast.makeText(this, "Remote download link unavailable", Toast.LENGTH_SHORT).show();
            return;
        }

        btnAction.setEnabled(false);
        pbDownload.setVisibility(View.VISIBLE);
        pbDownload.setProgress(0);
        tvProgress.setVisibility(View.VISIBLE);
        tvProgress.setText("Connecting to server...");

        new Thread(new Runnable() {
            @Override
            public void run() {
                try {
                    String rawUrl = att.downloadUrl;
                    List<String> tryUrls = new ArrayList<String>();
                    if (rawUrl.startsWith("http://") || rawUrl.startsWith("https://")) {
                        tryUrls.add(rawUrl);
                    } else {
                        String rel = rawUrl.startsWith("/") ? rawUrl : ("/" + rawUrl);
                        tryUrls.add("http://10.0.2.2:7070" + rel);
                        tryUrls.add("http://127.0.0.1:7070" + rel);
                        tryUrls.add("http://10.0.0.111:7070" + rel);
                        tryUrls.add("http://10.0.2.2:7071" + rel);
                        tryUrls.add("http://127.0.0.1:7071" + rel);
                    }

                    HttpURLConnection conn = null;
                    int responseCode = 0;
                    for (String candidateUrl : tryUrls) {
                        try {
                            if (conn != null) {
                                conn.disconnect();
                                conn = null;
                            }
                            conn = (HttpURLConnection) new URL(candidateUrl).openConnection();
                            conn.setConnectTimeout(4000);
                            conn.setReadTimeout(30000);
                            conn.setRequestMethod("GET");
                            responseCode = conn.getResponseCode();
                            if (responseCode == 200) {
                                break;
                            }
                        } catch (Exception ignored) {
                            responseCode = 0;
                        }
                    }

                    if (conn == null || responseCode != 200) {
                        throw new Exception("Server returned HTTP " + responseCode);
                    }

                    long totalLength = conn.getContentLengthLong();
                    if (totalLength <= 0) totalLength = att.size;

                    File targetFile = getAttachmentTargetFile(att);
                    if (targetFile.getParentFile() != null && !targetFile.getParentFile().exists()) {
                        targetFile.getParentFile().mkdirs();
                    }

                    InputStream is = conn.getInputStream();
                    FileOutputStream fos = new FileOutputStream(targetFile);
                    byte[] buffer = new byte[32768];
                    int read;
                    long downloaded = 0;
                    long lastUiUpdate = 0;

                    while ((read = is.read(buffer)) != -1) {
                        fos.write(buffer, 0, read);
                        downloaded += read;
                        long now = System.currentTimeMillis();
                        if (now - lastUiUpdate > 80) {
                            lastUiUpdate = now;
                            final int progressPct = totalLength > 0 ? (int) ((downloaded * 100) / totalLength) : 0;
                            final long dBytes = downloaded;
                            final long tBytes = totalLength;

                            runOnUiThread(new Runnable() {
                                @Override
                                public void run() {
                                    pbDownload.setProgress(progressPct);
                                    tvProgress.setText("Downloading " + progressPct + "% (" + formatBytes(dBytes) + " / " + formatBytes(tBytes) + ")...");
                                }
                            });
                        }
                    }

                    fos.flush();
                    fos.close();
                    is.close();
                    conn.disconnect();

                    final File finalFile = targetFile;
                    runOnUiThread(new Runnable() {
                        @Override
                        public void run() {
                            pbDownload.setVisibility(View.GONE);
                            tvProgress.setVisibility(View.GONE);
                            btnAction.setEnabled(true);
                            btnAction.setText("OPEN WITH");
                            loadAttachmentPreview(att, ivPreview);
                            Toast.makeText(DetailActivity.this, "Download complete", Toast.LENGTH_SHORT).show();
                            openWithNativeChooser(att);
                        }
                    });

                } catch (final Exception ex) {
                    runOnUiThread(new Runnable() {
                        @Override
                        public void run() {
                            pbDownload.setVisibility(View.GONE);
                            tvProgress.setVisibility(View.VISIBLE);
                            tvProgress.setText("Download failed: " + ex.getMessage());
                            btnAction.setEnabled(true);
                            btnAction.setText("RETRY");
                        }
                    });
                }
            }
        }).start();
    }

    private String formatBytes(long bytes) {
        if (bytes <= 0) return "0 B";
        if (bytes < 1024) return bytes + " B";
        if (bytes < 1024 * 1024) return (bytes / 1024) + " KB";
        if (bytes < 1024L * 1024 * 1024) return String.format(Locale.US, "%.1f MB", (float) bytes / (1024 * 1024));
        return String.format(Locale.US, "%.2f GB", (double) bytes / (1024L * 1024 * 1024));
    }

    private int calculateInSampleSize(BitmapFactory.Options options, int reqWidth, int reqHeight) {
        final int height = options.outHeight;
        final int width = options.outWidth;
        int inSampleSize = 1;

        if (height > reqHeight || width > reqWidth) {
            final int halfHeight = height / 2;
            final int halfWidth = width / 2;
            while ((halfHeight / inSampleSize) >= reqHeight && (halfWidth / inSampleSize) >= reqWidth) {
                inSampleSize *= 2;
            }
        }
        return inSampleSize;
    }

    @Override
    public void onClick(View v) {
        HapticHelper.performClick(v);
        int id = v.getId();
        if (id == R.id.btnBack) {
            finish();
        } else if (id == R.id.btnShare) {
            shareSummary();
        } else if (id == R.id.btnCall) {
            makeCall();
        } else if (id == R.id.btnWhatsApp) {
            openWhatsApp();
        } else if (id == R.id.btnEmail) {
            sendEmail();
        }
    }

    private void shareSummary() {
        if (item == null) return;
        String text = "Portfolio Inquiry:\n" +
                "From: " + item.name + "\n" +
                "Email: " + item.email + "\n" +
                "Phone: " + item.phone + "\n" +
                "Subject: " + item.subject + "\n" +
                "Message: " + item.message;

        Intent sendIntent = new Intent();
        sendIntent.setAction(Intent.ACTION_SEND);
        sendIntent.putExtra(Intent.EXTRA_TEXT, text);
        sendIntent.setType("text/plain");
        startActivity(Intent.createChooser(sendIntent, "Share Message"));
    }

    private void makeCall() {
        if (item == null || item.phone == null || item.phone.trim().isEmpty()) return;
        try {
            Intent intent = new Intent(Intent.ACTION_DIAL);
            intent.setData(Uri.parse("tel:" + item.phone.replaceAll("[^0-9+]", "")));
            startActivity(intent);
        } catch (Exception e) {
            Toast.makeText(this, "Could not launch dialer", Toast.LENGTH_SHORT).show();
        }
    }

    private void openWhatsApp() {
        if (item == null || item.phone == null || item.phone.trim().isEmpty()) return;
        try {
            String num = item.phone.replaceAll("[^0-9]", "");
            Intent intent = new Intent(Intent.ACTION_VIEW);
            intent.setData(Uri.parse("https://api.whatsapp.com/send?phone=" + num));
            startActivity(intent);
        } catch (Exception e) {
            Toast.makeText(this, "WhatsApp not available", Toast.LENGTH_SHORT).show();
        }
    }

    private void sendEmail() {
        if (item == null || item.email == null || item.email.trim().isEmpty()) return;
        try {
            Intent intent = new Intent(Intent.ACTION_SENDTO);
            intent.setData(Uri.parse("mailto:" + item.email));
            intent.putExtra(Intent.EXTRA_SUBJECT, "Re: " + (item.subject != null ? item.subject : ""));
            startActivity(intent);
        } catch (Exception e) {
            Toast.makeText(this, "Email client not available", Toast.LENGTH_SHORT).show();
        }
    }

    @Override
    public boolean onLongClick(View v) {
        if (item != null && !item.message.isEmpty()) {
            HapticHelper.performTick(this);
            ClipboardManager cm = (ClipboardManager) getSystemService(Context.CLIPBOARD_SERVICE);
            ClipData cd = ClipData.newPlainText("Message Text", item.message);
            if (cm != null) {
                cm.setPrimaryClip(cd);
                Toast.makeText(this, "Message copied to clipboard", Toast.LENGTH_SHORT).show();
            }
            return true;
        }
        return false;
    }
}
