# app/subscriptions/models.py
from sqlalchemy import Column, String, Integer, Date
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import declarative_base
from uuid import uuid4

Base = declarative_base()

class Subscription(Base):
    __tablename__ = "subscriptions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid4)
    service_name = Column(String, nullable=False)
    price = Column(Integer, nullable=False)
    user_id = Column(UUID(as_uuid=True), nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=True)
