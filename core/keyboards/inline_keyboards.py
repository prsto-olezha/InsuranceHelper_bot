from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder

def get_lesson_buttons(lesson_id: int, is_completed: bool = False):
    """Кнопки после урока"""
    builder = InlineKeyboardBuilder()
    
    builder.button(text="📝 Пройти тест", callback_data=f"test_{lesson_id}")
    builder.button(text="🔄 Повторить урок", callback_data=f"repeat_lesson_{lesson_id}")
    builder.button(text="📖 Следующий урок", callback_data=f"next_lesson_{lesson_id}")
    builder.button(text="🎮 Сценарии", callback_data="show_scenarios")
    
    builder.adjust(2)
    
    return builder.as_markup()


def get_scenario_buttons():
    """Кнопки выбора сценария"""
    builder = InlineKeyboardBuilder()
    
    builder.button(text="📱 Разбил телефон", callback_data="scenario_phone")
    builder.button(text="✈️ Заболел за границей", callback_data="scenario_travel")
    builder.button(text="🚲 Украли велосипед", callback_data="scenario_bike")
    builder.button(text="🏥 Травма на тренировке", callback_data="scenario_health")
    builder.button(text="🔥 Пожар в квартире", callback_data="scenario_fire")
    builder.button(text="🐕 Укусила собака", callback_data="scenario_dog")
    builder.button(text="📚 Вернуться к урокам", callback_data="back_to_lessons")
    builder.button(text="🏠 Главное меню", callback_data="back_to_menu")
    
    builder.adjust(2)
    
    return builder.as_markup()


def get_scenario_choice_buttons(scenario_id: str, option_index: int):
    """Кнопки выбора ответа в сценарии"""
    builder = InlineKeyboardBuilder()
    
    builder.button(
        text="✅ Выбрать этот вариант", 
        callback_data=f"choice_{scenario_id}_{option_index}"
    )
    builder.button(
        text="🤔 Показать подсказку", 
        callback_data=f"hint_{scenario_id}_{option_index}"
    )
    
    builder.adjust(1)
    
    return builder.as_markup()


def get_quiz_buttons(question_id: int, total_questions: int):
    """Кнопки для викторины"""
    builder = InlineKeyboardBuilder()
    
    # Кнопки вариантов ответов (A, B, C, D)
    builder.button(text="🔵 Вариант A", callback_data=f"quiz_{question_id}_0")
    builder.button(text="🟢 Вариант B", callback_data=f"quiz_{question_id}_1")
    builder.button(text="🟡 Вариант C", callback_data=f"quiz_{question_id}_2")
    
    if total_questions > 3:
        builder.button(text="🟠 Вариант D", callback_data=f"quiz_{question_id}_3")
    
    builder.button(text="❌ Завершить тест", callback_data="quit_quiz")
    builder.button(text="⏸️ Продолжить позже", callback_data="pause_quiz")
    
    builder.adjust(2)  # 2 колонки
    
    return builder.as_markup()


def get_pagination_buttons(page: int, total_pages: int, prefix: str):
    """Кнопки пагинации (для списка уроков, сценариев)"""
    builder = InlineKeyboardBuilder()
    
    if page > 0:
        builder.button(text="◀️ Назад", callback_data=f"{prefix}_page_{page-1}")
    
    builder.button(text=f"{page+1}/{total_pages}", callback_data="current_page")
    
    if page < total_pages - 1:
        builder.button(text="Вперед ▶️", callback_data=f"{prefix}_page_{page+1}")
    
    builder.button(text="🔙 Выход", callback_data="close_pagination")
    
    builder.adjust(3)
    
    return builder.as_markup()


def get_confirmation_buttons(action: str, item_id: str):
    """Кнопки подтверждения действия"""
    builder = InlineKeyboardBuilder()
    
    builder.button(text="✅ Да", callback_data=f"confirm_{action}_{item_id}")
    builder.button(text="❌ Нет", callback_data=f"cancel_{action}_{item_id}")
    
    builder.adjust(2)
    
    return builder.as_markup()


def get_rating_buttons():
    """Кнопки для рейтинга"""
    builder = InlineKeyboardBuilder()
    
    builder.button(text="🏆 Общий рейтинг", callback_data="rating_all")
    builder.button(text="📅 За неделю", callback_data="rating_week")
    builder.button(text="👥 По возрасту", callback_data="rating_age")
    builder.button(text="🔙 Назад", callback_data="back_to_profile")
    
    builder.adjust(2)
    
    return builder.as_markup()


def get_feedback_buttons(user_id: int):
    """Кнопки для оценки урока/сценария"""
    builder = InlineKeyboardBuilder()
    
    builder.button(text="😊 Отлично", callback_data=f"feedback_great_{user_id}")
    builder.button(text="😐 Нормально", callback_data=f"feedback_normal_{user_id}")
    builder.button(text="😞 Непонятно", callback_data=f"feedback_bad_{user_id}")
    builder.button(text="💡 Хочу доработок", callback_data=f"feedback_improve_{user_id}")
    
    builder.adjust(2)
    
    return builder.as_markup()


def get_share_buttons(lesson_id: int, scenario_id: str = None):
    """Кнопки для шаринга"""
    builder = InlineKeyboardBuilder()
    
    builder.button(text="📤 Поделиться уроком", switch_inline_query=f"урок {lesson_id}")
    builder.button(text="👥 Пригласить друга", callback_data="invite_friend")
    builder.button(text="⭐ В избранное", callback_data=f"favorite_{lesson_id}")
    
    if scenario_id:
        builder.button(text="🎮 Поделиться сценарием", switch_inline_query=f"сценарий {scenario_id}")
    
    builder.adjust(1)
    
    return builder.as_markup()


def get_settings_buttons():
    """Кнопки настроек"""
    builder = InlineKeyboardBuilder()
    
    builder.button(text="🔔 Вкл/Выкл уведомления", callback_data="toggle_notifications")
    builder.button(text="🌙 Тема (светлая/темная)", callback_data="toggle_theme")
    builder.button(text="📊 Сбросить прогресс", callback_data="reset_progress")
    builder.button(text="🌐 Язык", callback_data="change_language")
    builder.button(text="🔙 Назад", callback_data="back_to_profile")
    
    builder.adjust(1)
    
    return builder.as_markup()