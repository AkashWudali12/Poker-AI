from base_agent import BaseAgent
import random

class RandomAgent(BaseAgent):
    def __init__(self, name, reasoning_engine):
        super().__init__(name, reasoning_engine)

    def decide_action(self, game_state):
        # Possibly just picks actions at random or uses minimal logic
        possible_actions = ["fold", "call", "raise"]
        action = random.choice(possible_actions)
        if action == "raise":
            # Random raise size example
            return ("raise", random.randint(2, 10))
        return (action, 0)
