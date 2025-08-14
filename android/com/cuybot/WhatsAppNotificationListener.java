package com.cuybot;

import android.app.Notification;
import android.content.Intent;
import android.os.Build;
import android.os.Bundle;
import android.service.notification.NotificationListenerService;
import android.service.notification.StatusBarNotification;
import android.util.Log;

public class WhatsAppNotificationListener extends NotificationListenerService {

    private static final String TAG = "NotificationListener";
    private static final String BROADCAST_ACTION = "com.cuybot.whatsappnotification";

    // Supported app packages
    private static final class ApplicationPackageNames {
        public static final String WHATSAPP_PACK_NAME = "com.whatsapp";
        public static final String WHATSAPP_BUSINESS = "com.whatsapp.w4b";
        public static final String TELEGRAM = "org.telegram.messenger";
        public static final String SIGNAL = "org.thoughtcrime.securesms";
    }

    // Notification codes
    public static final class InterceptedNotificationCode {
        public static final int WHATSAPP_CODE = 1;
        public static final int WHATSAPP_BUSINESS_CODE = 2;
        public static final int TELEGRAM_CODE = 3;
        public static final int SIGNAL_CODE = 4;
        public static final int OTHER_CODE = 99;
    }

    @Override
    public void onCreate() {
        super.onCreate();
        Log.d(TAG, "NotificationListenerService created");
    }

    @Override
    public void onNotificationPosted(StatusBarNotification sbn) {
        try {
            String packageName = sbn.getPackageName();
            int notificationCode = getNotificationCode(packageName);

            Log.d(TAG, "Notification posted from: " + packageName + " (Code: " + notificationCode + ")");

            // Only process supported apps
            if (notificationCode == InterceptedNotificationCode.OTHER_CODE) {
                return;
            }

            Notification notification = sbn.getNotification();
            Bundle extras = notification.extras;

            if (extras == null) {
                Log.w(TAG, "Notification extras are null");
                return;
            }

            // Extract notification data
            String title = extractTitle(extras);
            String text = extractText(extras);
            
            Log.d(TAG, "Extracted - Title: '" + title + "', Text: '" + text + "'");

            // Validate extracted data
            if (isValidNotification(title, text)) {
                sendNotificationBroadcast(notificationCode, packageName, title, text, "posted");
                Log.d(TAG, "Broadcast sent for valid notification");
            } else {
                Log.d(TAG, "Invalid notification data, skipping");
            }

        } catch (Exception e) {
            Log.e(TAG, "Error in onNotificationPosted: " + e.getMessage(), e);
        }
    }

    @Override
    public void onNotificationRemoved(StatusBarNotification sbn) {
        try {
            String packageName = sbn.getPackageName();
            int notificationCode = getNotificationCode(packageName);
            
            Log.d(TAG, "Notification removed from: " + packageName);

            if (notificationCode != InterceptedNotificationCode.OTHER_CODE) {
                sendNotificationBroadcast(notificationCode, packageName, "", "", "removed");
            }
        } catch (Exception e) {
            Log.e(TAG, "Error in onNotificationRemoved: " + e.getMessage(), e);
        }
    }

    private String extractTitle(Bundle extras) {
        try {
            String title = extras.getString(Notification.EXTRA_TITLE);
            if (title != null && !title.trim().isEmpty()) {
                return title.trim();
            }

            // Try alternative title sources
            CharSequence titleSequence = extras.getCharSequence(Notification.EXTRA_TITLE);
            if (titleSequence != null) {
                return titleSequence.toString().trim();
            }

            return "Unknown Sender";
        } catch (Exception e) {
            Log.e(TAG, "Error extracting title: " + e.getMessage());
            return "Unknown Sender";
        }
    }

    private String extractText(Bundle extras) {
        try {
            // Try to get the main text
            CharSequence textSequence = extras.getCharSequence(Notification.EXTRA_TEXT);
            if (textSequence != null && !textSequence.toString().trim().isEmpty()) {
                return textSequence.toString().trim();
            }

            // Try big text for longer messages
            CharSequence bigText = extras.getCharSequence(Notification.EXTRA_BIG_TEXT);
            if (bigText != null && !bigText.toString().trim().isEmpty()) {
                return bigText.toString().trim();
            }

            // Try info text
            CharSequence infoText = extras.getCharSequence(Notification.EXTRA_INFO_TEXT);
            if (infoText != null && !infoText.toString().trim().isEmpty()) {
                return infoText.toString().trim();
            }

            // Try sub text
            CharSequence subText = extras.getCharSequence(Notification.EXTRA_SUB_TEXT);
            if (subText != null && !subText.toString().trim().isEmpty()) {
                return subText.toString().trim();
            }

            Log.w(TAG, "No text content found in notification");
            return "";

        } catch (Exception e) {
            Log.e(TAG, "Error extracting text: " + e.getMessage());
            return "";
        }
    }

    private boolean isValidNotification(String title, String text) {
        // Check if we have meaningful content
        if (title == null || title.trim().isEmpty()) {
            return false;
        }
        
        if (text == null || text.trim().isEmpty()) {
            return false;
        }

        // Filter out system notifications
        String[] systemPhrases = {
            "WhatsApp Web is currently active",
            "WhatsApp web login",
            "Checking for new messages",
            "new messages",
            "messages from",
            "WhatsApp calling"
        };

        String lowerText = text.toLowerCase();
        for (String phrase : systemPhrases) {
            if (lowerText.contains(phrase.toLowerCase())) {
                Log.d(TAG, "Filtered system notification: " + phrase);
                return false;
            }
        }

        return true;
    }

    private void sendNotificationBroadcast(int notificationCode, String packageName, 
                                         String title, String text, String action) {
        try {
            Intent intent = new Intent(BROADCAST_ACTION);
            intent.putExtra("NotificationCode", notificationCode);
            intent.putExtra("package", packageName);
            intent.putExtra("title", title);
            intent.putExtra("text", text);
            intent.putExtra("action", action);
            intent.putExtra("timestamp", System.currentTimeMillis());

            sendBroadcast(intent);
            Log.d(TAG, "Broadcast sent successfully for " + action + " action");
        } catch (Exception e) {
            Log.e(TAG, "Error sending broadcast: " + e.getMessage(), e);
        }
    }

    private int getNotificationCode(String packageName) {
        switch (packageName) {
            case ApplicationPackageNames.WHATSAPP_PACK_NAME:
                return InterceptedNotificationCode.WHATSAPP_CODE;
            case ApplicationPackageNames.WHATSAPP_BUSINESS:
                return InterceptedNotificationCode.WHATSAPP_BUSINESS_CODE;
            case ApplicationPackageNames.TELEGRAM:
                return InterceptedNotificationCode.TELEGRAM_CODE;
            case ApplicationPackageNames.SIGNAL:
                return InterceptedNotificationCode.SIGNAL_CODE;
            default:
                return InterceptedNotificationCode.OTHER_CODE;
        }
    }

    @Override
    public void onDestroy() {
        super.onDestroy();
        Log.d(TAG, "NotificationListenerService destroyed");
    }
}