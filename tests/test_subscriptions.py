import pytest
from httpx import AsyncClient
from app.main import app
import uuid

@pytest.fixture(scope="module")
async def async_client():
    async with AsyncClient(app=app, base_url="http://testserver") as client:
        yield client

@pytest.mark.asyncio(loop_scope="session")
async def test_create_subscription(async_client):
    payload = {
        "service_name": "Yandex Plus",
        "price": 400,
        "user_id": str(uuid.uuid4()),
        "start_date": "07-2025"
    }
    response = await async_client.post("/subscriptions/", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["service_name"] == payload["service_name"]
    assert data["price"] == payload["price"]

@pytest.mark.asyncio(loop_scope="session")
async def test_get_subscription(async_client):
    payload = {
        "service_name": "Netflix",
        "price": 500,
        "user_id": str(uuid.uuid4()),
        "start_date": "08-2025"
    }
    create_resp = await async_client.post("/subscriptions/", json=payload)
    sub_id = create_resp.json()["id"]

    get_resp = await async_client.get(f"/subscriptions/{sub_id}")
    assert get_resp.status_code == 200
    assert get_resp.json()["service_name"] == "Netflix"

@pytest.mark.asyncio(loop_scope="session")
async def test_update_subscription(async_client):
    payload = {
        "service_name": "Spotify",
        "price": 300,
        "user_id": str(uuid.uuid4()),
        "start_date": "09-2025"
    }
    create_resp = await async_client.post("/subscriptions/", json=payload)
    sub_id = create_resp.json()["id"]

    update_payload = {
        "service_name": "Spotify Premium",
        "price": 350,
        "start_date": "09-2025"
    }
    update_resp = await async_client.put(f"/subscriptions/{sub_id}", json=update_payload)
    assert update_resp.status_code == 200
    assert update_resp.json()["service_name"] == "Spotify Premium"
    assert update_resp.json()["price"] == 350

@pytest.mark.asyncio(loop_scope="session")
async def test_delete_subscription(async_client):
    payload = {
        "service_name": "Apple Music",
        "price": 450,
        "user_id": str(uuid.uuid4()),
        "start_date": "10-2025"
    }
    create_resp = await async_client.post("/subscriptions/", json=payload)
    sub_id = create_resp.json()["id"]

    delete_resp = await async_client.delete(f"/subscriptions/{sub_id}")
    assert delete_resp.status_code == 200
    assert delete_resp.json()["message"] == "Subscription deleted"
    get_resp = await async_client.get(f"/subscriptions/{sub_id}")
    assert get_resp.status_code == 404

@pytest.mark.asyncio(loop_scope="session")
async def test_list_subscriptions(async_client):
    user_id = str(uuid.uuid4())
    for service, price in [("ServiceA", 100), ("ServiceB", 200)]:
        await async_client.post("/subscriptions/", json={
            "service_name": service,
            "price": price,
            "user_id": user_id,
            "start_date": "07-2025"
        })

    list_resp = await async_client.get(f"/subscriptions/list/?user_id={user_id}&start_date=07-2025&end_date=07-2025")
    assert list_resp.status_code == 200
    assert len(list_resp.json()) >= 2

@pytest.mark.asyncio(loop_scope="session")
async def test_sum_subscriptions(async_client):
    user_id = str(uuid.uuid4())
    for service, price in [("ServiceX", 150), ("ServiceY", 250)]:
        await async_client.post("/subscriptions/", json={
            "service_name": service,
            "price": price,
            "user_id": user_id,
            "start_date": "07-2025"
        })

    sum_resp = await async_client.get(f"/subscriptions/sum/?user_id={user_id}&start_date=07-2025&end_date=07-2025")
    assert sum_resp.status_code == 200
    assert sum_resp.json()["sum"] == 400
