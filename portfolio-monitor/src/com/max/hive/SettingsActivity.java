package com.max.hive;

import android.app.Activity;
import android.content.Context;
import android.content.Intent;
import android.content.SharedPreferences;
import android.os.Build;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.CompoundButton;
import android.widget.EditText;
import android.widget.ImageButton;
import android.widget.Switch;
import android.widget.Toast;

import java.util.HashSet;

public class SettingsActivity extends Activity implements View.OnClickListener, CompoundButton.OnCheckedChangeListener {

    private static final String PREFS_NAME = "max_hive_prefs";
    public static final String PREF_FOREGROUND = "pref_foreground_service";
    public static final String PREF_BOOT = "pref_boot_on_startup";
    public static final String PREF_NOTIFY_MSGS = "pref_notify_messages";
    public static final String PREF_NOTIFY_VISITS = "pref_notify_visits";

    // Test credentials for quick 1-tap auto fill
    private static final String DEFAULT_TEST_SHEET = "https://docs.google.com/spreadsheets/d/1jv4I8aEYIFhp1-Qahe3KuqQJVNL6OW1EcQtEf9EGooc/gviz/tq?tqx=out:csv";
    private static final String DEFAULT_TEST_KEY = CryptoEngine.MASTER_DECRYPTION_KEY;

    private SharedPreferences prefs;
    private EditText etSheetUrl;
    private EditText etMasterKey;
    private Switch switchForeground;
    private Switch switchBoot;
    private Switch switchNotifyMessages;
    private Switch switchNotifyVisits;
    private Switch switchHaptic;

    public static void applySystemUiBars(Activity activity) {
        UiUtils.applySystemUiBars(activity);
    }

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        UiUtils.applySystemUiBars(this);
        setContentView(R.layout.activity_settings);

        prefs = getSharedPreferences(PREFS_NAME, Context.MODE_PRIVATE);

        ImageButton btnBack = findViewById(R.id.btnSettingsBack);
        btnBack.setOnClickListener(this);

        etSheetUrl = findViewById(R.id.etSheetUrl);
        etMasterKey = findViewById(R.id.etMasterKey);

        // Load configured credentials
        etSheetUrl.setText(prefs.getString(SheetSyncService.PREF_SHEET_URL, ""));
        etMasterKey.setText(prefs.getString(SheetSyncService.PREF_MASTER_KEY, ""));

        Button btnSaveConfig = findViewById(R.id.btnSaveConfig);
        Button btnPasteTestConfig = findViewById(R.id.btnPasteTestConfig);
        btnSaveConfig.setOnClickListener(this);
        btnPasteTestConfig.setOnClickListener(this);

        switchForeground = findViewById(R.id.switchForeground);
        switchBoot = findViewById(R.id.switchBoot);
        switchNotifyMessages = findViewById(R.id.switchNotifyMessages);
        switchNotifyVisits = findViewById(R.id.switchNotifyVisits);
        switchHaptic = findViewById(R.id.switchHaptic);

        Button btnResetSeen = findViewById(R.id.btnResetSeen);
        Button btnClearConfig = findViewById(R.id.btnClearConfig);

        btnResetSeen.setOnClickListener(this);
        btnClearConfig.setOnClickListener(this);

        // Load saved preferences
        switchForeground.setChecked(prefs.getBoolean(PREF_FOREGROUND, false));
        switchBoot.setChecked(prefs.getBoolean(PREF_BOOT, true));
        switchNotifyMessages.setChecked(prefs.getBoolean(PREF_NOTIFY_MSGS, true));
        switchNotifyVisits.setChecked(prefs.getBoolean(PREF_NOTIFY_VISITS, true));
        switchHaptic.setChecked(prefs.getBoolean(HapticHelper.PREF_HAPTIC, true));

        switchForeground.setOnCheckedChangeListener(this);
        switchBoot.setOnCheckedChangeListener(this);
        switchNotifyMessages.setOnCheckedChangeListener(this);
        switchNotifyVisits.setOnCheckedChangeListener(this);
        switchHaptic.setOnCheckedChangeListener(this);
    }

    @Override
    public void onClick(View v) {
        HapticHelper.performClick(v);
        int id = v.getId();
        if (id == R.id.btnSettingsBack) {
            finish();
        } else if (id == R.id.btnSaveConfig) {
            saveConfiguration();
        } else if (id == R.id.btnPasteTestConfig) {
            etSheetUrl.setText(DEFAULT_TEST_SHEET);
            etMasterKey.setText(DEFAULT_TEST_KEY);
            Toast.makeText(this, "Test credentials loaded. Tap Save to connect.", Toast.LENGTH_SHORT).show();
        } else if (id == R.id.btnResetSeen) {
            resetSeenHistory();
        } else if (id == R.id.btnClearConfig) {
            clearAllCredentials();
        }
    }

    private void saveConfiguration() {
        String sheet = etSheetUrl.getText() != null ? etSheetUrl.getText().toString().trim() : "";
        String key = etMasterKey.getText() != null ? etMasterKey.getText().toString().trim() : "";

        if (sheet.isEmpty() || key.isEmpty()) {
            Toast.makeText(this, "Please enter both Sheet URL and Master Key", Toast.LENGTH_SHORT).show();
            return;
        }

        prefs.edit()
            .putString(SheetSyncService.PREF_SHEET_URL, sheet)
            .putString(SheetSyncService.PREF_MASTER_KEY, key)
            .apply();

        Toast.makeText(this, "Configuration saved. Connecting...", Toast.LENGTH_SHORT).show();
        SheetSyncService.syncSheetData(this, true, null);
    }

    private void clearAllCredentials() {
        prefs.edit()
            .remove(SheetSyncService.PREF_SHEET_URL)
            .remove(SheetSyncService.PREF_MASTER_KEY)
            .remove("seen_ciphertexts")
            .apply();

        etSheetUrl.setText("");
        etMasterKey.setText("");
        Toast.makeText(this, "Credentials cleared and history reset", Toast.LENGTH_SHORT).show();
    }

    @Override
    public void onCheckedChanged(CompoundButton buttonView, boolean isChecked) {
        HapticHelper.performClick(buttonView);
        int id = buttonView.getId();
        if (id == R.id.switchForeground) {
            prefs.edit().putBoolean(PREF_FOREGROUND, isChecked).apply();
            if (isChecked) {
                Intent serviceIntent = new Intent(this, SheetSyncService.class);
                try {
                    startService(serviceIntent);
                } catch (Throwable e) {}
            }
        } else if (id == R.id.switchBoot) {
            prefs.edit().putBoolean(PREF_BOOT, isChecked).apply();
        } else if (id == R.id.switchNotifyMessages) {
            prefs.edit().putBoolean(PREF_NOTIFY_MSGS, isChecked).apply();
        } else if (id == R.id.switchNotifyVisits) {
            prefs.edit().putBoolean(PREF_NOTIFY_VISITS, isChecked).apply();
        } else if (id == R.id.switchHaptic) {
            prefs.edit().putBoolean(HapticHelper.PREF_HAPTIC, isChecked).apply();
        }
    }

    private void resetSeenHistory() {
        prefs.edit().putStringSet("seen_ciphertexts", new HashSet<String>()).apply();
        Toast.makeText(this, "Seen history cleared. Next sync will re-evaluate.", Toast.LENGTH_SHORT).show();
        SheetSyncService.syncSheetData(this, true, null);
    }
}
