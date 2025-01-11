from agents.passive_agent import PassiveAgent
from agents.aggressive_agent import AggressiveAgent
from agents.random_agent import RandomAgent
from reasoning.rule_based import RuleBasedReasoning
from environment.poker_game import PokerEnv

def main():
    # Initialize a reasoning engine (rule-based for now)
    rule_engine = RuleBasedReasoning()

    # Create agents with different strategies
    agent1 = PassiveAgent("PassivePlayer", rule_engine)
    agent2 = AggressiveAgent("AggressivePlayer", rule_engine)
    agent3 = RandomAgent("RandomPlayer", rule_engine)

    # Create the environment
    env = PokerEnv([agent1, agent2, agent3])

    # Run one round or multiple rounds
    env.reset()
    while not env.is_game_over():
        env.step()

    print("Game over!")

if __name__ == "__main__":
    main()
