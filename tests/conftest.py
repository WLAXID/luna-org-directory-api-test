import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi.testclient import TestClient
from app.database import Base, get_db
from app.main import app

# Test database URL
TEST_DATABASE_URL = "sqlite:///./test.db"

# Create test database engine
engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

@pytest.fixture(scope="function")
def db_session():
    """Create a test database session."""
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)

@pytest.fixture(scope="function")
def client(db_session):
    """Create a test client."""
    def override_get_db():
        try:
            yield db_session
        finally:
            pass
    
    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()

@pytest.fixture
def api_key():
    """Test API key."""
    return "dev-api-key-12345"

@pytest.fixture
def auth_headers(api_key):
    """Authorization headers for tests."""
    return {"Authorization": f"Bearer {api_key}"}

# Test data fixtures to avoid hardcoded values
@pytest.fixture
def test_building_data():
    """Standard test building data."""
    return {
        "address": "г. Москва, ул. Ленина 1",
        "latitude": 55.7558,
        "longitude": 37.6173
    }

@pytest.fixture
def test_organization_name():
    """Standard test organization name."""
    return "ООО Рога и Копыта"

@pytest.fixture
def test_phone_number():
    """Standard test phone number."""
    return "+7 (495) 123-45-67"

@pytest.fixture
def test_activity_data():
    """Standard test activity data."""
    return {"name": "Еда", "level": 1}

@pytest.fixture
def test_building_spb_data():
    """Test building data for St. Petersburg."""
    return {
        "address": "г. Санкт-Петербург, ул. Невский 1",
        "latitude": 59.9343,
        "longitude": 30.3351
    }

@pytest.fixture
def test_activity_tree_data():
    """Test activity tree structure data."""
    return {
        "root": {"name": "Еда", "level": 1},
        "children": [
            {"name": "Молочная продукция", "level": 2},
            {"name": "Мясная продукция", "level": 2}
        ]
    }