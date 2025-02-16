Avito Shop API

API для магазина мерча Avito.

## Установка и запуск

1. Клонируйте репозиторий:
```bash
git clone https://github.com/yourusername/merchshop.git
cd merchshop
```

2. Скопируйте `.env.example` в `.env` и заполните переменные окружения:

3. Запустите через Docker:
```bash
docker-compose up -d
```

## API Endpoints

- `POST /api/auth` - Аутентификация сотрудника

- `GET /api/info` - Информации о балансе и истории

- `GET /api/buy/{item}` - Покупка товара

- `POST /api/sendCoin` - Перевод монет другому сотруднику

## Тестирование

Запуск тестов:
```bash
# Все тесты
pytest

# Интеграционные тесты
pytest integration -v

# Юнит тесты
pytest unit -v
```