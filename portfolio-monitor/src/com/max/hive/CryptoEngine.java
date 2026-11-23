package com.max.hive;

import javax.crypto.Cipher;
import javax.crypto.spec.GCMParameterSpec;
import javax.crypto.spec.SecretKeySpec;
import java.io.ByteArrayInputStream;
import java.io.ByteArrayOutputStream;
import java.security.KeyFactory;
import java.security.MessageDigest;
import java.security.PrivateKey;
import java.security.spec.PKCS8EncodedKeySpec;
import java.util.Base64;
import java.util.zip.GZIPInputStream;

public class CryptoEngine {

    public static String decryptPayload(String encryptedArmor, String keyStr) {
        if (encryptedArmor == null || keyStr == null || keyStr.trim().isEmpty()) {
            return null;
        }
        encryptedArmor = encryptedArmor.trim();

        if (encryptedArmor.startsWith("MAXASYM1:")) {
            try {
                String cleanKey = keyStr
                        .replace("-----BEGIN PRIVATE KEY-----", "")
                        .replace("-----END PRIVATE KEY-----", "")
                        .replace("-----BEGIN RSA PRIVATE KEY-----", "")
                        .replace("-----END RSA PRIVATE KEY-----", "")
                        .replaceAll("\\s+", "");
                byte[] keyBytes = Base64.getDecoder().decode(cleanKey);
                PKCS8EncodedKeySpec spec = new PKCS8EncodedKeySpec(keyBytes);
                KeyFactory kf = KeyFactory.getInstance("RSA");
                PrivateKey privateKey = kf.generatePrivate(spec);

                byte[] raw = Base64.getDecoder().decode(encryptedArmor.substring("MAXASYM1:".length()).trim());
                if (raw.length < 256 + 12 + 16) {
                    return null;
                }

                byte[] encAesKey = new byte[256];
                System.arraycopy(raw, 0, encAesKey, 0, 256);

                byte[] iv = new byte[12];
                System.arraycopy(raw, 256, iv, 0, 12);

                byte[] cipherWithTag = new byte[raw.length - 268];
                System.arraycopy(raw, 268, cipherWithTag, 0, cipherWithTag.length);

                Cipher rsaCipher = Cipher.getInstance("RSA/ECB/OAEPWithSHA-1AndMGF1Padding");
                rsaCipher.init(Cipher.DECRYPT_MODE, privateKey);
                byte[] aesKey = rsaCipher.doFinal(encAesKey);

                SecretKeySpec aesKeySpec = new SecretKeySpec(aesKey, "AES");
                Cipher gcmCipher = Cipher.getInstance("AES/GCM/NoPadding");
                gcmCipher.init(Cipher.DECRYPT_MODE, aesKeySpec, new GCMParameterSpec(128, iv));
                byte[] decryptedBytes = gcmCipher.doFinal(cipherWithTag);

                return decompressGzipOrUtf8(decryptedBytes);
            } catch (Exception e) {
                return null;
            }
        } else if (encryptedArmor.startsWith("MAXENC1:")) {
            try {
                String b64 = encryptedArmor.substring("MAXENC1:".length()).trim();
                byte[] raw = Base64.getDecoder().decode(b64);
                if (raw.length < 28) {
                    return null;
                }

                byte[] iv = new byte[12];
                System.arraycopy(raw, 0, iv, 0, 12);

                byte[] cipherWithTag = new byte[raw.length - 12];
                System.arraycopy(raw, 12, cipherWithTag, 0, cipherWithTag.length);

                String[] candidateKeys = new String[] {
                    keyStr.trim()
                };

                MessageDigest md = MessageDigest.getInstance("SHA-256");
                for (String candidate : candidateKeys) {
                    if (candidate == null || candidate.isEmpty()) continue;
                    try {
                        byte[] keyBytes = md.digest(candidate.getBytes("UTF-8"));
                        SecretKeySpec keySpec = new SecretKeySpec(keyBytes, "AES");

                        Cipher cipher = Cipher.getInstance("AES/GCM/NoPadding");
                        cipher.init(Cipher.DECRYPT_MODE, keySpec, new GCMParameterSpec(128, iv));
                        byte[] decryptedBytes = cipher.doFinal(cipherWithTag);

                        String result = decompressGzipOrUtf8(decryptedBytes);
                        if (result != null && !result.trim().isEmpty()) {
                            return result;
                        }
                    } catch (Exception ignored) {
                        // Try next candidate key
                    }
                }
            } catch (Exception e) {
                return null;
            }
        }
        return null;
    }

    private static String decompressGzipOrUtf8(byte[] decryptedBytes) {
        try {
            ByteArrayInputStream bais = new ByteArrayInputStream(decryptedBytes);
            GZIPInputStream gis = new GZIPInputStream(bais);
            ByteArrayOutputStream baos = new ByteArrayOutputStream();
            byte[] buf = new byte[2048];
            int len;
            while ((len = gis.read(buf)) > 0) {
                baos.write(buf, 0, len);
            }
            gis.close();
            bais.close();
            return baos.toString("UTF-8");
        } catch (Exception e) {
            try {
                return new String(decryptedBytes, "UTF-8");
            } catch (Exception e2) {
                return null;
            }
        }
    }
}
