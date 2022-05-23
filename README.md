# api_yamdb
![yamdb_final](https://github.com/Keshail/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)

## Адрес проекта
http://0/admin

## Пример запроса
http://0/api/v1/titles/1/

## Описание
YAMDB собирает записи пользователей ввиде любых "жанров/категорий/тайтлов" , а также и их комментарии. Проект представляет собой web-приложение состоящие из 3-х контейнеров:
- База данных   **Postgresql**
- Само web-приложение на 2х Фреймворках  **Django и Django-rest-framework**
- И HTTP-сервер **NGINX**
> Запуск проекта осуществляется на **Docker**
##  Установка на Desktop
Для начала если у вас не присутствует **Docker**  , то его нужно установить , 
вот официальная ->[инструкция](https://docs.docker.com/engine/install/).
### Установка проекта:
-   Клонировать  [https://github.com/Keshail/infra_sp2](https://github.com/Keshail/infra_sp2)
-  Проверить 2 файла и это:
>   **Dockerfile**: проверить пути до локальных файлов и поправьте их, если это необходимо.
>   
>   **docker-compose.yaml**: в этом файле тоже проверить пути.


##  Развёртывание
-  Пересобирает  контейнеры и запускает их
>  ``` docker-compose up -d --build ```
- Остановка и удаление контейнеров с сохранением их образа
> Остановка -> ```docker-compose down ```

>Удаление контейнеров но с сейвом образов ->```docker-compose down -v ```
### Эти команды выполните по очереди:

``` docker-compose exec web python manage.py makemigrations ```
- создаёт  записи в бд
``` docker-compose exec web python manage.py migrate ``` 
- создаёт Admina
``` docker-compose exec web python manage.py createsuperuser``` 
- копирует статику в приложение
``` docker-compose exec web python manage.py collectstatic --no-input``` 
### Команда для инициализации данных
>```docker-compose run web python manage.py loaddata fixtures.json```

### API
>Документация описана в **redoc**

## Технологии
|   Язык   |                 Фреймворк                   |             БД                         | Проект для развертывания проектов |
|----------|---------------------------------------------|----------------------------------------|-----------------------------------|
|python 3.8|[django](https://www.djangoproject.com/)     |[posgresql](https://www.postgresql.org/)|[docker](https://www.docker.com/)  |          
|          |[drf](https://www.django-rest-framework.org/)|                                        |                                   |
## Автор - **KeNi**

