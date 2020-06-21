from src.database import get_database
from src.bot import Bot
from config_SECRET import TOKEN

if __name__ == "__main__":
    db = get_database()
    bot = Bot(db)
    bot.run(TOKEN)
