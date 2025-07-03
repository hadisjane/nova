import os
import json

class UserMemory:
    """Класс для управления памятью пользователя с учетом важности сообщений"""
    
    def __init__(self, max_messages=1000, decay_after=500):
        self.messages = []
        self.importance = []
        self.max_messages = max_messages
        self.decay_after = decay_after
    
    def add_message(self, role: str, content: str):
        """Добавляет новое сообщение с начальной важностью 1.0"""
        self.messages.append({"role": role, "content": content})
        self.importance.append(1.0)
        
        # Если достигли лимита, удаляем наименее важные сообщения
        if len(self.messages) > self.max_messages:
            self._prune_messages()
    
    def update_importance(self, message_index: int, delta: float):
        """Обновляет важность сообщения"""
        if 0 <= message_index < len(self.importance):
            self.importance[message_index] = max(0.1, self.importance[message_index] + delta)
    
    def _prune_messages(self):
        """Удаляем 20% наименее важных сообщений"""
        to_remove = max(10, len(self.messages) // 5)  # Удаляем хотя бы 10 сообщений
        
        # Сортируем индексы по важности (наименее важные сначала)
        sorted_indices = sorted(range(len(self.importance)), key=lambda i: self.importance[i])
        
        # Удаляем наименее важные сообщения
        indices_to_remove = sorted(sorted_indices[:to_remove], reverse=True)
        for idx in indices_to_remove:
            if idx < len(self.messages):
                del self.messages[idx]
                del self.importance[idx]
    
    def get_recent_messages(self, count: int):
        """Возвращает последние N сообщений"""
        return self.messages[-count:]
    
    def get_context(self, max_tokens=2000):
        """Собирает контекст, пока не достигнем лимита токенов"""
        context = []
        total_tokens = 0
        
        # Идём с конца, чтобы взять самые свежие сообщения
        for msg in reversed(self.messages):
            msg_tokens = len(str(msg).split()) * 1.5  # Примерная оценка токенов
            if total_tokens + msg_tokens > max_tokens:
                break
            context.insert(0, msg)  # Добавляем в начало, чтобы сохранить порядок
            total_tokens += msg_tokens
            
        return context

# Глобальное хранилище истории пользователей
user_memories = {}

def load_history_from_logs(logs_dir):
    """Загружает историю сообщений из файлов логов"""
    if not os.path.exists(logs_dir):
        print("[INFO] Директория логов не найдена")
        return {}
        
    history = {}
    for filename in os.listdir(logs_dir):
        if not filename.endswith('.json'):
            continue
            
        try:
            user_id = int(filename.split('.')[0])
            filepath = os.path.join(logs_dir, filename)
            
            with open(filepath, 'r', encoding='utf-8') as f:
                logs = json.load(f)
            
            if not isinstance(logs, list):
                print(f"[WARNING] Неверный формат лога {filename}: ожидался список")
                continue
                
            print(f"\n[DEBUG] Загружаем лог {filename}:")
            memory = UserMemory()
            message_count = 0
            
            for i, entry in enumerate(logs[-600:], 1):  # Берем последние 600 записей
                if not isinstance(entry, dict):
                    print(f"[WARNING] Пропуск записи {i}: неверный формат")
                    continue
                
                # Обрабатываем сообщение пользователя
                user_msg = entry.get('user_message', '').strip()
                if user_msg:
                    memory.add_message("USER", user_msg)
                    message_count += 1
                    print(f"[DEBUG] #{message_count} USER: {user_msg[:50]}{'...' if len(user_msg) > 50 else ''}")
                
                # Обрабатываем ответ бота
                bot_reply = entry.get('bot_reply', '').strip()
                if bot_reply:
                    memory.add_message("CHATBOT", bot_reply)
                    message_count += 1
                    print(f"[DEBUG] #{message_count} BOT: {bot_reply[:50]}{'...' if len(bot_reply) > 50 else ''}")
            
            history[user_id] = memory
            print(f"[INFO] Загружено {message_count} сообщений для пользователя {user_id}")
            
        except json.JSONDecodeError as e:
            print(f"[ERROR] Ошибка чтения JSON в файле {filename}: {str(e)}")
        except Exception as e:
            print(f"[ERROR] Неожиданная ошибка при загрузке лога {filename}: {str(e)}")
            import traceback
            traceback.print_exc()
    
    return history