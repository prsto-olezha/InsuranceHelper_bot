#!/usr/bin/env python3

import asyncio
from core.logger import logger
from create_bot import bot, dp
from core.db import init_mongo_db

# Импорт всех роутеров
from scripts.handlers import router
from scripts.admin_handlers import router as admin_router
from scripts import menu
from scripts import lessons
from scripts import scenarios
from scripts import quiz
from scripts import profile

from core.models import UserModel, LessonModel, ScenarioModel, QuizModel, UserProgressModel, AchievementModel

mongo_models = [
    UserModel,
    LessonModel,
    ScenarioModel,
    QuizModel,
    UserProgressModel,
    AchievementModel,
]


async def main():
    dp.include_router(router)
    dp.include_router(admin_router)
    dp.include_router(menu.router)
    dp.include_router(lessons.router)
    dp.include_router(scenarios.router)
    dp.include_router(quiz.router)
    dp.include_router(profile.router)
    
    await init_mongo_db()
    await bot.delete_webhook(drop_pending_updates=True)
    logger.info("Bot successfully activated!")
    await dp.start_polling(bot)


async def on_startup():
    await asyncio.gather(asyncio.create_task(main()))


if __name__ == "__main__":
    try:
        asyncio.run(on_startup())
    except KeyboardInterrupt:
        logger.info("Bot deactivated!")
    except Exception as e:
        logger.error(f"Error: {e}")