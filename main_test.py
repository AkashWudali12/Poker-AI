from agents.passive_agent import PassiveAgent
from agents.aggressive_agent import AggressiveAgent
from agents.random_agent import RandomAgent
from agents.user_agent import UserAgent
from reasoning.rule_based import RuleBasedReasoning
from environment.poker_game import PokerEnv

def start_game():
    # Initialize a reasoning engine (rule-based for now)
    rule_engine = RuleBasedReasoning()

    # Create agents with different strategies
    agent1 = PassiveAgent("PassivePlayer", rule_engine)
    agent2 = AggressiveAgent("AggressivePlayer", rule_engine)
    agent3 = RandomAgent("RandomPlayer", rule_engine)

    agents = [RandomAgent("Player 1", rule_engine), 
              RandomAgent("Player 2", rule_engine), 
              RandomAgent("Player 3", rule_engine),
              RandomAgent("User", rule_engine)]

    # Create the environment
    env = PokerEnv(agents, 20, None)

    for i in range(3):
        print("="*80)
        print(f"ROUND: {i+1}".center(80))
        print("="*80)
        env.play()
        env.rotate()

    print("Game over!")
    print("=====================================")
    print("Final results:")
    for agent in agents:
        print(f"{agent.name}: {agent.stack}")
        print(f"Net profit: {agent.net_profit}")
        print("=====================================")

if __name__ == "__main__":
    start_game()
