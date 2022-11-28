# Проект yamdb_final
![Django-app workflow](https://github.com/mtedoradze/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)

## Описание проекта
Для проекта  API_yamdb настроен поток _Continuous Integration_ и _Continuous Deployment_, который включает:
* автоматический запуск тестов,
* обновление образов на Docker Hub,
* автоматический деплой на боевой сервер при пуше в главную ветку main,
* отправление сообщения в телеграм с отчетом об успешном деплое проекта.
Проект разворачивается в контейнере на основании образа на Docker Hub.
Проект собирает отзывы пользователей на произведения. Произведения делятся на категории: «Книги», «Фильмы», «Музыка».
Сами произведения в YaMDb не хранятся, здесь нельзя посмотреть фильм или послушать музыку.
Благодарные или возмущённые пользователи оставляют к произведениям текстовые отзывы и ставят произведению оценку в диапазоне от одного до десяти.

## Технологии в проекте:
Python 3.7, 
Django 3.2, 
Docker, 
Unicorn, 
Nginx,
DevOps (CI/CD)

## Шаблон наполнения env-файла:
См. файл .env.example

## Установка
1. Клонировать репозиторий и перейти в него в командной строке:
`git@github.com:mtedoradze/yamdb_final.git`
2. Cоздать и активировать виртуальное окружение:
`python3 -m venv env`
`source env/bin/activate`
3. Установить зависимости из файла requirements.txt:
`python3 -m pip install --upgrade pip`
`pip install -r requirements.txt`
4. Развернуть контейнеры в «фоновом режиме»:
`docker-compose up -d`
5. Выполнить миграции в контейнере web:
`docker-compose exec web python manage.py migrate`
6. Создать суперпользователь:
`docker-compose exec web python manage.py createsuperuser`
7. Собрать статику:
`docker-compose exec web python manage.py collectstatic —no-input `
8. Документация по проекту:
 [http://localhost:5000/redoc/](_http://localhost:5000/redoc/_)  

