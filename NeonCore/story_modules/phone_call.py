class PhoneCall():
    AVAILABLE_SKILLS = ["perception", "brawling", "persuasion", "hacking"]
    def __init__(self, character):
        self.character = character
        self.game_state = 'before_perception_check'
        self.prompt = "(pc) "

    def execute(self):
        wprint("Yo, listen up. You and your crew just hit the South Night City"
               " docks and now you're chillin' with a burner phone call from "
               "Lazlo, your fixer.")
        wprint("He's all like, 'Yo, we gotta change the spot for the payout. "
               "Meet me at the industrial park in Heywood.")
        wprint("But something ain't right, 'cause Lazlo ain't telling you why."
               " He's just saying it's all good, but you can tell "
               "he's sweatin'.")
        print("You got a bad feeling about this. Like, real bad.")
        
    def get_available_skills(self):

def do_phone_call(self, args):
        """Yo, chummer! You wanna make some eddies and climb the ranks? 
You wanna be a player in Night City? Type 'jack_in' and let's get this 
show on the road. Gotta choose your character first, make sure you roll 
'em up tight and make the right choice. Remember, in Night City, you 
gotta be quick on your feet and make the right moves, or you'll end up 
as another memory on the streets. So, you in or what?
"""
        wprint("Yo, listen up. You and your crew just hit the South Night City"
               " docks and now you're chillin' with a burner phone call from "
               "Lazlo, your fixer.")
        wprint("He's all like, 'Yo, we gotta change the spot for the payout. "
               "Meet me at the industrial park in Heywood.")
        wprint("But something ain't right, 'cause Lazlo ain't telling you why."
               " He's just saying it's all good, but you can tell "
               "he's sweatin'.")
        print("You got a bad feeling about this. Like, real bad.")
        self.game_state = 'before_perception_check'
        self.prompt = "(pc) "