from flask import Flask, request
import os
import logging
from aiogram import types  # ← ДОБАВИТЬ эту строку!
from main import bot, dp
import asyncio

app = Flask(__name__)

# Берем токен из переменных окружения
BOT_TOKEN = os.environ.get('BOT_TOKEN')

# Формируем путь вебхука
WEBHOOK_PATH = f"/webhook/{BOT_TOKEN}"

# Берем URL из переменных окружения, если нет - используем хардкод
RENDER_EXTERNAL_URL = os.environ.get('RENDER_EXTERNAL_URL', 'https://shop-bot-public.onrender.com')
WEBHOOK_URL = RENDER_EXTERNAL_URL + WEBHOOK_PATH

logging.basicConfig(level=logging.INFO)


@app.route('/')
def home():
    return "🛒 Telegram Shop Bot is running (Webhook mode)!"


@app.route(WEBHOOK_PATH, methods=['POST'])
async def webhook():
    try:
        # Получаем обновление от Telegram
        update = request.json
        update = types.Update(**update)

        # Передаем диспетчеру
        await dp.feed_update(bot, update)

        return 'ok', 200
    except Exception as e:
        logging.error(f"Ошибка в вебхуке: {e}")
        return 'error', 500


async def on_startup():
    """Устанавливаем вебхук при запуске"""
    try:
        # Удаляем старый вебхук (на всякий случай)
        await bot.delete_webhook(drop_pending_updates=True)

        # Устанавливаем новый
        await bot.set_webhook(WEBHOOK_URL)
        logging.info(f"✅ Вебхук установлен: {WEBHOOK_URL}")
    except Exception as e:
        logging.error(f"❌ Ошибка установки вебхука: {e}")


if __name__ == "__main__":
    # Запускаем установку вебхука
    loop = asyncio.get_event_loop()
    loop.run_until_complete(on_startup())

    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)