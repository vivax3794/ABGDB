from .database import get_database
from .bot import Bot
from config_SECRET import TOKEN

if __name__ == "__main__":
    db = get_database()
    bot = Bot(db)
    bot.run(TOKEN)
