import uuid

import pytest


@pytest.mark.asyncio
async def test_update_subscription(async_client):
    payload = {
        "service_name": "Spotify",
        "price": 300,
        "user_id": str(uuid.uuid4()),
        "start_date": "09-2025",
    }
    create_resp = await async_client.post("/subscriptions/", json=payload)
    sub_id = create_resp.json()["id"]

    update_payload = {"service_name": "Spotify Premium", "price": 350, "start_date": "09-2025"}
    update_resp = await async_client.put(f"/subscriptions/{sub_id}", json=update_payload)
    assert update_resp.status_code == 200
    assert update_resp.json()["service_name"] == "Spotify Premium"
    assert update_resp.json()["price"] == 350


@pytest.mark.asyncio
async def test_delete_subscription(async_client):
    payload = {
        "service_name": "Apple Music",
        "price": 450,
        "user_id": str(uuid.uuid4()),
        "start_date": "10-2025",
    }
    create_resp = await async_client.post("/subscriptions/", json=payload)
    sub_id = create_resp.json()["id"]

    delete_resp = await async_client.delete(f"/subscriptions/{sub_id}")
    assert delete_resp.status_code == 200
    assert delete_resp.json()["message"] == "Subscription deleted"
    get_resp = await async_client.get(f"/subscriptions/{sub_id}")
    assert get_resp.status_code == 404


@pytest.mark.asyncio
async def test_list_subscriptions(async_client):
    user_id = str(uuid.uuid4())
    for service, price in [("Netflix", 500), ("Spotify", 300)]:
        await async_client.post(
            "/subscriptions/",
            json={
                "service_name": service,
                "price": price,
                "user_id": user_id,
                "start_date": "07-2025",
            },
        )

    list_resp = await async_client.get(
        f"/subscriptions/list/?user_id={user_id}&start_date=07-2025&end_date=07-2025"
    )
    assert list_resp.status_code == 200
    assert len(list_resp.json()) == 2

    list_resp = await async_client.get(
        f"/subscriptions/list/?user_id={user_id}&start_date=07-2025&end_date=07-2025&limit=1"
    )
    assert list_resp.status_code == 200
    assert len(list_resp.json()) == 1
    assert list_resp.json()[0]["service_name"] == "Netflix"

    list_resp = await async_client.get(
        f"/subscriptions/list/?user_id={user_id}&start_date=07-2025&end_date=07-2025&offset=1&limit=1"
    )
    assert list_resp.status_code == 200
    assert len(list_resp.json()) == 1
    assert list_resp.json()[0]["service_name"] == "Spotify"


@pytest.mark.asyncio
async def test_sum_subscriptions(async_client):
    user_id = str(uuid.uuid4())
    for service, price in [("Netflix", 500), ("Spotify", 200)]:
        await async_client.post(
            "/subscriptions/",
            json={
                "service_name": service,
                "price": price,
                "user_id": user_id,
                "start_date": "01-2025",
                "end_date": "12-2025",
            },
        )

    sum_resp = await async_client.get(
        f"/subscriptions/sum/?user_id={user_id}&start_date=02-2025&end_date=07-2025"
    )
    assert sum_resp.status_code == 200
    assert sum_resp.json()["sum"] == (500 + 200) * 6


@pytest.mark.asyncio
async def test_sum_subscriptions_with_same_service(async_client):
    user_id = str(uuid.uuid4())
    for service, price, start, end in [
        ("Spotify", 200, "01-2025", "12-2025"),
        ("Spotify", 100, "03-2025", "10-2025"),
    ]:
        await async_client.post(
            "/subscriptions/",
            json={
                "service_name": service,
                "price": price,
                "user_id": user_id,
                "start_date": start,
                "end_date": end,
            },
        )

    sum_resp = await async_client.get(
        f"/subscriptions/sum/?user_id={user_id}&start_date=02-2025&end_date=07-2025"
    )
    assert sum_resp.status_code == 200
    assert sum_resp.json()["sum"] == (200) * 6


@pytest.mark.asyncio
async def test_sum_subscriptions_with_empty_end(async_client):
    user_id = str(uuid.uuid4())
    await async_client.post(
        "/subscriptions/",
        json={
            "service_name": "Spotify",
            "price": 200,
            "user_id": user_id,
            "start_date": "01-2025",
        },
    )

    sum_resp = await async_client.get(
        f"/subscriptions/sum/?user_id={user_id}&start_date=01-2025&end_date=09-2025"
    )
    assert sum_resp.status_code == 200
    assert sum_resp.json()["sum"] == (200) * 9
