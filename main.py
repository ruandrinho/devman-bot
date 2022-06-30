import requests
import os
import telegram
from dotenv import load_dotenv

if __name__ == '__main__':
    load_dotenv()
    devman_token = os.getenv('DEVMAN_TOKEN')
    chat_id = int(os.getenv('TELEGRAM_CHAT_ID'))
    bot = telegram.Bot(token=os.getenv('TELEGRAM_BOT_TOKEN'))
    timestamp_to_request = ''
    
    while True:
        try:
            response = requests.get(
                'https://dvmn.org/api/long_polling/',
                headers={'Authorization': f'Token {devman_token}'},
                params={'timestamp': timestamp_to_request}
            )
            if response.json()['status'] == 'timeout':
                timestamp_to_request = response.json()['timestamp_to_request']
            elif response.json()['status'] == 'found':
                for attempt in response.json()['new_attempts']:
                    message = f'У вас проверили работу «{attempt["lesson_title"]}»\n\n'
                    if attempt['is_negative']:
                        message += 'К сожалению, в работе нашлись ошибки\n\n'
                    else:
                        message += 'Преподавателю всё понравилось, можно приступать к следующему уроку!\n\n'
                    message += attempt['lesson_url']
                bot.send_message(chat_id=chat_id, text=message)
                timestamp_to_request = response.json()['last_attempt_timestamp']
        except requests.exceptions.ReadTimeout:
            pass
        except requests.exceptions.ConnectionError:
            pass