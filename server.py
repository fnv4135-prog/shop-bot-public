from flask import Flask, request, Response
import os
import logging
import asyncio

app = Flask(__name__)

# Импортируем из main только после инициализации Flask
from main import bot, dp
from aiogram import types  # ← критически важно!

BOT_TOKEN = os.environ.get('BOT_TOKEN')
WEBHOOK_PATH = f"/webhook/{BOT_TOKEN}"
WEBHOOK_URL = f"https://shop-bot-public.onrender.com" + WEBHOOK_PATH

logging.basicConfig(level=logging.INFO)


@app.route('/')
def home():
    return "🛒 Бот работает! Webhook mode"


@app.route(WEBHOOK_PATH, methods=['POST'])
def webhook():
    """Обработчик вебхука"""
    try:
        # Получаем данные от Telegram
        data = request.get_json()

        # Создаем объект Update
        update = types.Update(**data)

        # Запускаем асинхронную обработку в новом event loop
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(dp.feed_update(update))

        return Response(status=200)

    except Exception as e:
        logging.error(f"Webhook error: {str(e)}", exc_info=True)
        return Response(status=500)


async def setup_webhook():
    """Настройка вебхука"""
    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await bot.set_webhook(WEBHOOK_URL)
        logging.info(f"✅ Webhook установлен: {WEBHOOK_URL}")
    except Exception as e:
        logging.error(f"Webhook setup error: {e}")


# Устанавливаем вебхук при старте
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)
loop.run_until_complete(setup_webhook())

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)