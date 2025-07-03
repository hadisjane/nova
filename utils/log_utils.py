import os
import json
from datetime import datetime, timezone

async def save_log(logs_dir, sender_id, user_msg, bot_reply):
    """Сохраняет лог сообщения в JSON файл"""
    log_path = os.path.join(logs_dir, f"{sender_id}.json")
    entry = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "user_message": user_msg,
        "bot_reply": bot_reply
    }
    
    logs = []
    if os.path.exists(log_path):
        try:
            with open(log_path, "r", encoding="utf-8") as f:
                logs = json.load(f)
        except (json.JSONDecodeError, FileNotFoundError):
            logs = []
    
    logs.append(entry)
    
    with open(log_path, "w", encoding="utf-8") as f:
        json.dump(logs, f, indent=2, ensure_ascii=False)