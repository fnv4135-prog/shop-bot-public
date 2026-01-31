import asyncio
import logging
import os
from aiohttp import web
from aiogram import types

# Импортируем бота и диспетчера
from main import bot, dp

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Получаем переменные окружения
BOT_TOKEN = os.environ.get('BOT_TOKEN')
WEBHOOK_PATH = f"/webhook/{BOT_TOKEN}"
WEBHOOK_URL = f"https://shop-bot-public.onrender.com" + WEBHOOK_PATH


async def handle_webhook(request):
    """Обработчик вебхука"""
    try:
        # Получаем обновление
        data = await request.json()
        update = types.Update(**data)

        # Передаем диспетчеру
        await dp.feed_update(bot, update)

        return web.Response(status=200)
    except Exception as e:
        logger.error(f"Webhook error: {e}")
        return web.Response(status=500)


async def handle_index(request):
    """Главная страница"""
    return web.Response(text="🛒 Telegram Shop Bot is running (Webhook mode)!")


async def on_startup(app):
    """Установка вебхука при старте"""
    try:
        await bot.delete_webhook(drop_pending_updates=True)
        await bot.set_webhook(WEBHOOK_URL)
        logger.info(f"✅ Webhook установлен: {WEBHOOK_URL}")
    except Exception as e:
        logger.error(f"Webhook setup error: {e}")


async def on_shutdown(app):
    """Очистка при завершении"""
    await bot.session.close()


def create_app():
    """Создание приложения"""
    app = web.Application()

    # Регистрируем маршруты
    app.router.add_get('/', handle_index)
    app.router.add_post(WEBHOOK_PATH, handle_webhook)

    # Регистрируем события
    app.on_startup.append(on_startup)
    app.on_shutdown.append(on_shutdown)

    return app


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))

    # Запускаем сервер
    web.run_app(
        create_app(),
        host='0.0.0.0',
        port=port,
        access_log=logger
    )