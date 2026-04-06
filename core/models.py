from beanie import Document, Indexed
from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from enum import Enum

class UserLevel(str, Enum):
    NEWBIE = "Новичок"
    STUDENT = "Ученик"
    ADVANCED = "Продвинутый"
    EXPERT = "Эксперт"

class UserModel(Document):
    """Модель пользователя"""
    telegram_id: Indexed(int, unique=True)
    username: Optional[str] = None
    first_name: Optional[str] = None
    age: Optional[int] = None
    points: int = 0
    level: str = UserLevel.NEWBIE
    
    completed_lessons: List[int] = []      # ID пройденных уроков
    completed_scenarios: List[str] = []    # ID пройденных сценариев
    completed_quizzes: List[int] = []      # ID пройденных тестов (НОВОЕ)
    quiz_scores: List[float] = []          # Результаты тестов
    
    notification_enabled: bool = True
    notification_time: str = "18:00"
    bonus_received: bool = False
    
    registered_at: datetime = Field(default_factory=datetime.utcnow)
    last_active: datetime = Field(default_factory=datetime.utcnow)
    
    class Settings:
        name = "users"


class LessonModel(Document):
    """Модель урока"""
    id: int
    title: str
    content: str
    order: int  # Порядок прохождения
    quiz_id: Optional[int] = None  # ID связанной викторины
    image_url: Optional[str] = None
    video_url: Optional[str] = None
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Settings:
        name = "lessons"


class ScenarioOption(BaseModel):
    """Вариант ответа в сценарии"""
    text: str
    consequence: str
    points: int = 0
    is_correct: bool = False

class ScenarioModel(Document):
    """Модель сценария"""
    id: str  # phone, travel, bike и т.д.
    title: str
    description: str
    options: List[ScenarioOption]
    moral: str
    category: str  # "tech", "health", "travel", "property"
    image_url: Optional[str] = None
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Settings:
        name = "scenarios"


class QuizQuestion(BaseModel):
    """Вопрос викторины"""
    question: str
    options: List[str]
    correct_index: int
    explanation: str

class QuizModel(Document):
    """Модель викторины"""
    id: int
    title: str
    lesson_id: Optional[int] = None  # Связанный урок
    questions: List[QuizQuestion]
    passing_score: int = 70  # Проходной балл в процентах
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    class Settings:
        name = "quizzes"


class UserProgressModel(Document):
    """Прогресс пользователя по дням"""
    user_id: int
    date: str  # YYYY-MM-DD
    points_earned: int = 0
    lessons_completed: int = 0
    scenarios_completed: int = 0
    quiz_taken: bool = False
    
    class Settings:
        name = "user_progress"


class AchievementModel(Document):
    """Достижения"""
    id: str
    title: str
    description: str
    icon: str
    required_points: Optional[int] = None
    required_lessons: Optional[int] = None
    required_scenarios: Optional[int] = None
    
    class Settings:
        name = "achievements"