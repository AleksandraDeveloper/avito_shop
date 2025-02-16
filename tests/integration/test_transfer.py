import pytest
from app.models import User, Transaction
from app.core.security import get_password

def test_transfer(client, db_session):
    # Создаем отправителя с 1000 монетами
    sender = User(
        username="sender",
        password=get_password("testpass"),
        coins=1000
    )
    # Создаем получателя с 0 монетами
    receiver = User(
        username="receiver",
        password=get_password("testpass"),
        coins=0
    )
    db_session.add(sender)
    db_session.add(receiver)
    db_session.commit()

    # Авторизуемся за отправителя и получаем токен
    auth_response = client.post(
        "/api/auth",
        json={"username": "sender", "password": "testpass"}
    )
    assert auth_response.status_code == 200
    token = auth_response.json()["token"]

    # Отправляем 500 монет
    response = client.post(
        "/api/sendCoin",
        headers={"Authorization": f"Bearer {token}"},
        json={"toUser": "receiver", "amount": 500}
    )
    print(f"Transfer response: {response.status_code}")  # Отладка
    print(f"Response body: {response.json()}")  # Отладка
    assert response.status_code == 200

    # Проверяем балансы обоих пользователей
    sender = db_session.query(User).filter(User.username == "sender").first()
    receiver = db_session.query(User).filter(User.username == "receiver").first()
    assert sender.coins == 500  # 1000 - 500
    assert receiver.coins == 500  # 0 + 500

def test_insufficient_funds(client, db_session):
    # Создаем отправителя с малым количеством монет
    sender = User(
        username="poor_sender",
        password=get_password("testpass"),
        coins=100
    )
    receiver = User(
        username="receiver2",
        password=get_password("testpass"),
        coins=0
    )
    db_session.add(sender)
    db_session.add(receiver)
    db_session.commit()

    # Авторизуемся за отправителя
    auth_response = client.post(
        "/api/auth",
        json={"username": "poor_sender", "password": "testpass"}
    )
    assert auth_response.status_code == 200
    token = auth_response.json()["token"]

    # Пытаемся отправить больше монет, чем есть
    response = client.post(
        "/api/sendCoin",
        headers={"Authorization": f"Bearer {token}"},
        json={"toUser": "receiver2", "amount": 500}
    )
    print(f"Transfer response: {response.status_code}")  # Отладка
    print(f"Response body: {response.json()}")  # Отладка
    assert response.status_code == 400

def test_receiver_not_found(client, db_session):
    # Создаем только отправителя
    sender = User(
        username="sender2",
        password=get_password("testpass"),
        coins=1000
    )
    db_session.add(sender)
    db_session.commit()

    # Авторизуемся за отправителя
    auth_response = client.post(
        "/api/auth",
        json={"username": "sender2", "password": "testpass"}
    )
    assert auth_response.status_code == 200
    token = auth_response.json()["token"]

    # Пытаемся отправить монеты несуществующему пользователю
    response = client.post(
        "/api/sendCoin",
        headers={"Authorization": f"Bearer {token}"},
        json={"toUser": "nonexistent_user", "amount": 500}
    )
    print(f"Transfer response: {response.status_code}")  # Отладка
    print(f"Response body: {response.json()}")  # Отладка
    assert response.status_code == 400
    assert "Получатель не найден" in response.json()["detail"]

@pytest.fixture(autouse=True)
def clean_db(db_session):
    yield
    # Очищаем таблицы после каждого теста
    db_session.query(Transaction).delete()
    db_session.query(User).delete()
    db_session.commit() 