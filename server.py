from flask import Flask
import threading
import asyncio
import os
import sys
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)


@app.route('/')
def home():
    return "Telegram bot is running!"


# Импортируем и запускаем бота в отдельном потоке
def run_bot():
    # Добавляем путь к текущей директории
    sys.path.append(os.path.dirname(os.path.abspath(__file__)))

    from main import main as bot_main
    asyncio.run(bot_main())


if __name__ == "__main__":
    # Запускаем бота в отдельном потоке
    bot_thread = threading.Thread(target=run_bot, daemon=True)
    bot_thread.start()

    # Запускаем Flask сервер
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)