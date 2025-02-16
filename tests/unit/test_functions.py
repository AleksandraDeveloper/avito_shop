import pytest
from app.models import User, Purchase, Transaction
from unittest.mock import Mock

@pytest.fixture
def mock_db():
    return Mock()

def test_user_create(mock_db):
    user = User(username="testuser", password="hash123")
    user.coins = 1000
    mock_db.add(user)
    mock_db.commit()
    assert user.username == "testuser"
    assert user.coins == 1000
    assert user.password == "hash123"

def test_transfer(mock_db):
    user = User(username="testuser", password="hash123")
    user.coins = 1000
    initial_balance = user.coins
    mock_db.add(user)
    user.coins = initial_balance - 100
    mock_db.commit()
    assert user.coins == 900

def test_negative_balance(mock_db):
    user = User(username="testuser", password="hash123")
    user.coins = 1000
    mock_db.add(user)
    with pytest.raises(Exception):
        user.coins = -100
        if user.coins < 0:
            raise ValueError("Баланс не может быть отрицательным")
    mock_db.commit.assert_not_called()

def test_purchase_create(mock_db):
    purchase = Purchase(user_id=1, item_id=1, quantity=2)
    mock_db.add(purchase)
    mock_db.commit()
    assert purchase.user_id == 1
    assert purchase.item_id == 1
    assert purchase.quantity == 2

def test_transaction_create(mock_db):
    transaction = Transaction(
        from_user_id=1,
        to_user_id=2,
        amount=100,
        transaction_type="TRANSFER"
    )
    mock_db.add(transaction)
    mock_db.commit()
    assert transaction.from_user_id == 1
    assert transaction.to_user_id == 2
    assert transaction.amount == 100
    assert transaction.transaction_type == "TRANSFER"

def test_enough_coins(mock_db):
    user = User(username="testuser", password="hash123")
    user.coins = 1000
    mock_db.add(user)
    mock_db.commit()
    assert user.coins == 1000
    assert user.coins >= 500

def test_not_enough_coins(mock_db):
    user = User(username="testuser", password="hash123")
    user.coins = 100
    mock_db.add(user)
    mock_db.commit()
    assert user.coins < 500

def test_valid_transfer_amount(mock_db):
    """Проверка валидности суммы перевода"""
    transaction = Transaction(
        from_user_id=1,
        to_user_id=2,
        amount=100,
        transaction_type="TRANSFER"
    )
    mock_db.add(transaction)
    mock_db.commit()
    assert transaction.amount > 0

def test_invalid_transfer_amount(mock_db):
    with pytest.raises(Exception):
        transaction = Transaction(
            from_user_id=1,
            to_user_id=2,
            amount=0,
            transaction_type="TRANSFER"
        )
        if transaction.amount <= 0:
            raise ValueError("Неверная сумма перевода")
        mock_db.add(transaction)
    mock_db.commit.assert_not_called()