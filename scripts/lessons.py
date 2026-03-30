from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from core.keyboards.reply_keyboards import get_lessons_menu_keyboard, get_back_keyboard
from core.keyboards.inline_keyboards import get_lesson_buttons
from core.replics import get_lesson
from core.db import get_user_stats, complete_lesson, add_points

router = Router()


@router.message(F.text == "📚 Уроки")
async def show_lessons(message: Message):
    """Показать меню уроков"""
    await message.answer(
        "📖 <b>Выбери урок:</b>\n\n"
        "Рекомендую проходить по порядку, но можно начать с любого!",
        reply_markup=get_lessons_menu_keyboard(),
        parse_mode="HTML"
    )


@router.message(F.text.startswith("📖 Урок"))
async def show_lesson(message: Message):
    """Показать конкретный урок"""
    text = message.text
    if "Урок 1" in text:
        lesson_id = 1
    elif "Урок 2" in text:
        lesson_id = 2
    elif "Урок 3" in text:
        lesson_id = 3
    elif "Урок 4" in text:
        lesson_id = 4
    else:
        await message.answer("Урок не найден!")
        return
    
    lesson = get_lesson(lesson_id)
    if lesson:
        await message.answer(
            f"📚 <b>{lesson['title']}</b>\n\n{lesson['content']}",
            parse_mode="HTML",
            reply_markup=get_lesson_buttons(lesson_id)
        )
        
        # Отмечаем урок как пройденный и начисляем очки
        await complete_lesson(message.from_user.id, lesson_id, 10)
    else:
        await message.answer("Урок временно недоступен!")


@router.callback_query(lambda c: c.data.startswith("repeat_lesson_"))
async def repeat_lesson(callback: CallbackQuery):
    """Повторить урок"""
    lesson_id = int(callback.data.split("_")[2])
    lesson = get_lesson(lesson_id)
    
    if lesson:
        await callback.message.edit_text(
            f"📚 <b>{lesson['title']}</b>\n\n{lesson['content']}",
            parse_mode="HTML"
        )
        await callback.answer("Повторяй и запоминай! 📖")
    else:
        await callback.answer("Урок не найден!")


@router.callback_query(lambda c: c.data.startswith("next_lesson_"))
async def next_lesson(callback: CallbackQuery):
    """Следующий урок"""
    current_id = int(callback.data.split("_")[2])
    next_id = current_id + 1
    
    if next_id <= 4:
        lesson = get_lesson(next_id)
        if lesson:
            await callback.message.edit_text(
                f"📚 <b>{lesson['title']}</b>\n\n{lesson['content']}",
                parse_mode="HTML",
                reply_markup=get_lesson_buttons(next_id)
            )
            await complete_lesson(callback.from_user.id, next_id, 10)
            await callback.answer(f"Урок {next_id} начат!")
        else:
            await callback.answer("Следующий урок скоро появится!")
    else:
        await callback.answer("🎉 Поздравляю! Ты прошел все уроки!", show_alert=True)


@router.callback_query(lambda c: c.data == "show_scenarios")
async def show_scenarios_from_lesson(callback: CallbackQuery):
    """Показать сценарии из урока"""
    from core.keyboards.inline_keyboards import get_scenario_buttons
    
    await callback.message.edit_text(
        "🎮 <b>Выбери жизненную ситуацию:</b>",
        parse_mode="HTML",
        reply_markup=get_scenario_buttons()
    )
    await callback.answer()