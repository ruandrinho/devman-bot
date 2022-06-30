import requests
import os
import telegram
import time
from dotenv import load_dotenv

if __name__ == '__main__':
    load_dotenv()
    devman_token = os.getenv('DEVMAN_TOKEN')
    chat_id = int(os.getenv('TELEGRAM_CHAT_ID'))
    bot = telegram.Bot(token=os.getenv('TELEGRAM_BOT_TOKEN'))
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
            decoded_response = response.json()
            if 'error' in decoded_response:
                raise requests.exceptions.HTTPError(decoded_response['error'])
            if decoded_response['status'] == 'timeout':
                timestamp_to_request = decoded_response['timestamp_to_request']
            elif decoded_response['status'] == 'found':
                for attempt in decoded_response['new_attempts']:
                    message = f'У вас проверили работу «{attempt["lesson_title"]}»\n\n'
                    if attempt['is_negative']:
                        message += 'К сожалению, в работе нашлись ошибки\n\n'
                    else:
                        message += 'Преподавателю всё понравилось, можно приступать к следующему уроку!\n\n'
                    message += attempt['lesson_url']
                bot.send_message(chat_id=chat_id, text=message)
                timestamp_to_request = decoded_response['last_attempt_timestamp']
        except requests.exceptions.ReadTimeout:
            pass
        except requests.exceptions.ConnectionError:
            time.sleep(sleep_before_repeat_request)
            sleep_before_repeat_request *= 2