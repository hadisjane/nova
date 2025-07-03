#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import sys
from telethon import TelegramClient
from core.config import LOGS_DIR, get_env_vars
from core.memory import user_memories, load_history_from_logs
from handlers.telegram_handler import TelegramHandler

async def main():
    """Основная функция запуска бота"""
    try:
        # Загрузка конфигурации
        print("[INFO] Загрузка конфигурации...")
        env_vars = get_env_vars()
        
        # Создание директории для логов
        os.makedirs(LOGS_DIR, exist_ok=True)
        
        # Загрузка истории сообщений
        print("[INFO] Загрузка истории сообщений...")
        user_memories.update(load_history_from_logs(LOGS_DIR))
        print(f"[INFO] Загружены данные для {len(user_memories)} пользователей")
        
        # Инициализация Telegram клиента
        print("[INFO] Инициализация Telegram клиента...")
        client = TelegramClient(
            "hf_responder_bot",
            env_vars["TELEGRAM_API_ID"],
            env_vars["TELEGRAM_API_HASH"]
        )
        
        # Инициализация обработчика Telegram
        handler = TelegramHandler(
            client=client,
            groq_api_key=env_vars["GROQ_API_KEY"],
            target_user_ids=env_vars["TARGET_USER_IDS"],
            logs_dir=LOGS_DIR
        )
        
        # Проверка на наличие целевых пользователей
        if not env_vars["TARGET_USER_IDS"]:
            print("[WARNING] Не указаны TARGET_USER_IDS в .env файле. Бот не будет отвечать никому.")
        else:
            print(f"[INFO] Отслеживаем пользователей с ID: {env_vars['TARGET_USER_IDS']}")
        
        # Запуск клиента
        print("[INFO] Запуск бота...")
        await client.start()
        print("[INFO] Бот успешно запущен и ожидает сообщений...")
        
        # Запускаем бота до отключения
        await client.run_until_disconnected()
        
    except ValueError as e:
        print(f"[ERROR] Ошибка конфигурации: {e}")
        sys.exit(1)
    except KeyboardInterrupt:
        print("\n[INFO] Остановка бота...")
    except Exception as e:
        print(f"[FATAL] Неожиданная ошибка при запуске бота: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
    finally:
        if 'client' in locals():
            await client.disconnect()

def run():
    try:
        import asyncio
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n[INFO] Бот остановлен.")
    except Exception as e:
        print(f"[FATAL] Критическая ошибка: {e}")
        import traceback
        traceback.print_exc()
        return 1
    return 0

if __name__ == "__main__":
    import sys
    sys.exit(run())