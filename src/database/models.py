from sqlalchemy import String, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base

# in SQLAlchemy, a model is a py class that describes the structure of a database table.
class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))

    research_notes: Mapped[list["ResearchNote"]] = relationship(
        back_populates="user"
    )

class Category(Base):
    __tablename__ = "categories"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(100))

    research_notes: Mapped[list["ResearchNote"]] = relationship(
        back_populates="category"
    )

class ResearchNote(Base):
    __tablename__ = "research_notes"

    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String(200))

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"))

    user: Mapped[User] = relationship(
        back_populates="research_notes"
    )

    category: Mapped[Category] = relationship(
        back_populates="research_notes"
    )