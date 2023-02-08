import datetime
import string
import time, utils
from crud import crud_cron

from fastapi import FastAPI, Request
from starlette.middleware.cors import CORSMiddleware

from api.api_v1.api import api_router
from core.config import settings
import random

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/2openapi.json",
    # docs_url=None,
    redoc_url=None,
)

# Set all CORS enabled origins
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

utils.init_settings() # читать настройки из TCDBINFO в config.settings


app.include_router(api_router, prefix=settings.API_V1_STR)
 

@app.middleware("http")
async def log_requests(request: Request, call_next):
    idem = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))

    print(f"[{datetime.datetime.now()}]: rid={idem} start request path={request.url.path}")
    content = '%s %s %s' % (request.method, request.url.path, request.headers)
    print(content)
    start_time = time.time()
    response = await call_next(request)
    process_time = (time.time() - start_time) * 1000
    formatted_process_time = '{0:.2f}'.format(process_time)
    print(
          f"[{datetime.datetime.now()}]: "
          f"rid={idem} completed_in={formatted_process_time}ms "
          f"status_code={response.status_code}")

    return response

@app.on_event("startup")
async def run_scheduler():
    crud_cron.StartCron()
