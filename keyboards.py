from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# Кнопка "вперёд" после приветствия
forward_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="➡ Вперёд", callback_data="start_more")]
])

# Основное меню после "вперёд"
start_options_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="📚 Курсы и кружки", callback_data="show_courses")],
    [InlineKeyboardButton(text="👤 О руководителе студии", callback_data="about_director")],
    [InlineKeyboardButton(text="💬 Задать вопрос руководителю", callback_data="write_direct")],
    [InlineKeyboardButton(text="📍 Где нас найти", url="https://2gis.ru/gornoaltaysk/firm/70000001093540016")]
])

# Список курсов
courses_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="🌞 Летняя школа (1–14 июня)", callback_data="course_summer")],
    [InlineKeyboardButton(text="📘 Русский на отлично! (с 1 августа)", callback_data="course_russian")],
    [InlineKeyboardButton(text="📚 Подготовка к ОГЭ/ЕГЭ (с 1 сентября)", callback_data="course_exams")]
])

# Индивидуальные клавиатуры под курсами
course_summer_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="← Назад к списку курсов", callback_data="show_courses")],
    [InlineKeyboardButton(text="📩 Оставить заявку", callback_data="signup_direct")]
])

course_russian_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="← Назад к списку курсов", callback_data="show_courses")],
    [InlineKeyboardButton(text="📩 Оставить заявку", callback_data="signup_direct")]
])

course_exams_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="← Назад к списку курсов", callback_data="show_courses")],
    [InlineKeyboardButton(text="📩 Оставить заявку", callback_data="signup_direct")]
])
