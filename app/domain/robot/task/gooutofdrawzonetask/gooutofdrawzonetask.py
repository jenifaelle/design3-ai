from domain.command.visionregulation import VisionRegulation
from domain.pathfinding import get_segments
from domain.robot.feedback import Feedback
from domain.robot.task.task import Task
from service import pathfinding_application_service
from service.destinationcalculator import DestinationCalculator
from service.globalinformation import GlobalInformation

class GoOutOfDrawzoneTask(Task):
    def __init__(self, feedback: Feedback,
                        vision_regulation: VisionRegulation,
                        destination_calculator: DestinationCalculator,
                        global_information: GlobalInformation,
                        pathfinding_application_service: pathfinding_application_service,
                        get_segments: get_segments):
        self.feedback = feedback
        self.vision_regulation = vision_regulation
        self.destination_calculator = destination_calculator
        self.global_information = global_information
        self.pathfinding_application_service = pathfinding_application_service
        self.get_segments = get_segments

    def execute(self):
        obstacles = self.global_information.get_obstacles()
        robot_position = self.global_information.get_robot_position()
        gameboard_width = self.global_information.get_gameboard_width()
        gameboard_length = self.global_information.get_gameboard_length()
        safezone_position = self.destination_calculator.get_safezone(obstacles, robot_position)
        path = self.pathfinding_application_service.find(obstacles, gameboard_width, gameboard_length, robot_position, safezone_position)
        destinations_path = self.get_segments.get_filter_path(path)
        for destination in destinations_path:
            self.vision_regulation.go_to_position(destination)

        self.feedback.send_comment("end going to safezone")