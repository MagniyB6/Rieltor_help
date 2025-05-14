# ========== 🔒 МОДУЛЬ ЛИМИТОВ ==========
# Этот модуль отвечает за проверку и уменьшение лимитов для пользователей.
# Используется для ограничения генераций контента, изображений и прочего.

import json
from datetime import datetime, timedelta

USERS_FILE = "data/users.json"

def load_users():
    try:
        with open(USERS_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}

def save_users(users):
    with open(USERS_FILE, "w", encoding="utf-8") as f:
        json.dump(users, f, ensure_ascii=False, indent=4)

def reset_limits_if_needed(user_data):
    now = datetime.now()
    last_reset_str = user_data.get("last_reset")

    if not last_reset_str:
        user_data["last_reset"] = now.isoformat()
        return True

    last_reset = datetime.fromisoformat(last_reset_str)
    if now.date() != last_reset.date():
        user_data["limits"] = {
            "post": 3,
            "image": 1
        }
        user_data["last_reset"] = now.isoformat()
        return True

    return False

def check_and_decrease_limit(user_id: int, action: str) -> bool:
    users = load_users()
    user_id = str(user_id)

    user_data = users.get(user_id, {
        "limits": {
            "post": 3,
            "image": 1
        },
        "last_reset": datetime.now().isoformat()
    })

    reset_limits_if_needed(user_data)
    
    if user_data["limits"].get(action, 0) > 0:
        user_data["limits"][action] -= 1
        users[user_id] = user_data
        save_users(users)
        return True
    else:
        return False
