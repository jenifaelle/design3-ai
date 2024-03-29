from domain.command.lighter import Lighter
from domain.robot.task.task import Task

from service.feedback import Feedback


class ShutDownRedLedTask(Task):
    def __init__(self, feedback: Feedback, lighter: Lighter):
        self.feedback = feedback
        self.lighter = lighter

    def execute(self):
        self.lighter.shut_down_red_led()
        self.feedback.send_new_cycle()
