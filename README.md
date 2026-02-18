# Интернет-магазин продуктов

## Описание


Это веб-приложение представляет собой интернет-магазин продуктов с REST API, разработанный на Django с использованием Django Rest Framework. Приложение позволяет пользователям просматривать категории и продукты, а также управлять своей корзиной покупок.

## Функциональные возможности

### Для неавторизованных пользователей:
- Просмотр всех категорий с подкатегориями
- Просмотр списка продуктов с информацией о каждом продукте

### Для авторизованных пользователей:
- Управление своей корзиной (добавление, изменение количества, удаление продуктов)
- Полная очистка корзины
- Просмотр содержимого своей корзины с подсчётом количества товаров и общей стоимости

### Администраторы могут:
- Создавать, редактировать и удалять категории и подкатегории
- Управлять продуктами (добавление, изменение, удаление)

## Технические особенности
- Авторизация по токену
- Пагинация для списков категорий и продуктов
- Swagger-документация API
- Тесты для основных функций
- Фикстуры для начальных данных 

## Установка и запуск

### Установка uv (если не установлен):

#### Linux/macOS:
```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

#### Windows:
```powershell
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### Создание виртуального окружения и установка зависимостей:

#### С использованием uv:
```bash
# Установка зависимостей
uv sync
```
#### Активация виртуального окружения
```bash
# Linux/macOS
source .venv/bin/activate
# Windows
.venv\Scripts\Activate.ps1
```

#### С использованием pip:
```bash
# Linux/macOS
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

# Windows
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### Создание .env файла:
В корне проекта создайте файл .env со следующим содержимым:
```env
# Настройки базы данных
DB_NAME=your_db_name
DB_USER=your_db_user_name
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=5432

# Настройки приложения
SECRET_KEY=your_django_secret_key
ALLOWED_HOSTS=127.0.0.1,localhost
DEBUG=True
```

### Установка и настройка PostgreSQL:
1. Установите PostgreSQL на вашу систему
2. Создайте базу данных:
```bash
# Linux/macOS
sudo -u postgres createdb your_db_name

# Windows
createdb -U postgres your_db_name
```
3. Убедитесь, что в файле .env указаны правильные параметры подключения к базе данных


## Запуск проекта:
1. Клонируйте репозиторий:
```bash
git clone https://github.com/SavinNik/Alfa_test_case
cd Ecosystem_Alfa_TC/
```

2. Выполните миграции:
```bash
python manage.py migrate
```

3. Загрузите фикстуры:
```bash
python manage.py loaddata category.json
python manage.py loaddata subcategory.json
python manage.py loaddata product.json
```

4. Создайте суперпользователя:
```bash
python manage.py createsuperuser
```

5. Запустите сервер:
```bash
python manage.py runserver
```

6. Войти в админ-панель
```bash
http://127.0.0.1:8000/admin
```

7. Для доступа к Swagger-документации перейдите по адресу:
```bash
http://127.0.0.1:8000/swagger/
```

## API Эндпоинты
- GET /api/categories/ - Список всех категорий с подкатегориями
- GET /api/products/ - Список всех продуктов
- POST /api/cart/add/ - Добавить продукт в корзину
- PUT /api/cart/change/ - Изменить количество продукта в корзине
- DELETE /api/cart/remove/ - Удалить продукт из корзины
- GET /api/cart/view/ - Просмотр содержимого корзины
- DELETE /api/cart/clear/ - Очистить корзину
- POST /api/auth/token/ - Получить токен авторизации

 
## Тестирование
Для запуска тестов выполните:
```bash
python manage.py pytest
```