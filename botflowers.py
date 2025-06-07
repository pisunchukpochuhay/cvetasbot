импорт асинсио
импорт лесозаготовка
импорт мультипроцессинг
из айограмма импорт Бот, Диспетчер, типы
из айограмма.фильтры импорт Командование
из айограмма.исключения импорт TelegramAPIError, TelegramConflictError
Из типы айогремм импорт InlineKeyboardMarkup, InlineKeyboardButton
из колорама импорт Фор, Стиль, инициализация

# Иноциализазация колорама
инициализация(автоустановка=Правда)

# Настройка логирования
лесозаготовка.базовыйКонфиг(формат='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
 уровень=лесозаготовка.ИНФОРМАЦИЯ)
регистратор = ведение журнала.getLogger(__имя__)

# Сообщение, которое будет отправляться при нажатии кнопки /start
start_message = (
    "Обро пожаловть в \"Уфлор\"\n"
    "Премиальная доставка свежих букетов\n\n"
    "Почему именно мы?\н"
    "🌵 10 лет на рынке\n"
    "🌵 Более 20 поставщиков\n"
    "🌵 Максимальное качество и свежесть всех цветов\n\n"
    "Наши преимущества:\n"
    "💐 Быстрая и бесплатная доставка\n"
    "💐 Бонусы с каждой покупки\n"
    "💐 Забота о каждом клиенте\n"
    "💐 Широкий ассортимент\n\n"
    "Для заказа букета переходите по ссылке 🥰\n"
    "https://t.me/+9uWpi78dXfUwNDAy\n\n"
)

# Кнопки
кнопка1 = Встроенная кнопка клавиатуры(текст="🌹Каталог букетов, контакт для заказа🌹", url="https://t.me/+9uWpi78dXfUwNDAy")
кнопка2 = Встроенная кнопка клавиатуры(текст="🌸Наш официальный сайт с отзывами🌸", url="http://uflor.site")
клавиатура = InlineKeyboardMarkup(встроенная_клавиатура=[[кнопка1], [кнопка2]])

# Функция для обработки команды /старт
асинхронизация деф начинать(сообщение: типы.Сообщение):
 ждать сообщение.ответить(start_message, reply_markup=клавирата)

# Функция для запуска одного бота
асинхронизация деф запустить_бота(api_key: str, идс: int, nuda�шя_боты: свисок, удоенныыыыыыыыѵ_боты: наѱр):
 пока Правда:
 попробовать:
 бот = Бот(токен=api_key)
 дп = Диспетчер()
 дп.сообщение.регистрировать(начать, Командование(команды=['старт']))

            # Удаляем вебхук перед запуском долгого опроса
 ждать бот.удалить_вебхук(drop_pending_updates=Правда)

 регистратор.информация(ф"{Предний план.ЗЕЛЫЙ}Бт на лнии {иѴс + 1} с тотм {api_key} ициализиЀован успшно.{Стиль.СБРОСИТЬ_ВСЕ}")
 ждать дп.начать_опрос(бот)
 кроме TelegramConflictError:
 регистратор.ошибка(ф"{Пѵедний план.КРАСНЫЙ}Ошибка кфлита пр� запуске боЂа в токе {иѴс + 1} с токоном {api_key}: Север Телегамма говЀt - Кѽфлиt{Сь.СБРОСИТЬ_ВСЕ}")
 неудавшиеся_боты.добавить(api_key)  # Добавляем API ключ нерабочего бота в список
 кроме TelegramAPIError как е:
 если «Несанкционированный» в стр(e):
 регистратор.ошибка(ф"{Предний план.КРАСНЫЙ}НеЁанкционированная ошибка заѿуска боЂ� в стоке {иѴс + 1} с токоном {api_key}: {e}{СЂиѻь.СБРОСИТЬ_ВСЕ}")
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
