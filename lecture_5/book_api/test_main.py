import pytest
import anyio
from httpx import AsyncClient
from httpx import ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from database import Base
from main import app, get_db

# ---------------------------
# Test DB setup (in-memory)
# ---------------------------
SQLALCHEMY_TEST_DATABASE_URL = "sqlite+aiosqlite:///:memory:"
engine_test = create_async_engine(SQLALCHEMY_TEST_DATABASE_URL, future=True, echo=False)
TestingSessionLocal = async_sessionmaker(bind=engine_test, expire_on_commit=False, class_=AsyncSession)


# Override get_db dependency to use test DB
async def override_get_db():
    async with TestingSessionLocal() as session:
        yield session


app.dependency_overrides[get_db] = override_get_db


# ---------------------------
# Fixtures
# ---------------------------
@pytest.fixture(scope="module", autouse=True)
def prepare_db():
    """Create tables before tests and drop after."""
    async def setup():
        async with engine_test.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)

    async def teardown():
        async with engine_test.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
    anyio.run(setup)
    yield
    anyio.run(teardown)


@pytest.fixture
async def client(prepare_db):
    """HTTP client for testing with ASGI transport."""
    transport = ASGITransport(app=app)
    async with AsyncClient(transport=transport, base_url="http://testserver") as c:
        yield c


# ---------------------------
# Tests
# ---------------------------
@pytest.mark.anyio
async def test_create_book(client):
    response = await client.post("/books/", json={"title": "Test Book", "author": "John Doe", "year": 2023})
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Test Book"


@pytest.mark.anyio
async def test_read_books(client):
    response = await client.get("/books/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


@pytest.mark.anyio
async def test_read_book_by_id(client):
    create_resp = await client.post("/books/", json={"title": "Single Book", "author": "Alice", "year": 2022})
    book_id = create_resp.json()["id"]
    response = await client.get(f"/books/{book_id}")
    assert response.status_code == 200
    assert response.json()["id"] == book_id


@pytest.mark.anyio
async def test_update_book(client):
    create_resp = await client.post("/books/", json={"title": "Old Title", "author": "Bob", "year": 2020})
    book_id = create_resp.json()["id"]
    response = await client.put(f"/books/{book_id}", json={"title": "New Title"})
    assert response.status_code == 200
    assert response.json()["title"] == "New Title"


@pytest.mark.anyio
async def test_delete_book(client):
    create_resp = await client.post("/books/", json={"title": "Delete Me", "author": "Eve", "year": 2019})
    book_id = create_resp.json()["id"]
    response = await client.delete(f"/books/{book_id}")
    assert response.status_code == 200
    response_get = await client.get(f"/books/{book_id}")
    assert response_get.status_code == 404


@pytest.mark.anyio
async def test_search_books(client):
    await client.post("/books/", json={"title": "Search Me", "author": "Tester", "year": 2021})
    await client.post("/books/", json={"title": "Another One", "year": 2021})
    resp_title = await client.get("/books/search/?title=Search")
    assert any(b["title"] == "Search Me" for b in resp_title.json())
