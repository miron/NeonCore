from .bootstrapper import Bootstrapper

if __name__ == "__main__":
    bootstrapper = Bootstrapper()
    act_mngr = bootstrapper.create_action_manager()
    act_mngr.start_game()



