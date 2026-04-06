import os
from dotenv import load_dotenv
#===============
load_dotenv()

TOKEN = os.getenv("BOT_TOKEN")

MONGO_DB_CONNECT = {
    'db_Users': os.getenv("MONGODB_DB_USERS"),
    'host': os.getenv("MONGODB_HOST_USERS"),
    'port': int(os.getenv("MONGODB_PORT_USERS")),
    'username': os.getenv("MONGODB_USERNAME_USERS"),
    'password': os.getenv("MONGODB_PASSWORD_USERS"),
}

# Админы (через запятую)
ADMIN_IDS = [int(id.strip()) for id in os.getenv("ADMIN_IDS", "").split(",") if id.strip()]