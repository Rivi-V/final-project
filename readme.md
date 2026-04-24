# TeamFinder

TeamFinder — это веб-приложение для поиска команды и совместной работы над проектами.  
Пользователи могут создавать проекты, просматривать профили других участников, присоединяться к интересующим проектам и управлять своими данными через личный кабинет.

## Возможности проекта

- регистрация и авторизация пользователей по email и паролю;
- просмотр списка проектов на главной странице;
- создание, редактирование и завершение проектов;
- просмотр публичных профилей пользователей;
- редактирование собственного профиля;
- добавление проектов в избранное;
- участие в проектах других пользователей;
- пагинация списков проектов и пользователей;
- административное управление пользователями и проектами через Django admin.

## Технологический стек

- Python 3.12
- Django
- PostgreSQL
- Docker / Docker Compose
- HTML, CSS, JavaScript
- Pillow
- python-decouple
- pytest

Точные версии зависимостей указаны в `requirements.txt`.

## Структура `.env`

Создайте файл `.env` в корне проекта и заполните его по примеру `.env_example`.

Пример содержимого:

```env
DJANGO_SECRET_KEY=your-secret-key
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1
POSTGRES_DB=teamfinder
POSTGRES_USER=teamfinder_user
POSTGRES_PASSWORD=teamfinder_password
POSTGRES_HOST=db
POSTGRES_PORT=5432
```

### Назначение переменных окружения

- `DJANGO_SECRET_KEY` — секретный ключ Django;
- `DJANGO_DEBUG` — режим отладки (`True` или `False`);
- `DJANGO_ALLOWED_HOSTS` — список разрешённых хостов через запятую;
- `POSTGRES_DB` — имя базы данных PostgreSQL;
- `POSTGRES_USER` — пользователь PostgreSQL;
- `POSTGRES_PASSWORD` — пароль PostgreSQL;
- `POSTGRES_HOST` — хост базы данных;
- `POSTGRES_PORT` — порт базы данных.

## Запуск проекта через Docker Compose

1. Склонируйте репозиторий:
   ```bash
   git clone <ссылка_на_репозиторий>
   cd team-finder-ad-main-3
   ```

2. Создайте `.env` на основе примера:
   ```bash
   cp .env_example .env
   ```

   Для Windows:
   ```bash
   copy .env_example .env
   ```

3. Запустите контейнеры:
   ```bash
   docker compose up --build
   ```

4. Если миграции и заполнение тестовыми данными не выполняются автоматически, выполните:
   ```bash
   docker compose exec web python manage.py migrate
   docker compose exec web python manage.py seed_demo_data
   ```

5. Проект будет доступен по адресу:
   `http://localhost:8000`

6. Админ-панель:
   `http://localhost:8000/admin/`

### Остановка контейнеров

```bash
docker compose down
```

### Остановка с удалением томов

```bash
docker compose down -v
```

## Локальный запуск без Docker

1. Создайте виртуальное окружение:
   ```bash
   python -m venv venv
   ```

2. Активируйте его.

   Windows:
   ```bash
   venv\Scripts\activate
   ```

   Linux / macOS:
   ```bash
   source venv/bin/activate
   ```

3. Установите зависимости:
   ```bash
   pip install -r requirements.txt
   ```

4. Создайте и заполните `.env`.

5. Примените миграции:
   ```bash
   python manage.py migrate
   ```

6. Загрузите тестовые данные:
   ```bash
   python manage.py seed_demo_data
   ```

7. Запустите сервер:
   ```bash
   python manage.py runserver
   ```

После запуска проект будет доступен по адресу:
`http://127.0.0.1:8000`

## Тестовые данные

В проекте предусмотрена команда для загрузки демонстрационных пользователей и проектов:

```bash
python manage.py seed_demo_data
```

При запуске через Docker:

```bash
docker compose exec web python manage.py seed_demo_data
```

## Проверка кода и тестов

Проверка стиля кода:

```bash
flake8 users projects team_finder
```

Запуск тестов:

```bash
pytest
```

или через Docker:

```bash
docker compose exec web python manage.py test
```