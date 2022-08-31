### Пробный проект на FastAPI

#### Стек:
    Python 3.x
    FastAPI
    SQLAlchemy
    PostgreSQL

### Приложение предсталвяет из себя Аукцион быстрых ставок на лоты других пользователей
###### реализация не доведена до конечного результата (нет тестов и определения победителя)


### Запустите проект можно следующим образом
#### Скопировать проект
    git clone git@github.com:N4lkin/autction_FastAPI.git
или

    git clone https://github.com/N4lkin/autction_FastAPI.git


#### Установить зависимости
    pip3 install requirements.txt

#### Поднять базу
    docker-compose up -d
#### Выполнить миграции
    alembic upgrade head
#### Запустить сервер
    uvicorn --reload main:app