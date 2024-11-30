import unittest
from NeonCore.managers.command_manager import CommandManager


class TestCommandManager(unittest.TestCase):
    def setUp(self):
        self.command_manager = CommandManager()

    def test_get_check_command(self):
        self.command_manager.game_state = "before_perception_check"
        self.assertIsNone(self.command_manager.get_check_command())
        self.command_manager.game_state = None
        self.assertIsNone(self.command_manager.get_check_command())
        self.assertRaises(AttributeError, self.command_manager.get_check_command)


if __name__ == "__main__":
    unittest.main()


#    def test_get_check_command(self):
#        # create mock objects for the dependencies
#        mock_player = MagicMock()
#        mock_npcs = MagicMock()
#
#        # create an instance of the CommandManager class
#        command_manager = CommandManager(mock_player, mock_npcs)
#
#        # set the game state to 'before_perception_check'
#        command_manager.game_state = 'before_perception_check'
#
#        # call the get_check_command method
#        check_cmd = command_manager.get_check_command()
#
#        # assert that the returned object is an instance of SkillCheckCommand
#        self.assertIsInstance(check_cmd, SkillCheckCommand)


# import contextlib
# from managers.command_manager import CommandManager
#
# @contextlib.contextmanager
# def patch_dependencies(player, npcs):
#    with mock.patch('managers.command_manager.CommandManager.player', new_callable=mock.PropertyMock) as player_mock:
#        player_mock.return_value = player
#        with mock.patch('managers.command_manager.CommandManager.npcs', new_callable=mock.PropertyMock) as npcs_mock:
#            npcs_mock.return_value = npcs
#            yield
#
# class TestCommandManager(unittest.TestCase):
#    def test_get_check_command(self):
#        # create mock objects for the dependencies
#        mock_player = MagicMock()
#        mock_npcs = MagicMock()
#
#        with patch_dependencies(mock_player, mock_npcs):
#            # create an instance of the CommandManager class
#            command_manager = CommandManager()
#
#            # set the game state to 'before_perception_check'
#            command_manager.game_state = 'before_perception_check'
#
#            # call the get_check_command method
#            check_cmd = command_manager.get_check_command()
#
#            # assert that the returned object is an instance of SkillCheckCommand
#            self.assertIsInstance(check_cmd, SkillCheckCommand)


# from functools import singledispatch
#
# class CommandManager:
#    def __init__(self, character_manager, map):
#        self.character_manager = character_manager
#        self.map = map
#
# @singledispatch
# def inject_dependencies(command_manager):
#    pass
#
# @inject_dependencies.register(CommandManager)
# def _(command_manager):
#    command_manager.character_manager = mock.Mock()
#    command_manager.map = mock.Mock()
#
# class TestCommandManager:
#    def setup(self):
#        self.command_manager = CommandManager()
#        inject_dependencies(self.command_manager)
#
#    def test_get_check_command(self):
#        check_cmd = self.command_manager.get_check_command()
#        assert check_cmd is not None
