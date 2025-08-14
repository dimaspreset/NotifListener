from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.card import MDCard
from kivymd.uix.scrollview import MDScrollView
from kivymd.uix.button import MDRaisedButton
from kivy.lang import Builder
from kivy.clock import Clock
from kivy.utils import platform
import logging

# Set up logging
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# Import notification bridge
try:
    from notification_bridge import set_callback, start as notif_start, stop as notif_stop
    logger.info("Successfully imported notification_bridge")
except ImportError as e:
    logger.error(f"Failed to import notification_bridge: {e}")
    # Create dummy functions for testing
    def set_callback(fn): pass
    def notif_start(): pass
    def notif_stop(): pass

KV = '''
<NotificationCard@MDCard>:
    orientation: "vertical"
    padding: "16dp"
    spacing: "8dp"
    size_hint_y: None
    height: self.minimum_height
    md_bg_color: 0.15, 0.15, 0.15, 1
    radius: [12, 12, 12, 12]
    elevation: 4
    
    MDLabel:
        id: sender_label
        text: "Waiting for notifications..."
        font_style: "H6"
        theme_text_color: "Custom"
        text_color: 0.2, 0.8, 1, 1
        size_hint_y: None
        height: self.texture_size[1]
        
    MDLabel:
        id: message_label
        text: "Make sure notification permission is granted"
        font_style: "Body1"
        theme_text_color: "Custom"
        text_color: 0.9, 0.9, 0.9, 1
        size_hint_y: None
        height: self.texture_size[1]
        text_size: self.width, None
        
    MDLabel:
        id: time_label
        text: ""
        font_style: "Caption"
        theme_text_color: "Custom"
        text_color: 0.6, 0.6, 0.6, 1
        size_hint_y: None
        height: self.texture_size[1]

Screen:
    MDBoxLayout:
        orientation: "vertical"

        MDTopAppBar:
            title: "CuyBot - Notification Reader"
            elevation: 4
            md_bg_color: 0.1, 0.1, 0.1, 1

        MDBoxLayout:
            orientation: "vertical"
            padding: "16dp"
            spacing: "16dp"

            # Status Card
            MDCard:
                size_hint_y: None
                height: "80dp"
                md_bg_color: 0.1, 0.3, 0.1, 1
                radius: [8, 8, 8, 8]
                padding: "16dp"
                
                MDLabel:
                    id: status_label
                    text: "Status: Initializing..."
                    font_style: "Subtitle1"
                    theme_text_color: "Custom"
                    text_color: 0.8, 1, 0.8, 1
                    halign: "center"

            # Current Notification Card
            NotificationCard:
                id: current_notif

            # Control Buttons
            MDBoxLayout:
                orientation: "horizontal"
                spacing: "16dp"
                size_hint_y: None
                height: "48dp"
                
                MDRaisedButton:
                    id: clear_btn
                    text: "Clear Log"
                    size_hint_x: 0.5
                    on_release: app.clear_log()
                    
                MDRaisedButton:
                    id: test_btn
                    text: "Test Notification"
                    size_hint_x: 0.5
                    on_release: app.test_notification()

            # Log Section
            MDLabel:
                text: "Message Log:"
                font_style: "Subtitle1"
                theme_text_color: "Custom"
                text_color: 0.8, 0.8, 0.8, 1
                size_hint_y: None
                height: "32dp"

            MDCard:
                md_bg_color: 0.05, 0.05, 0.05, 1
                radius: [8, 8, 8, 8]
                padding: "8dp"
                size_hint_y: None
                height: "200dp"
                
                MDScrollView:
                    MDBoxLayout:
                        id: log_box
                        orientation: "vertical"
                        adaptive_height: True
                        spacing: "4dp"
'''

class CuyBotApp(MDApp):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.notification_count = 0
        self.is_service_running = False
        
    def build(self):
        self.title = "CuyBotApp"
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Blue"
        logger.info("Building app interface")
        return Builder.load_string(KV)

    def on_start(self):
        logger.info("App starting...")
        self.update_status("App started - Setting up notification listener...")
        
        try:
            # Set up notification callback
            set_callback(self.on_notification_received)
            
            # Start notification service
            notif_start()
            self.is_service_running = True
            
            logger.info("Notification service started")
            self.update_status("Ready - Waiting for notifications")
            
            # Schedule a test notification after 3 seconds
            Clock.schedule_once(self.delayed_setup, 3.0)
            
        except Exception as e:
            logger.error(f"Error starting notification service: {e}")
            self.update_status(f"Error: {str(e)}")

    def delayed_setup(self, dt):
        """Additional setup after app is fully loaded"""
        if platform == 'android':
            self.update_status("Android detected - Notification service active")
        else:
            self.update_status("Desktop mode - Notifications simulated")
            # Add a sample notification for desktop testing
            Clock.schedule_once(lambda dt: self.test_notification(), 2.0)

    def on_stop(self):
        logger.info("App stopping...")
        try:
            notif_stop()
            self.is_service_running = False
            logger.info("Notification service stopped")
        except Exception as e:
            logger.error(f"Error stopping notification service: {e}")

    def on_notification_received(self, data):
        """Called when a notification is received from the Java service"""
        try:
            logger.info(f"Notification received: {data}")
            
            sender = data.get('sender', 'Unknown')
            message = data.get('message', 'No message content')
            package = data.get('package', 'unknown')
            action = data.get('action', 'posted')
            timestamp = data.get('timestamp', 0)
            
            # Only process 'posted' notifications, ignore 'removed'
            if action != 'posted':
                return
                
            self.notification_count += 1
            
            # Format timestamp
            from datetime import datetime
            if timestamp:
                time_str = datetime.fromtimestamp(timestamp/1000).strftime('%H:%M:%S')
            else:
                time_str = datetime.now().strftime('%H:%M:%S')
            
            # Update current notification display
            Clock.schedule_once(lambda dt: self.update_current_notification(sender, message, time_str), 0)
            
            # Add to log
            Clock.schedule_once(lambda dt: self.add_to_log(sender, message, package, time_str), 0)
            
            # Update status
            Clock.schedule_once(lambda dt: self.update_status(f"Active - {self.notification_count} notifications received"), 0)
            
        except Exception as e:
            logger.error(f"Error processing notification: {e}")
            Clock.schedule_once(lambda dt: self.update_status(f"Error: {str(e)}"), 0)

    def update_current_notification(self, sender, message, time_str):
        """Update the main notification display card"""
        try:
            current_card = self.root.ids.current_notif
            current_card.ids.sender_label.text = f"From: {sender}"
            current_card.ids.message_label.text = message
            current_card.ids.time_label.text = f"Received: {time_str}"
        except Exception as e:
            logger.error(f"Error updating current notification: {e}")

    def add_to_log(self, sender, message, package, time_str):
        """Add notification to the log area"""
        try:
            log_box = self.root.ids.log_box
            
            # Create log entry
            log_entry = MDLabel(
                text=f"[{time_str}] {sender}: {message[:50]}..." if len(message) > 50 else f"[{time_str}] {sender}: {message}",
                theme_text_color="Custom",
                text_color=(0.8, 0.8, 0.8, 1),
                size_hint_y=None,
                height="24dp",
                font_size="12sp"
            )
            
            log_box.add_widget(log_entry)
            
            # Keep only last 20 entries
            if len(log_box.children) > 20:
                log_box.remove_widget(log_box.children[-1])
                
        except Exception as e:
            logger.error(f"Error adding to log: {e}")

    def update_status(self, message):
        """Update the status label"""
        try:
            if hasattr(self.root, 'ids') and 'status_label' in self.root.ids:
                self.root.ids.status_label.text = f"Status: {message}"
            logger.info(f"Status: {message}")
        except Exception as e:
            logger.error(f"Error updating status: {e}")

    def clear_log(self):
        """Clear the message log"""
        try:
            log_box = self.root.ids.log_box
            log_box.clear_widgets()
            self.notification_count = 0
            self.update_status("Log cleared - Ready for new notifications")
            logger.info("Log cleared")
        except Exception as e:
            logger.error(f"Error clearing log: {e}")

    def test_notification(self):
        """Generate a test notification for testing purposes"""
        try:
            import random
            test_data = {
                'sender': 'Test Contact',
                'message': f'This is a test message #{random.randint(1, 100)}',
                'package': 'com.whatsapp',
                'action': 'posted',
                'timestamp': int(Clock.get_time() * 1000),
                'notificationCode': '1'
            }
            
            self.on_notification_received(test_data)
            logger.info("Test notification generated")
            
        except Exception as e:
            logger.error(f"Error generating test notification: {e}")

if __name__ == "__main__":
    try:
        CuyBotApp().run()
    except Exception as e:
        logger.error(f"App crashed: {e}")
        print(f"App crashed: {e}")  # Fallback print