### Название проекта
# Foodgram - Продуктовый помощник

### Статус
![main workflow](https://github.com/andresparraDC/foodgram-project-react/actions/workflows/main.yml/badge.svg)

### Краткое описание

Foodgram это ресурс для публикации рецептов.  
Пользователи могут создавать свои рецепты, читать рецепты других пользователей, подписываться на интересных авторов, добавлять лучшие рецепты в избранное, а также создавать список покупок и загружать его в pdf формате.

## Сайт
Сайт доступен по ссылке:
[https://stolovyana.ddns.net/](https://stolovyana.ddns.net/)

## Документация к API
API документация доступна по ссылке (создана с помощью redoc):
[https://stolovyana.ddns.net/api/docs/](https://stolovyana.ddns.net/api/docs/)

# Технологии в проекте
[![Python](https://img.shields.io/badge/-Python-464646?style=flat-square&logo=Python)](https://www.python.org/)
[![Django](https://img.shields.io/badge/-Django-464646?style=flat-square&logo=Django)](https://www.djangoproject.com/)
[![Django REST Framework](https://img.shields.io/badge/-Django%20REST%20Framework-464646?style=flat-square&logo=Django%20REST%20Framework)](https://www.django-rest-framework.org/)
[![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-464646?style=flat-square&logo=PostgreSQL)](https://www.postgresql.org/)
[![Nginx](https://img.shields.io/badge/-NGINX-464646?style=flat-square&logo=NGINX)](https://nginx.org/ru/)
[![gunicorn](https://img.shields.io/badge/-gunicorn-464646?style=flat-square&logo=gunicorn)](https://gunicorn.org/)
[![docker](https://img.shields.io/badge/-Docker-464646?style=flat-square&logo=docker)](https://www.docker.com/)
[![GitHub%20Actions](https://img.shields.io/badge/-GitHub%20Actions-464646?style=flat-square&logo=GitHub%20actions)](https://github.com/features/actions)
[![Yandex.Cloud](https://img.shields.io/badge/-Yandex.Cloud-464646?style=flat-square&logo=Yandex.Cloud)](https://cloud.yandex.ru/)

# Инструкции по запуску

* Склонировать репозиторий на локальную машину:
```bash
git clone https://github.com/andresparraDC/foodgram-project-react.git
cd foodgram-project-react
```

* Cоздать и активировать виртуальное окружение:

```bash
python -m venv env
```

```bash
source env/bin/activate
```

* Cоздайте файл `.env` в директории `/infra/` с содержанием:

```
SECRET_KEY=секретный ключ django
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
```

* Перейти в директирию и установить зависимости из файла requirements.txt:

```bash
cd backend/
pip install -r requirements.txt
```

* Выполните миграции:

```bash
python manage.py migrate
```

* Запустите сервер:
```bash
python manage.py runserver
```

## Запуск проекта в Docker контейнере
* Установите Docker.

Параметры запуска описаны в файлах `docker-compose.yml` и `nginx.conf` которые находятся в директории `infra/`.  
При необходимости добавьте/измените адреса проекта в файле `nginx.conf`

* Запустите docker compose:
```bash
docker-compose up -d --build
```  
  > После сборки появляются 3 контейнера:
  > 1. контейнер базы данных **db**
  > 2. контейнер приложения **web**
  > 3. контейнер web-сервера **nginx**
* Примените миграции:
```bash
docker-compose exec web python manage.py migrate
```
* Загрузите ингредиенты:
```bash
docker-compose exec web python manage.py load_csv
```

* Создайте администратора:
```bash
docker-compose exec web python manage.py createsuperuser
```
* Соберите статику:
```bash
docker-compose exec web python manage.py collectstatic --noinput
```

# Автор
[Фредди Андрес Парра](https://github.com/andresparraDC) - Python разработчик.
Студент факультета Бэкенд. Когорта 14+
