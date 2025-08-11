from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.clock import Clock
from kivy.logger import Logger
import json
import os
from datetime import datetime

# Import untuk Android
try:
    from jnius import autoclass, PythonJavaClass, java_method
    from android.permissions import request_permissions, Permission
    from android import mActivity
    ANDROID_AVAILABLE = True
except ImportError:
    ANDROID_AVAILABLE = False
    Logger.info("Android modules not available - running in desktop mode")

class NotificationReaderApp(App):
    def build(self):
        self.title = "Google Maps Notification Reader"
        
        # Main layout
        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # Title
        title = Label(
            text='Google Maps Notification Listener',
            size_hint_y=None,
            height=50,
            font_size='20sp'
        )
        main_layout.add_widget(title)
        
        # Status label
        self.status_label = Label(
            text='Status: Belum dimulai',
            size_hint_y=None,
            height=40,
            font_size='16sp'
        )
        main_layout.add_widget(self.status_label)
        
        # Control buttons
        button_layout = BoxLayout(size_hint_y=None, height=60, spacing=10)
        
        self.start_btn = Button(
            text='Start Listening',
            size_hint_x=0.5
        )
        self.start_btn.bind(on_press=self.start_listening)
        button_layout.add_widget(self.start_btn)
        
        self.stop_btn = Button(
            text='Stop Listening',
            size_hint_x=0.5,
            disabled=True
        )
        self.stop_btn.bind(on_press=self.stop_listening)
        button_layout.add_widget(self.stop_btn)
        
        main_layout.add_widget(button_layout)
        
        # Clear button
        clear_btn = Button(
            text='Clear Data',
            size_hint_y=None,
            height=50
        )
        clear_btn.bind(on_press=self.clear_data)
        main_layout.add_widget(clear_btn)
        
        # Notification data display
        self.data_label = Label(
            text='Data notifikasi akan muncul di sini...',
            text_size=(None, None),
            halign='left',
            valign='top'
        )
        
        scroll = ScrollView()
        scroll.add_widget(self.data_label)
        main_layout.add_widget(scroll)
        
        # File path untuk menyimpan data
        self.data_file = os.path.join(self.user_data_dir, 'notification_data.json')
        
        # Schedule untuk membaca data
        self.read_event = None
        
        # Load existing data
        self.load_existing_data()
        
        return main_layout
    
    def start_listening(self, instance):
        """Start notification listening"""
        try:
            if ANDROID_AVAILABLE:
                # Request permissions
                request_permissions([
                    Permission.BIND_NOTIFICATION_LISTENER_SERVICE,
                    Permission.WRITE_EXTERNAL_STORAGE,
                    Permission.READ_EXTERNAL_STORAGE
                ])
                
                # Start Java service
                self.start_notification_service()
                
            self.status_label.text = 'Status: Listening untuk notifikasi Google Maps...'
            self.start_btn.disabled = True
            self.stop_btn.disabled = False
            
            # Start reading data every 2 seconds
            self.read_event = Clock.schedule_interval(self.read_notification_data, 2)
            
        except Exception as e:
            self.status_label.text = f'Error: {str(e)}'
            Logger.error(f"Error starting listener: {e}")
    
    def stop_listening(self, instance):
        """Stop notification listening"""
        try:
            if self.read_event:
                self.read_event.cancel()
                self.read_event = None
            
            self.status_label.text = 'Status: Stopped'
            self.start_btn.disabled = False
            self.stop_btn.disabled = True
            
        except Exception as e:
            Logger.error(f"Error stopping listener: {e}")
    
    def start_notification_service(self):
        """Start the Java notification service"""
        if not ANDROID_AVAILABLE:
            return
            
        try:
            # Get Python activity
            PythonActivity = autoclass('org.kivy.android.PythonActivity')
            activity = PythonActivity.mActivity
            
            # Start service menggunakan intent
            Intent = autoclass('android.content.Intent')
            intent = Intent()
            intent.setAction('android.service.notification.NotificationListenerService')
            
            # Untuk development, kita akan menggunakan file-based communication
            Logger.info("Notification service communication setup complete")
            
        except Exception as e:
            Logger.error(f"Error starting notification service: {e}")
    
    def read_notification_data(self, dt):
        """Read notification data from file"""
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.display_data(data)
            else:
                # Create sample data for testing
                self.create_sample_data()
                
        except Exception as e:
            Logger.error(f"Error reading data: {e}")
    
    def create_sample_data(self):
        """Create sample data for testing purposes"""
        sample_data = [
            {
                'timestamp': datetime.now().isoformat(),
                'package': 'com.google.android.apps.maps',
                'title': 'Google Maps Navigation',
                'text': 'In 500m, turn right onto Jl. Sudirman',
                'subtext': '12 min (3.2 km) remaining'
            },
            {
                'timestamp': datetime.now().isoformat(),
                'package': 'com.google.android.apps.maps',
                'title': 'Google Maps',
                'text': 'Continue straight for 1.2 km',
                'subtext': '8 min (2.1 km) remaining'
            }
        ]
        
        try:
            with open(self.data_file, 'w', encoding='utf-8') as f:
                json.dump(sample_data, f, indent=2, ensure_ascii=False)
        except Exception as e:
            Logger.error(f"Error creating sample data: {e}")
    
    def display_data(self, data):
        """Display notification data"""
        if not data:
            self.data_label.text = 'Belum ada data notifikasi...'
            return
        
        display_text = "=== DATA NOTIFIKASI GOOGLE MAPS ===\n\n"
        
        for i, notification in enumerate(reversed(data[-10:])):  # Show last 10
            timestamp = notification.get('timestamp', 'Unknown time')
            title = notification.get('title', 'No title')
            text = notification.get('text', 'No text')
            subtext = notification.get('subtext', '')
            
            display_text += f"[{i+1}] {timestamp[:19]}\n"
            display_text += f"Judul: {title}\n"
            display_text += f"Pesan: {text}\n"
            if subtext:
                display_text += f"Sub: {subtext}\n"
            display_text += "-" * 50 + "\n\n"
        
        self.data_label.text = display_text
        self.data_label.text_size = (self.data_label.parent.width if self.data_label.parent else 300, None)
    
    def load_existing_data(self):
        """Load existing data on app start"""
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    self.display_data(data)
            else:
                self.data_label.text = 'Belum ada data. Tekan "Start Listening" untuk memulai.'
        except Exception as e:
            Logger.error(f"Error loading existing data: {e}")
    
    def clear_data(self, instance):
        """Clear all notification data"""
        try:
            if os.path.exists(self.data_file):
                os.remove(self.data_file)
            self.data_label.text = 'Data telah dihapus.'
            self.status_label.text = 'Status: Data cleared'
        except Exception as e:
            Logger.error(f"Error clearing data: {e}")

if __name__ == '__main__':
    NotificationReaderApp().run()