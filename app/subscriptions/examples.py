subscription_example_create = {
    "service_name": "Yandex Plus",
    "price": 100,
    "user_id": "550e8400-e29b-41d4-a716-446655440000",
    "start_date": "01-2025",
    "end_date": "12-2025",
}

subscription_example_update = {
    "service_name": "Yandex Plus",
    "price": 200,
    "start_date": "Дата в формате 02-2025",
    "end_date": "Дата в формате 11-2025",
}

subscription_example_out = {
    "id": "342201dd-6d0f-469b-9491-6c389065523f",
    **subscription_example_create,
}
