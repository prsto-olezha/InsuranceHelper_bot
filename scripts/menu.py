from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from core.keyboards.reply_keyboards import (
    get_main_menu_keyboard,
    get_lessons_menu_keyboard,
    get_quiz_menu_keyboard,
    get_profile_keyboard,
    get_back_keyboard
)
from core.keyboards.inline_keyboards import (
        get_scenarios_menu_keyboard,
)
from core.db import get_user_stats
import core.FSM as FSM

router = Router()

@router.callback_query(lambda c: c.data == "back_to_menu")
async def back_to_menu(callback: CallbackQuery, state: FSMContext):
    """Возврат в главное меню"""
    await state.set_state(FSM.UserStates.default)
    await callback.message.answer(
        "🏠 <b>Главное меню</b>\n\n"
        "Выбери, что хочешь сделать:",
        parse_mode="HTML",
        reply_markup=get_main_menu_keyboard()
    )


@router.message(F.text == "🔙 Назад в меню")
@router.message(F.text == "🔙 Назад")
async def back_to_main_menu(message: Message, state: FSMContext):
    """Возврат в главное меню"""
    await state.set_state(FSM.UserStates.default)
    await message.answer(
        "🏠 <b>Главное меню</b>\n\n"
        "Выбери, что хочешь сделать:",
        parse_mode="HTML",
        reply_markup=get_main_menu_keyboard()
    )

    
@router.message(F.text == "📚 Уроки")
async def show_lessons_menu(message: Message, state: FSMContext):
    """Показать меню уроков"""
    await state.set_state(FSM.UserStates.reading_lesson)
    await message.answer(
        "📖 <b>Уроки по страхованию</b>\n\n"
        "Выбери урок, который хочешь изучить:\n\n"
        "✨ <i>Совет: проходи уроки по порядку, так будет легче понять материал</i>",
        parse_mode="HTML",
        reply_markup=get_lessons_menu_keyboard()
    )


@router.message(F.text == "🎮 Сценарии")
async def show_scenarios_menu(message: Message, state: FSMContext):
    """Показать меню сценариев"""
    await state.set_state(FSM.ScenarioStates.CHOOSING_SCENARIO)
    
    scenarios_text = """
🎮 <b>Реальные жизненные ситуации</b>

Выбери сценарий и узнай, как страхование помогает в жизни!

<b>Доступные сценарии:</b>
📱 <b>Разбил телефон</b> — что делать?
✈️ <b>Заболел за границей</b> — как не разориться?
🚲 <b>Украли велосипед</b> — вернут ли деньги?
🏥 <b>Травма на тренировке</b> — кто заплатит за лечение?

🔥 <i>Каждый сценарий — это реальная жизненная ситуация. 
Твой выбор влияет на результат!</i>

👇 <b>Нажми на кнопку ниже, чтобы начать!</b>
"""
    await message.answer(
        scenarios_text,
        parse_mode="HTML",
        reply_markup=get_scenarios_menu_keyboard()
    )


@router.message(F.text == "📝 Тест")
async def show_quiz_menu(message: Message, state: FSMContext):
    """Показать меню тестов"""
    await message.answer(
        "🧠 <b>Проверь свои знания</b>\n\n"
        "Здесь ты можешь:\n"
        "• Пройти тест из 5 вопросов\n"
        "• Посмотреть свои результаты\n"
        "• Закрепить пройденный материал\n\n"
        "🔥 <i>Каждый правильный ответ приносит очки для рейтинга!</i>\n\n"
        "👇 <b>Нажми кнопку ниже, чтобы начать тест:</b>",
        parse_mode="HTML",
        reply_markup=get_quiz_menu_keyboard()
    )


@router.message(F.text == "❓ Помощь")
async def show_help_menu(message: Message, state: FSMContext):
    """Показать меню помощи"""
    help_text = """
❓ <b>Помощь</b>

<b>🤖 Как пользоваться ботом?</b>

1️⃣ <b>📚 Уроки</b>
   • Изучи теорию страхования
   • 4 урока с простыми объяснениями
   • За каждый урок даём +10 очков

2️⃣ <b>🎮 Сценарии</b>
   • Окажись в реальной жизненной ситуации
   • Сделай выбор и узнай результат
   • За правильные решения даём до +20 очков

3️⃣ <b>📝 Тест</b>
   • Проверь свои знания
   • 5 вопросов по основам страхования
   • За правильные ответы — бонусные очки

4️⃣ <b>🏆 Мой прогресс</b>
   • Смотри свою статистику
   • Отслеживай уровень и очки
   • Узнай место в рейтинге

<b>💡 Полезные советы:</b>
• Проходи уроки по порядку — так легче
• В сценариях пробуй разные варианты
• Чем больше очков — тем выше уровень

<b>📞 Контакты:</b>
По вопросам и предложениям: @prsto_olezha
"""
    await message.answer(
        help_text,
        parse_mode="HTML",
        reply_markup=get_back_keyboard()
    )


@router.message(F.text == "ℹ️ О боте")
async def show_about(message: Message, state: FSMContext):
    """Показать информацию о боте"""
    about_text = """
ℹ️ <b>О боте</b>

<b>🤖 СтрахоГид</b> — это интерактивный помощник, который учит основам страхования простым и понятным языком.

<b>🎯 Наша цель:</b>
• Научить подростков финансовой грамотности
• Показать, как страхование помогает в жизни
• Развеять мифы о страховках
• Подготовить к взрослой жизни

<b>📊 Статистика бота:</b>
• 4 урока с теорией
• 4 жизненных сценария
• 5 тестовых вопросов
• Система уровней и очков
• Рейтинг пользователей

<b>🏆 Система уровней:</b>
• Новичок: 0-49 очков 🌱
• Ученик: 50-199 очков 📚
• Продвинутый: 200-499 очков ⭐
• Эксперт: 500+ очков 🏆

<b>📝 Контакты:</b>
По всем вопросам: @prsto_olezha
Предложения по улучшению: @prsto_olezha

<i>Страхование — это не сложно, когда есть СтрахоГид! 😊</i>
"""
    await message.answer(
        about_text,
        parse_mode="HTML",
        reply_markup=get_back_keyboard()
    )


@router.message(F.text == "🔙 Выход из админки")
async def exit_admin_from_menu(message: Message, state: FSMContext):
    """Выход из админки (если случайно попал)"""
    from core.keyboards.reply_keyboards import get_main_menu_keyboard
    
    await state.set_state(FSM.UserStates.default)
    await message.answer(
        "👋 Возврат в главное меню",
        reply_markup=get_main_menu_keyboard()
    )
