package com.max.hive;

import java.util.Comparator;

public class ItemComparator implements Comparator<IngestionItem> {
    private final int sortMode;
    private final boolean isMessage;

    public ItemComparator(int sortMode, boolean isMessage) {
        this.sortMode = sortMode;
        this.isMessage = isMessage;
    }

    @Override
    public int compare(IngestionItem a, IngestionItem b) {
        switch (sortMode) {
            case MainActivity.SORT_OLDEST:
                return Long.compare(a.timestamp, b.timestamp);
            case MainActivity.SORT_ACTIVITY:
                if (isMessage) {
                    return a.name.compareToIgnoreCase(b.name);
                } else {
                    return Integer.compare(b.visitCount, a.visitCount);
                }
            case MainActivity.SORT_LOCATION:
                String locA = a.city + " " + a.country;
                String locB = b.city + " " + b.country;
                return locA.compareToIgnoreCase(locB);
            case MainActivity.SORT_NEWEST:
            default:
                return Long.compare(b.timestamp, a.timestamp);
        }
    }
}
