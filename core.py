from sqlalchemy import create_engine
from sqlalchemy.orm import Session as SQLAlchemySession


class Session:
    _instance = None
    _engine_string = "sqlite:///DB/DataBase.sqlite"
    _engine = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is not None:
            return cls._instance
        cls._engine = create_engine(cls._engine_string, echo=False)
        return super().__new__(cls, *args, **kwargs)

    def __enter__(self):
        self.session = SQLAlchemySession(self._engine)
        return self.session

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()
