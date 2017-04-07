from domain.robot.blackboard import Blackboard
from domain.robot.task.task import Task
from domain.command.drawer import Drawer
from service.feedback import Feedback
from service.globalinformation import GlobalInformation
from service.feedback import TASK_DRAW_IMAGE

MESSAGE = "End of drawing task!"


class DrawTask(Task):
    def __init__(self, feedback: Feedback, drawer: Drawer, blackboard: Blackboard, global_information: GlobalInformation):
        super().__init__()
        self.drawer = drawer
        self.feedback = feedback
        self.blackboard = blackboard
        self.global_information = global_information

    def execute(self):
        draw_path = self.blackboard.get_image_segments()
        self.global_information.send_path(draw_path + [draw_path[0]])
        self.drawer.draw(draw_path)
        self.feedback.send_comment(TASK_DRAW_IMAGE)