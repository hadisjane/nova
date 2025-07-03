from telethon import events
from core.config import DEFAULT_MODE
from api.nova_api import ask_grok
from utils.log_utils import save_log

class TelegramHandler:
    """Класс для обработки событий Telegram"""
    
    def __init__(self, client, groq_api_key, target_user_ids, logs_dir):
        self.client = client
        self.groq_api_key = groq_api_key
        self.target_user_ids = target_user_ids
        self.logs_dir = logs_dir
        self.user_modes = {}
        
        # Регистрация обработчиков событий
        self.client.add_event_handler(
            self.message_handler,
            events.NewMessage
        )
    
    def set_user_mode(self, user_id, mode):
        """Устанавливает режим работы для пользователя"""
        self.user_modes[user_id] = mode
    
    def get_user_mode(self, user_id):
        """Получает режим работы для пользователя"""
        return self.user_modes.get(user_id, DEFAULT_MODE)
    
    async def message_handler(self, event):
        """Обработчик новых сообщений"""
        try:
            sender = await event.get_sender()
            if not sender:
                return

            sender_id = sender.id
            
            # Проверяем, должны ли мы отвечать этому пользователю
            if self.target_user_ids and sender_id not in self.target_user_ids:
                return

            user_msg = event.raw_text
            username = sender.username or str(sender_id)
            mode = self.get_user_mode(sender_id)

            print(f"[IN] From {username} (ID: {sender_id}) | Mode: {mode} | Msg: {user_msg}")

            # Получаем ответ от Grok
            reply = await ask_grok(self.groq_api_key, user_msg, mode, sender_id)
            print(f"[OUT] To {username} | Reply: {reply}")

            # Отправляем ответ пользователю
            await event.respond(reply)
            
            # Сохраняем лог диалога
            await save_log(self.logs_dir, sender_id, user_msg, reply)
            
        except Exception as e:
            print(f"[ERROR] Error processing message: {e}")
            try:
                await event.respond("что-то сломалось, повтори позже")
            except:
                pass