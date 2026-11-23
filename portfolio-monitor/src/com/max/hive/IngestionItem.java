package com.max.hive;

import org.json.JSONArray;
import org.json.JSONObject;
import java.io.Serializable;
import java.util.ArrayList;
import java.util.List;
import java.util.Locale;

public class IngestionItem implements Serializable {
    private static final long serialVersionUID = 1L;

    public static class AttachmentItem implements Serializable {
        private static final long serialVersionUID = 1L;

        public String name = "";
        public String type = "";
        public long size = 0;
        public String dataUri = "";
        public String downloadUrl = "";
        public String fileId = "";

        public boolean isImage() {
            if (type != null && type.startsWith("image/")) return true;
            String n = name != null ? name.toLowerCase(Locale.US) : "";
            return n.endsWith(".jpg") || n.endsWith(".jpeg") || n.endsWith(".png") || n.endsWith(".webp") || n.endsWith(".gif");
        }

        public boolean isPdf() {
            if (type != null && type.contains("pdf")) return true;
            String n = name != null ? name.toLowerCase(Locale.US) : "";
            return n.endsWith(".pdf");
        }

        public boolean isZip() {
            String n = name != null ? name.toLowerCase(Locale.US) : "";
            return n.endsWith(".zip") || n.endsWith(".tar") || n.endsWith(".gz") || n.endsWith(".rar") || n.endsWith(".7z");
        }

        public String getFormattedSize() {
            if (size <= 0) return "File";
            if (size < 1024) return size + " B";
            if (size < 1024 * 1024) return (size / 1024) + " KB";
            if (size < 1024L * 1024 * 1024) return String.format(Locale.US, "%.1f MB", (float) size / (1024 * 1024));
            return String.format(Locale.US, "%.2f GB", (double) size / (1024L * 1024 * 1024));
        }

        public int getIconResId() {
            if (isImage()) return R.drawable.ic_image;
            if (isPdf()) return R.drawable.ic_file_pdf;
            if (isZip()) return R.drawable.ic_file_zip;
            return R.drawable.ic_file_generic;
        }

        public void ensureNonNull() {
            if (name == null) name = "";
            if (type == null) type = "";
            if (dataUri == null) dataUri = "";
            if (downloadUrl == null) downloadUrl = "";
            if (fileId == null) fileId = "";
        }
    }

    public String rowTimestamp = "";
    public String rawCiphertext = "";
    public String type = "UNKNOWN"; // "CONTACT_SUBMISSION" or "VISITOR_ALERT"
    public String id = "";
    public String visitorId = "";
    public String referredBy = "";
    public int visitCount = 1;
    public long timestamp = 0;

    // Contact fields
    public String name = "";
    public String email = "";
    public String phone = "";
    public String subject = "";
    public String message = "";

    // Telemetry fields
    public String device = "";
    public String os = "";
    public String browser = "";
    public String ip = "";
    public String city = "";
    public String country = "";
    public String battery = "";
    public String network = "";
    public String isp = "";
    public String ram = "";
    public String cores = "";
    public String screen = "";
    public String gpu = "";
    public String timezone = "";

    // Multi-Attachment collection
    public boolean hasAttachment = false;
    public String attachmentName = "";
    public String attachmentDataUri = "";
    public final List<AttachmentItem> attachments = new ArrayList<>();

    public boolean isSharedVisit() {
        return referredBy != null && !referredBy.trim().isEmpty() && !referredBy.equalsIgnoreCase("None") && !referredBy.equalsIgnoreCase("null");
    }

    public void ensureNonNull() {
        if (rowTimestamp == null) rowTimestamp = "";
        if (rawCiphertext == null) rawCiphertext = "";
        if (type == null) type = "UNKNOWN";
        if (id == null) id = "";
        if (visitorId == null) visitorId = "";
        if (referredBy == null) referredBy = "";
        if (name == null) name = "";
        if (email == null) email = "";
        if (phone == null) phone = "";
        if (subject == null) subject = "";
        if (message == null) message = "";
        if (device == null) device = "";
        if (os == null) os = "";
        if (browser == null) browser = "";
        if (ip == null) ip = "";
        if (city == null) city = "";
        if (country == null) country = "";
        if (battery == null) battery = "";
        if (network == null) network = "";
        if (isp == null) isp = "";
        if (ram == null) ram = "";
        if (cores == null) cores = "";
        if (screen == null) screen = "";
        if (gpu == null) gpu = "";
        if (timezone == null) timezone = "";
        if (attachmentName == null) attachmentName = "";
        if (attachmentDataUri == null) attachmentDataUri = "";
        if (attachments != null) {
            for (AttachmentItem att : attachments) {
                if (att != null) att.ensureNonNull();
            }
        }
    }

    public String getCountryFlag() {
        return CountryUtils.getFlagEmoji(country);
    }

    public int getDeviceIconResId() {
        return DeviceUtils.getDeviceIconResId(device, os, browser);
    }

    public boolean matchesQuery(String q) {
        if (q == null || q.trim().isEmpty()) return true;
        String query = q.trim().toLowerCase(Locale.US);

        if (name != null && name.toLowerCase(Locale.US).contains(query)) return true;
        if (email != null && email.toLowerCase(Locale.US).contains(query)) return true;
        if (phone != null && phone.toLowerCase(Locale.US).contains(query)) return true;
        if (subject != null && subject.toLowerCase(Locale.US).contains(query)) return true;
        if (message != null && message.toLowerCase(Locale.US).contains(query)) return true;
        if (city != null && city.toLowerCase(Locale.US).contains(query)) return true;
        if (country != null && country.toLowerCase(Locale.US).contains(query)) return true;
        if (ip != null && ip.toLowerCase(Locale.US).contains(query)) return true;
        if (device != null && device.toLowerCase(Locale.US).contains(query)) return true;
        if (browser != null && browser.toLowerCase(Locale.US).contains(query)) return true;
        if (id != null && id.toLowerCase(Locale.US).contains(query)) return true;
        if (referredBy != null && referredBy.toLowerCase(Locale.US).contains(query)) return true;

        for (AttachmentItem att : attachments) {
            if (att.name != null && att.name.toLowerCase(Locale.US).contains(query)) return true;
        }

        return false;
    }

    public static String cleanText(String input) {
        if (input == null) return "";
        return input.replaceAll("[\\u2014\\u2013]", " - ")
                    .trim();
    }

    public static IngestionItem fromJson(String sheetTimestamp, String rawCipher, String jsonStr) {
        if (jsonStr == null || jsonStr.trim().isEmpty()) return null;
        try {
            JSONObject obj = new JSONObject(jsonStr);

            // Unwrap nested payload wrapper if present
            if (obj.has("encrypted") && obj.optJSONObject("encrypted") != null) {
                obj = obj.getJSONObject("encrypted");
            } else if (obj.has("payload") && obj.optJSONObject("payload") != null) {
                obj = obj.getJSONObject("payload");
            } else if (obj.has("data") && obj.optJSONObject("data") != null) {
                obj = obj.getJSONObject("data");
            }

            IngestionItem item = new IngestionItem();
            item.rowTimestamp = cleanText(sheetTimestamp != null ? sheetTimestamp : "");
            // Memory optimization: Store compact fingerprint instead of retaining giant base64 payload
            item.rawCiphertext = (rawCipher != null && rawCipher.length() > 64) ? rawCipher.substring(0, 64) : (rawCipher != null ? rawCipher : "");
            item.type = obj.optString("type", "UNKNOWN");
            item.id = obj.optString("id", "");
            item.visitorId = cleanText(obj.optString("visitorId", ""));
            item.referredBy = cleanText(obj.optString("referredBy", obj.optString("sharedBy", "")));
            item.visitCount = obj.optInt("visitCount", 1);
            item.timestamp = obj.optLong("timestamp", System.currentTimeMillis());

            // 1. Parse Sender (Check nested sender object first)
            if (obj.has("sender") && obj.optJSONObject("sender") != null) {
                JSONObject s = obj.getJSONObject("sender");
                item.name = cleanText(s.optString("name", s.optString("fullName", s.optString("senderName", ""))));
                item.email = cleanText(s.optString("email", ""));
                item.phone = cleanText(s.optString("phone", ""));
                item.subject = cleanText(s.optString("subject", ""));
                item.message = cleanText(s.optString("message", ""));
            }

            // 2. Fallback to root-level fields if name/contact info is at top level
            if (item.name.isEmpty()) {
                item.name = cleanText(obj.optString("name", obj.optString("fullName", obj.optString("senderName", obj.optString("firstname", "")))));
                String lastName = cleanText(obj.optString("lastname", ""));
                if (!lastName.isEmpty()) {
                    item.name = (item.name + " " + lastName).trim();
                }
            }
            if (item.email.isEmpty()) {
                item.email = cleanText(obj.optString("email", ""));
            }
            if (item.phone.isEmpty()) {
                item.phone = cleanText(obj.optString("phone", ""));
            }
            if (item.subject.isEmpty()) {
                item.subject = cleanText(obj.optString("subject", "Direct Contact"));
            }
            if (item.message.isEmpty()) {
                item.message = cleanText(obj.optString("message", ""));
            }

            // If contact submission and name is still empty, fallback to email user or clean title
            if ("CONTACT_SUBMISSION".equals(item.type) && item.name.isEmpty()) {
                if (!item.email.isEmpty() && item.email.contains("@")) {
                    item.name = item.email.substring(0, item.email.indexOf("@"));
                } else {
                    item.name = "Portfolio Submitter";
                }
            }

            // Parse Telemetry
            if (obj.has("telemetry") && obj.optJSONObject("telemetry") != null) {
                JSONObject t = obj.getJSONObject("telemetry");
                item.device = cleanText(t.optString("device", t.optString("deviceModel", "Unknown Device")));
                item.os = cleanText(t.optString("os", ""));
                item.browser = cleanText(t.optString("browser", ""));
                item.ip = cleanText(t.optString("ip", ""));
                item.city = cleanText(t.optString("city", ""));
                item.country = cleanText(t.optString("country", ""));
                item.battery = cleanText(t.optString("battery", ""));
                item.network = cleanText(t.optString("network", t.optString("connection", "")));
                item.isp = cleanText(t.optString("isp", ""));
                item.ram = cleanText(t.optString("ram", t.optString("memory", "")));
                item.cores = cleanText(t.optString("cores", t.optString("cpu", "")));
                item.screen = cleanText(t.optString("screen", ""));
                item.gpu = cleanText(t.optString("gpu", ""));
                item.timezone = cleanText(t.optString("timezone", ""));
                if (item.referredBy.isEmpty() || item.referredBy.equalsIgnoreCase("None")) {
                    item.referredBy = cleanText(t.optString("referredBy", t.optString("sharedBy", "")));
                }
            } else {
                if (item.device.isEmpty()) item.device = cleanText(obj.optString("device", "Desktop"));
                if (item.city.isEmpty()) item.city = cleanText(obj.optString("city", ""));
                if (item.country.isEmpty()) item.country = cleanText(obj.optString("country", ""));
                if (item.ip.isEmpty()) item.ip = cleanText(obj.optString("ip", ""));
            }

            if (item.referredBy.equalsIgnoreCase("None") || item.referredBy.equalsIgnoreCase("null")) {
                item.referredBy = "";
            }

            // Parse Multi-Attachments
            if (obj.has("attachments")) {
                JSONArray arr = obj.optJSONArray("attachments");
                if (arr != null && arr.length() > 0) {
                    item.hasAttachment = true;
                    for (int i = 0; i < arr.length(); i++) {
                        JSONObject attObj = arr.getJSONObject(i);
                        AttachmentItem att = new AttachmentItem();
                        att.name = cleanText(attObj.optString("name", "Attachment_" + (i + 1)));
                        att.type = attObj.optString("type", "application/octet-stream");
                        att.size = attObj.optLong("size", 0);
                        String dUri = attObj.optString("dataUri", "");
                        if (dUri.isEmpty()) dUri = attObj.optString("data", "");
                        if (dUri.isEmpty()) dUri = attObj.optString("preview", "");
                        att.dataUri = dUri;
                        att.downloadUrl = attObj.optString("downloadUrl", attObj.optString("url", ""));
                        att.fileId = attObj.optString("id", "");
                        item.attachments.add(att);
                    }
                    if (!item.attachments.isEmpty()) {
                        item.attachmentName = item.attachments.get(0).name;
                        item.attachmentDataUri = item.attachments.get(0).dataUri;
                    }
                }
            }

            return item;
        } catch (Exception e) {
            e.printStackTrace();
            return null;
        }
    }
}
