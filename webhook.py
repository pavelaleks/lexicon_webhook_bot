import asyncio
import logging
import os

from aiohttp import web
from aiogram import Bot, Dispatcher, F
from aiogram.enums import ParseMode
from aiogram.types import (
    Message, CallbackQuery, FSInputFile, BotCommand,
    InlineKeyboardMarkup, InlineKeyboardButton
)
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from dotenv import load_dotenv

from keyboards import (
    forward_kb, start_options_kb, courses_kb,
    course_summer_kb, course_russian_kb, course_exams_kb
)

# Загрузка переменных
load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
PORT = int(os.getenv("PORT", 8080))

from aiogram.client.default import DefaultBotProperties

bot = Bot(
    token=TOKEN,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
dp = Dispatcher(storage=MemoryStorage())

# Обработчики
@dp.message(F.text == "/start")
async def start_handler(message: Message):
    photo = FSInputFile("lesha.jpg")
    await message.answer_photo(
        photo=photo,
        caption="<b>\U0001F44B Добро пожаловать!</b>\n\n"
                "Меня зовут Лёша Буковкин — я виртуальный помощник Студии «Лексикон»!\n"
                "Нажмите кнопку «Вперёд», и я расскажу, чем могу быть полезен.",
        reply_markup=forward_kb
    )

@dp.callback_query(F.data == "start_more")
async def continue_start(callback: CallbackQuery):
    await callback.answer()
    await callback.message.answer(
        "<b>Чем я могу помочь:</b>\n\n"
        "• рассказать о наших курсах и кружках\n"
        "• познакомить вас с руководителем студии\n"
        "• передать ваш вопрос Павлу Викторовичу Алексееву\n\n"
        "\U0001F447 Выберите, что вас интересует:",
        reply_markup=start_options_kb
    )

@dp.callback_query(F.data == "about_director")
async def about_director(callback: CallbackQuery):
    await callback.answer()
    photo = FSInputFile("alekseev-2.jpg")
    await callback.message.answer_photo(
        photo=photo,
        caption="<b>Павел Викторович Алексеев</b> — профессор, руководитель студии «Лексикон», преподаватель ГАГУ.\n\n"
                "\U0001F4DA Доктор филологических наук, исследователь литературы, автор курсов по русскому языку и литературе.\n\n"
                "Ниже — ссылки, где можно узнать больше:",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="\U0001F310 Персональный сайт", url="https://palekseev.ru")],
            [InlineKeyboardButton(text="\U0001F3DB На сайте ГАГУ", url="https://www.gasu.ru/university/faculty_and_staff/2296/")],
            [InlineKeyboardButton(text="⬅ Назад", callback_data="start_more")]
        ])
    )

@dp.callback_query(F.data == "show_courses")
@dp.message(F.text == "/courses")
async def show_courses(event: CallbackQuery | Message):
    if isinstance(event, CallbackQuery):
        await event.answer()
        msg = event.message
    else:
        msg = event
    await msg.answer("<b>Выберите интересующий вас курс:</b>", reply_markup=courses_kb)

@dp.callback_query(F.data == "course_summer")
async def show_course_summer(callback: CallbackQuery):
    await callback.answer()
    await callback.message.answer(
        "<b>\U0001F31E Летняя языковая школа «Приключения с Лёшей Буковкиным»</b>\n\n...",  # Сокращено для читаемости
        reply_markup=course_summer_kb
    )

@dp.callback_query(F.data == "course_russian")
async def show_course_russian(callback: CallbackQuery):
    await callback.answer()
    await callback.message.answer("<b>\U0001F4D8 Курс «Русский на отлично!»</b>\n\n...", reply_markup=course_russian_kb)

@dp.callback_query(F.data == "course_exams")
async def show_course_exams(callback: CallbackQuery):
    await callback.answer()
    await callback.message.answer("<b>\U0001F4DA Подготовка к ОГЭ и ЕГЭ</b>\n\n...", reply_markup=course_exams_kb)

@dp.callback_query(F.data.startswith("signup_course_"))
async def handle_signup(callback: CallbackQuery):
    user = callback.from_user
    course_name = {
        "signup_course_summer": "Летняя школа",
        "signup_course_russian": "Русский на отлично!",
        "signup_course_exams": "Подготовка к ОГЭ/ЕГЭ"
    }.get(callback.data, "неизвестный курс")
    message_text = (
        f"<b>Заявка на курс:</b> {course_name}\n"
        f"От: @{user.username or 'без username'} (id: {user.id})"
    )
    await bot.send_message(chat_id=ADMIN_ID, text=message_text)
    await callback.answer("Спасибо! Ваша заявка передана.")

@dp.message(F.text == "/about")
async def about_command(message: Message):
    await message.answer("<b>Студия «Лексикон»</b>\n\n...")

@dp.message(F.text == "/location")
async def location_command(message: Message):
    await message.answer("📍 Мы находимся по адресу: ...", disable_web_page_preview=True)

@dp.callback_query(F.data == "signup_direct")
@dp.message(F.text == "/signup")
async def signup_direct(event: CallbackQuery | Message):
    if isinstance(event, CallbackQuery):
        await event.answer()
        msg = event.message
    else:
        msg = event
    await msg.answer("✍️ Напишите, на какой курс хотите записаться — и я передам это Павлу Викторовичу.")

@dp.callback_query(F.data == "write_direct")
@dp.message(F.text == "/write")
async def write_direct(event: CallbackQuery | Message):
    if isinstance(event, CallbackQuery):
        await event.answer()
        msg = event.message
    else:
        msg = event
    await msg.answer("💬 Напишите ваш вопрос — и Павел Викторович ответит вам лично.")

@dp.message()
async def forward_message(message: Message):
    user = message.from_user
    text = f"<b>Сообщение от @{user.username or 'без username'}:</b>\n\n{message.text}"
    try:
        await bot.send_message(chat_id=ADMIN_ID, text=text)
        await message.answer("Спасибо! Ваше сообщение передано.")
    except Exception:
        await message.answer("Произошла ошибка при передаче сообщения.")

# Webhook
async def on_startup(app):
    await bot.set_webhook(WEBHOOK_URL)
    await bot.set_my_commands([
        BotCommand(command="start", description="📍 Старт"),
        BotCommand(command="courses", description="📚 Курсы"),
        BotCommand(command="about", description="ℹ️ О студии"),
        BotCommand(command="write", description="✉️ Написать руководителю"),
        BotCommand(command="location", description="📍 Где нас найти"),
    ])

async def on_shutdown(app):
    await bot.delete_webhook()
    await bot.session.close()

async def create_app():
    app = web.Application()
    app.on_startup.append(on_startup)
    app.on_shutdown.append(on_shutdown)
    SimpleRequestHandler(dispatcher=dp, bot=bot).register(app, path="/webhook")
    setup_application(app, dp, bot=bot)
    return app

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    web.run_app(create_app(), port=PORT)
