# app/subscriptions/schemas.py
from datetime import date
from uuid import UUID
from pydantic import BaseModel, Field, field_validator


class SubscriptionBase(BaseModel):
    service_name: str = Field(..., description="Название подписки или сервиса")
    price: int = Field(..., description="Стоимость подписки в рублях")
    start_date: date = Field(..., description="Дата начала подписки (месяц-год)")
    end_date: date | None = Field(None, description="Дата окончания подписки (если есть)")

    model_config = {
        'from_attributes': True
    }

    @field_validator("start_date", "end_date", mode="before")
    @classmethod
    def parse_month_year(cls, v):
        if isinstance(v, date):
            return v
        if isinstance(v, str):
            v = v.strip()
            try:
                month, year = map(int, v.split('-'))
                return date(year, month, 1)
            except Exception:
                raise ValueError(f"Invalid month-year format: {v!r}")
        return v


class SubscriptionCreate(SubscriptionBase):
    user_id: UUID = Field(..., description="ID пользователя, которому принадлежит подписка")

    model_config = {
        "json_schema_extra": {
            "example": {
                "service_name": "Yandex Plus",
                "price": 400,
                "start_date": "07-2025",
                "end_date": "12-2025",
                "user_id": "550e8400-e29b-41d4-a716-446655440000"
            }
        }
    }


class SubscriptionUpdate(SubscriptionBase):
    service_name: str | None = Field(None, description="Название подписки")
    price: int | None = Field(None, description="Стоимость подписки")
    start_date: date | None = Field(None, description="Дата начала")
    end_date: date | None = Field(None, description="Дата окончания")

    model_config = {
        "json_schema_extra": {
            "example": {
                "service_name": "Netflix",
                "price": 500,
                "start_date": "08-2025",
                "end_date": "09-2025"
            }
        }
    }


class SubscriptionOut(SubscriptionBase):
    id: UUID = Field(..., description="Уникальный идентификатор подписки")
    user_id: UUID = Field(..., description="ID пользователя")

    model_config = {
        "json_schema_extra": {
            "example": {
                "id": "123e4567-e89b-12d3-a456-426614174000",
                "service_name": "Yandex Plus",
                "price": 400,
                "start_date": "07-2025",
                "end_date": "12-2025",
                "user_id": "550e8400-e29b-41d4-a716-446655440000"
            }
        }
    }
