package com.cuybot;

import android.app.Activity;
import android.app.AlertDialog;
import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.content.IntentFilter;
import android.os.Build;
import android.os.Bundle;
import android.provider.Settings;
import android.util.Log;

public class MainActivity extends Activity {

    private static final String TAG = "MainActivity";
    private static final String BROADCAST_ACTION = "com.cuybot.whatsappnotification";

    private ReceiveBroadcastReceiver broadcastReceiver;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        Log.d(TAG, "MainActivity created");

        // Check notification permission first
        checkNotificationPermission();

        // Setup broadcast receiver
        setupBroadcastReceiver();
    }

    private void checkNotificationPermission() {
        if (!isNotificationServiceEnabled()) {
            Log.w(TAG, "Notification service not enabled, requesting permission");
            showPermissionDialog();
        } else {
            Log.d(TAG, "Notification service is enabled");
        }
    }

    private void showPermissionDialog() {
        try {
            new AlertDialog.Builder(this)
                    .setTitle("Permission Required")
                    .setMessage("CuyBot needs notification access to read WhatsApp messages. Please enable it in the next screen.")
                    .setPositiveButton("Grant Permission", new android.content.DialogInterface.OnClickListener() {
                        public void onClick(android.content.DialogInterface dialog, int which) {
                            Intent intent = new Intent(Settings.ACTION_NOTIFICATION_LISTENER_SETTINGS);
                            startActivity(intent);
                        }
                    })
                    .setNegativeButton("Cancel", new android.content.DialogInterface.OnClickListener() {
                        public void onClick(android.content.DialogInterface dialog, int which) {
                            Log.w(TAG, "User cancelled permission request");
                            finish();
                        }
                    })
                    .setCancelable(false)
                    .show();
        } catch (Exception e) {
            Log.e(TAG, "Error showing permission dialog: " + e.getMessage());
            // Fallback - just open settings
            Intent intent = new Intent(Settings.ACTION_NOTIFICATION_LISTENER_SETTINGS);
            startActivity(intent);
        }
    }

    private void setupBroadcastReceiver() {
        // Unregister existing receiver if any
        if (broadcastReceiver != null) {
            try {
                unregisterReceiver(broadcastReceiver);
                Log.d(TAG, "Previous receiver unregistered");
            } catch (IllegalArgumentException ignored) {
                // Receiver wasn't registered
            }
        }

        broadcastReceiver = new ReceiveBroadcastReceiver();
        IntentFilter intentFilter = new IntentFilter();
        intentFilter.addAction(BROADCAST_ACTION);

        // Register receiver with proper flags for newer Android versions
        try {
            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.TIRAMISU) {
                registerReceiver(broadcastReceiver, intentFilter, Context.RECEIVER_NOT_EXPORTED);
            } else {
                registerReceiver(broadcastReceiver, intentFilter);
            }
            Log.d(TAG, "BroadcastReceiver registered successfully");
        } catch (Exception e) {
            Log.e(TAG, "Failed to register BroadcastReceiver: " + e.getMessage(), e);
            // Fallback to basic registration
            try {
                registerReceiver(broadcastReceiver, intentFilter);
                Log.d(TAG, "BroadcastReceiver registered with fallback");
            } catch (Exception e2) {
                Log.e(TAG, "Failed fallback registration: " + e2.getMessage());
            }
        }
    }

    private boolean isNotificationServiceEnabled() {
        String packageName = getPackageName();
        String flat = Settings.Secure.getString(getContentResolver(), "enabled_notification_listeners");
        boolean enabled = flat != null && flat.contains(packageName);
        Log.d(TAG, "Package: " + packageName + ", Notification service enabled: " + enabled);
        return enabled;
    }

    @Override
    protected void onResume() {
        super.onResume();
        // Re-check permission when user returns to app
        if (isNotificationServiceEnabled()) {
            Log.d(TAG, "Notification permission granted");
        }
    }

    @Override
    protected void onDestroy() {
        super.onDestroy();
        if (broadcastReceiver != null) {
            try {
                unregisterReceiver(broadcastReceiver);
                Log.d(TAG, "BroadcastReceiver unregistered in onDestroy");
            } catch (IllegalArgumentException e) {
                Log.e(TAG, "Error unregistering receiver: " + e.getMessage());
            }
        }
    }

    public class ReceiveBroadcastReceiver extends BroadcastReceiver {
        @Override
        public void onReceive(Context context, Intent intent) {
            try {
                Log.d(TAG, "Broadcast received");
                
                int receivedNotificationCode = intent.getIntExtra("NotificationCode", -1);
                String title = intent.getStringExtra("title");
                String text = intent.getStringExtra("text");
                String packageName = intent.getStringExtra("package");

                Log.d(TAG, "Received - Code: " + receivedNotificationCode +
                        ", Package: " + packageName +
                        ", Title: " + title + 
                        ", Text: " + text);

                // Validate data
                if (title == null) title = "Unknown";
                if (text == null || text.trim().isEmpty()) {
                    Log.w(TAG, "Empty message text, skipping");
                    return;
                }

                // Filter out system notifications
                if (isSystemNotification(text)) {
                    Log.d(TAG, "System notification filtered out: " + text);
                    return;
                }

                Log.d(TAG, "Valid notification, processing...");
                
                // Create Users object and log it (no Firebase for now)
                Users users = new Users(title, text, String.valueOf(receivedNotificationCode));
                Log.i(TAG, "NOTIFICATION CAPTURED: " + users.toString());

            } catch (Exception e) {
                Log.e(TAG, "Error in onReceive: " + e.getMessage(), e);
            }
        }

        private boolean isSystemNotification(String text) {
            if (text == null) return true;
            
            String[] systemMessages = {
                "new messages",
                "WhatsApp Web is currently active",
                "WhatsApp web login",
                "WhatsApp Web login",
                "WhatsApp calling",
                "Checking for new messages"
            };

            String lowerText = text.toLowerCase();
            for (String systemMsg : systemMessages) {
                if (lowerText.contains(systemMsg.toLowerCase())) {
                    return true;
                }
            }
            return false;
        }
    }
}