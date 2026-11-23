package com.max.hive;

import java.util.Locale;

public class DeviceUtils {
    public static final int TYPE_ANDROID = 1;
    public static final int TYPE_APPLE = 2;
    public static final int TYPE_PC = 3;
    public static final int TYPE_BOT = 4;

    public static int getDeviceType(String device, String os, String browser) {
        String combined = (device + " " + os + " " + browser).toLowerCase(Locale.US);

        if (combined.contains("bot") || combined.contains("crawler") || combined.contains("spider") ||
            combined.contains("googlebot") || combined.contains("bingbot") || combined.contains("yandex") ||
            combined.contains("headless") || combined.contains("slurp") || combined.contains("duckduckgo")) {
            return TYPE_BOT;
        }

        if (combined.contains("android") || combined.contains("samsung") || combined.contains("pixel") ||
            combined.contains("xiaomi") || combined.contains("redmi") || combined.contains("oneplus") ||
            combined.contains("oppo") || combined.contains("vivo") || combined.contains("realme") ||
            combined.contains("motorola") || combined.contains("huawei")) {
            return TYPE_ANDROID;
        }

        if (combined.contains("iphone") || combined.contains("ipad") || combined.contains("ios") ||
            combined.contains("mac") || combined.contains("macintosh") || combined.contains("apple") ||
            combined.contains("darwin") || combined.contains("safari") && !combined.contains("chrome")) {
            return TYPE_APPLE;
        }

        if (combined.contains("windows") || combined.contains("linux") || combined.contains("pc") ||
            combined.contains("desktop") || combined.contains("x11") || combined.contains("cros") ||
            combined.contains("ubuntu") || combined.contains("fedora") || combined.contains("arch")) {
            return TYPE_PC;
        }

        return TYPE_PC;
    }

    public static int getDeviceIconResId(String device, String os, String browser) {
        int type = getDeviceType(device, os, browser);
        switch (type) {
            case TYPE_BOT:
                return R.drawable.ic_device_bot;
            case TYPE_ANDROID:
                return R.drawable.ic_device_android;
            case TYPE_APPLE:
                return R.drawable.ic_device_apple;
            case TYPE_PC:
            default:
                return R.drawable.ic_device_pc;
        }
    }
}
