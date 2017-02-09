import unittest

import mcu.commands
from mcu.commands import regulator


class TestCommands(unittest.TestCase):
    def setUp(self):
        self.null_position = 0, 0, 0

    def tearDown(self):
        pass

    def test_zero_regulator(self):
        regulator.set_point = (0, 0, 0)
        exp_cmd = (0, 0, 0)
        reg_cmd = regulator.next_speed_command(self.null_position)
        self.assertEqual(exp_cmd, reg_cmd)

    def test_deadzone_regulator(self):
        regulator.set_point = (10, 10, 0)
        exp_cmd = (0, 0, 0)
        reg_cmd = regulator.next_speed_command(self.null_position)
        self.assertEqual(exp_cmd, reg_cmd)

    def test_saturation_regulator(self):
        regulator.set_point = (200, 200, 0)
        exp_cmd = (125, 125, 0)
        reg_cmd = regulator.next_speed_command(self.null_position)
        self.assertEqual(exp_cmd, reg_cmd)

    def test_negative_saturation_regulator(self):
        regulator.set_point = (-200, 0, 0)
        exp_cmd = (-125, 0, 0)
        reg_cmd = regulator.next_speed_command(self.null_position)
        self.assertEqual(exp_cmd, reg_cmd)