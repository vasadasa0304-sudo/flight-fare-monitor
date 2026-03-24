from datetime import datetime, timezone
from sqlalchemy import String, Numeric, DateTime, Integer
from sqlalchemy.orm import Mapped, mapped_column
from app.db.base import Base

class FareSnapshot(Base):
    __tablename__ = "fare_snapshots"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    origin: Mapped[str] = mapped_column(String(3), nullable=False)
    destination: Mapped[str] = mapped_column(String(3), nullable=False)
    departure_date: Mapped[str] = mapped_column(String(10), nullable=False)
    airline: Mapped[str] = mapped_column(String(10), nullable=True)
    cabin: Mapped[str] = mapped_column(String(20), nullable=True)
    price: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False)
    currency: Mapped[str] = mapped_column(String(3), nullable=False)
    fetched_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
