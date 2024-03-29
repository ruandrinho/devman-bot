# devman-bot

Скрипт для получения новых проверок уроков через API Девмана и отправки уведомлений в Телеграм.

## Как установить

Клонируйте репозиторий или скачайте архив и распакуйте.

Создайте файл окружения `.env` и запишите в него ключ API Девмана, токен бота Telegram и ID телеграм-чата для уведомлений:
```sh
DEVMAN_TOKEN=
TELEGRAM_BOT_TOKEN=
TELEGRAM_CHAT_ID=
```

Python3 должен быть уже установлен. 
Затем используйте `pip` (или `pip3`, если есть конфликт с Python2) для установки зависимостей:
```sh
pip install -r requirements.txt
```

## Запуск скрипта
```sh
python main.py
```

## Запуск через контейнер

Установите Docker, если его ещё нет в вашей системе. Перейдите в папку проекта и последовательно выполните:
```sh
docker build -t devman-bot .
docker run --env-file .env devman-bot
```

## Деплой на Heroku

Скрипт полностью готов к деплою. 

Создайте новое приложение на Heroku, после чего в разделе Settings задайте те же Config Vars, что и для файла `.env`

Затем либо подключите приложение к своему репозиторию на вкладке Deploy, либо разместите контейнер через Docker командами:
```sh
heroku container:login
heroku container:push -a <your_app_name>
heroku container:release -a <your_app_name>
```

## Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).
