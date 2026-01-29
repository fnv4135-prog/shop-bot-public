from flask import Flask, request
import threading
import asyncio
import os
import sys
import logging
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)


@app.route('/')
def home():
    return "🛒 Telegram Shop Bot is running!"


@app.route('/health')
def health():
    return "✅ OK", 200


# Импортируем и запускаем бота в отдельном потоке
def run_bot():
    try:
        # Добавляем путь к текущей директории
        sys.path.append(os.path.dirname(os.path.abspath(__file__)))

        # Импортируем и запускаем бота
        from main import main as bot_main

        # Создаем новый event loop для потока
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(bot_main())

    except Exception as e:
        logging.error(f"Bot error: {e}")
        # Перезапуск через 5 секунд при ошибке
        threading.Timer(5.0, run_bot).start()


if __name__ == "__main__":
    # Настройка логирования
    logging.basicConfig(level=logging.INFO)

    # Запускаем бота в отдельном потоке
    bot_thread = threading.Thread(target=run_bot, daemon=True)
    bot_thread.start()

    # Запускаем Flask сервер
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)