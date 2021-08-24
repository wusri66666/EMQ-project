from EMQ.utils.emq_utils import get_time_now


class TaskPeriod(object):
    def __init__(self, client, app_id, task_id, task_name, task_parameter):
        """
        client:EMQ实例化对象
        :param client:
        """
        self.client = client
        self.app_id = app_id
        self.task_id = task_id
        self.task_name = task_name
        self.task_parameter = task_parameter
        self.topic = "/app/" + str(self.app_id) + "/" + str(self.task_id) + "/task/period"

    def receive_task(self):
        time_now = get_time_now()
        payload = "{} 下发任务命令{}任务,任务参数{}".format(str(time_now), self.task_name, self.task_parameter)
        self.client.publish_raw_data(self.topic, payload)

    def manage_task(self):
        time_now = get_time_now()
        payload = "{} 安排任务成功{}任务，已收到任务指令".format(str(time_now), self.task_name)
        self.client.publish_raw_data(self.topic, payload)

    def start_task(self):
        time_now = get_time_now()
        payload = "{} 开始执行任务{}任务,执行中".format(str(time_now), self.task_name)
        self.client.publish_raw_data(self.topic, payload)

    def execute_task(self, temp_result):
        time_now = get_time_now()
        payload = "{} {}任务执行中,中间结果{}".format(str(time_now), self.task_name, temp_result)
        self.client.publish_raw_data(self.topic, payload)

    def error_task(self, error_info):
        time_now = get_time_now()
        payload = "{} {}任务执行异常,{}".format(str(time_now), self.task_name, error_info)
        self.client.publish_raw_data(self.topic, payload)

    def finish_task(self, result):
        time_now = get_time_now()
        payload = "{} {}任务执行成功,{}".format(str(time_now), self.task_name, result)
        self.client.publish_raw_data(self.topic, payload)
