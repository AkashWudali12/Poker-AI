from abc import ABC, abstractmethod

class BaseAgent(ABC):
    """
    The abstract base class for all poker agents.
    Defines the interface required by the environment.
    """

    def __init__(self, name, reasoning_engine):
        """
        :param name: A string identifier for the agent.
        :param reasoning_engine: The module/class that implements the agent's reasoning.
        """
        self.name = name
        self.reasoning_engine = reasoning_engine
        self.hand = []  # The agent's current hand, initially empty
        self.stack = 0 # current stack
        self.net_profit = 0 # Track the agent's net gain/loss
        self.folded = False  # Flag to indicate if the agent has folded

    @abstractmethod
    def decide_action(self, game_state):
        """
        Decide the next action based on the current game_state.
        :param game_state: A dictionary or object containing info such as:
                           - agent's current hand
                           - community cards
                           - betting round (pre-flop, flop, turn, river)
                           - pot size, bet amounts, etc.
        :return: An action, e.g. "fold", "call", "raise", along with optional raise size.
        """
        pass
