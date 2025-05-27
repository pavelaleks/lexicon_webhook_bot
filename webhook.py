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
from aiogram.client.default import DefaultBotProperties

from keyboards import (
    forward_kb, start_options_kb, courses_kb,
    course_summer_kb, course_russian_kb, course_exams_kb
)

load_dotenv()
TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
PORT = int(os.getenv("PORT", 8080))

bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher(storage=MemoryStorage())

@dp.message(F.text == "/start")
async def start_handler(message: Message):
    photo = FSInputFile("lesha.jpg")
    await message.answer_photo(
        photo=photo,
        caption="<b>👋 Добро пожаловать!</b>\n\n"
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
        "👇 Выберите, что вас интересует:",
        reply_markup=start_options_kb
    )

@dp.callback_query(F.data == "about_director")
async def about_director(callback: CallbackQuery):
    await callback.answer()
    photo = FSInputFile("alekseev-2.jpg")
    await callback.message.answer_photo(
        photo=photo,
        caption="<b>Павел Викторович Алексеев</b> — профессор, руководитель студии «Лексикон», преподаватель ГАГУ.\n\n"
                "📚 Доктор филологических наук, исследователь литературы, автор курсов по русскому языку и литературе.\n\n"
                "Ниже — ссылки, где можно узнать больше:",
        reply_markup=InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="🌐 Персональный сайт", url="https://palekseev.ru")],
            [InlineKeyboardButton(text="🏛 На сайте ГАГУ", url="https://www.gasu.ru/university/faculty_and_staff/2296/")],
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
        "<b>🌞 Летняя языковая школа «Приключения с Лёшей Буковкиным»</b>\n\n"
        "📅 <b>Даты:</b> 1–14 июня 2025\n"
        "👧👦 <b>Возраст:</b> ученики 1–3 классов\n"
        "👥 <b>Формат:</b> занятия по 2 ч. в день в мини-группах (до 4 человек)\n"
        "📍 <b>Место:</b> Горно-Алтайск, студия «Лексикон»\n"
        "💰 <b>Стоимость:</b> 6000 рублей\n\n"
        "💡 <b>Кому подойдёт курс:</b>\n"
        "• тем, кто хочет подтянуть русский язык в непринуждённой форме\n"
        "• детям, которые любят истории, загадки, игры со словами\n"
        "• тем, кто устал от учебников, но хочет развиваться летом\n\n"
        "🔎 <b>Программа:</b>\n"
        "• языковые квесты и грамматические игры\n"
        "• чтение и обсуждение интересных текстов\n"
        "• творческие задания, письма и сочинения\n"
        "• развитие речи, памяти, воображения\n\n"
        "💬 Это курс, где дети не только учатся, но и отдыхают с пользой — весело, дружно, в языковой среде.\n\n"
        "📝 Осталось несколько мест!\n"
        "✉ Чтобы записаться — нажмите кнопку ниже.",
        reply_markup=course_summer_kb
    )

@dp.callback_query(F.data == "course_russian")
async def show_course_russian(callback: CallbackQuery):
    await callback.answer()
    await callback.message.answer(
        "<b>📘 Курс «Русский на отлично!»</b>\n\n"
        "🎒 <b>Классы:</b> 4–8\n"
        "📅 <b>Старт:</b> с 1 августа 2025 года (на весь учебный год)\n"
        "🕒 <b>Занятия:</b> 2 раза в неделю по 60 минут\n"
        "👥 <b>Формат:</b> мини-группы и индивидуальные занятия\n"
        "📍 <b>Место:</b> студия «Лексикон», Горно-Алтайск\n"
        "💰 <b>Стоимость:</b> 5200 рублей в месяц\n\n"
        "💡 <b>Кому подойдёт:</b>\n"
        "• школьникам, которым нужен прочный уровень по русскому языку\n"
        "• тем, кто готовится к ВПР или хочет перейти на «5»\n"
        "• детям, которым не хватает системности в школьной программе\n"
        "• тем, кто уже думает об успешной сдаче ОГЭ и ЕГЭ в будущем\n\n"
        "🔍 <b>На занятиях:</b>\n"
        "• отрабатываем орфографию и пунктуацию\n"
        "• учим писать изложение, сочинение, рассуждение\n"
        "• разбираем грамматические темы и тренируемся на реальных заданиях\n"
        "• развиваем речь, учим анализировать текст и формулировать мысли\n\n"
        "🧭 Курс даёт не только текущий результат, но и уверенную базу на будущее.\n\n"
        "✉ Чтобы узнать расписание или записаться — нажмите кнопку ниже.",
        reply_markup=course_russian_kb
    )

@dp.callback_query(F.data == "course_exams")
async def show_course_exams(callback: CallbackQuery):
    await callback.answer()
    await callback.message.answer(
        "<b>📚 Подготовка к ОГЭ и ЕГЭ</b>\n\n"
        "📅 <b>Старт:</b> с 1 сентября 2025 года (на весь учебный год)\n"
        "📘 <b>Предметы:</b> русский язык, литература, история, обществознание\n"
        "🕒 <b>Занятия:</b> 1–2 раза в неделю по 60–120 минут\n"
        "👥 <b>Формат:</b> индивидуально или в мини-группах\n"
        "📍 <b>Место:</b> студия «Лексикон» (очно) или онлайн\n"
        "💰 <b>Стоимость:</b> от 4800 рублей в месяц (в зависимости от формата)\n\n"
        "💡 <b>Кому подойдёт:</b>\n"
        "• девятиклассникам и одиннадцатиклассникам, которым нужна стабильная подготовка\n"
        "• тем, кто хочет уверенно сдать экзамены, не откладывая «на потом»\n"
        "• ученикам, которым важно не просто пройти тесты, но и разобраться в материале\n\n"
        "🔍 <b>На занятиях:</b>\n"
        "• системно разбираем все типы экзаменационных заданий\n"
        "• тренируем написание сочинений, эссе и устных ответов\n"
        "• формируем стратегию и уверенность на экзамене\n"
        "• отрабатываем навыки под формат ОГЭ и ЕГЭ (по спецификациям ФИПИ)\n\n"
        "👨‍🏫 Преподаватели — опытные педагоги и эксперты, которые помогут справиться даже с самыми сложными темами.\n\n"
        "✉ Напишите, по какому предмету вы хотите готовиться — и мы подберём удобный формат занятий.",
        reply_markup=course_exams_kb
    )

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

@dp.message(F.text == "/about")
async def about_command(message: Message):
    await message.answer(
        "<b>Студия «Лексикон»</b>\n\n"
        "«Лексикон» — это образовательная студия по русскому языку и литературе для учеников 4–11 классов.\n"
        "Мы проводим занятия по школьной программе, готовим к <b>ОГЭ и ЕГЭ по русскому языку, литературе, истории и обществознанию</b>, развиваем письменную и устную речь, "
        "помогаем полюбить чтение и уверенно чувствовать себя на уроках.\n\n"
        "👨‍🏫 В студии работают преподаватели с университетским и школьным стажем, научной степенью и серьёзным методическим опытом.\n"
        "Занятия строятся по авторским программам, с учётом уровня, целей и возраста каждого ученика.\n\n"
        "📚 Что мы предлагаем:\n"
        "• углублённые занятия по русскому языку и литературе\n"
        "• индивидуальную и групповую подготовку к ОГЭ и ЕГЭ\n"
        "• курсы для 4–8 классов «Русский на отлично»\n"
        "• летнюю языковую школу «Приключения с Лешей Буковкиным»\n"
        "• творческие кружки и мастерские\n\n"
        "💻 Мы активно используем технологии:\n"
        "в студии работает Telegram-бот для подготовки к ОГЭ — <b>@lexicon_punctuation_bot</b>,\n"
        "а также интерактивные материалы и цифровые тренажёры.\n\n"
        "📍 Мы находимся в Горно-Алтайске: пр. Коммунистический, 47 (вход со стороны ул. Головина)\n"
        "🗺 <a href=\"https://2gis.ru/gornoaltaysk/firm/70000001093540016\">Посмотреть на карте (2ГИС)</a>\n\n"
        "<b>«Лексикон» — это не просто занятия, это языковая культура, внимание к ученику и серьёзный подход к обучению.</b>"
    )

@dp.message(F.text == "/location")
async def location_command(message: Message):
    await message.answer("📍 Мы находимся по адресу: Горно-Алтайск, пр. Коммунистический, 47", disable_web_page_preview=True)

@dp.message()
async def forward_message(message: Message):
    user = message.from_user
    text = f"<b>Сообщение от @{user.username or 'без username'}:</b>\n\n{message.text}"
    try:
        await bot.send_message(chat_id=ADMIN_ID, text=text)
        await message.answer("Спасибо! Ваше сообщение передано.")
    except Exception:
        await message.answer("Произошла ошибка при передаче сообщения.")

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