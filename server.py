from flask import Flask, request
import os
import logging
from main import bot, dp
import asyncio

app = Flask(__name__)

WEBHOOK_PATH = f"/webhook/{os.environ.get('BOT_TOKEN')}"
WEBHOOK_URL = f"https://shop-bot-public.onrender.com" + WEBHOOK_PATH


@app.route('/')
def home():
    return "🛒 Telegram Shop Bot is running (Webhook mode)!"


@app.route(WEBHOOK_PATH, methods=['POST'])
async def webhook():
    update = request.json
    update = types.Update(**update)
    await dp.feed_update(bot, update)
    return 'ok'


async def on_startup():
    await bot.set_webhook(WEBHOOK_URL)
    logging.info("Webhook установлен")


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    # Запускаем установку вебхука
    loop = asyncio.new_event_loop()
    loop.run_until_complete(on_startup())

    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)