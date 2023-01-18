class SkillCheck:
    """
    Attacker vs Defender
    Trying Again:
      only if chances of success have improved
      - you took longer
      - used better tool
      - you or friends made Complementary Skill Check
    Complementary Skill Check
      Single +1 bonus for subsequent similar skill
    Taking Extra Time
      Single +1 bonus when taking four times longer
    """
    
    def __init__(self, character):
        self.character = character

    def handle_npc_encounter(self, npc):
        """
        Spends a specified number of luck points on a skill check.

        Parameters:
        luck_points (int): 
        The number of luck points to spend on the skill check.
        """
        while True:
            luck_points = int(
                input(
                      f'Use LUCK {self.character.lucky_pool}'
                      f'/{self.character.stats["luck"]} '
                      )
            )
            if luck_points > self.character.lucky_pool:
                print("Not enough luck points!")
            else:
                self.perform_check('brawling', 'Professional', luck_points)
                # subtract the luck points from the lucky pool
                self.character.lucky_pool -= luck_points
                print(f"Lucky Pool: {self.character.lucky_pool}")
                break
        raise StopIteration

    def perform_check(self, skill_name, difficulty_value, luck_points):
        """
        Perform a skill check using a specified skill and difficulty
        level.

        Args:
        skill_name (str): The name of the skill to use for the check.
        difficulty_value (str): The difficulty level of the check.
        luck_points (int): The number of luck points to use for the
        check.

        Returns:
        None
        """
        # Generate a random number from 1 to 10
        d10_roll = random.randint(1, 10)
        # Add d10 roll to total skill level
        skill_check_total = (self.character.skill_total(skill_name)
                             + d10_roll + luck_points)
        if d10_roll == 10:
            print("Critical Success! Rolling another one")
            # Generate another random number from 1 to 10
            skill_check_total += random.randint(1,10)
        elif d10_roll == 1:
            print("Critical Failure! Rolling another one")
            # Generate another random number from 1 to 10
            skill_check_total -= random.randint(1,10)
        # Get the DV for the specified difficulty level
        difficulty_value = DIFFICULTY_VALUE[difficulty_value]
        if skill_check_total > difficulty_value:
            print(f"Success! Attacker roll: {skill_check_total}, "
                  f"Defender DV: {difficulty_value}")
        elif skill_check_total < difficulty_value:
            print(f"Failure! Attacker roll: {skill_check_total}, "
                  f"Defender DV: {difficulty_value}")
        else:
            wprint(f"Tie! Attacker roll: {skill_check_total}, "
                   f"Defender DV: {difficulty_value}")
            print("Attacker loses.")
