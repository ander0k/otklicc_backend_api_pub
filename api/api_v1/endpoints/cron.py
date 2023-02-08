from fastapi import APIRouter, Depends, HTTPException, Request, status
from typing import Any,Optional
from enum import Enum
from core import config
import schemas
from schemas import CronConfig
from api import deps
import crud


router = APIRouter()


@router.get("/cfg/", response_model=CronConfig)
def get_cfg(*,
    request: Request,
    current_user: schemas.TokenData = Depends(deps.check_current_user),
) -> CronConfig:
    if not current_user.is_adm:
        raise HTTPException(status_code=config.EC_NOACCESS, detail=config.ER_NOACCESS)
    return crud.cron.get_cfg()


@router.put("/cfg/", response_model=CronConfig)
def put_cfg(*,
    request: Request,
    current_user: schemas.TokenData = Depends(deps.check_current_user),
    recom_working: Optional[bool] = None,
    recom_period_sec: Optional[int] = None,
    dedline_working: Optional[bool] = None,
    dedline_hour: Optional[int] = None,
    garbage_working: Optional[bool] = None,
    garbage_hour: Optional[int] = None,
) -> CronConfig:
    if not current_user.is_adm:
        raise HTTPException(status_code=config.EC_NOACCESS, detail=config.ER_NOACCESS)
    cfg = CronConfig(
        recom_period = recom_period_sec,
        recom_working = recom_working,
        dedline_hour = dedline_hour,
        dedline_working = dedline_working,
        garbage_hour = garbage_hour,
        garbage_working = garbage_working,
    )
    return crud.cron.put_cfg(cfg=cfg)


class TCronFunc(str, Enum):
    recomends = 'recomends'
    dedline = 'dedline'
    garbage= 'garbage'


@router.post("/exec_one/{cron_func}/", response_model=None)
async def post_mail(*,
    request: Request,
    current_user: schemas.TokenData = Depends(deps.check_current_user),
    cron_func: TCronFunc = None
)-> None:
    '''
    однократная рассылка рекомендаций
    '''
    if not current_user.is_adm:
        raise HTTPException(status_code=config.EC_NOACCESS, detail=config.ER_NOACCESS)
    if cron_func == TCronFunc.recomends:
        await crud.crud_cron.cron_recomends(force=True)
    if cron_func == TCronFunc.dedline:
        await crud.crud_cron.cron_dedline(force=True)
    if cron_func == TCronFunc.garbage:
        await crud.crud_cron.cron_garbage(force=True)
