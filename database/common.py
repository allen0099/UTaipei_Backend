import logging

from sqlalchemy import Engine
from sqlmodel import create_engine

logger: logging.Logger = logging.getLogger(__name__)


def _get_sql_url() -> str:
    return "sqlite:///test.db"


def _get_engine() -> Engine:
    logger.info("Generating engine...")
    engine: Engine = create_engine(_get_sql_url())

    return engine
