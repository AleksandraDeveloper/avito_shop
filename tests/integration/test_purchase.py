import pytest
from app.models import User, Item, Purchase
from app.core.security import get_password

def test_purchase(client, db_session):
    user = User(
        username="buyer",
        password=get_password("testpass"),
        coins=1000
    )
    db_session.add(user)
    db_session.commit()
    
    item = db_session.query(Item).filter(Item.name == "pink-hoody").first()
    print(f"Item in database: {item}") 
    if item:
        print(f"Item price: {item.price}") 

    auth_response = client.post(
        "/api/auth",
        json={"username": "buyer", "password": "testpass"}
    )
    assert auth_response.status_code == 200
    token = auth_response.json()["token"]

    response = client.get(
        "/api/buy/pink-hoody",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 200
    user = db_session.query(User).filter(User.username == "buyer").first()
    assert user.coins == 500

def test_not_enough_coins(client, db_session):
    # Недостаточно монет
    user = User(
        username="poorbuyer",
        password=get_password("testpass"),
        coins=10
    )
    db_session.add(user)
    db_session.commit()

    # Авторизуемся и получаем токен
    auth_response = client.post(
        "/api/auth",
        json={"username": "poorbuyer", "password": "testpass"}
    )
    assert auth_response.status_code == 200
    token = auth_response.json()["token"]

    response = client.get(
        "/api/buy/pink-hoody",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    assert response.status_code == 400

@pytest.fixture(autouse=True)
def clean_users(db_session):
    yield
    db_session.query(Purchase).delete()
    db_session.query(User).delete()
    db_session.commit() 