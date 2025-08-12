package com.yourpackage.mapsnotificationreader;

import android.app.Notification;
import android.content.Context;
import android.os.Bundle;
import android.service.notification.NotificationListenerService;
import android.service.notification.StatusBarNotification;
import android.util.Log;
import org.json.JSONArray;
import org.json.JSONException;
import org.json.JSONObject;

import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.text.SimpleDateFormat;
import java.util.ArrayList;
import java.util.Date;
import java.util.List;
import java.util.Locale;

public class MapsNotificationListener extends NotificationListenerService {
    
    private static final String TAG = "MapsNotificationListener";
    private static final String MAPS_PACKAGE = "com.google.android.apps.maps";
    private static final String DATA_FILE = "notification_data.json";
    
    private List<NotificationData> notificationList;
    private SimpleDateFormat dateFormat;
    
    @Override
    public void onCreate() {
        super.onCreate();
        notificationList = new ArrayList<>();
        dateFormat = new SimpleDateFormat("yyyy-MM-dd HH:mm:ss", Locale.getDefault());
        Log.i(TAG, "MapsNotificationListener service created");
    }
    
    @Override
    public void onNotificationPosted(StatusBarNotification sbn) {
        // Filter hanya notifikasi dari Google Maps
        if (!MAPS_PACKAGE.equals(sbn.getPackageName())) {
            return;
        }
        
        Log.i(TAG, "Google Maps notification detected");
        
        try {
            Notification notification = sbn.getNotification();
            Bundle extras = notification.extras;
            
            // Extract notification data
            String title = getStringFromBundle(extras, Notification.EXTRA_TITLE);
            String text = getStringFromBundle(extras, Notification.EXTRA_TEXT);
            String subText = getStringFromBundle(extras, Notification.EXTRA_SUB_TEXT);
            String bigText = getStringFromBundle(extras, Notification.EXTRA_BIG_TEXT);
            
            // Use bigText if available, otherwise use regular text
            String mainText = (bigText != null && !bigText.isEmpty()) ? bigText : text;
            
            // Create notification data object
            NotificationData data = new NotificationData(
                dateFormat.format(new Date()),
                MAPS_PACKAGE,
                title,
                mainText,
                subText
            );
            
            // Add to list (keep only last 50 notifications)
            notificationList.add(data);
            if (notificationList.size() > 50) {
                notificationList.remove(0);
            }
            
            // Save to file
            saveNotificationData();
            
            Log.i(TAG, String.format("Notification saved - Title: %s, Text: %s", title, mainText));
            
        } catch (Exception e) {
            Log.e(TAG, "Error processing notification", e);
        }
    }
    
    @Override
    public void onNotificationRemoved(StatusBarNotification sbn) {
        if (MAPS_PACKAGE.equals(sbn.getPackageName())) {
            Log.i(TAG, "Google Maps notification removed");
        }
    }
    
    private String getStringFromBundle(Bundle bundle, String key) {
        if (bundle == null) return null;
        
        CharSequence charSeq = bundle.getCharSequence(key);
        return charSeq != null ? charSeq.toString() : null;
    }
    
    private void saveNotificationData() {
        try {
            JSONArray jsonArray = new JSONArray();
            
            for (NotificationData data : notificationList) {
                JSONObject jsonObj = new JSONObject();
                jsonObj.put("timestamp", data.timestamp);
                jsonObj.put("package", data.packageName);
                jsonObj.put("title", data.title);
                jsonObj.put("text", data.text);
                jsonObj.put("subtext", data.subText);
                jsonArray.put(jsonObj);
            }
            
            // Get app's internal files directory (accessible to main app)
            File filesDir = getApplicationContext().getFilesDir();
            File file = new File(filesDir, DATA_FILE);
            
            FileWriter writer = new FileWriter(file);
            writer.write(jsonArray.toString(2));
            writer.close();
            
            Log.i(TAG, "Notification data saved to: " + file.getAbsolutePath());
            
            // Also save to external directory if available (for debugging)
            try {
                File externalFile = new File(getExternalFilesDir(null), DATA_FILE);
                FileWriter externalWriter = new FileWriter(externalFile);
                externalWriter.write(jsonArray.toString(2));
                externalWriter.close();
                Log.i(TAG, "Notification data also saved to external: " + externalFile.getAbsolutePath());
            } catch (Exception e) {
                Log.w(TAG, "Could not save to external directory", e);
            }
            
        } catch (JSONException | IOException e) {
            Log.e(TAG, "Error saving notification data", e);
        }
    }
    
    // Inner class to hold notification data
    private static class NotificationData {
        String timestamp;
        String packageName;
        String title;
        String text;
        String subText;
        
        NotificationData(String timestamp, String packageName, String title, String text, String subText) {
            this.timestamp = timestamp;
            this.packageName = packageName;
            this.title = title != null ? title : "";
            this.text = text != null ? text : "";
            this.subText = subText != null ? subText : "";
        }
    }
    
    @Override
    public void onDestroy() {
        super.onDestroy();
        Log.i(TAG, "MapsNotificationListener service destroyed");
    }
}