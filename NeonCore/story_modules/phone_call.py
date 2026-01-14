from ..managers.story_manager import Story
from ..managers.action_manager import ActionManager

class PhoneCall(Story):
    def __init__(self):
        super().__init__("phone_call")

    async def start(self, game_context):
        """
        Triggered when the story starts.
        Effect: Prints notification of incoming call.
        """
        self.state = "ringing"
        self.state = "ringing"
        await game_context.io.send("\n\033[1;36m[INCOMING HOLO-CALL]\033[0m: Burner Phone")
        await game_context.io.send("(It continues to buzz violently.)")
        
        # Ensure dialogue context is cleared until answered
        if game_context.char_mngr.player:
            game_context.char_mngr.player.dialogue_context = None

    async def handle_answer(self, game_context):
        """
        Called when the player answers the call.
        """
        if self.state != "ringing":
             return "already_answered"

        self.state = "in_call"
        await game_context.io.send("\n\033[1;32m[CALLER ID: LAZLO (FIXER)]\033[0m")
        await game_context.io.send(
            "He's all like, 'Yo, we gotta change the spot for the payout. "
            "Meet me at the industrial park in Heywood.'"
        )
        await game_context.io.send(
            "But something ain't right, 'cause Lazlo ain't telling you why."
            " He's just saying it's all good, but you can tell "
            "he's sweatin'."
        )
        await game_context.io.send("You got a bad feeling about this. Like, real bad.")
        await game_context.io.send("Yo chummer, you wanna roll for \033[1mHuman Perception\033[0m? (DV 17)")
        
        if game_context.char_mngr.player:
            game_context.char_mngr.player.dialogue_context = "analyzing_lazlo_call"
        
        return "success"

    async def update(self, game_context):
        """
        Check for triggers.
        """
        player = game_context.char_mngr.player
        if not player or not getattr(player, "digital_soul", None):
            return

        # Check for Human Perception result
        history_key = "Checked Lazlo Call"
        if any(history_key in e for e in player.digital_soul.recent_events):
            # The skill check logic (HumanPerceptionCheckCommand) already printed the reveal.
            # We can now transition the story or mark it as resolved.
            if self.state != "checked_perception":
                self.state = "checked_perception"
                # End the story as the call is finished
                # This ensures ActionManager knows the story is over.
                # await game_context.story_manager.end_story()  <-- CHANGED: Chain to next story
                await game_context.story_manager.start_story("heywood_ambush")
        
        # Fallback: If player leaves the area without checking, advance the story anyway
        # Assuming call happened in 'start_square' (or wherever they were)
        # We can just check if state is 'in_call' and they execute a move?
        # Simpler: If they are 'in_call' and move to a new location.
        if self.state == "in_call":
            # If they leave start_square? Hard to know where they started without tracking.
            # Let's just allow the story to proceed if they just move.
            pass
            # Actually, simply starting HeywoodAmbush doesn't hurt.
            # But let's verify if they arrive at Heywood while still in 'PhoneCall'?
            if game_context.world.player_position == "heywood_alley":
                 # They arrived! Switch immediately.
                 await game_context.story_manager.start_story("heywood_ambush")

    async def end(self, game_context):
        pass
