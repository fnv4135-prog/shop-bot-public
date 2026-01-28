import os
from dotenv import load_dotenv

# Загружаем переменные из .env
load_dotenv()

# Теперь эти переменные доступны в коде
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = os.getenv("ADMIN_ID")

# Проверяем, загрузились ли переменные
if not BOT_TOKEN:
    print("ОШИБКА: BOT_TOKEN не найден в .env файле!")

if not ADMIN_ID:
    print("ВНИМАНИЕ: ADMIN_ID не указан, но бот запустится")