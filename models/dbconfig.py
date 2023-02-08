import sqlalchemy
import sqlalchemy.dialects.postgresql as postgres_dialect
from db.base_class import Base
from sqlalchemy import Column
from sqlalchemy.schema import FetchedValue

class Tcdbinfo(Base):
    __tablename__ = 'tcdbinfo'
    name = Column(postgres_dialect.TEXT,nullable=False,primary_key=True,server_default=FetchedValue())
    mask = Column(postgres_dialect.TEXT,nullable=True, server_default=FetchedValue())
    value = Column(postgres_dialect.TEXT,nullable=True, server_default=FetchedValue())
    tag = Column(postgres_dialect.INTEGER,nullable=True, server_default=FetchedValue())
