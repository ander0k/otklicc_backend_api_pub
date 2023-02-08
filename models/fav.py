import sqlalchemy
import sqlalchemy.dialects.postgresql as postgres_dialect
from db.base_class import Base
from sqlalchemy import Column, ForeignKeyConstraint, UniqueConstraint, Index
from sqlalchemy.orm import relationship
from sqlalchemy.schema import FetchedValue

class Fav(Base):
    __tablename__ = 'fav'
    id = Column(postgres_dialect.UUID,primary_key=True,server_default=FetchedValue())
    owner = Column(postgres_dialect.UUID,server_default=FetchedValue())
    apply_time = Column(postgres_dialect.TIMESTAMP,server_default=FetchedValue())
    name = Column(postgres_dialect.TEXT,nullable=False, server_default=FetchedValue())
    professions = Column(postgres_dialect.TEXT,nullable=True, server_default=FetchedValue())
    parent_professions = Column(postgres_dialect.TEXT,nullable=True, server_default=FetchedValue())
    company = Column(postgres_dialect.TEXT,nullable=True, server_default=FetchedValue())
    parent_company = Column(postgres_dialect.TEXT,nullable=True, server_default=FetchedValue())
    geos = Column(postgres_dialect.TEXT,nullable=True, server_default=FetchedValue())
    parent_geos = Column(postgres_dialect.TEXT,nullable=True, server_default=FetchedValue())
    experience = Column(postgres_dialect.TEXT,nullable=True, server_default=FetchedValue())
    deadline = Column(postgres_dialect.BOOLEAN,nullable=True, server_default=FetchedValue())
    popular = Column(postgres_dialect.BOOLEAN,nullable=True, server_default=FetchedValue())
