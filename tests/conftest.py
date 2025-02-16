import pytest
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from fastapi.testclient import TestClient
from app.main import app
from app.database import Base, get_db
from app.models import Item

TEST_DATABASE_URL = os.getenv("TEST_DATABASE_URL")

engine = create_engine(TEST_DATABASE_URL)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_test_db(db: Session):
    if not db.query(Item).first():
        items = [
            Item(name="t-shirt", price=80),
            Item(name="cup", price=20),
            Item(name="book", price=50),
            Item(name="pen", price=10),
            Item(name="powerbank", price=200),
            Item(name="hoody", price=300),
            Item(name="umbrella", price=200),
            Item(name="socks", price=10),
            Item(name="wallet", price=50),
            Item(name="pink-hoody", price=500)
        ]
        for item in items:
            db.add(item)
        db.commit()

@pytest.fixture(scope="function")
def db_session():
    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()
    init_test_db(session)
    try:
        yield session
    finally:
        session.rollback()
        session.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def client(db_session):
    def override_get_db():
        try:
            yield db_session
        finally:
            db_session.close()
    
    app.dependency_overrides[get_db] = override_get_db
    
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()