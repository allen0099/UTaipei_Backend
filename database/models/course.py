from typing import Optional

from sqlmodel import Field, SQLModel


class Course(SQLModel):
    id: str
