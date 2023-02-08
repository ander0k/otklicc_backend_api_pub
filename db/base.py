# Import all the models, so that Base has them before being
# imported by Alembic
from db.base_class import Base  # noqa
from models.item import Item  # noqa
from models.app_user import AppUser  # noqa
from models.vacancy import Vacancy  # noqa
