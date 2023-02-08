from typing import Any, Dict, List, Optional
import threading
import utils,time
from models import CronUser, CronVac, CronVacDead
from sqlalchemy.orm import Session
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from db.session import SessionLocal
from apscheduler.job import Job
from core.config import settings
from schemas import CronConfig,vacancy
import utils

job_recom: Job = None
job_dedline: Job = None
job_garbage: Job = None
mtx_recom = threading.Lock()
mtx_dedline = threading.Lock()
mtx_garbage = threading.Lock()


def StartCron():
    sch = AsyncIOScheduler()
    sch.start()
    # Using max_instances=1 guarantees that only one job runs at the same time (in this event loop).
    global job_recom
    job_recom = sch.add_job(cron_recomends, 'interval',
                            seconds=settings.CRON_MAIL_PERIOD, max_instances=1)
    if not settings.CRON_MAIL_ON:
        job_recom.pause()

    global job_dedline
    job_dedline = sch.add_job(cron_dedline, 'cron', day_of_week='mon-sun',
                              hour=settings.CRON_DEDLINE_HOUR, minute="*", second="*", max_instances=1)
    if not settings.CRON_DEDLINE_ON:
        job_dedline.pause()

    global job_garbage
    job_garbage = sch.add_job(cron_garbage, 'cron', day_of_week='mon-sun',
                              hour=settings.CRON_GARBAGE_HOUR, minute="*", second="*", max_instances=1)
    if not settings.CRON_GARBAGE_ON:
        job_garbage.pause()


async def cron_recomends(force: bool = False):
    '''рассылка писем с рекомендациями по шедулеру'''
    if not force and not settings.CRON_MAIL_ON:
        return
    # print('!!!')
    with mtx_recom:
        db = SessionLocal()
        try:
            u: CronUser
            users = db.query(CronUser).limit(25).all()
            if not users:
                return
            print('>>>> cron_recomends >>>>', time.strftime("%H:%M:%S", time.localtime()))
            for u in users:
                vacs = db.query(CronVac).filter(CronVac.user_id == u.user_id)
                token = utils.create_access_token(
                    subject=u.user_id,
                    code=u.user_code,
                    utype='CUS',
                    email=u.mailto,
                )
                utils.send_recomend_email(
                    mailto=u.mailto,
                    token=token,
                    vacs=vacs,
                )
                qry = "update vcn_user set mail_sended = current_date where user_id = :user_id"
                db.execute(qry, {"user_id": u.user_id})
                db.commit()
        finally:
            db.close()
        print('<<<< cron_recomends <<<<')


async def cron_dedline(force: bool = False):
    '''рассылка писем о dedline'''
    if not force and not settings.CRON_DEDLINE_ON:
        return
    with mtx_dedline:
        db = SessionLocal()
        try:
            vacs: List = db.query(CronVacDead).order_by(CronVacDead.mail_sended).all()
            if not vacs:
                return
            print('>>>> cron_dedline >>>>')
            vac: CronVacDead
            for vac in vacs:
                if vac.left_days > 0 and vac.status != vacancy.STATUS_ARCHIVE:
                    # ---------- еще есть время и вакансия еще не в архиве
                    if vac.mail_sended == 0:  # --- и письмо не послано
                        # for email_to in vac.vac_owners.split(','):
                        utils.send_dedline_mail(  # --- send mail to HRs за 3 дня до смерти
                            email_to=vac.vac_owners,  # email_to,
                            vac_code=vac.vac_code,
                            vac_title=vac.vac_title,
                            comp_code=vac.comp_code,
                            comp_title=vac.comp_title,
                        )
                        vac.mail_sended = 1
                else:   #--- день смерти (или позже), прощальные письма не посланы
                    # for email_to in vac.vac_owners.split(','):
                    utils.send_vac_archive_mail(  # --- send mail to HRs
                        email_to=vac.vac_owners,  # email_to,
                        vac_code=vac.vac_code,
                        vac_title=vac.vac_title,
                        comp_code=vac.comp_code,
                        comp_title=vac.comp_title,
                    )
                    query = '''
                        select coalesce(sum(r.grade * d.coefficient),0) as grade_sum,u.id,u.email
                        from vcn_response r
                        join vcn_demand d on r.demand_id = d.id
                        join app_user u on u.id = r.user_id
                        where d.vacancy_id = :vac_id
                        group by u.id, u.email
                        order by 1 desc
                    '''
                    # --- все откликнувшиеся CUS в порядке их grade_sum (desc)
                    users = db.execute(query, {"vac_id": vac.vac_id}).fetchall()
                    cnt = len(users)
                    if cnt > 0:
                        n = cnt
                        k = 100.0 / cnt  #-- ля вычисления %%
                        for cus in users:
                            if cus['grade_sum'] == 0: #-- письмо неудачнику
                                utils.send_zero_feedback_mail(
                                    email_to=cus['email'],
                                    vac_code=vac.vac_code,
                                    vac_title=vac.vac_title,
                                    comp_code=vac.comp_code,
                                    comp_title=vac.comp_title,
                                )
                            else:
                                query = '''
                                    select d.metatag
                                    from vcn_demand d
                                    join vcn_response r on r.demand_id = d.id
                                    where r.user_id = :user_id
                                      and d.vacancy_id = :vacancy_id
                                    and r.grade > 0
                                '''
                                #--- оценки (skills) соискателя больше нуля
                                skills = []
                                for row in db.execute(query, { "user_id": cus['id'], "vacancy_id": vac.vac_id }).fetchall():
                                    skills.append(row[0])
                                utils.send_feedback_mail(
                                    email_to=cus['email'],
                                    vac_code=vac.vac_code,
                                    vac_title=vac.vac_title,
                                    comp_code=vac.comp_code,
                                    comp_title=vac.comp_title,
                                    percent=min(95, round(k * n)),  #-- процент лучше/хуже
                                    skills=skills,
                                )
                            n -= 1
                    vac.mail_sended = 2
                if vac.mail_sended > 0:
                    db.add(vac)
                    db.commit()
        finally:
            db.close()
        print('<<<< cron_dedline <<<<')


async def cron_garbage(force: bool = False):
    '''удаление просроченных откликов от неавторизованных CUS (и самих не зарегистрированных CUS)'''
    if not force and not settings.CRON_GARBAGE_ON:
        return
    # print('!garbage!')
    with mtx_garbage:
        print('>>>> cron_garbage >>>>')
        db = SessionLocal()
        try:
            #-- автозарегистрированные при анонимных откликах CUSы
            query = 'delete from app_user u where u.passkey is null and not u.is_active and u.created < current_date -1'
            db.execute(query)
            db.commit()
            #-- оставшиеся левые отклики
            query = 'delete from vcn_response r where r.is_draft and r.created < current_date -1'
            db.execute(query)
            db.commit()
        finally:
            db.close()
        print('<<<< cron_garbage <<<<')

###############################################################################

class CRUDCron:
    def get_cfg(self) -> CronConfig:
        return CronConfig(
            recom_period=settings.CRON_MAIL_PERIOD,
            recom_working=settings.CRON_MAIL_ON,
            dedline_hour=settings.CRON_DEDLINE_HOUR,
            dedline_working=settings.CRON_DEDLINE_ON,
            garbage_hour=settings.CRON_GARBAGE_HOUR,
            garbage_working=settings.CRON_GARBAGE_ON,
        )

    def put_cfg(self, cfg: CronConfig) -> CronConfig:
        if cfg.recom_working != None:
            settings.CRON_MAIL_ON = cfg.recom_working
        if cfg.recom_period:
            settings.CRON_MAIL_PERIOD = cfg.recom_period
        if settings.CRON_MAIL_ON:
            job_recom.reschedule('interval', seconds=settings.CRON_MAIL_PERIOD)
        else:
            job_recom.pause()
        # --------------------
        if cfg.dedline_working != None:
            settings.CRON_DEDLINE_ON = cfg.dedline_working
        if cfg.dedline_hour:
            settings.CRON_DEDLINE_HOUR = cfg.dedline_hour
        if settings.CRON_DEDLINE_ON:
            job_dedline.reschedule('cron', hour=cfg.dedline_hour)
        else:
            job_dedline.pause()
        # --------------------
        if cfg.garbage_working != None:
            settings.CRON_GARBAGE_ON = cfg.garbage_working
        if cfg.garbage_hour:
            settings.CRON_GARBAGE_HOUR = cfg.garbage_hour
        if settings.CRON_GARBAGE_ON:
            job_garbage.reschedule('cron', hour=cfg.garbage_hour)
        else:
            job_garbage.pause()
        # --------------------

        return self.get_cfg()


cron = CRUDCron()
