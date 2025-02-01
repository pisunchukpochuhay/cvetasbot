import asyncio
import logging
import multiprocessing
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.exceptions import TelegramAPIError, TelegramConflictError
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from colorama import Fore, Style, init

# Инициализация colorama
init(autoreset=True)

# Настройка логирования
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Сообщение, которое будет отправляться при нажатии кнопки /start
start_message = (
    "Добро пожаловать в \"Uflor\"\n"
    "Премиальная доставка свежих букетов\n\n"
    "Почему именно мы?\n"
    "🌵 10 лет на рынке\n"
    "🌵 Более 20 поставщиков\n"
    "🌵 Максимальное качество и свежесть всех цветов\n\n"
    "Наши преимущества:\n"
    "💐 Быстрая и бесплатная доставка\n"
    "💐 Бонусы с каждой покупки\n"
    "💐 Забота о каждом клиенте\n"
    "💐 Широкий ассортимент\n\n"
    "Для заказа букета переходите по ссылке 🥰\n"
    "https://t.me/+1tfHkcot7YxjY2Ri\n\n"
    "Оформить заказ вам поможет наш менеджер: Оксана⬇️\n"
    "@Oksana_dostavkacvetov\n"
)

# Кнопки
button1 = InlineKeyboardButton(text="🌹Заказать букет🌹", url="https://t.me/Oksana_dostavkacvetov")
button2 = InlineKeyboardButton(text="🌸Наш ассортимент🌸", url="https://t.me/+1tfHkcot7YxjY2Ri")
keyboard = InlineKeyboardMarkup(inline_keyboard=[[button1], [button2]])

# Функция для обработки команды /start
async def start(message: types.Message):
    await message.reply(start_message, reply_markup=keyboard)

# Функция для запуска одного бота
async def run_bot(api_key: str, index: int, failed_bots: list, deleted_bots: set):
    while True:
        try:
            bot = Bot(token=api_key)
            dp = Dispatcher()
            dp.message.register(start, Command(commands=['start']))

            # Удаляем вебхук перед запуском долгого опроса
            await bot.delete_webhook(drop_pending_updates=True)

            logger.info(f"{Fore.GREEN}Bot at line {index + 1} with token {api_key} initialized successfully.{Style.RESET_ALL}")
            await dp.start_polling(bot)
        except TelegramConflictError:
            logger.error(f"{Fore.RED}Conflict error starting bot at line {index + 1} with token {api_key}: Telegram server says - Conflict{Style.RESET_ALL}")
            failed_bots.append(api_key)  # Добавляем API ключ нерабочего бота в список
        except TelegramAPIError as e:
            if "Unauthorized" in str(e):
                logger.error(f"{Fore.RED}Unauthorized error starting bot at line {index + 1} with token {api_key}: {e}{Style.RESET_ALL}")
                if api_key not in deleted_bots:
                    with open('deletedBOT.txt', 'a') as file:
                        file.write(f"{api_key}\n")
                    deleted_bots.add(api_key)  # Добавляем API ключ нерабочего бота в множество
            else:
                logger.error(f"{Fore.RED}Error starting bot at line {index + 1} with token {api_key}: {e}{Style.RESET_ALL}")
                failed_bots.append(api_key)  # Добавляем API ключ нерабочего бота в список
        except Exception as e:
            logger.error(f"{Fore.RED}Unexpected error starting bot at line {index + 1} with token {api_key}: {e}{Style.RESET_ALL}")
            failed_bots.append(api_key)  # Добавляем API ключ нерабочего бота в список

        # Пауза на 24 часа перед следующим запросом
        await asyncio.sleep(86400)  # 86400 секунд = 24 часа

# Функция для запуска всех ботов
def run_bot_process(api_key, index, failed_bots, deleted_bots):
    asyncio.run(run_bot(api_key, index, failed_bots, deleted_bots))

def main():
    try:
        with open('api_keys.txt', 'r') as file:
            api_keys = file.readlines()
    except FileNotFoundError:
        logger.error("api_keys.txt file not found.")
        return
    except Exception as e:
        logger.error(f"Error reading api_keys.txt file: {e}")
        return

    manager = multiprocessing.Manager()
    failed_bots = manager.list()
    deleted_bots = manager.list()
    processes = []

    for index, api_key in enumerate(api_keys):
        api_key = api_key.strip()
        if api_key and api_key not in failed_bots:
            process = multiprocessing.Process(target=run_bot_process, args=(api_key, index, failed_bots, deleted_bots))
            process.start()
            processes.append(process)

    for process in processes:
        process.join()

    if failed_bots:
        logger.info(f"Failed to start bots with the following API keys: {failed_bots}")
    logger.info(f"All bots started successfully.")

if __name__ == '__main__':
    main()
