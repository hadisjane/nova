import os
import ssl
import certifi
from dotenv import load_dotenv

# Загружаем переменные окружения
load_dotenv()

# Настройки путей
LOGS_DIR = "logs"
os.makedirs(LOGS_DIR, exist_ok=True)

# Режимы работы бота
DEFAULT_MODE = 'nova'

# Load system prompt from file
def load_system_prompt():
    """Загружает системный промпт из файла"""
    try:
        with open('instructions/nova.md', 'r', encoding='utf-8') as f:
            return f.read().strip()
    except Exception as e:
        print(f"[WARNING] Не удалось загрузить системный промпт: {e}")
        return ""

# System prompts
MODE_PROMPTS = {
    "nova": load_system_prompt() or (
        "Вы — виртуальный помощник в стиле Джарвиса. "
        "Отвечайте вежливо и профессионально."
    )
}

def create_ssl_context():
    """Создает SSL контекст для HTTPS запросов"""
    return ssl.create_default_context(cafile=certifi.where())

def parse_target_users(raw_ids):
    """Парсит строку с ID пользователей в множество"""
    if not raw_ids:
        return set()
    return {int(uid.strip()) for uid in raw_ids.split(",") if uid.strip()}

def get_env_vars():
    """Получает и валидирует переменные окружения"""
    groq_key = os.getenv("GROQ_API_KEY")
    if not groq_key:
        raise ValueError("GROQ_API_KEY is not set in .env file")
    
    try:
        api_id = int(os.getenv("TELEGRAM_API_ID"))
    except (TypeError, ValueError):
        raise ValueError("TELEGRAM_API_ID is not set or invalid in .env file")
    
    api_hash = os.getenv("TELEGRAM_API_HASH")
    if not api_hash:
        raise ValueError("TELEGRAM_API_HASH is not set in .env file")
    
    return {
        "GROQ_API_KEY": groq_key,
        "TELEGRAM_API_ID": api_id,
        "TELEGRAM_API_HASH": api_hash,
        "TARGET_USER_IDS": parse_target_users(os.getenv("TARGET_USER_IDS", "")),
    }