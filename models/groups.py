import sqlalchemy
import sqlalchemy.dialects.postgresql as postgres_dialect
from db.base_class import Base
from sqlalchemy import Column, ForeignKeyConstraint, UniqueConstraint, Index
from sqlalchemy.orm import relationship
from sqlalchemy.schema import FetchedValue

class Group(Base):
    """Datamodel for Groups
    модель групп (гео, тэги, профессии)
    """
    __tablename__ = 'grouptree'
    id = Column(postgres_dialect.UUID,primary_key=True,server_default=FetchedValue())
    id_own = Column(postgres_dialect.UUID,server_default=FetchedValue())
    grp_class = Column(postgres_dialect.TEXT,unique=False,index=True,nullable=False, server_default=FetchedValue())
    name = Column(postgres_dialect.TEXT,unique=False,index=True,nullable=False, server_default=FetchedValue())
    code = Column(postgres_dialect.TEXT,unique=False,index=True,nullable=False, server_default=FetchedValue())
    checked = Column(postgres_dialect.BOOLEAN,unique=False,index=True,nullable=False, server_default=FetchedValue())
    created = Column(postgres_dialect.TIMESTAMP(timezone=True),nullable=True,server_default=FetchedValue(),
        comment='[дата и] время создания записи'
    )
    updated = Column(postgres_dialect.TIMESTAMP(timezone=True),nullable=True,server_default=FetchedValue(),
        comment='[дата и] время изменения записи'
    )
    deleted = Column(postgres_dialect.TIMESTAMP(timezone=True),nullable=True,
        comment='признак и [дата и] время удаления записи, запись считается удалённой, если значение этого поля отлично от NULL'
    )
    last_db_user = Column(postgres_dialect.TEXT,nullable=True,server_default=FetchedValue(),
        comment='имя пользователя базы данных, внесшего последнее изменение записи'
    )
