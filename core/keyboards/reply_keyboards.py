from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton, ReplyKeyboardRemove, KeyboardButton

#========================================
# # ReplyKeyboard example
# def get_reply_keyboard():
#     builder = ReplyKeyboardBuilder()
#     builder.button(text="Кнопка 1")
#     builder.button(text="Кнопка 2")
#     builder.button(text="Кнопка 3")
#     builder.adjust(2)  # Расположить кнопки в 2 колонки
#     return builder.as_markup(resize_keyboard=True)


# # Inlinekeboard example
# def get_inline_keyboard():
#     builder = InlineKeyboardBuilder()
#     builder.button(text="Кнопка 1", callback_data="button1")
#     builder.button(text="Кнопка 2", callback_data="button2")
#     builder.button(text="Кнопка 3", callback_data="button3")
#     builder.adjust(2)  # Расположить кнопки в 2 колонки    
#     return builder.as_markup()


def get_main_menu_keyboard():
    """Главное меню бота"""
    builder = ReplyKeyboardBuilder()
    
    # Кнопки в 2 ряда по 2 кнопки
    builder.button(text="📚 Уроки")
    builder.button(text="🎮 Сценарии")
    builder.button(text="📝 Тест")
    builder.button(text="🏆 Мой прогресс")
    builder.button(text="❓ Помощь")
    builder.button(text="ℹ️ О боте")
    
    builder.adjust(2)  # 2 колонки
    
    return builder.as_markup(
        resize_keyboard=True,  # Авто-подгон размера
        input_field_placeholder="Выбери действие 👇"  # Подсказка в поле ввода
    )


def get_lessons_menu_keyboard():
    """Меню уроков"""
    builder = ReplyKeyboardBuilder()
    
    builder.button(text="📖 Урок 1: Что такое страхование?")
    builder.button(text="📖 Урок 2: Виды страхования")
    builder.button(text="📖 Урок 3: Как работает страховка")
    builder.button(text="📖 Урок 4: Как выбрать страховку")
    builder.button(text="📖 Урок 5: Страховые мифы")
    builder.button(text="🔙 Назад в меню")
    
    builder.adjust(1)  # 1 колонка (вертикальный список)
    
    return builder.as_markup(
        resize_keyboard=True,
        input_field_placeholder="Выбери урок 📚"
    )


def get_scenarios_menu_keyboard():
    """Кнопки выбора сценария"""
    builder = InlineKeyboardBuilder()
    
    builder.button(text="📱 Разбил телефон", callback_data="scenario_phone")
    builder.button(text="✈️ Заболел за границей", callback_data="scenario_travel")
    builder.button(text="🚲 Украли велосипед", callback_data="scenario_bike")
    builder.button(text="🏥 Травма на тренировке", callback_data="scenario_health")
    builder.button(text="🔙 Назад в меню", callback_data="back_to_menu")
    
    builder.adjust(1)  # По одной кнопке в ряд
    
    return builder.as_markup()


def get_quiz_menu_keyboard():
    """Меню для тестов"""
    builder = ReplyKeyboardBuilder()
    
    builder.button(text="🧠 Начать новый тест")
    builder.button(text="📊 Мои результаты")
    builder.button(text="🔄 Пройти сложные вопросы")
    builder.button(text="🔙 Назад в меню")
    
    builder.adjust(2)  # 2 колонки
    
    return builder.as_markup(
        resize_keyboard=True,
        input_field_placeholder="Что хочешь проверить? 📝"
    )


def get_profile_keyboard():
    """Клавиатура профиля"""
    builder = ReplyKeyboardBuilder()
    
    builder.button(text="📊 Моя статистика")
    builder.button(text="📈 Прогресс по урокам")
    builder.button(text="🏆 Рейтинг")
    builder.button(text="🔙 Назад в меню")
    
    builder.adjust(2)  # 2 колонки
    
    return builder.as_markup(
        resize_keyboard=True,
        input_field_placeholder="Твой прогресс 🏆"
    )


def get_help_keyboard():
    """Клавиатура помощи"""
    builder = ReplyKeyboardBuilder()
    
    builder.button(text="❓ Как пользоваться ботом")
    builder.button(text="📚 Что такое страхование")
    builder.button(text="💬 Задать вопрос")
    builder.button(text="🔙 Назад в меню")
    
    builder.adjust(2)
    
    return builder.as_markup(
        resize_keyboard=True,
        input_field_placeholder="Нужна помощь? ❓"
    )


def get_back_keyboard():
    """Универсальная кнопка 'Назад'"""
    builder = ReplyKeyboardBuilder()
    
    builder.button(text="🔙 Назад")
    
    builder.adjust(1)
    
    return builder.as_markup(
        resize_keyboard=True,
        input_field_placeholder="Нажми 'Назад' для возврата 🔙"
    )


def get_admin_keyboard():
    """Админская клавиатура (только для админов)"""
    builder = ReplyKeyboardBuilder()
    
    builder.button(text="📊 Статистика бота")
    builder.button(text="📨 Рассылка")
    builder.button(text="👥 Список пользователей")
    builder.button(text="⚙️ Настройки")
    builder.button(text="🔙 Выход из админки")
    
    builder.adjust(2)
    
    return builder.as_markup(
        resize_keyboard=True,
        input_field_placeholder="Админ-панель 🔧"
    )

    
def get_age_keyboard():
    """Клавиатура для выбора возраста"""
    builder = ReplyKeyboardBuilder()
    
    for age in [11, 12, 13, 14, 15, 16, 17, 18]:
        builder.button(text=str(age))
    
    builder.button(text="⏩ Пропустить")
    builder.adjust(4)  # 4 колонки
    
    return builder.as_markup(
        resize_keyboard=True,
        input_field_placeholder="Введи свой возраст или выбери из кнопок 👇"
    )