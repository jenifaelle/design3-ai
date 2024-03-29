from unittest import TestCase
from unittest.mock import Mock
from domain.robot.task.drawtask.drawtask import DrawTask
from domain.robot.task.gooutofdrawzonetask.gooutofdrawzonetask import GoOutOfDrawzoneTask
from domain.robot.task.gotodrawzonetask.gotodrawzonetask import GoToDrawzoneTask
from domain.robot.task.gotoimagetask.gotoimagetask import GoToImageTask
from domain.robot.task.identifyantennatask.identifyantennatask import IdentifyAntennaTask
from domain.robot.task.identifyantennataskproxy.identifyantennataskproxy import IdentifyAntennaTaskProxy
from domain.robot.task.initialorientationtask.initialorientationtask import InitialOrientationTask
from domain.robot.task.lightredledtask.lightredledtask import LightRedLedTask
from domain.robot.task.receiveinformationtask.receiveinformationtask import ReceiveInformationTask
from domain.robot.task.shutdownredledtask.shutdownredledtask import ShutDownRedLedTask
from domain.robot.task.taskfactory import TaskFactory
from domain.robot.task.takepicturetask.takepicturetask import TakePictureTask


class TaskFactoryTest(TestCase):
    def setUp(self):
        self.robot_controler = Mock()
        self.global_information = Mock()
        self.task_factory = TaskFactory(self.global_information, self.robot_controler)

    def test_can_create_an_initial_orientation_task(self):

        task = self.task_factory.create_initial_orientation_task()

        self.assertTrue(type(task) is InitialOrientationTask)

    def test_can_create_an_identify_antenna_task(self):
        task = self.task_factory.create_indentify_antenna_task()

        self.assertTrue(type(task) is IdentifyAntennaTask)

    def test_can_create_a_receive_information_task(self):
        task = self.task_factory.create_receive_informations_task()

        self.assertTrue(type(task) is ReceiveInformationTask)

    def test_can_create_a_go_to_image_task(self):
        task = self.task_factory.create_go_to_image_task()

        self.assertTrue(type(task) is GoToImageTask)

    def test_can_create_a_take_picture_task(self):
        task = self.task_factory.create_take_picture_task()

        self.assertTrue(type(task) is TakePictureTask)

    def test_can_create_a_go_to_drawzone_task(self):
        task = self.task_factory.create_go_to_drawzone_task()

        self.assertTrue(type(task) is GoToDrawzoneTask)

    def test_can_create_a_draw_task(self):
        task = self.task_factory.create_draw_task()

        self.assertTrue(type(task) is DrawTask)

    def test_can_create_a_go_out_of_drawzone_task(self):
        task = self.task_factory.create_go_out_of_drawzone_task()

        self.assertTrue(type(task) is GoOutOfDrawzoneTask)

    def test_can_create_a_shut_down_red_led_task(self):
        task = self.task_factory.create_shut_down_red_led_task()

        self.assertTrue(type(task) is ShutDownRedLedTask)

    def test_can_create_a_light_red_led_task(self):
        task = self.task_factory.create_light_red_led_task()

        self.assertTrue(type(task) is LightRedLedTask)

    def test_can_create_proxy_identify_antenna_task(self):
        task = self.task_factory.create_proxy_identify_antenna_task()

        self.assertTrue(type(task) is IdentifyAntennaTaskProxy)

    def test_can_create_all_competition_tasks(self):
        task_list = self.task_factory.create_competition_tasks()

        self.assertEquals(len(task_list), 10)
        self.assertTrue(type(task_list[0]) is ShutDownRedLedTask)
        self.assertTrue(type(task_list[1]) is InitialOrientationTask)
        self.assertTrue(type(task_list[2]) is IdentifyAntennaTaskProxy)
        self.assertTrue(type(task_list[3]) is ReceiveInformationTask)
        self.assertTrue(type(task_list[4]) is GoToImageTask)
        self.assertTrue(type(task_list[5]) is TakePictureTask)
        self.assertTrue(type(task_list[6]) is GoToDrawzoneTask)
        self.assertTrue(type(task_list[7]) is DrawTask)
        self.assertTrue(type(task_list[8]) is GoOutOfDrawzoneTask)
        self.assertTrue(type(task_list[9]) is LightRedLedTask)
