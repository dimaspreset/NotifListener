package com.cuybot;

import android.app.Notification;
import android.content.Intent;
import android.os.Build;
import android.os.Bundle;
import android.os.Parcelable;
import android.service.notification.NotificationListenerService;
import android.service.notification.StatusBarNotification;
import android.util.Log;

public class WhatsAppNotificationListener extends NotificationListenerService {

    private static final String TAG = "WhatsAppNotificationListener";
    private static final String BROADCAST_ACTION = "com.cuybot.whatsappnotification";

    private static final class ApplicationPackageNames {
        public static final String FACEBOOK_PACK_NAME = "com.facebook.katana";
        public static final String FACEBOOK_MESSENGER_PACK_NAME = "com.facebook.orca";
        public static final String WHATSAPP_PACK_NAME = "com.whatsapp";
        public static final String INSTAGRAM_PACK_NAME = "com.instagram.android";
    }

    public static final class InterceptedNotificationCode {
        public static final int FACEBOOK_CODE = 1;
        public static final int WHATSAPP_CODE = 2;
        public static final int INSTAGRAM_CODE = 3;
        public static final int OTHER_NOTIFICATION_CODE = 4;
    }

    @Override
    public void onNotificationPosted(StatusBarNotification sbn) {
        try {
            int notificationCode = matchNotificationCode(sbn);
            String packageName = sbn.getPackageName();

            Log.d(TAG, "Notification received from: " + packageName + ", Code: " + notificationCode);

            if (notificationCode != InterceptedNotificationCode.OTHER_NOTIFICATION_CODE) {
                Bundle extras = sbn.getNotification().extras;

                if (extras != null) {
                    String title = extras.getString(Notification.EXTRA_TITLE);
                    CharSequence textSequence = extras.getCharSequence(Notification.EXTRA_TEXT);
                    String text = textSequence != null ? textSequence.toString() : "";

                    Log.d(TAG, "Title: " + title + ", Text: " + text);

                    if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.KITKAT) {
                        // Try to get more detailed message content
                        String detailedText = extractDetailedMessage(extras);
                        if (!detailedText.isEmpty()) {
                            text = detailedText;
                        }
                    }

                    // Send broadcast with notification data
                    if (title != null && text != null && !text.isEmpty()) {
                        Intent intent = new Intent(BROADCAST_ACTION);
                        intent.putExtra("NotificationCode", notificationCode);
                        intent.putExtra("package", packageName);
                        intent.putExtra("title", title);
                        intent.putExtra("text", text);

                        sendBroadcast(intent);
                        Log.d(TAG, "Broadcast sent successfully");
                    } else {
                        Log.w(TAG, "Skipping notification due to null/empty data");
                    }
                } else {
                    Log.w(TAG, "Notification extras are null");
                }
            } else {
                Log.d(TAG, "Ignoring notification from other apps");
            }

        } catch (Exception e) {
            Log.e(TAG, "Error processing notification: " + e.getMessage(), e);
        }
    }

    private String extractDetailedMessage(Bundle extras) {
        try {
            if (Build.VERSION.SDK_INT >= Build.VERSION_CODES.KITKAT) {
                Parcelable[] messages = (Parcelable[]) extras.get(Notification.EXTRA_MESSAGES);

                if (messages != null && messages.length > 0) {
                    // Get the latest message
                    Bundle latestMessage = (Bundle) messages[messages.length - 1];
                    String messageText = latestMessage.getString("text");

                    if (messageText != null && !messageText.isEmpty()) {
                        Log.d(TAG, "Extracted detailed message: " + messageText);
                        return messageText;
                    }
                }
            }
        } catch (Exception e) {
            Log.e(TAG, "Error extracting detailed message: " + e.getMessage());
        }
        return "";
    }

    @Override
    public void onNotificationRemoved(StatusBarNotification sbn) {
        try {
            int notificationCode = matchNotificationCode(sbn);
            Log.d(TAG, "Notification removed, code: " + notificationCode);

            if (notificationCode != InterceptedNotificationCode.OTHER_NOTIFICATION_CODE) {
                StatusBarNotification[] activeNotifications = this.getActiveNotifications();

                if (activeNotifications != null && activeNotifications.length > 0) {
                    for (StatusBarNotification activeNotification : activeNotifications) {
                        if (notificationCode == matchNotificationCode(activeNotification)) {
                            Intent intent = new Intent(BROADCAST_ACTION);
                            intent.putExtra("NotificationCode", notificationCode);
                            intent.putExtra("action", "removed");
                            sendBroadcast(intent);
                            Log.d(TAG, "Removal broadcast sent");
                            break;
                        }
                    }
                }
            }
        } catch (Exception e) {
            Log.e(TAG, "Error in onNotificationRemoved: " + e.getMessage(), e);
        }
    }

    private int matchNotificationCode(StatusBarNotification sbn) {
        String packageName = sbn.getPackageName();

        if (packageName.equals(ApplicationPackageNames.FACEBOOK_PACK_NAME) ||
                packageName.equals(ApplicationPackageNames.FACEBOOK_MESSENGER_PACK_NAME)) {
            return InterceptedNotificationCode.FACEBOOK_CODE;
        } else if (packageName.equals(ApplicationPackageNames.INSTAGRAM_PACK_NAME)) {
            return InterceptedNotificationCode.INSTAGRAM_CODE;
        } else if (packageName.equals(ApplicationPackageNames.WHATSAPP_PACK_NAME)) {
            return InterceptedNotificationCode.WHATSAPP_CODE;
        } else {
            return InterceptedNotificationCode.OTHER_NOTIFICATION_CODE;
        }
    }
}