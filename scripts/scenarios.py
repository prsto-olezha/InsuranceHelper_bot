from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from core.keyboards.reply_keyboards import get_back_keyboard, get_main_menu_keyboard
from core.keyboards.inline_keyboards import get_scenario_buttons, get_scenario_choice_buttons
from core.replics import get_scenario
from core.db import add_points, complete_scenario
import core.FSM as FSM

router = Router()


@router.message(F.text == "🎮 Сценарии")
async def show_scenarios(message: Message, state: FSMContext):
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

👇 <b>Нажми на кнопку ниже, чтобы начать сценарий!</b>
"""
    await message.answer(
        scenarios_text,
        parse_mode="HTML",
        reply_markup=get_scenario_buttons()
    )


@router.callback_query(lambda c: c.data.startswith("scenario_"))
async def run_scenario(callback: CallbackQuery, state: FSMContext):
    """Запустить сценарий"""
    scenario_id = callback.data.replace("scenario_", "")
    scenario = get_scenario(scenario_id)
    
    if not scenario:
        await callback.answer("Сценарий не найден!")
        return
    
    await state.set_state(FSM.ScenarioStates.READING_SITUATION)
    await state.update_data(scenario_id=scenario_id)
    
    # Отправляем описание ситуации
    await callback.message.edit_text(
        f"<b>{scenario['title']}</b>\n\n"
        f"📖 <b>Ситуация:</b>\n{scenario['description']}\n\n"
        f"<b>Что ты выберешь?</b>",
        parse_mode="HTML"
    )
    
    # Отправляем варианты ответов
    for i, option in enumerate(scenario['options']):
        await callback.message.answer(
            f"{i+1}. {option['text']}",
            reply_markup=get_scenario_choice_buttons(scenario_id, i)
        )
    
    await callback.answer()


@router.callback_query(lambda c: c.data.startswith("choice_"))
async def handle_choice(callback: CallbackQuery, state: FSMContext):
    """Обработка выбора варианта в сценарии"""
    _, scenario_id, option_index = callback.data.split("_")
    option_index = int(option_index)
    scenario = get_scenario(scenario_id)
    
    if not scenario:
        await callback.answer("Ошибка!")
        return
    
    option = scenario['options'][option_index]
    
    await state.set_state(FSM.ScenarioStates.SHOWING_RESULT)
    
    # Отправляем результат выбора
    await callback.message.answer(
        f"<b>Твой выбор:</b> {option['text']}\n\n"
        f"<b>Результат:</b>\n{option['consequence']}\n\n"
        f"{scenario['moral']}",
        parse_mode="HTML"
    )
    
    # Начисляем баллы за правильный ответ
    if option.get('correct', False):
        await add_points(callback.from_user.id, option.get('points', 20))
        await complete_scenario(callback.from_user.id, scenario_id, option.get('points', 20))
        await callback.message.answer(
            f"🎉 <b>+{option.get('points', 20)} очков!</b> Ты принял правильное решение!",
            parse_mode="HTML"
        )
    elif option.get('points', 0) > 0:
        await add_points(callback.from_user.id, option['points'])
        await callback.message.answer(
            f"📚 <b>+{option['points']} очков за попытку!</b> Но есть вариант лучше — посмотри другие ответы.",
            parse_mode="HTML"
        )
    else:
        await callback.message.answer(
            f"😔 <b>{option.get('points', 0)} очков.</b> В следующий раз попробуй другой вариант!",
            parse_mode="HTML"
        )
    
    await state.set_state(FSM.ScenarioStates.COMPLETED)
    
    # Предлагаем попробовать другой сценарий
    await callback.message.answer(
        "🔄 <b>Хочешь попробовать другой сценарий?</b>\n\n"
        "Нажми /start или выбери '🎮 Сценарии' в меню.",
        parse_mode="HTML",
        reply_markup=get_back_keyboard()
    )
    
    await callback.answer()


@router.callback_query(lambda c: c.data == "back_to_menu")
async def back_to_menu(callback: CallbackQuery, state: FSMContext):
    """Вернуться в главное меню"""
    await state.set_state(FSM.UserStates.default)
    await callback.message.edit_text(
        "🏠 <b>Главное меню</b>",
        parse_mode="HTML",
        reply_markup=get_main_menu_keyboard()
    )
    await callback.answer()