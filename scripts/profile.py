from aiogram import Router, F
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
from core.keyboards.reply_keyboards import (
    get_back_keyboard, 
    get_main_menu_keyboard,
    get_profile_keyboard
)
from core.db import get_user_stats, get_top_users, get_user_progress_by_lessons
from core.replics import LESSONS
import core.FSM as FSM

router = Router()


@router.message(F.text == "🏆 Мой прогресс")
async def show_profile_menu(message: Message, state: FSMContext):
    """Показать главное меню профиля"""
    await state.set_state(FSM.UserStates.default)
    
    stats = await get_user_stats(message.from_user.id)
    
    if not stats or stats['points'] == 0:
        await message.answer(
            "👤 <b>Твой профиль</b>\n\n"
            "📊 Статистика пока пуста.\n\n"
            "🎯 <b>Как заработать первые очки?</b>\n"
            "• Пройди уроки в разделе 📚 Уроки\n"
            "• Попробуй сценарии в разделе 🎮 Сценарии\n"
            "• Проверь знания в разделе 📝 Тест\n\n"
            "💡 За каждый пройденный урок ты получишь +10 очков!\n"
            "💡 За правильное решение в сценарии до +20 очков!\n"
            "💡 За хороший результат теста до +30 очков!\n\n"
            "👇 <b>Начни обучение прямо сейчас!</b>",
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
    
    # Прогресс-бар
    if stats['level'] == "Новичок":
        progress = min(int(stats['points'] / 50 * 100), 100)
        next_level = "Ученик"
        needed = 50 - stats['points']
    elif stats['level'] == "Ученик":
        progress = min(int((stats['points'] - 50) / 150 * 100), 100)
        next_level = "Продвинутый"
        needed = 200 - stats['points']
    elif stats['level'] == "Продвинутый":
        progress = min(int((stats['points'] - 200) / 300 * 100), 100)
        next_level = "Эксперт"
        needed = 500 - stats['points']
    else:
        progress = 100
        next_level = "Максимум"
        needed = 0
    
    progress_bar = "█" * (progress // 10) + "░" * (10 - (progress // 10))
    
    text = (
        f"👤 <b>Твой профиль</b>\n\n"
        f"{level_emoji} <b>Уровень:</b> {stats['level']}\n"
        f"⭐ <b>Очки:</b> {stats['points']}\n"
        f"📊 <b>Прогресс:</b> [{progress_bar}] {progress}%\n"
    )
    
    if needed > 0:
        text += f"📈 <b>До уровня {next_level}:</b> {needed} очков\n\n"
    else:
        text += f"\n🏆 <b>Ты достиг максимального уровня!</b>\n\n"
    
    text += (
        f"📖 <b>Пройдено уроков:</b> {stats['lessons_completed']}/4\n"
        f"🎮 <b>Пройдено сценариев:</b> {stats['scenarios_completed']}/4\n"
    )
    
    if stats.get('quiz_average', 0) > 0:
        text += f"📊 <b>Средний результат тестов:</b> {stats['quiz_average']:.0f}%\n"
    
    # Мотивационная фраза
    if stats['lessons_completed'] == 0:
        text += "\n💡 <b>Совет:</b> Начни с первого урока в разделе 📚 Уроки!"
    elif stats['lessons_completed'] < 4:
        text += "\n💡 <b>Совет:</b> Продолжай проходить уроки, чтобы повысить уровень!"
    elif stats['scenarios_completed'] < 4:
        text += "\n💡 <b>Совет:</b> Попробуй все сценарии в разделе 🎮 Сценарии!"
    else:
        text += "\n🎉 <b>Ты молодец!</b> Поделись ботом с друзьями!"
    
    await message.answer(text, parse_mode="HTML", reply_markup=get_profile_keyboard())


@router.message(F.text == "📊 Моя статистика")
async def show_detailed_stats(message: Message, state: FSMContext):
    """Показать детальную статистику пользователя"""
    await state.set_state(FSM.UserStates.default)
    
    stats = await get_user_stats(message.from_user.id)
    
    if not stats or stats['points'] == 0:
        await message.answer(
            "📊 <b>Детальная статистика</b>\n\n"
            "У вас пока нет пройденных материалов.\n\n"
            "📚 Начните с первого урока в разделе 'Уроки'!",
            parse_mode="HTML",
            reply_markup=get_back_keyboard()
        )
        return
    
    # Получаем прогресс по каждому уроку
    lessons_progress = await get_user_progress_by_lessons(message.from_user.id)
    
    text = (
        f"📊 <b>Детальная статистика</b>\n\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"🏆 <b>Общая информация</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"⭐ <b>Всего очков:</b> {stats['points']}\n"
        f"📚 <b>Уровень:</b> {stats['level']}\n"
        f"🎯 <b>Всего действий:</b> {stats['total_actions']}\n\n"
    )
    
    if stats.get('quiz_average', 0) > 0:
        text += f"📝 <b>Средний балл тестов:</b> {stats['quiz_average']:.1f}%\n\n"
    
    text += (
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"📖 <b>Прогресс по урокам</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
    )
    
    # Отображаем каждый урок
    for lesson_id in range(1, 5):
        lesson = LESSONS.get(lesson_id, {})
        title = lesson.get('title', f'Урок {lesson_id}')
        # Сокращаем название
        if len(title) > 25:
            title = title[:22] + "..."
        
        is_completed = lesson_id in lessons_progress.get('completed', [])
        status = "✅" if is_completed else "⭕"
        text += f"{status} {title}\n"
    
    text += f"\n📊 <b>Прогресс:</b> {stats['lessons_completed']}/4 уроков\n"
    
    # Процент выполнения
    percent = int(stats['lessons_completed'] / 4 * 100)
    bar = "█" * (percent // 10) + "░" * (10 - (percent // 10))
    text += f"[{bar}] {percent}%\n\n"
    
    text += (
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"🎮 <b>Сценарии</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
    )
    
    scenarios_dict = {"phone": "Разбил телефон",
                      "travel": "Болезнь за границей",
                      "bike": "Украли велосипед",
                      "health": "Травма на тренировке"
                      }
    completed_scenarios = lessons_progress.get('scenarios', [])

    for i, name in enumerate(scenarios_dict):
        status = "✅" if name in completed_scenarios else "⭕"
        text += f"{status} {scenarios_dict[name]}\n"

    text += f"\n📊 <b>Прогресс:</b> {stats['scenarios_completed']}/4 сценариев\n"
    
    # Процент выполнения
    percent = int(stats['scenarios_completed'] / 4 * 100)
    bar = "█" * (percent // 10) + "░" * (10 - (percent // 10))
    text += f"[{bar}] {percent}%\n\n"
    
    # Рекомендации
    text += f"\n━━━━━━━━━━━━━━━━━━━━\n"
    text += f"💡 <b>Рекомендации</b>\n"
    text += f"━━━━━━━━━━━━━━━━━━━━\n"
    
    if stats['lessons_completed'] < 4:
        next_lesson = stats['lessons_completed'] + 1
        text += f"📚 Пройди урок {next_lesson}, чтобы получить +10 очков!\n"
    elif stats['scenarios_completed'] < 4:
        text += f"🎮 Попробуй новые сценарии, чтобы заработать до +20 очков!\n"
    else:
        text += f"🎉 Ты прошел весь курс! Поделись ботом с друзьями!\n"
    
    await message.answer(text, parse_mode="HTML", reply_markup=get_back_keyboard())


@router.message(F.text == "📈 Прогресс по урокам")
async def show_lessons_progress(message: Message, state: FSMContext):
    """Показать подробный прогресс по каждому уроку"""
    await state.set_state(FSM.UserStates.default)
    
    stats = await get_user_stats(message.from_user.id)
    lessons_progress = await get_user_progress_by_lessons(message.from_user.id)
    
    if not stats or stats['points'] == 0:
        await message.answer(
            "📈 <b>Прогресс по урокам</b>\n\n"
            "Вы ещё не начали обучение!\n\n"
            "📚 Нажмите на кнопку 'Уроки' в главном меню и выберите первый урок.",
            parse_mode="HTML",
            reply_markup=get_back_keyboard()
        )
        return
    
    text = (
        "📈 <b>Прогресс по урокам</b>\n\n"
        "━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
    )
    
    # Детально по каждому уроку
    for lesson_id in range(1, 5):
        lesson = LESSONS.get(lesson_id, {})
        title = lesson.get('title', f'Урок {lesson_id}')
        is_completed = lesson_id in lessons_progress.get('completed', [])
        
        status = "✅ ПРОЙДЕН" if is_completed else "⭕ НЕ ПРОЙДЕН"
        
        text += f"\n<b>📖 Урок {lesson_id}: {title}</b>\n"
        text += f"   Статус: {status}\n"
        
        if is_completed:
            text += f"   🎁 Награда: +10 очков\n"
        else:
            text += f"   🎯 Начни урок, чтобы получить +10 очков!\n"
        
        text += "━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
    
    # Общая статистика
    completed = stats['lessons_completed']
    total = 4
    percent = int(completed / total * 100) if total > 0 else 0
    
    text += f"\n<b>📊 Общий прогресс:</b> {completed}/{total} уроков\n"
    
    # Прогресс-бар
    bar = "█" * (percent // 10) + "░" * (10 - (percent // 10))
    text += f"[{bar}] {percent}%\n\n"
    
    # Следующие шаги
    if completed < total:
        next_lesson = completed + 1
        text += f"💡 <b>Следующий шаг:</b>\n"
        text += f"   Перейди в раздел 'Уроки' и выбери 'Урок {next_lesson}'\n"
    else:
        text += f"🎉 <b>Поздравляю!</b> Ты прошел все уроки!\n"
        text += f"   Теперь можешь проверить знания в разделе 'Тест'!\n"
    
    # Бонус за все уроки
    if completed == 4 and lessons_progress.get('bonus_received', False) == False:
        text += f"\n🎁 <b>Бонус!</b> За прохождение всех уроков ты получаешь +50 очков!"
    
    await message.answer(text, parse_mode="HTML", reply_markup=get_back_keyboard())


@router.message(F.text == "🏆 Рейтинг")
async def show_rating(message: Message, state: FSMContext):
    """Показать рейтинг пользователей"""
    await state.set_state(FSM.UserStates.default)
    
    top_users = await get_top_users(limit=10)
    
    if not top_users:
        await message.answer(
            "🏆 <b>Рейтинг пользователей</b>\n\n"
            "Пока нет пользователей в рейтинге!\n\n"
            "🌟 Будь первым — начни обучение прямо сейчас!",
            parse_mode="HTML",
            reply_markup=get_back_keyboard()
        )
        return
    
    text = "🏆 <b>Рейтинг пользователей</b>\n\n"
    text += "━━━━━━━━━━━━━━━━━━━━\n"
    
    for i, user in enumerate(top_users, 1):
        medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else "📌"
        name = user.first_name or user.username or f"User_{user.telegram_id}"
        if len(name) > 20:
            name = name[:17] + "..."
        text += f"{medal} {i}. {name} — {user.points} ⭐\n"
    
    text += "━━━━━━━━━━━━━━━━━━━━\n"
    
    # Позиция текущего пользователя
    all_users = await get_top_users(limit=100)
    position = next(
        (i for i, u in enumerate(all_users, 1) if u.telegram_id == message.from_user.id), 
        None
    )
    
    current_stats = await get_user_stats(message.from_user.id)
    
    if position and current_stats and current_stats['points'] > 0:
        text += f"\n📌 <b>Твоя позиция:</b> {position}-е место"
        
        if position > 1 and position <= len(all_users):
            prev_user = all_users[position - 2]
            diff = prev_user.points - current_stats['points']
            if diff > 0:
                text += f"\n📈 До {position-1}-го места: {diff} ⭐"
    elif current_stats and current_stats['points'] > 0:
        text += f"\n📌 <b>Ты пока не в топе</b>\n"
        if all_users:
            last_user = all_users[-1]
            diff = last_user.points - current_stats['points'] + 1
            if diff > 0:
                text += f"📈 До попадания в топ-10: {diff} ⭐"
    
    text += f"\n\n💡 <b>Совет:</b> Проходи уроки и сценарии, чтобы заработать больше очков!"
    
    await message.answer(text, parse_mode="HTML", reply_markup=get_back_keyboard())