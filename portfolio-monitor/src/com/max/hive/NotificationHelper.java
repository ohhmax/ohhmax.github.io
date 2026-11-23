package com.max.hive;

import android.app.Notification;
import android.app.NotificationChannel;
import android.app.NotificationManager;
import android.app.PendingIntent;
import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.net.Uri;
import android.os.Build;

public class NotificationHelper {
    public static final String CHANNEL_ID_ALERTS = "max_hive_alerts_v4";
    public static final String CHANNEL_NAME_ALERTS = "Portfolio Alerts";

    public static final String CHANNEL_ID_FOREGROUND = "max_hive_service_v4";
    public static final String CHANNEL_NAME_FOREGROUND = "Background Monitor";

    public static void initChannels(Context context) {
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            NotificationManager nm = (NotificationManager) context.getSystemService(Context.NOTIFICATION_SERVICE);
            if (nm != null) {
                NotificationChannel alertsChannel = new NotificationChannel(
                        CHANNEL_ID_ALERTS,
                        CHANNEL_NAME_ALERTS,
                        NotificationManager.IMPORTANCE_HIGH
                );
                alertsChannel.setDescription("Alerts for portfolio messages and visits");
                alertsChannel.enableVibration(true);
                alertsChannel.setVibrationPattern(new long[]{0, 250, 150, 250});
                alertsChannel.setLockscreenVisibility(Notification.VISIBILITY_PUBLIC);
                nm.createNotificationChannel(alertsChannel);

                NotificationChannel fgChannel = new NotificationChannel(
                        CHANNEL_ID_FOREGROUND,
                        CHANNEL_NAME_FOREGROUND,
                        NotificationManager.IMPORTANCE_MIN
                );
                fgChannel.setDescription("Silent background synchronization");
                fgChannel.setShowBadge(false);
                nm.createNotificationChannel(fgChannel);
            }
        }
    }

    public static Notification buildForegroundNotification(Context context) {
        initChannels(context);
        Intent intent = new Intent(context, MainActivity.class);
        intent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK | Intent.FLAG_ACTIVITY_CLEAR_TOP);

        PendingIntent pi = PendingIntent.getActivity(
                context,
                0,
                intent,
                PendingIntent.FLAG_UPDATE_CURRENT | (Build.VERSION.SDK_INT >= Build.VERSION_CODES.M ? PendingIntent.FLAG_IMMUTABLE : 0)
        );

        Notification.Builder builder;
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            builder = new Notification.Builder(context, CHANNEL_ID_FOREGROUND);
        } else {
            builder = new Notification.Builder(context);
        }

        builder.setSmallIcon(R.drawable.ic_launcher)
               .setContentTitle("Portfolio Monitor")
               .setContentText("Sync active")
               .setContentIntent(pi)
               .setOngoing(true)
               .setPriority(Notification.PRIORITY_MIN);

        return builder.build();
    }

    public static void notifyMessage(Context context, IngestionItem item, int notificationId) {
        if (context == null || item == null) return;
        SharedPreferences prefs = context.getSharedPreferences("max_hive_prefs", Context.MODE_PRIVATE);
        if (!prefs.getBoolean(SettingsActivity.PREF_NOTIFY_MSGS, true)) {
            return;
        }

        initChannels(context);
        NotificationManager nm = (NotificationManager) context.getSystemService(Context.NOTIFICATION_SERVICE);
        if (nm == null) return;

        // Bounded notification ID to avoid exceeding system limits
        int safeId = 2000 + (item.id != null ? Math.abs(item.id.hashCode() % 20) : (notificationId % 20));

        // Store full item in cache to avoid binder TransactionTooLargeException
        DataRepository.putItem(item.id, item);

        Intent intent = new Intent(context, DetailActivity.class);
        intent.putExtra("item_id", item.id);
        intent.putExtra("extra_id", item.id);
        intent.putExtra("extra_type", item.type);
        intent.putExtra("extra_name", item.name);
        intent.putExtra("extra_email", item.email);
        intent.putExtra("extra_phone", item.phone);
        intent.putExtra("extra_subject", item.subject);
        intent.putExtra("extra_message", item.message);
        intent.putExtra("extra_city", item.city);
        intent.putExtra("extra_country", item.country);
        intent.putExtra("extra_device", item.device);
        intent.putExtra("extra_ip", item.ip);
        intent.putExtra("extra_timestamp", item.rowTimestamp);
        intent.putExtra("extra_visit_count", item.visitCount);
        intent.putExtra("extra_visitor_id", item.visitorId);
        intent.putExtra("extra_has_attachment", item.hasAttachment);
        intent.putExtra("extra_attachment_name", item.attachmentName);
        intent.putExtra("extra_ram", item.ram);
        intent.putExtra("extra_cores", item.cores);
        intent.putExtra("extra_gpu", item.gpu);
        intent.putExtra("extra_screen", item.screen);
        intent.putExtra("extra_timezone", item.timezone);
        intent.setAction("com.max.hive.VIEW_MSG_" + safeId);
        intent.setData(Uri.parse("hive://msg/" + (item.id != null && !item.id.isEmpty() ? item.id : safeId)));
        intent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK | Intent.FLAG_ACTIVITY_CLEAR_TOP);

        // Lightweight item copy without huge base64 attachments for binder safety
        IngestionItem lightItem = new IngestionItem();
        lightItem.id = item.id;
        lightItem.name = item.name;
        lightItem.email = item.email;
        lightItem.phone = item.phone;
        lightItem.subject = item.subject;
        lightItem.message = item.message;
        lightItem.city = item.city;
        lightItem.country = item.country;
        lightItem.device = item.device;
        lightItem.ip = item.ip;
        lightItem.timestamp = item.timestamp;
        lightItem.rowTimestamp = item.rowTimestamp;
        lightItem.hasAttachment = item.hasAttachment;
        lightItem.attachmentName = item.attachmentName;
        lightItem.ram = item.ram;
        lightItem.cores = item.cores;
        lightItem.gpu = item.gpu;
        lightItem.screen = item.screen;
        lightItem.timezone = item.timezone;
        intent.putExtra("item", lightItem);

        PendingIntent pi = PendingIntent.getActivity(
                context,
                safeId,
                intent,
                PendingIntent.FLAG_UPDATE_CURRENT | (Build.VERSION.SDK_INT >= Build.VERSION_CODES.M ? PendingIntent.FLAG_IMMUTABLE : 0)
        );

        Notification.Builder builder;
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            builder = new Notification.Builder(context, CHANNEL_ID_ALERTS);
        } else {
            builder = new Notification.Builder(context);
        }

        String flag = item.getCountryFlag();
        String locHeader = flag.isEmpty() ? "" : (flag + " ");
        String title = "New Message: " + locHeader + (item.name.isEmpty() ? "Anonymous" : item.name);
        String preview = (item.subject.isEmpty() ? "Inquiry" : item.subject) + " - " + item.message;

        builder.setSmallIcon(R.drawable.ic_launcher)
               .setContentTitle(title)
               .setContentText(preview)
               .setStyle(new Notification.BigTextStyle().bigText(preview))
               .setAutoCancel(true)
               .setContentIntent(pi)
               .setDefaults(Notification.DEFAULT_ALL)
               .setPriority(Notification.PRIORITY_HIGH);

        nm.notify(safeId, builder.build());
    }

    public static void notifyVisit(Context context, IngestionItem item, int notificationId) {
        if (context == null || item == null) return;
        SharedPreferences prefs = context.getSharedPreferences("max_hive_prefs", Context.MODE_PRIVATE);
        if (!prefs.getBoolean(SettingsActivity.PREF_NOTIFY_VISITS, true)) {
            return;
        }

        initChannels(context);
        NotificationManager nm = (NotificationManager) context.getSystemService(Context.NOTIFICATION_SERVICE);
        if (nm == null) return;

        // Bounded notification ID
        int safeId = 3000 + (item.id != null ? Math.abs(item.id.hashCode() % 20) : (notificationId % 20));

        DataRepository.putItem(item.id, item);

        Intent intent = new Intent(context, MainActivity.class);
        intent.putExtra("tab", "visits");
        intent.setAction("com.max.hive.VIEW_VISIT_" + safeId);
        intent.setData(Uri.parse("hive://visit/" + safeId));
        intent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK | Intent.FLAG_ACTIVITY_CLEAR_TOP);

        PendingIntent pi = PendingIntent.getActivity(
                context,
                safeId,
                intent,
                PendingIntent.FLAG_UPDATE_CURRENT | (Build.VERSION.SDK_INT >= Build.VERSION_CODES.M ? PendingIntent.FLAG_IMMUTABLE : 0)
        );

        Notification.Builder builder;
        if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
            builder = new Notification.Builder(context, CHANNEL_ID_ALERTS);
        } else {
            builder = new Notification.Builder(context);
        }

        String flag = item.getCountryFlag();
        String flagPrefix = flag.isEmpty() ? "" : (flag + " ");
        String loc = (item.city.isEmpty() ? "Site Visit" : flagPrefix + item.city + ", " + item.country);
        String title = "Visit: " + loc + " (#" + item.visitCount + ")";
        String devSnippet = item.device + (!item.ram.isEmpty() && !item.ram.equals("N/A") ? " (" + item.ram + ")" : "");
        String text = devSnippet + " • " + item.ip;

        builder.setSmallIcon(R.drawable.ic_launcher)
               .setContentTitle(title)
               .setContentText(text)
               .setStyle(new Notification.BigTextStyle().bigText(text))
               .setAutoCancel(true)
               .setContentIntent(pi)
               .setDefaults(Notification.DEFAULT_ALL)
               .setPriority(Notification.PRIORITY_HIGH);

        nm.notify(safeId, builder.build());
    }
}
