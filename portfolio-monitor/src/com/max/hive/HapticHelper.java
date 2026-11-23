package com.max.hive;

import android.content.Context;
import android.content.SharedPreferences;
import android.os.Build;
import android.os.VibrationEffect;
import android.os.Vibrator;
import android.view.HapticFeedbackConstants;
import android.view.View;

public class HapticHelper {
    public static final String PREF_HAPTIC = "pref_haptic_feedback";

    public static boolean isHapticEnabled(Context context) {
        if (context == null) return true;
        SharedPreferences prefs = context.getSharedPreferences("max_hive_prefs", Context.MODE_PRIVATE);
        return prefs.getBoolean(PREF_HAPTIC, true);
    }

    public static void performClick(View view) {
        if (view == null) return;
        if (!isHapticEnabled(view.getContext())) return;
        try {
            view.performHapticFeedback(HapticFeedbackConstants.KEYBOARD_TAP);
        } catch (Throwable t) {}
    }

    public static void performTick(Context context) {
        if (context == null) return;
        if (!isHapticEnabled(context)) return;
        try {
            Vibrator v = (Vibrator) context.getSystemService(Context.VIBRATOR_SERVICE);
            if (v != null && v.hasVibrator()) {
                if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.O) {
                    v.vibrate(VibrationEffect.createOneShot(12, VibrationEffect.DEFAULT_AMPLITUDE));
                } else {
                    v.vibrate(12);
                }
            }
        } catch (Throwable t) {}
    }
}
