from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime
from EMQ.client.task_period import TaskPeriod
from EMQ.utils.emq_utils import asynchronous


@asynchronous
def cron_work(client, app_id, task_id, task_name, task_parameter, type):
    obj = TaskPeriod(client, app_id, task_id, task_name, task_parameter)
    obj.receive_task()
    obj.manage_task()
    obj.start_task()
    scheduler = BackgroundScheduler()
    scheduler.add_job(job, type, **task_parameter)
    scheduler.start()


# 模拟任务
def job():
    print(datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
