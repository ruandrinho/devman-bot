import requests
import os
import telegram
import time
import logging
from dotenv import load_dotenv

logger = logging.getLogger(__file__)


class TelegramLogsHandler(logging.Handler):

    def __init__(self, tg_bot, chat_id):
        super().__init__()
        self.chat_id = chat_id
        self.tg_bot = tg_bot

    def emit(self, record):
        log_entry = self.format(record)
        self.tg_bot.send_message(chat_id=self.chat_id, text=log_entry)


if __name__ == '__main__':
    load_dotenv()
    devman_token = os.getenv('DEVMAN_TOKEN')
    chat_id = int(os.getenv('TELEGRAM_CHAT_ID'))
    bot = telegram.Bot(token=os.getenv('TELEGRAM_BOT_TOKEN'))

    logging.basicConfig(
        level=logging.DEBUG,
        format='%(asctime)s %(levelname)s %(message)s'
    )
    logger.addHandler(TelegramLogsHandler(bot, chat_id))
    logger.info('Бот запущен')

    timestamp_to_request = ''
    sleep_before_repeat_request = 1

    while True:
        try:
            response = requests.get(
                'https://dvmn.org/api/long_polling/',
                headers={'Authorization': f'Token {devman_token}'},
                params={'timestamp': timestamp_to_request}
            )
            response.raise_for_status()
            devman_reviews = response.json()
            if devman_reviews['status'] == 'timeout':
                timestamp_to_request = devman_reviews['timestamp_to_request']
            elif devman_reviews['status'] == 'found':
                for attempt in devman_reviews['new_attempts']:
                    message = f'У вас проверили работу «{attempt["lesson_title"]}»\n\n'
                    if attempt['is_negative']:
                        message += 'К сожалению, в работе нашлись ошибки\n\n'
                    else:
                        message += 'Преподавателю всё понравилось, можно приступать к следующему уроку!\n\n'
                    message += attempt['lesson_url']
                logger.warning(message)
                timestamp_to_request = devman_reviews['last_attempt_timestamp']
        except requests.exceptions.ReadTimeout:
            pass
        except requests.exceptions.ConnectionError:
            time.sleep(sleep_before_repeat_request)
            sleep_before_repeat_request *= 2
        except Exception:
            logger.exception('Бот упал с ошибкой:')
