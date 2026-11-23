package com.max.hive;

import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Build;

public class BootReceiver extends BroadcastReceiver {
    public static final String PREF_BOOT_ON_STARTUP = "pref_boot_on_startup";

    @Override
    public void onReceive(Context context, Intent intent) {
        if (context == null || intent == null) return;

        String action = intent.getAction();
        if (Intent.ACTION_BOOT_COMPLETED.equals(action) ||
            "android.intent.action.QUICKBOOT_POWERON".equals(action) ||
            Intent.ACTION_MY_PACKAGE_REPLACED.equals(action)) {

            SharedPreferences prefs = context.getSharedPreferences("max_hive_prefs", Context.MODE_PRIVATE);
            boolean bootEnabled = prefs.getBoolean(PREF_BOOT_ON_STARTUP, true);

            if (bootEnabled) {
                Intent serviceIntent = new Intent(context, SheetSyncService.class);
                try {
                    if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
                        context.startForegroundService(serviceIntent);
                    } else {
                        context.startService(serviceIntent);
                    }
                } catch (Exception e) {}
            }
        }
    }
}
