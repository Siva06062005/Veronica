from __future__ import annotations

import json
from datetime import datetime
from sqlalchemy import Boolean, DateTime, Integer, String, Text, create_engine, select
from sqlalchemy.orm import DeclarativeBase, Mapped, Session, mapped_column
from app.config import settings
from app.models.schemas import ActivityRecord


class Base(DeclarativeBase):
    pass


class PreferenceRow(Base):
    __tablename__ = "preferences"
    key: Mapped[str] = mapped_column(String(200), primary_key=True)
    value: Mapped[str] = mapped_column(Text)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)


class ActivityRow(Base):
    __tablename__ = "activity"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    timestamp: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    user_request: Mapped[str] = mapped_column(Text)
    intent: Mapped[str] = mapped_column(String(100))
    tool: Mapped[str | None] = mapped_column(String(100), nullable=True)
    arguments: Mapped[str] = mapped_column(Text, default="{}")
    risk: Mapped[str] = mapped_column(String(20))
    confirmation: Mapped[bool] = mapped_column(Boolean, default=False)
    success: Mapped[bool] = mapped_column(Boolean)
    result: Mapped[str] = mapped_column(Text)
    error: Mapped[str | None] = mapped_column(Text, nullable=True)


class MemoryStore:
    def __init__(self) -> None:
        self.engine = create_engine(f"sqlite:///{settings.data_dir / 'veronica.db'}")
        Base.metadata.create_all(self.engine)

    def set_preference(self, key: str, value: str) -> None:
        with Session(self.engine) as session:
            row = session.get(PreferenceRow, key)
            if row: row.value = value
            else: session.add(PreferenceRow(key=key, value=value))
            session.commit()

    def preferences(self) -> dict[str, str]:
        with Session(self.engine) as session:
            return {row.key: row.value for row in session.scalars(select(PreferenceRow)).all()}

    def forget(self, key: str | None = None) -> int:
        with Session(self.engine) as session:
            rows = session.scalars(select(PreferenceRow)).all() if key is None else [session.get(PreferenceRow, key)]
            count = 0
            for row in rows:
                if row is not None: session.delete(row); count += 1
            session.commit()
            return count

    def log(self, record: ActivityRecord) -> None:
        with Session(self.engine) as session:
            session.add(ActivityRow(timestamp=record.timestamp, user_request=record.user_request, intent=record.intent,
                tool=record.tool, arguments=json.dumps(record.arguments), risk=record.risk.value,
                confirmation=record.confirmation, success=record.success, result=record.result, error=record.error))
            session.commit()

    def activity(self, limit: int = 100) -> list[ActivityRecord]:
        with Session(self.engine) as session:
            rows = session.scalars(select(ActivityRow).order_by(ActivityRow.id.desc()).limit(limit)).all()
            return [ActivityRecord(id=r.id, timestamp=r.timestamp, user_request=r.user_request, intent=r.intent, tool=r.tool,
                arguments=json.loads(r.arguments), risk=r.risk, confirmation=r.confirmation, success=r.success,
                result=r.result, error=r.error) for r in rows]
