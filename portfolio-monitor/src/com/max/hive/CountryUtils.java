package com.max.hive;

import java.util.HashMap;
import java.util.Locale;
import java.util.Map;

public class CountryUtils {
    private static final Map<String, String> COUNTRY_TO_CODE = new HashMap<>();

    static {
        COUNTRY_TO_CODE.put("INDIA", "IN");
        COUNTRY_TO_CODE.put("UNITED STATES", "US");
        COUNTRY_TO_CODE.put("USA", "US");
        COUNTRY_TO_CODE.put("UNITED KINGDOM", "GB");
        COUNTRY_TO_CODE.put("UK", "GB");
        COUNTRY_TO_CODE.put("CANADA", "CA");
        COUNTRY_TO_CODE.put("GERMANY", "DE");
        COUNTRY_TO_CODE.put("FRANCE", "FR");
        COUNTRY_TO_CODE.put("AUSTRALIA", "AU");
        COUNTRY_TO_CODE.put("SINGAPORE", "SG");
        COUNTRY_TO_CODE.put("JAPAN", "JP");
        COUNTRY_TO_CODE.put("NETHERLANDS", "NL");
        COUNTRY_TO_CODE.put("RUSSIA", "RU");
        COUNTRY_TO_CODE.put("BRAZIL", "BR");
        COUNTRY_TO_CODE.put("UAE", "AE");
        COUNTRY_TO_CODE.put("UNITED ARAB EMIRATES", "AE");
        COUNTRY_TO_CODE.put("CHINA", "CN");
        COUNTRY_TO_CODE.put("ITALY", "IT");
        COUNTRY_TO_CODE.put("SPAIN", "ES");
        COUNTRY_TO_CODE.put("SWITZERLAND", "CH");
        COUNTRY_TO_CODE.put("SWEDEN", "SE");
        COUNTRY_TO_CODE.put("SOUTH KOREA", "KR");
        COUNTRY_TO_CODE.put("KOREA", "KR");
        COUNTRY_TO_CODE.put("INDONESIA", "ID");
        COUNTRY_TO_CODE.put("MALAYSIA", "MY");
        COUNTRY_TO_CODE.put("VIETNAM", "VN");
        COUNTRY_TO_CODE.put("PHILIPPINES", "PH");
        COUNTRY_TO_CODE.put("TURKEY", "TR");
        COUNTRY_TO_CODE.put("SAUDI ARABIA", "SA");
        COUNTRY_TO_CODE.put("ISRAEL", "IL");
        COUNTRY_TO_CODE.put("SOUTH AFRICA", "ZA");
        COUNTRY_TO_CODE.put("MEXICO", "MX");
        COUNTRY_TO_CODE.put("NEW ZEALAND", "NZ");
        COUNTRY_TO_CODE.put("PAKISTAN", "PK");
        COUNTRY_TO_CODE.put("BANGLADESH", "BD");
        COUNTRY_TO_CODE.put("NEPAL", "NP");
        COUNTRY_TO_CODE.put("SRI LANKA", "LK");
    }

    public static String getFlagEmoji(String country) {
        if (country == null || country.trim().isEmpty()) {
            return "";
        }
        String normalized = country.trim().toUpperCase(Locale.US);

        String code = null;
        if (normalized.length() == 2 && normalized.charAt(0) >= 'A' && normalized.charAt(0) <= 'Z' && normalized.charAt(1) >= 'A' && normalized.charAt(1) <= 'Z') {
            code = normalized;
        } else {
            code = COUNTRY_TO_CODE.get(normalized);
            if (code == null) {
                for (Map.Entry<String, String> entry : COUNTRY_TO_CODE.entrySet()) {
                    if (normalized.contains(entry.getKey())) {
                        code = entry.getValue();
                        break;
                    }
                }
            }
        }

        if (code == null || code.length() != 2) {
            return "";
        }

        int firstChar = 0x1F1E6 + (code.charAt(0) - 'A');
        int secondChar = 0x1F1E6 + (code.charAt(1) - 'A');
        return new String(Character.toChars(firstChar)) + new String(Character.toChars(secondChar));
    }
}
