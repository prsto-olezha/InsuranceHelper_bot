from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
import core.config as config
from core.db import get_user_count, get_all_users
from core.keyboards.reply_keyboards import get_admin_keyboard, get_back_keyboard
import core.FSM as FSM

router = Router()


def is_admin(user_id: int) -> bool:
    """Проверка, является ли пользователь админом"""
    return user_id in config.ADMIN_IDS


@router.message(Command("admin"))
async def admin_panel(message: Message, state: FSMContext):
    """Админ-панель"""
    if not is_admin(message.from_user.id):
        await message.answer("⛔ У вас нет доступа к админ-панели!")
        return
    
    await state.set_state(FSM.AdminStates.MENU)
    
    stats_text = (
        "🔧 <b>Админ-панель</b>\n\n"
        f"📊 <b>Статистика бота:</b>\n"
        f"👥 Пользователей: {await get_user_count()}\n\n"
        "Выберите действие:"
    )
    
    await message.answer(stats_text, parse_mode="HTML", reply_markup=get_admin_keyboard())


@router.message(FSM.AdminStates.MENU, F.text == "📊 Статистика бота")
async def admin_stats(message: Message):
    """Показать статистику бота"""
    if not is_admin(message.from_user.id):
        return
    
    users = await get_all_users()
    total_points = sum(u.points for u in users)
    
    stats_text = (
        "📊 <b>Подробная статистика</b>\n\n"
        f"👥 Всего пользователей: <b>{len(users)}</b>\n"
        f"⭐ Всего очков: <b>{total_points}</b>\n"
        f"📈 Средний балл: <b>{total_points // len(users) if users else 0}</b>\n\n"
        f"🏆 <b>Топ-3:</b>\n"
    )
    
    top_users = sorted(users, key=lambda x: x.points, reverse=True)[:3]
    for i, user in enumerate(top_users, 1):
        name = user.first_name or user.username or str(user.telegram_id)
        stats_text += f"{i}. {name} — {user.points} ⭐\n"
    
    await message.answer(stats_text, parse_mode="HTML", reply_markup=get_admin_keyboard())


@router.message(FSM.AdminStates.MENU, F.text == "📨 Рассылка")
async def start_broadcast(message: Message, state: FSMContext):
    """Начать рассылку"""
    if not is_admin(message.from_user.id):
        return
    
    await state.set_state(FSM.AdminStates.WAITING_BROADCAST)
    await message.answer(
        "📨 <b>Рассылка сообщений</b>\n\n"
        "Отправь текст сообщения для рассылки всем пользователям.\n\n"
        "❌ Для отмены нажми /cancel",
        parse_mode="HTML",
        reply_markup=get_back_keyboard()
    )


@router.message(FSM.AdminStates.WAITING_BROADCAST, F.text)
async def send_broadcast(message: Message, state: FSMContext):
    """Отправить рассылку"""
    if not is_admin(message.from_user.id):
        return
    
    users = await get_all_users()
    text = message.text
    
    sent = 0
    for user in users:
        try:
            await message.bot.send_message(user.telegram_id, text)
            sent += 1
        except Exception:
            pass
    
    await message.answer(
        f"✅ Рассылка завершена!\n"
        f"📨 Отправлено: {sent} из {len(users)} пользователей",
        reply_markup=get_admin_keyboard()
    )
    await state.set_state(FSM.AdminStates.MENU)


@router.message(FSM.AdminStates.MENU, F.text == "🔙 Выход из админки")
async def exit_admin(message: Message, state: FSMContext):
    """Выход из админки"""
    from core.keyboards.reply_keyboards import get_main_menu_keyboard
    
    await state.set_state(FSM.UserStates.default)
    await message.answer(
        "👋 Вы вышли из админ-панели",
        reply_markup=get_main_menu_keyboard()
    )


@router.message(Command("cancel"))
async def cancel(message: Message, state: FSMContext):
    """Отмена текущего действия"""
    current_state = await state.get_state()
    
    if current_state is None:
        await message.answer("Нет активных действий для отмены")
        return
    
    await state.set_state(FSM.UserStates.default)
    from core.keyboards.reply_keyboards import get_main_menu_keyboard
    await message.answer(
        "❌ Действие отменено",
        reply_markup=get_main_menu_keyboard()
    )