from datetime import date
from typing import List, Optional
from uuid import UUID

from fastapi import Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_db_session
from app.subscriptions import schemas
from app.subscriptions.repository import SubscriptionRepository
from app.utils.date import parse_month_year


def get_repository(
    session: AsyncSession = Depends(get_db_session),
) -> SubscriptionRepository:
    return SubscriptionRepository(session)


def start_date_query(
    start_date: Optional[str] = Query(None, description="Month-Year MM-YYYY"),
) -> Optional[date]:
    if start_date is None:
        return None
    return parse_month_year(start_date)


def end_date_query(
    end_date: Optional[str] = Query(None, description="Month-Year MM-YYYY"),
) -> Optional[date]:
    if end_date is None:
        return None
    return parse_month_year(end_date)


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
        start_date: Optional[date] = Depends(start_date_query),
        end_date: Optional[date] = Depends(end_date_query),
        limit: Optional[int] = 10,
        offset: Optional[int] = 0,
        repo: SubscriptionRepository = Depends(get_repository),
    ) -> List[schemas.SubscriptionOut]:
        return await repo.list_by_user(user_id, service_name, start_date, end_date, limit, offset)

    async def sums(
        self,
        user_id: UUID,
        service_name: Optional[str] = None,
        start_date: Optional[date] = Depends(start_date_query),
        end_date: Optional[date] = Depends(end_date_query),
        repo: SubscriptionRepository = Depends(get_repository),
    ) -> dict:
        total = await repo.sum_by_user(user_id, service_name, start_date, end_date)
        return {"sum": total}
