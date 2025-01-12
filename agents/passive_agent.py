from .base_agent import BaseAgent

class PassiveAgent(BaseAgent):
    def __init__(self, name, reasoning_engine):
        super().__init__(name, reasoning_engine)
        # Additional attributes for conservative style if needed

    def decide_action(self, game_state):
        # Delegates the decision to the reasoning engine 
        # with some conservative thresholds or modifiers
        decision = self.reasoning_engine.evaluate(
            game_state, strategy="conservative"
        )
        return decision
