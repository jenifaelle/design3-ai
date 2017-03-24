from domain.command.visionregulation import VisionRegulation
from domain.robot.feedback import Feedback
from domain.robot.task.task import Task
from service.globalinformation import GlobalInformation

INITIAL_ANGLE = 0

class InitialOrientationTask(Task):
    def __init__(self, feedback: Feedback,
                        vision_regulation: VisionRegulation,
                        global_information: GlobalInformation):
        super().__init__()
        self.feedback = feedback
        self.vision_regulation = vision_regulation
        self.global_information = global_information

    def execute(self):
        if self.global_information.get_robot_orientation() !=0:
            self.vision_regulation.oriente_robot(INITIAL_ANGLE)

        self.feedback.send_comment("End task initial orientation")