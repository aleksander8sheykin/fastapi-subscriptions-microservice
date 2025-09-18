# app/subscriptions/handlers.py
from typing import List, Optional
from uuid import UUID
from datetime import date

from fastapi import Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_db_session
from app.subscriptions.repository import SubscriptionRepository
from app.subscriptions import schemas


def get_repository(session: AsyncSession = Depends(get_db_session)) -> SubscriptionRepository:
    return SubscriptionRepository(session)


class SubscriptionHandler:
    async def create(
        self,
        sub: schemas.SubscriptionCreate,
        repo: SubscriptionRepository = Depends(get_repository),
    ) -> schemas.SubscriptionOut:
        return await repo.create(sub)

    async def get(
        self,
        subscription_id: UUID,
        repo: SubscriptionRepository = Depends(get_repository),
    ) -> schemas.SubscriptionOut:
        sub = await repo.get(subscription_id)
        if not sub:
            raise HTTPException(status_code=404, detail="Subscription not found")
        return sub

    async def update(
        self,
        subscription_id: UUID,
        sub: schemas.SubscriptionUpdate,
        repo: SubscriptionRepository = Depends(get_repository),
    ) -> schemas.SubscriptionOut:
        updated = await repo.update(subscription_id, sub)
        if not updated:
            raise HTTPException(status_code=404, detail="Subscription not found")
        return updated

    async def delete(
        self,
        subscription_id: UUID,
        repo: SubscriptionRepository = Depends(get_repository),
    ) -> dict:
        success = await repo.delete(subscription_id)
        if not success:
            raise HTTPException(status_code=404, detail="Subscription not found")
        return {"message": "Subscription deleted"}

    async def lists(
        self,
        user_id: UUID,
        service_name: Optional[str] = None,
        start: Optional[date] = None,
        end: Optional[date] = None,
        repo: SubscriptionRepository = Depends(get_repository),
    ) -> List[schemas.SubscriptionOut]:
        return await repo.list_by_user(user_id, service_name, start, end)

    async def sums(
        self,
        user_id: UUID,
        service_name: Optional[str] = None,
        start: Optional[date] = None,
        end: Optional[date] = None,
        repo: SubscriptionRepository = Depends(get_repository),
    ) -> dict:
        total = await repo.sum_by_user(user_id, service_name, start, end)
        return {"sum": total}
