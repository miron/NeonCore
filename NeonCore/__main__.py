from .bootstrapper import Bootstrapper

bootstrapper = Bootstrapper()
act_mngr = bootstrapper.create_action_manager()
act_mngr.start_game()
