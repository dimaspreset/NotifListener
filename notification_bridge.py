from kivy.utils import platform
from kivy.clock import Clock
import logging

# Set up logging
logger = logging.getLogger(__name__)

_receiver = None
_callback = None

def set_callback(fn):
    """Set the callback function to handle received notifications"""
    global _callback
    _callback = fn
    logger.info("Notification callback set")

def start():
    """Start the notification receiver"""
    logger.info(f"Starting notification bridge on platform: {platform}")
    
    if platform != 'android':
        logger.warning("Not on Android, notification bridge will not start")
        return
        
    try:
        _start_android_receiver()
    except Exception as e:
        logger.error(f"Failed to start Android receiver: {e}")

def stop():
    """Stop the notification receiver"""
    logger.info("Stopping notification bridge")
    
    if platform != 'android':
        return
        
    try:
        _stop_android_receiver()
    except Exception as e:
        logger.error(f"Failed to stop Android receiver: {e}")

def _start_android_receiver():
    """Start the Android broadcast receiver"""
    global _receiver
    
    if _receiver is not None:
        logger.warning("Receiver already active")
        return

    try:
        # Import Android/Java classes
        from jnius import autoclass, PythonJavaClass, java_method
        
        PythonActivity = autoclass('org.kivy.android.PythonActivity')
        IntentFilter = autoclass('android.content.IntentFilter')
        Context = autoclass('android.content.Context')
        
        ACTION = 'com.cuybot.whatsappnotification'
        
        class _BroadcastReceiver(PythonJavaClass):
            __javainterfaces__ = ['android/content/BroadcastReceiver']
            __javacontext__ = 'app'

            @java_method('(Landroid/content/Context;Landroid/content/Intent;)V')
            def onReceive(self, context, intent):
                try:
                    logger.debug("Broadcast received in Python")
                    
                    # Extract data from intent
                    title = intent.getStringExtra('title') or 'Unknown'
                    text = intent.getStringExtra('text') or ''
                    package = intent.getStringExtra('package') or 'unknown'
                    code = intent.getIntExtra('NotificationCode', -1)
                    action = intent.getStringExtra('action') or 'posted'
                    timestamp = intent.getLongExtra('timestamp', 0)

                    # Create data dictionary
                    data = {
                        'sender': title,
                        'message': text,
                        'notificationCode': str(code),
                        'package': package,
                        'action': action,
                        'timestamp': timestamp
                    }

                    logger.info(f"Received notification data: {data}")

                    # Call the callback function on the main thread
                    if _callback:
                        Clock.schedule_once(lambda dt: _callback(data), 0)
                    else:
                        logger.warning("No callback function set")
                        
                except Exception as e:
                    logger.error(f'Broadcast receiver error: {e}')

        # Create and register the receiver
        _receiver = _BroadcastReceiver()
        activity = PythonActivity.mActivity
        intent_filter = IntentFilter()
        intent_filter.addAction(ACTION)
        
        # Register with appropriate flags for Android version
        try:
            if hasattr(Context, 'RECEIVER_NOT_EXPORTED'):
                activity.registerReceiver(_receiver, intent_filter, Context.RECEIVER_NOT_EXPORTED)
            else:
                activity.registerReceiver(_receiver, intent_filter)
        except Exception as e:
            # Fallback to basic registration
            activity.registerReceiver(_receiver, intent_filter)
            
        logger.info(f'Broadcast receiver registered for action: {ACTION}')

    except ImportError as e:
        logger.error(f'Failed to import Java classes: {e}')
        raise
    except Exception as e:
        logger.error(f'Failed to start Android receiver: {e}')
        raise

def _stop_android_receiver():
    """Stop the Android broadcast receiver"""
    global _receiver
    
    if _receiver is None:
        logger.warning("No receiver to stop")
        return
        
    try:
        from jnius import autoclass
        PythonActivity = autoclass('org.kivy.android.PythonActivity')
        
        activity = PythonActivity.mActivity
        activity.unregisterReceiver(_receiver)
        _receiver = None
        
        logger.info('Broadcast receiver unregistered')
        
    except Exception as e:
        logger.error(f'Error stopping receiver: {e}')
        _receiver = None  # Reset anyway

def is_running():
    """Check if the receiver is currently running"""
    return _receiver is not None

def get_status():
    """Get current status of the notification bridge"""
    if platform != 'android':
        return "Not on Android platform"
    elif _receiver is not None:
        return "Active and listening"
    else:
        return "Inactive"