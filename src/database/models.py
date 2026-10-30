from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column

from src.database.database import Base

class ResearchPaper(Base):
    __tablename__ = "research_papers"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200), nullable=False)
    author: Mapped[str] = mapped_column(String(200), nullable=False)
    file_path: Mapped[str] = mapped_column(String(1000), unique=True, nullable=False)
    summary: Mapped[str] = mapped_column(Text, nullable=False)


__all__ = ["ResearchPaper"]