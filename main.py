from kivymd.app import MDApp
from kivymd.uix.boxlayout import MDBoxLayout
from kivymd.uix.label import MDLabel
from kivymd.uix.card import MDCard
from kivymd.uix.scrollview import MDScrollView
from kivy.lang import Builder
from kivy.clock import Clock

from notification_bridge import set_callback, start as notif_start, stop as notif_stop

KV = '''
<NotificationCard@MDCard>:
    orientation: "vertical"
    padding: "12dp"
    spacing: "8dp"
    size_hint_y: None
    height: self.minimum_height
    md_bg_color: 0.1, 0.1, 0.1, 1
    radius: [12, 12, 12, 12]
    MDLabel:
        id: sender
        text: "Sender"
        font_style: "H6"
        theme_text_color: "Custom"
        text_color: 1, 0.8, 0, 1
    MDLabel:
        id: message
        text: "Message"
        font_style: "Body1"
        theme_text_color: "Custom"
        text_color: 1, 1, 1, 1

Screen:
    MDBoxLayout:
        orientation: "vertical"

        MDTopAppBar:
            title: "CuyBot Notification Viewer"
            elevation: 4
            md_bg_color: 0.3, 0.2, 0.5, 1

        MDBoxLayout:
            orientation: "vertical"
            padding: "12dp"
            spacing: "12dp"

            NotificationCard:
                id: current_notif

            MDLabel:
                text: "Notification Log:"
                font_style: "Subtitle1"
                theme_text_color: "Secondary"

            MDScrollView:
                size_hint_y: None
                height: "200dp"
                MDBoxLayout:
                    id: log_box
                    orientation: "vertical"
                    adaptive_height: True
'''

class MainScreen(MDBoxLayout):
    pass


class CuyBotApp(MDApp):
    def build(self):
        self.title = "CuyBotApp"
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "DeepPurple"
        return Builder.load_string(KV)

    def on_start(self):
        # Set callback untuk terima notifikasi dari Java
        set_callback(self.on_notification)
        notif_start()

    def on_stop(self):
        notif_stop()

    def on_notification(self, data):
        """Dipanggil saat notifikasi masuk dari service Java."""
        print("[NOTIF]", data)

        sender = data.get('sender', '')
        message = data.get('message', '')

        # Update card utama
        current_card = self.root.ids.current_notif
        current_card.ids.sender.text = sender
        current_card.ids.message.text = message

        # Tambahkan ke log area
        log_label = MDLabel(
            text=f"[b]{sender}[/b]: {message}",
            markup=True,
            theme_text_color="Custom",
            text_color=(1, 1, 1, 1),
            size_hint_y=None,
            height=30
        )
        self.root.ids.log_box.add_widget(log_label)


if __name__ == "__main__":
    CuyBotApp().run()
