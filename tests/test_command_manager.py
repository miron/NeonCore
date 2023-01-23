import unittest
from unittest.mock import MagicMock
from .managers import CommandManager

class TestCommandManager(unittest.TestCase):
    def setUp(self):
        self.command_manager = CommandManager()

    def test_get_check_command(self):
        command_manager = CommandManager()
        self.assertRaises(AttributeError,
                          self.command_manager.get_check_command)
        self.assertIsNone(self.command_manager.get_check_command())

if __name__ == '__main__':
    unittest.main()




    def test_get_check_command(self):
        # create mock objects for the dependencies
        mock_player = MagicMock()
        mock_npcs = MagicMock()

        # create an instance of the CommandManager class
        command_manager = CommandManager(mock_player, mock_npcs)

        # set the game state to 'before_perception_check'
        command_manager.game_state = 'before_perception_check'

        # call the get_check_command method
        check_cmd = command_manager.get_check_command()

        # assert that the returned object is an instance of SkillCheckCommand
        self.assertIsInstance(check_cmd, SkillCheckCommand)

