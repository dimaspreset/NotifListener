from kivy.utils import platform
from kivy.clock import Clock

_receiver = None
_callback = None

def set_callback(fn):
    global _callback
    _callback = fn

def start():
    if platform != 'android':
        return
    _start_android_receiver()

def stop():
    if platform != 'android':
        return
    _stop_android_receiver()

def _start_android_receiver():
    global _receiver
    if _receiver is not None:
        return

    from jnius import autoclass, PythonJavaClass, java_method
    PythonActivity = autoclass('org.kivy.android.PythonActivity')
    IntentFilter = autoclass('android.content.IntentFilter')

    ACTION = 'com.cuybot.whatsappnotification'

    class _BroadcastReceiver(PythonJavaClass):
        __javainterfaces__ = ['android/content/BroadcastReceiver']
        __javacontext__ = 'app'

        @java_method('(Landroid/content/Context;Landroid/content/Intent;)V')
        def onReceive(self, context, intent):
            try:
                title = intent.getStringExtra('title') or ''
                text = intent.getStringExtra('text') or ''
                pkg = intent.getStringExtra('package') or ''
                code = str(intent.getIntExtra('NotificationCode', -1))
                action = intent.getStringExtra('action') or 'posted'

                data = {
                    'sender': title,
                    'message': text,
                    'notificationCode': code,
                    'package': pkg,
                    'action': action
                }

                if _callback:
                    Clock.schedule_once(lambda dt: _callback(data), 0)
            except Exception as e:
                print('Receiver error:', e)

    _receiver = _BroadcastReceiver()
    activity = PythonActivity.mActivity
    filt = IntentFilter()
    filt.addAction(ACTION)
    activity.registerReceiver(_receiver, filt)
    print('Receiver registered for', ACTION)

def _stop_android_receiver():
    from jnius import autoclass
    PythonActivity = autoclass('org.kivy.android.PythonActivity')
    global _receiver
    if _receiver:
        try:
            PythonActivity.mActivity.unregisterReceiver(_receiver)
            print('Receiver unregistered')
        except Exception as e:
            print('Error unregistering receiver:', e)
        _receiver = None
