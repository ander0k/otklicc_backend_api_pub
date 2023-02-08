from .crud_item import item
from .crud_app_user import app_user
from .crud_profile import profile
from .crud_company import company
from .crud_vacancy import vacancy
from .crud_vcn_response import vcn_response
from .crud_groups import group
from .crud_search import search
from .crud_scoring import scoring
from .crud_result import result
from .crud_feed import feed
from .crud_fav import fav
from .crud_cron import cron
from .crud_dbconfig import dbconfig

# For a new basic set of CRUD operations you could just do

# from .base import CRUDBase
# from models.item import Item
# from schemas.item import ItemCreate, ItemUpdate

# item = CRUDBase[Item, ItemCreate, ItemUpdate](Item)
