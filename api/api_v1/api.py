from fastapi import APIRouter

from api.api_v1.endpoints import items, login, utils, vacancy, ander_test, auth, profile,\
    company, groups, search, scoring, result, feed, fav, cron, dbconfig
from core import config

api_router = APIRouter()
api_router.include_router(auth.router, tags=["auth"])
api_router.include_router(cron.router, prefix="/cron", tags=["cron"])
api_router.include_router(dbconfig.router, prefix="/dbconfig", tags=["dbconfig"])
api_router.include_router(profile.router,prefix="/profile", tags=["profile"])
api_router.include_router(company.router,prefix="/company", tags=["company"])
api_router.include_router(vacancy.router, prefix="/vacancy", tags=["vacancy"])
api_router.include_router(groups.router, prefix="/groups", tags=["groups"])
api_router.include_router(search.router, prefix="/search", tags=["search"])
api_router.include_router(scoring.router, prefix="/scoring", tags=["scoring"])
api_router.include_router(result.router, prefix="/result", tags=["result"])
api_router.include_router(feed.router, prefix="/feed", tags=["feed"])
api_router.include_router(fav.router, prefix="/fav", tags=["fav"])

api_router.include_router(ander_test.router, prefix="/ander_test", tags=["ander_test"])
api_router.include_router(login.router, tags=["login"])
api_router.include_router(utils.router, prefix="/utils", tags=["utils"])
api_router.include_router(items.router, prefix="/items", tags=["items"])
