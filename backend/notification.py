from abc import ABC, abstractmethod

# Interface de Notificação
class Notification(ABC):
    @abstractmethod
    def send_notification(self, destinatario: str, mensagem: str) -> None:
        pass

# Implementações concretas de Notification
class WhatsApp(Notification):
    def __init__(self):
        self.access_token = "access-token-whatsapp"
    
    def send_notification(self, destinatario: str, mensagem: str) -> None:
        # Lógica para enviar notificação via WhatsApp
        print(f"WhatsApp para {destinatario}: {mensagem}")

class Telegram(Notification):
    def __init__(self):
        self.bot_token = "bot-token-telegram"
        self.chat_id = "default-chat-id"
        self.api_url = "https://api.telegram.org"
    
    def send_notification(self, destinatario: str, mensagem: str) -> None:
        # Lógica para enviar notificação via Telegram
        print(f"Telegram para {destinatario}: {mensagem}")

class Email(Notification):
    def __init__(self):
        self.email_origin = "sistema@festas.com"
        self.senha_app = "senha-app-email"
        self.servidor_smtp = "smtp.festas.com"
        self.porta = 587
    
    def send_notification(self, destinatario: str, mensagem: str) -> None:
        # Lógica para enviar notificação via Email
        print(f"Email para {destinatario}: {mensagem}")

# Fábrica abstrata de Notification
class NotificationFactory(ABC):
    @abstractmethod
    def create_notification(self) -> Notification:
        pass

# Implementações concretas da fábrica
class WhatsAppNotificationFactory(NotificationFactory):
    def create_notification(self) -> Notification:
        return WhatsApp()

class TelegramNotificationFactory(NotificationFactory):
    def create_notification(self) -> Notification:
        return Telegram()

class EmailNotificationFactory(NotificationFactory):
    def create_notification(self) -> Notification:
        return Email()

# Cliente que utiliza a fábrica
class NotificationService:
    def __init__(self, notification_factory: NotificationFactory):
        self.notification = notification_factory.create_notification()
    
    def notify(self, destinatario: str, mensagem: str) -> None:
        self.notification.send_notification(destinatario, mensagem)
