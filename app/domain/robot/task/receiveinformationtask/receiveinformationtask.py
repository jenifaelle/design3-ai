from domain.command.decoder import Decoder
from domain.command.visionregulation import VisionRegulation
from domain.robot.blackboard import Blackboard
from domain.robot.task.task import Task
from service.feedback import Feedback
from service.feedback import TASK_RECEIVE_INFORMATION

class ReceiveInformationTask(Task):
    def __init__(self, feedback: Feedback, decoder: Decoder, vision_regulation: VisionRegulation, blackboard: Blackboard):
        self.feedback = feedback
        self.decoder = decoder
        self.vision_regulation = vision_regulation
        self.blackboard = blackboard

    def execute(self):
        self.decoder.decode_information()
        self.blackboard.id_image = self.decoder.get_image_number()
        self.blackboard.orientation = self.decoder.get_image_orientation()
        self.blackboard.magnification = self.decoder.get_image_magnification()
        self.feedback.send_comment(TASK_RECEIVE_INFORMATION)
