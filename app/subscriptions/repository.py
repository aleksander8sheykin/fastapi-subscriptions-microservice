# app/subscriptions/repository.py
from datetime import date
from typing import List, Optional
from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.subscriptions import schemas
from app.subscriptions.models import Subscription


class SubscriptionRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def _get_subscription_obj(self, subscription_id: UUID) -> Subscription:
        result = await self.session.execute(
            select(Subscription).where(Subscription.id == subscription_id)
        )
        return result.scalar_one_or_none()

    async def create(self, sub_in: schemas.SubscriptionCreate) -> schemas.SubscriptionOut:
        subscription = Subscription(**sub_in.model_dump())
        self.session.add(subscription)
        await self.session.commit()
        await self.session.refresh(subscription)
        return schemas.SubscriptionOut.model_validate(subscription)

    async def get(self, subscription_id: UUID) -> Optional[schemas.SubscriptionOut]:
        sub = await self._get_subscription_obj(subscription_id)
        if sub:
            return schemas.SubscriptionOut.model_validate(sub)
        return None

    async def update(
        self, subscription_id: UUID, sub_in: schemas.SubscriptionUpdate
    ) -> Optional[schemas.SubscriptionOut]:
        sub = await self._get_subscription_obj(subscription_id)
        if not sub:
            return None
        for field, value in sub_in.model_dump(exclude_unset=True).items():
            setattr(sub, field, value)
        await self.session.commit()
        await self.session.refresh(sub)
        return schemas.SubscriptionOut.model_validate(sub)

    async def delete(self, subscription_id: UUID) -> bool:
        sub = await self._get_subscription_obj(subscription_id)
        if not sub:
            return False
        await self.session.delete(sub)
        await self.session.commit()
        return True

    async def list_by_user(
        self,
        user_id: UUID,
        service_name: Optional[str] = None,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
    ) -> List[schemas.SubscriptionOut]:
        query = select(Subscription).where(Subscription.user_id == user_id)

        if service_name:
            query = query.where(Subscription.service_name == service_name)

        if start_date and end_date:
            query = query.where(Subscription.start_date.between(start_date, end_date))

        result = await self.session.execute(query)
        return [schemas.SubscriptionOut.model_validate(sub) for sub in result.scalars().all()]

    async def sum_by_user(
        self,
        user_id: UUID,
        service_name: Optional[str] = None,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
    ) -> int:
        query = select(func.sum(Subscription.price)).where(Subscription.user_id == user_id)

        if start_date and end_date:
            query = query.where(Subscription.start_date.between(start_date, end_date))
        if service_name:
            query = query.where(Subscription.service_name == service_name)

        result = await self.session.execute(query)
        return result.scalar() or 0
