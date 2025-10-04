import pytest
from httpx import AsyncClient
from sqlalchemy import text

from app.core.db import Base, async_session_maker, engine, get_db_session
from app.main import app

tables_recreated = False


@pytest.fixture(scope="function", autouse=True)
async def prepare_database():
    global tables_recreated
    async with engine.begin() as conn:
        if not tables_recreated:
            tables_recreated = True
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)
        else:
            table_names = ", ".join(table.name for table in reversed(Base.metadata.sorted_tables))
            await conn.execute(text(f"TRUNCATE TABLE {table_names} RESTART IDENTITY CASCADE"))
    yield
    await engine.dispose()


@pytest.fixture(scope="function")
async def async_client():
    async def override_get_db():
        async with async_session_maker() as session:
            yield session

    app.dependency_overrides[get_db_session] = override_get_db

    async with AsyncClient(app=app, base_url="http://testserver") as client:
        yield client

    app.dependency_overrides.clear()
