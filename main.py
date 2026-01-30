import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from config import BOT_TOKEN, ADMIN_ID  # Импортируем из config.py

# Настройка логирования
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Создаем объекты бота и диспетчера
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Товары (временное хранилище)
products = [
    {"id": 1, "name": "📱 Чек-лист по Python", "price": 500, "description": "Основные команды Python"},
    {"id": 2, "name": "🎨 Дизайн логотипа", "price": 1500, "description": "Простой логотип для проекта"},
    {"id": 3, "name": "🤖 Настройка бота", "price": 3000, "description": "Базовая настройка Telegram бота"},
]


@dp.message(Command("start"))
async def start_command(message: types.Message):
    """Обработчик команды /start"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🛍️ Каталог товаров", callback_data="catalog")],
        [InlineKeyboardButton(text="📞 Контакты", callback_data="contacts")],
        [InlineKeyboardButton(text="🛒 Корзина (0)", callback_data="cart")]
    ])
    await message.answer(
        "👋 *Добро пожаловать в наш магазин!*\n\n"
        "Здесь вы можете приобрести цифровые товары.",
        reply_markup=keyboard,
        parse_mode="Markdown"
    )


@dp.callback_query(F.data == "catalog")
async def show_catalog(callback: types.CallbackQuery):
    """Показ каталога товаров"""
    keyboard = []
    for product in products:
        keyboard.append([
            InlineKeyboardButton(
                text=f"{product['name']} - {product['price']}₽",
                callback_data=f"product_{product['id']}"
            )
        ])

    # Кнопка "Назад"
    keyboard.append([InlineKeyboardButton(text="⬅️ Назад", callback_data="back_to_start")])

    await callback.message.edit_text(
        "🎁 *Каталог товаров:*\nВыберите товар:",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=keyboard),
        parse_mode="Markdown"
    )


@dp.callback_query(F.data.startswith("product_"))
async def show_product(callback: types.CallbackQuery):
    """Показ информации о товаре"""
    product_id = int(callback.data.split("_")[1])
    product = next((p for p in products if p["id"] == product_id), None)

    if product:
        keyboard = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="✅ Купить", callback_data=f"buy_{product_id}")],
            [InlineKeyboardButton(text="⬅️ Назад в каталог", callback_data="catalog")]
        ])

        await callback.message.edit_text(
            f"*{product['name']}*\n\n"
            f"💰 Цена: *{product['price']}₽*\n"
            f"📝 Описание: {product['description']}\n\n"
            f"Для покупки нажмите кнопку ниже:",
            reply_markup=keyboard,
            parse_mode="Markdown"
        )


@dp.callback_query(F.data == "contacts")
async def show_contacts(callback: types.CallbackQuery):
    """Показ контактов"""
    keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="⬅️ Назад", callback_data="back_to_start")]
    ])

    await callback.message.edit_text(
        "📞 *Контакты:*\n\n"
        "• Телеграм: @your_username\n"
        "• Email: your@email.com\n"
        "• Время работы: 10:00-22:00\n\n"
        "📢 По всем вопросам пишите!",
        reply_markup=keyboard,
        parse_mode="Markdown"
    )


@dp.callback_query(F.data == "back_to_start")
async def back_to_start(callback: types.CallbackQuery):
    """Возврат в главное меню"""
    await start_command(callback.message)


async def main():
    """Запуск бота"""
    logger.info("Бот запускается...")
    await dp.start_polling(bot)


async def run_bot():
    await main()

#if __name__ == "__main__":
#    asyncio.run(run_bot())