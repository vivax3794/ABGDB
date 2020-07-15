from loguru import logger

from .database import get_database
from .bot import Bot
from config_SECRET import TOKEN

# custom levels
logger.level("SPY", no=10, color="<yellow>")

if __name__ == "__main__":
    logger.info("starting bot")
    db = get_database()
    bot = Bot(db)
    bot.run(TOKEN)
