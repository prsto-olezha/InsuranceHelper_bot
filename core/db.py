from motor.motor_asyncio import AsyncIOMotorClient
from beanie import init_beanie
from core.config import MONGO_DB_CONNECT
from core.models import (
    UserModel, 
    LessonModel, 
    ScenarioModel, 
    QuizModel,
    UserProgressModel,
    AchievementModel
)

# mongo
MONGO_DB_URL = f"mongodb://{MONGO_DB_CONNECT['username']}:{MONGO_DB_CONNECT['password']}@{MONGO_DB_CONNECT['host']}:{MONGO_DB_CONNECT['port']}/"

async def init_mongo_db():
    """Инициализация MongoDB и Beanie с моделями"""
    client = AsyncIOMotorClient(MONGO_DB_URL, uuidRepresentation="standard")
    
    # Инициализируем Beanie со всеми моделями
    await init_beanie(
        database=client[MONGO_DB_CONNECT['db_Users']],
        document_models=[
            UserModel,
            LessonModel,
            ScenarioModel,
            QuizModel,
            UserProgressModel,
            AchievementModel
        ]
    )
    return client


# ========== ПОЛЬЗОВАТЕЛИ ==========

async def find_user_by_id(user_id: int) -> UserModel | None:
    """Найти пользователя по Telegram ID"""
    user = await UserModel.find_one(UserModel.telegram_id == user_id)
    return user


async def create_user(telegram_id: int, username: str, first_name: str, age: int = None) -> UserModel:
    """Создать нового пользователя"""
    user = UserModel(
        telegram_id=telegram_id,
        username=username,
        first_name=first_name,
        age=age,
        points=0,
        level="Новичок",
        completed_lessons=[],
        completed_scenarios=[],
        quiz_scores=[]
    )
    await user.insert()
    return user


async def update_user_age(telegram_id: int, age: int):
    """Обновить возраст пользователя"""
    user = await find_user_by_id(telegram_id)
    if user:
        user.age = age
        await user.save()
        return True
    return False


async def add_points(user_id: int, points: int):
    """Добавить очки пользователю"""
    user = await find_user_by_id(user_id)
    if user:
        user.points += points
        # Обновляем уровень на основе очков
        if user.points >= 500:
            user.level = "Эксперт"
        elif user.points >= 200:
            user.level = "Продвинутый"
        elif user.points >= 50:
            user.level = "Ученик"
        await user.save()
        return user.points
    return 0


async def complete_lesson(user_id: int, lesson_id: int, score: int = 10):
    """Отметить урок как пройденный"""
    user = await find_user_by_id(user_id)
    if user and lesson_id not in user.completed_lessons:
        user.completed_lessons.append(lesson_id)
        user.points += score
        await user.save()
        return True
    return False


async def complete_scenario(user_id: int, scenario_id: str, score: int = 20):
    """Отметить сценарий как пройденный"""
    user = await find_user_by_id(user_id)
    if user and scenario_id not in user.completed_scenarios:
        user.completed_scenarios.append(scenario_id)
        user.points += score
        await user.save()
        return True
    return False


async def get_user_stats(user_id: int) -> dict:
    """Получить статистику пользователя"""
    user = await find_user_by_id(user_id)
    if not user:
        return {}
    
    return {
        "points": user.points,
        "level": user.level,
        "lessons_completed": len(user.completed_lessons),
        "scenarios_completed": len(user.completed_scenarios),
        "quiz_average": sum(user.quiz_scores) / len(user.quiz_scores) if user.quiz_scores else 0,
        "total_actions": len(user.completed_lessons) + len(user.completed_scenarios)
    }

async def get_user_progress_by_lessons(telegram_id: int) -> dict:
    """Получить прогресс пользователя по урокам и сценариям"""
    user = await find_user_by_id(telegram_id)
    if not user:
        return {
            "completed": [],
            "scenarios": [],
            "bonus_received": False
        }
    
    return {
        "completed": user.completed_lessons,
        "scenarios": user.completed_scenarios,
        "bonus_received": getattr(user, 'bonus_received', False)
    }


async def award_bonus_for_all_lessons(telegram_id: int) -> bool:
    """Начислить бонус за прохождение всех уроков"""
    user = await find_user_by_id(telegram_id)
    if not user:
        return False
    
    if len(user.completed_lessons) >= 4 and not getattr(user, 'bonus_received', False):
        user.points += 50
        user.bonus_received = True
        await user.save()
        return True
    return False

# ========== УРОКИ ==========

async def get_all_lessons() -> list[LessonModel]:
    """Получить все уроки"""
    return await LessonModel.find_all().to_list()


async def get_lesson_by_id(lesson_id: int) -> LessonModel | None:
    """Получить урок по ID"""
    return await LessonModel.find_one(LessonModel.id == lesson_id)


async def create_lesson(title: str, content: str, order: int, quiz_id: int = None):
    """Создать новый урок"""
    lesson = LessonModel(
        title=title,
        content=content,
        order=order,
        quiz_id=quiz_id
    )
    await lesson.insert()
    return lesson


# ========== СЦЕНАРИИ ==========

async def get_all_scenarios() -> list[ScenarioModel]:
    """Получить все сценарии"""
    return await ScenarioModel.find_all().to_list()


async def get_scenario_by_id(scenario_id: str) -> ScenarioModel | None:
    """Получить сценарий по ID"""
    return await ScenarioModel.find_one(ScenarioModel.id == scenario_id)


async def create_scenario(title: str, description: str, options: list, moral: str, category: str):
    """Создать новый сценарий"""
    scenario = ScenarioModel(
        title=title,
        description=description,
        options=options,
        moral=moral,
        category=category
    )
    await scenario.insert()
    return scenario


# ========== ВИКТОРИНЫ ==========

async def get_quiz_by_id(quiz_id: int) -> QuizModel | None:
    """Получить викторину по ID"""
    return await QuizModel.find_one(QuizModel.id == quiz_id)


async def save_quiz_result(user_id: int, quiz_id: int, score: int, total: int):
    """Сохранить результат викторины"""
    user = await find_user_by_id(user_id)
    if user:
        percentage = (score / total) * 100
        user.quiz_scores.append(percentage)
        await user.save()
        
        # Начисляем бонусные очки за хороший результат
        if percentage >= 80:
            await add_points(user_id, 30)
        elif percentage >= 60:
            await add_points(user_id, 15)
        
        return True
    return False


# ========== АДМИН-ФУНКЦИИ ==========

async def get_all_users() -> list[UserModel]:
    """Получить всех пользователей"""
    return await UserModel.find_all().to_list()


async def get_user_count() -> int:
    """Получить количество пользователей"""
    return await UserModel.count()


async def get_top_users(limit: int = 10) -> list[UserModel]:
    """Получить топ пользователей по очкам"""
    return await UserModel.find_all().sort(-UserModel.points).limit(limit).to_list()


async def broadcast_to_all(message_text: str, exclude_admin: bool = True):
    """Рассылка сообщений всем пользователям (для админов)"""
    users = await get_all_users()
    return [user.telegram_id for user in users]