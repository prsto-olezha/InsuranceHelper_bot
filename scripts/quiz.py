from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from core.keyboards.reply_keyboards import get_back_keyboard, get_main_menu_keyboard
from core.keyboards.inline_keyboards import get_quiz_buttons
from core.db import add_points, save_quiz_result
from core.replics import get_quiz_questions
import core.FSM as FSM

router = Router()

# Хранилище временных данных пользователя для викторины
user_quiz_data = {}


@router.message(F.text == "📝 Тест")
async def start_quiz(message: Message, state: FSMContext):
    """Начать викторину"""
    await state.set_state(FSM.QuizStates.IN_PROGRESS)
    
    questions = get_quiz_questions()
    
    user_quiz_data[message.from_user.id] = {
        "current": 0,
        "score": 0,
        "total": len(questions),
        "questions": questions
    }
    
    await ask_question(message, state)


async def ask_question(message: Message, state: FSMContext):
    """Задать вопрос пользователю"""
    data = user_quiz_data.get(message.from_user.id)
    if not data or data["current"] >= data["total"]:
        await finish_quiz(message, state)
        return
    
    q = data["questions"][data["current"]]
    
    text = f"<b>🧠 Вопрос {data['current'] + 1} из {data['total']}</b>\n\n"
    text += f"<b>{q['question']}</b>\n\n"
    for i, opt in enumerate(q['options']):
        text += f"{i+1}. {opt}\n"
    
    await state.set_state(FSM.QuizStates.WAITING_FOR_ANSWER)
    await message.answer(
        text,
        parse_mode="HTML",
        reply_markup=get_quiz_buttons(data["current"], data["total"])
    )


@router.callback_query(FSM.QuizStates.WAITING_FOR_ANSWER, lambda c: c.data.startswith("quiz_"))
async def process_answer(callback: CallbackQuery, state: FSMContext):
    """Обработка ответа на вопрос"""
    _, q_idx, ans_idx = callback.data.split("_")
    q_idx = int(q_idx)
    ans_idx = int(ans_idx)
    
    data = user_quiz_data.get(callback.from_user.id)
    if not data:
        await callback.answer("Ошибка! Начни тест заново.")
        return
    
    q = data["questions"][data["current"]]
    is_correct = (ans_idx == q["correct"])
    
    if is_correct:
        data["score"] += 1
        response = f"✅ <b>Правильно!</b>\n\n{q['explanation']}"
    else:
        correct_text = q['options'][q['correct']]
        response = f"❌ <b>Неправильно!</b>\n\nПравильный ответ: {correct_text}\n\n{q['explanation']}"
    
    data["current"] += 1
    await callback.message.edit_text(response, parse_mode="HTML")
    await ask_question(callback.message, state)
    await callback.answer()


async def finish_quiz(message: Message, state: FSMContext):
    """Завершить викторину и показать результат"""
    data = user_quiz_data.pop(message.from_user.id, None)
    if not data:
        return
    
    score = data["score"]
    total = data["total"]
    percent = (score / total) * 100
    
    # Сохраняем результат
    await save_quiz_result(message.from_user.id, 1, score, total)
    
    # Бонусные очки
    bonus = 0
    if percent >= 80:
        bonus = 30
        medal = "🏆 Отлично!"
    elif percent >= 60:
        bonus = 15
        medal = "🎉 Хорошо!"
    else:
        medal = "📚 Неплохо, но стоит повторить уроки!"
    
    if bonus:
        await add_points(message.from_user.id, bonus)
    
    await state.set_state(FSM.UserStates.default)
    
    result_text = (
        f"<b>📊 Результаты теста</b>\n\n"
        f"Правильных ответов: <b>{score}/{total}</b>\n"
        f"Процент: <b>{percent:.1f}%</b>\n\n"
        f"{medal}\n"
    )
    
    if bonus:
        result_text += f"\n✨ Ты получил <b>+{bonus}</b> очков!"
    
    await message.answer(
        result_text,
        parse_mode="HTML",
        reply_markup=get_main_menu_keyboard()
    )


@router.callback_query(lambda c: c.data == "quit_quiz")
async def quit_quiz(callback: CallbackQuery, state: FSMContext):
    """Прервать викторину"""
    user_quiz_data.pop(callback.from_user.id, None)
    await state.set_state(FSM.UserStates.default)
    await callback.message.edit_text(
        "❌ Тест прерван! Возвращайся в любое время.",
        parse_mode="HTML",
        reply_markup=get_main_menu_keyboard()
    )
    await callback.answer()