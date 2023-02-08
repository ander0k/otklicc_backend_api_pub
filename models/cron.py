import sqlalchemy
import sqlalchemy.dialects.postgresql as postgres_dialect
from sqlalchemy.sql.schema import ColumnDefault
from db.base_class import Base
from sqlalchemy import Column
from sqlalchemy.schema import FetchedValue

class CronUser(Base):
    __tablename__ = 'v_notif_usr'
    user_id = Column(postgres_dialect.UUID,primary_key=True,server_default=FetchedValue())
    mailto = Column(postgres_dialect.TEXT,nullable=False, server_default=FetchedValue())
    user_code = Column(postgres_dialect.TEXT,nullable=False, server_default=FetchedValue())


class CronVac(Base):
    __tablename__ = 'v_notif_vacs'
    id = Column(postgres_dialect.UUID,primary_key=True,server_default=FetchedValue())
    user_id = Column(postgres_dialect.UUID,primary_key=False,server_default=FetchedValue())
    vac_code = Column(postgres_dialect.TEXT,nullable=False, server_default=FetchedValue())
    vac_title = Column(postgres_dialect.TEXT,nullable=False, server_default=FetchedValue())
    com_code = Column(postgres_dialect.TEXT,nullable=False, server_default=FetchedValue())
    com_name = Column(postgres_dialect.TEXT,nullable=False, server_default=FetchedValue())
    com_img = Column(postgres_dialect.TEXT,nullable=False, server_default=FetchedValue())



class CronVacDead(Base):
    __tablename__ = 'v_vac_deads'
    vac_id = Column(postgres_dialect.UUID,primary_key=True)
    deadline = Column(postgres_dialect.DATE)
    left_days = Column(postgres_dialect.INTEGER)
    mail_sended = Column(postgres_dialect.SMALLINT)
    vac_code = Column(postgres_dialect.TEXT)
    status = Column(postgres_dialect.INTEGER)
    vac_title = Column(postgres_dialect.TEXT)
    comp_code = Column(postgres_dialect.TEXT)
    comp_title = Column(postgres_dialect.TEXT)
    vac_owners = Column(postgres_dialect.TEXT)
