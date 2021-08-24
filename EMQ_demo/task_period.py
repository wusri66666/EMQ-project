import time

from EMQ.client.task_period import TaskPeriod
from EMQ.utils.emq_utils import asynchronous


# 异步执行任务，同时发送任务执行状态/结果
@asynchronous
def execute_task(client, app_id, task_id, task_name, task_parameter):
    obj = TaskPeriod(client, app_id, task_id, task_name, task_parameter)
    obj.receive_task()
    obj.manage_task()
    obj.start_task()
    res = task1(task_parameter)
    obj.finish_task(res)


# 模拟任务
def task1(num):
    total = 0
    for i in range(1,num):
        total += i
        time.sleep(0.1)
    return total



