from datetime import date
from typing import List, Optional
from uuid import UUID

from sqlalchemy import func, or_, select, text
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

    def _base_query(
        self,
        user_id: UUID,
        service_name: Optional[str] = None,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
    ):
        query = select(Subscription)
        query = query.where(Subscription.user_id == user_id)

        if service_name:
            query = query.where(Subscription.service_name == service_name)

        if start_date:
            query = query.where(
                or_(Subscription.end_date >= start_date, Subscription.end_date.is_(None))
            )

        if end_date:
            query = query.where(Subscription.start_date <= end_date)

        return query

    async def list_by_user(
        self,
        user_id: UUID,
        service_name: Optional[str] = None,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
        limit: Optional[int] = None,
        offset: Optional[int] = None,
    ) -> List[schemas.SubscriptionOut]:
        query = self._base_query(user_id, service_name, start_date, end_date)
        query = query.limit(limit).offset(offset)

        result = await self.session.execute(query)
        return [schemas.SubscriptionOut.model_validate(sub) for sub in result.scalars().all()]

    async def sum_by_user(
        self,
        user_id: UUID,
        service_name: Optional[str] = None,
        start_date: Optional[date] = None,
        end_date: Optional[date] = None,
    ) -> int:
        filtered_subs = (
            self._base_query(user_id, service_name, start_date, end_date)
            .with_only_columns(
                Subscription.service_name,
                Subscription.price,
                Subscription.start_date,
                Subscription.end_date,
            )
            .subquery("filtered_subs")
        )

        series_sub = (
            select(
                filtered_subs.c.service_name,
                filtered_subs.c.price,
                func.generate_series(
                    func.date_trunc("month", filtered_subs.c.start_date),
                    func.date_trunc(
                        "month", func.coalesce(filtered_subs.c.end_date, func.current_date())
                    ),
                    text("interval '1 month'"),
                ).label("month"),
            )
            .select_from(filtered_subs)
            .subquery("series_sub")
        )

        per_service_month = (
            select(
                series_sub.c.month,
                series_sub.c.service_name,
                func.max(series_sub.c.price).label("max_price"),
            )
            .group_by(series_sub.c.month, series_sub.c.service_name)
            .subquery("per_service_month")
        )

        per_month_conditions = []
        if start_date:
            per_month_conditions.append(per_service_month.c.month >= start_date)
        if end_date:
            per_month_conditions.append(per_service_month.c.month <= end_date)

        max_per_month = (
            select(
                per_service_month.c.month,
                func.sum(per_service_month.c.max_price).label("service_max_price"),
            )
            .where(*per_month_conditions)
            .group_by(per_service_month.c.month)
            .subquery("max_per_month")
        )

        query = select(func.sum(max_per_month.c.service_max_price).label("total_sum"))
        result = await self.session.execute(query)
        return int(result.scalar() or 0)
