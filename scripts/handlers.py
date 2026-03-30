from aiogram import Router, F
from aiogram.filters import CommandStart, Command
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from core.keyboards.reply_keyboards import get_main_menu_keyboard, get_age_keyboard
from core.keyboards.inline_keyboards import get_scenario_buttons
import core.FSM as FSM
from core.models import UserModel
import core.db as db
from core.logger import logger
import core.replics as repl

router = Router()


@router.message(CommandStart())
async def start(msg: Message, state: FSMContext):
    """Обработка команды /start"""
    user = await db.find_user_by_id(msg.from_user.id)
    
    if not user:
        # Новый пользователь — запрашиваем возраст
        await state.set_state(FSM.UserStates.waiting_for_age)
        await msg.answer(
            "🎉 <b>Привет! Я СтрахоГид!</b>\n\n"
            "Расскажи, сколько тебе лет?\n"
            "<i>Это поможет подобрать примеры под твой возраст.</i>",
            parse_mode="HTML",
            reply_markup=get_age_keyboard()
        )
    else:
        # Существующий пользователь
        await msg.answer(
            f"👋 <b>С возвращением, {user.first_name or user.username}!</b>\n\n"
            f"{repl.WELCOME_TEXT}",
            parse_mode="HTML",
            reply_markup=get_main_menu_keyboard()
        )
        await state.set_state(FSM.UserStates.default)


@router.message(FSM.UserStates.waiting_for_age, F.text.regexp(r'^\d+$'))
async def process_age(msg: Message, state: FSMContext):
    """Обработка возраста пользователя"""
    age = int(msg.text)
    
    if age < 11:
        await msg.answer(
            "😊 Тебе пока рановато. Возвращайся, когда подрастешь!\n\n"
            "А пока можешь почитать книги по финансовой грамотности.",
            parse_mode="HTML"
        )
        await state.clear()
        return
    
    if age > 25:
        await msg.answer(
            "👍 Отлично! Наш бот подойдет и взрослым, но контент адаптирован под подростков.",
            parse_mode="HTML"
        )
    
    # Сохраняем пользователя и возраст
    user = await db.create_user(
        telegram_id=msg.from_user.id,
        username=msg.from_user.username,
        first_name=msg.from_user.first_name,
        age=age
    )
    
    # Начисляем приветственные очки
    await db.add_points(msg.from_user.id, 10)
    
    await state.set_state(FSM.UserStates.default)
    
    await msg.answer(
        f"🎉 <b>Отлично, {msg.from_user.first_name}!</b>\n\n"
        f"Ты получил <b>+10 очков</b> за регистрацию!\n\n"
        f"{repl.WELCOME_TEXT}",
        parse_mode="HTML",
        reply_markup=get_main_menu_keyboard()
    )


@router.message(FSM.UserStates.waiting_for_age, F.text == "⏩ Пропустить")
async def skip_age(msg: Message, state: FSMContext):
    """Пропустить ввод возраста"""
    user = await db.create_user(
        telegram_id=msg.from_user.id,
        username=msg.from_user.username,
        first_name=msg.from_user.first_name,
        age=None
    )
    
    await db.add_points(msg.from_user.id, 5)
    await state.set_state(FSM.UserStates.default)
    
    await msg.answer(
        f"👍 <b>Хорошо, продолжим!</b>\n\n"
        f"Ты получил <b>+5 очков</b> за регистрацию!\n\n"
        f"{repl.WELCOME_TEXT}",
        parse_mode="HTML",
        reply_markup=get_main_menu_keyboard()
    )


@router.message(FSM.UserStates.waiting_for_age)
async def invalid_age(msg: Message):
    """Некорректный ввод возраста"""
    await msg.answer(
        "❓ Пожалуйста, введи возраст цифрами или выбери из кнопок!",
        reply_markup=get_age_keyboard()
    )