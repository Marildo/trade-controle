"""
 @author Marildo Cesar 22/04/2023
"""
from abc import ABC, abstractmethod

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class BaseConnection(ABC):

    def __init__(self):
        self._engine = create_engine(self._get_url(), echo=False)
        maker = sessionmaker(expire_on_commit=False)
        self._session = maker(bind=self._engine)

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def close(self):
        self.session.close()
        self.engine.dispose()

    @abstractmethod
    def _get_url(self) -> str:
        raise NotImplementedError

    @property
    def session(self):
        return self._session

    @property
    def engine(self):
        return self._engine
