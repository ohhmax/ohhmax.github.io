package com.max.hive;

import java.util.ArrayList;
import java.util.Collections;
import java.util.HashSet;
import java.util.List;
import java.util.Map;
import java.util.Set;
import java.util.concurrent.ConcurrentHashMap;

public class DataRepository {
    private static final Map<String, IngestionItem> ITEM_CACHE = new ConcurrentHashMap<>();
    private static final Set<String> MESSAGE_IDS = Collections.synchronizedSet(new HashSet<String>());
    private static final Set<String> VISIT_IDS = Collections.synchronizedSet(new HashSet<String>());

    private static final List<IngestionItem> ALL_MESSAGES = Collections.synchronizedList(new ArrayList<IngestionItem>());
    private static final List<IngestionItem> ALL_VISITS = Collections.synchronizedList(new ArrayList<IngestionItem>());

    private static long totalMessagesCount = 0;
    private static long totalVisitsCount = 0;

    public static void putItem(String id, IngestionItem item) {
        if (id == null || item == null) return;
        ITEM_CACHE.put(id, item);
    }

    public static IngestionItem getItem(String id) {
        if (id == null) return null;
        return ITEM_CACHE.get(id);
    }

    public static void setTotalCounts(long totalMessages, long totalVisits) {
        totalMessagesCount = totalMessages;
        totalVisitsCount = totalVisits;
    }

    public static long getTotalMessagesCount() {
        return totalMessagesCount > 0 ? totalMessagesCount : ALL_MESSAGES.size();
    }

    public static long getTotalVisitsCount() {
        return totalVisitsCount > 0 ? totalVisitsCount : ALL_VISITS.size();
    }

    public static void updateData(List<IngestionItem> messages, List<IngestionItem> visits) {
        synchronized (ALL_MESSAGES) {
            ALL_MESSAGES.clear();
            MESSAGE_IDS.clear();
            if (messages != null) {
                for (IngestionItem item : messages) {
                    if (item.id != null && !item.id.isEmpty()) {
                        ALL_MESSAGES.add(item);
                        MESSAGE_IDS.add(item.id);
                        ITEM_CACHE.put(item.id, item);
                    }
                }
            }
        }
        synchronized (ALL_VISITS) {
            ALL_VISITS.clear();
            VISIT_IDS.clear();
            if (visits != null) {
                for (IngestionItem item : visits) {
                    if (item.id != null && !item.id.isEmpty()) {
                        ALL_VISITS.add(item);
                        VISIT_IDS.add(item.id);
                        ITEM_CACHE.put(item.id, item);
                    }
                }
            }
        }
    }

    public static int appendMessages(List<IngestionItem> newItems) {
        if (newItems == null || newItems.isEmpty()) return 0;
        int added = 0;
        synchronized (ALL_MESSAGES) {
            for (IngestionItem item : newItems) {
                if (item.id != null && !item.id.isEmpty() && !MESSAGE_IDS.contains(item.id)) {
                    ALL_MESSAGES.add(item);
                    MESSAGE_IDS.add(item.id);
                    ITEM_CACHE.put(item.id, item);
                    added++;
                }
            }
        }
        return added;
    }

    public static int appendVisits(List<IngestionItem> newItems) {
        if (newItems == null || newItems.isEmpty()) return 0;
        int added = 0;
        synchronized (ALL_VISITS) {
            for (IngestionItem item : newItems) {
                if (item.id != null && !item.id.isEmpty() && !VISIT_IDS.contains(item.id)) {
                    ALL_VISITS.add(item);
                    VISIT_IDS.add(item.id);
                    ITEM_CACHE.put(item.id, item);
                    added++;
                }
            }
        }
        return added;
    }

    public static List<IngestionItem> getMessages() {
        synchronized (ALL_MESSAGES) {
            return new ArrayList<>(ALL_MESSAGES);
        }
    }

    public static List<IngestionItem> getVisits() {
        synchronized (ALL_VISITS) {
            return new ArrayList<>(ALL_VISITS);
        }
    }
}
