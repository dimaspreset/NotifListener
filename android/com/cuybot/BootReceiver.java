package com.cuybot;

import android.content.BroadcastReceiver;
import android.content.Context;
import android.content.Intent;
import android.util.Log;

/**
 * Boot receiver to restart the notification listener service after device reboot
 */
public class BootReceiver extends BroadcastReceiver {
    
    private static final String TAG = "BootReceiver";
    
    @Override
    public void onReceive(Context context, Intent intent) {
        if (Intent.ACTION_BOOT_COMPLETED.equals(intent.getAction())) {
            Log.d(TAG, "Device boot completed, checking notification service status");
            
            try {
                // Start MainActivity to ensure notification service is running
                Intent mainIntent = new Intent(context, MainActivity.class);
                mainIntent.addFlags(Intent.FLAG_ACTIVITY_NEW_TASK);
                context.startActivity(mainIntent);
                
                Log.d(TAG, "MainActivity started after boot");
            } catch (Exception e) {
                Log.e(TAG, "Error starting MainActivity after boot: " + e.getMessage(), e);
            }
        }
    }
}