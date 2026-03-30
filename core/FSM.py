from aiogram.fsm.storage.mongo import MongoStorage
from aiogram.fsm.state import default_state, State, StatesGroup
from core.db import MONGO_DB_URL

storage = MongoStorage.from_url(MONGO_DB_URL)

class UserStates(StatesGroup):
    """Состояния пользователя для обучения страхованию"""
    
    # Базовые состояния
    default = default_state
    
    # Регистрация и настройка
    waiting_for_age = State()          # Ожидание возраста
    waiting_for_experience = State()   # Опыт в страховании (новичок/продвинутый)
    waiting_for_interests = State()    # Интересы (какие темы интересны)
    
    # Обучение
    reading_lesson = State()            # Чтение урока
    answering_quiz = State()            # Ответ на вопрос теста
    playing_scenario = State()          # Прохождение сценария
    waiting_for_scenario_choice = State()  # Выбор варианта в сценарии
    
    # Обратная связь
    waiting_for_feedback = State()      # Оценка урока/сценария
    waiting_for_question = State()      # Задать вопрос эксперту
    
    # Профиль и настройки
    waiting_for_new_name = State()      # Изменение имени
    waiting_for_notification_time = State()  # Настройка времени уведомлений


class AdminStates(StatesGroup):
    """Состояния для админ-панели"""
    
    MENU = State()                       # Главное меню админа
    REQUEST = State()                    # Ожидание ввода запроса
    ACCEPT_LIST = State()                # Просмотр списка на подтверждение
    REJECT_LIST = State()                # Просмотр списка на отклонение
    WAIT_USER_ID = State()               # Ожидание ID пользователя
    WAIT_ADD_USER = State()              # Ожидание данных для добавления пользователя
    
    # Дополнительные состояния для страхование бота
    WAITING_BROADCAST = State()          # Рассылка сообщений
    WAITING_NEW_LESSON = State()         # Добавление нового урока
    WAITING_NEW_SCENARIO = State()       # Добавление нового сценария
    WAITING_EDIT_CONTENT = State()       # Редактирование контента


class QuizStates(StatesGroup):
    """Состояния для прохождения викторины"""
    
    IN_PROGRESS = State()                # Викторина в процессе
    WAITING_FOR_ANSWER = State()         # Ожидание ответа на вопрос
    SHOWING_RESULT = State()             # Показ результата после ответа
    COMPLETED = State()                  # Викторина завершена


class ScenarioStates(StatesGroup):
    """Состояния для прохождения сценариев"""
    
    CHOOSING_SCENARIO = State()          # Выбор сценария
    READING_SITUATION = State()          # Чтение ситуации
    WAITING_FOR_CHOICE = State()         # Ожидание выбора варианта
    SHOWING_RESULT = State()             # Показ результата выбора
    SHOWING_MORAL = State()              # Показ морали/вывода
    COMPLETED = State()                  # Сценарий завершен