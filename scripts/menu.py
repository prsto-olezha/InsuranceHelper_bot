from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from core.keyboards.reply_keyboards import (
    get_main_menu_keyboard,
    get_lessons_menu_keyboard,
    get_scenarios_menu_keyboard,
    get_quiz_menu_keyboard,
    get_profile_keyboard,
    get_help_keyboard,
    get_back_keyboard
)
from core.db import get_user_stats
import core.FSM as FSM

router = Router()


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


@router.message(F.text == "🏆 Мой прогресс")
async def show_profile_menu(message: Message, state: FSMContext):
    """Показать меню профиля"""
    stats = await get_user_stats(message.from_user.id)
    
    if not stats:
        await message.answer(
            "👤 <b>Твой профиль</b>\n\n"
            "Статистика пока пуста. Начни обучение, чтобы заработать очки!\n\n"
            "📚 Начни с первого урока или попробуй сценарий!",
            parse_mode="HTML",
            reply_markup=get_profile_keyboard()
        )
        return
    
    # Эмодзи для уровня
    level_emoji = {
        "Новичок": "🌱",
        "Ученик": "📚",
        "Продвинутый": "⭐",
        "Эксперт": "🏆"
    }.get(stats['level'], "📖")
    
    text = (
        f"👤 <b>Твой профиль</b>\n\n"
        f"{level_emoji} <b>Уровень:</b> {stats['level']}\n"
        f"⭐ <b>Очки:</b> {stats['points']}\n"
        f"📖 <b>Пройдено уроков:</b> {stats['lessons_completed']}/4\n"
        f"🎮 <b>Пройдено сценариев:</b> {stats['scenarios_completed']}/4\n"
    )
    
    if stats.get('quiz_average', 0) > 0:
        text += f"📊 <b>Средний результат тестов:</b> {stats['quiz_average']:.0f}%\n"
    
    # Прогресс до следующего уровня
    points = stats['points']
    if stats['level'] == "Новичок":
        next_level = "Ученик"
        needed = 50 - points
        if needed > 0:
            text += f"\n📈 <b>До уровня {next_level}:</b> {needed} очков"
    elif stats['level'] == "Ученик":
        next_level = "Продвинутый"
        needed = 200 - points
        if needed > 0:
            text += f"\n📈 <b>До уровня {next_level}:</b> {needed} очков"
    elif stats['level'] == "Продвинутый":
        next_level = "Эксперт"
        needed = 500 - points
        if needed > 0:
            text += f"\n📈 <b>До уровня {next_level}:</b> {needed} очков"
    elif stats['level'] == "Эксперт":
        text += f"\n🏆 <b>Ты достиг максимального уровня!</b>"
    
    # Мотивационная фраза
    if stats['lessons_completed'] == 0 and stats['scenarios_completed'] == 0:
        text += "\n\n💡 <b>Совет:</b> Начни с первого урока, чтобы заработать первые очки!"
    elif stats['lessons_completed'] < 4:
        text += "\n\n💡 <b>Совет:</b> Пройди все 4 урока, чтобы стать экспертом!"
    elif stats['scenarios_completed'] < 4:
        text += "\n\n💡 <b>Совет:</b> Попробуй все жизненные сценарии!"
    else:
        text += "\n\n🎉 <b>Ты молодец!</b> Продолжай в том же духе!"
    
    await message.answer(text, parse_mode="HTML", reply_markup=get_profile_keyboard())


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
По вопросам и предложениям: @support_bot

<b>📌 Версия бота:</b> 1.0.0
"""
    await message.answer(
        help_text,
        parse_mode="HTML",
        reply_markup=get_help_keyboard()
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


@router.message(F.text == "🏆 Рейтинг")
async def show_rating_from_menu(message: Message):
    """Показать рейтинг (вызывается из меню профиля)"""
    from core.db import get_top_users, get_user_stats
    
    top_users = await get_top_users(limit=10)
    
    if not top_users:
        await message.answer("Пока нет пользователей в рейтинге! Будь первым! 🏆")
        return
    
    text = "🏆 <b>Топ пользователей</b>\n\n"
    
    for i, user in enumerate(top_users, 1):
        medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else "📌"
        name = user.first_name or user.username or f"User_{user.telegram_id}"
        if len(name) > 20:
            name = name[:17] + "..."
        text += f"{medal} {i}. {name} — {user.points} ⭐\n"
    
    # Позиция текущего пользователя
    all_users = await get_top_users(limit=100)
    position = next(
        (i for i, u in enumerate(all_users, 1) if u.telegram_id == message.from_user.id), 
        None
    )
    
    if position:
        text += f"\n📌 <b>Твоя позиция:</b> {position}-е место"
        
        # Показываем, сколько очков до следующего места
        if position > 1 and position <= len(all_users):
            prev_user = all_users[position - 2]  # пользователь на позиции выше
            current_user = next((u for u in all_users if u.telegram_id == message.from_user.id), None)
            if current_user and prev_user:
                diff = prev_user.points - current_user.points
                if diff > 0:
                    text += f"\n📈 До {position-1}-го места: {diff} ⭐"
    else:
        # Пользователь не в топе
        current_user = await get_user_stats(message.from_user.id)
        if current_user:
            last_user = all_users[-1] if all_users else None
            if last_user:
                diff = last_user.points - current_user['points'] + 1
                if diff > 0:
                    text += f"\n📈 До попадания в топ-10: {diff} ⭐"
    
    await message.answer(text, parse_mode="HTML", reply_markup=get_back_keyboard())