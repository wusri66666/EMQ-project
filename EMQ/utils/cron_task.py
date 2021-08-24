from apscheduler.schedulers.blocking import BlockingScheduler
from datetime import datetime

from EMQ.utils.emq_utils import asynchronous


@asynchronous
def interval_work():
    scheduler = BlockingScheduler()
    scheduler.add_job(job, 'interval', seconds=5)
    scheduler.start()


@asynchronous
def cron_work():
    scheduler = BlockingScheduler()
    scheduler.add_job(job, 'cron', minute='*')
    scheduler.start()


# 模拟任务
def job():
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))


