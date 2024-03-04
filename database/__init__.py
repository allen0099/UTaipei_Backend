import logging
import typing as t

from sqlalchemy import Engine
from sqlmodel import Session
from sqlmodel import SQLModel

from .common import _get_engine
from .common import _get_sql_url
from .models import *

logger: logging.Logger = logging.getLogger(__name__)

engine: Engine = _get_engine()


def get_session() -> t.Generator[Session, None, None]:
    with Session(engine) as session:
        yield session


def setup_database() -> None:
    logger.info("Creating database...")
    # SQLModel.metadata.create_all(engine)
