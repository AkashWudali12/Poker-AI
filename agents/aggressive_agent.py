from .base_agent import BaseAgent

class AggressiveAgent(BaseAgent):
    def __init__(self, name, reasoning_engine):
        super().__init__(name, reasoning_engine)
        # Additional attributes for aggressive style if needed

    def decide_action(self, game_state):
        decision = self.reasoning_engine.evaluate(
            game_state, strategy="aggressive"
        )
        return decision
