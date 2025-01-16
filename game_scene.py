import pygame
from components.button import Button
from game_objects.poker_game_animations import PokerGameAnimations, GameState
from agents.passive_agent import PassiveAgent
from agents.aggressive_agent import AggressiveAgent
from agents.random_agent import RandomAgent
from agents.user_agent import UserAgent
from reasoning.rule_based import RuleBasedReasoning
from environment.poker_game import PokerEnv

def game(screen):
    """
    A poker game scene optimized for 1040x720 display with game control buttons.
    """

    # initialize game agents

    rule_engine = RuleBasedReasoning()

    # Create agents with different strategies
    agent1 = PassiveAgent("PassivePlayer", rule_engine)
    agent2 = AggressiveAgent("AggressivePlayer", rule_engine)
    agent3 = RandomAgent("RandomPlayer", rule_engine)

    agents = [RandomAgent("Player 1", rule_engine), 
              RandomAgent("Player 2", rule_engine), 
              RandomAgent("Player 3", rule_engine),
              UserAgent("User", rule_engine)]
    
    # initialize game environment
    env = PokerEnv(agents, 20, screen)

    # Button callbacks
    def on_deal_players():
        # Example player hands (in real game, this would come from game logic)
        player_hands = {
            "player_1": [(2, "hearts"), (3, "clubs")],
            "player_2": [(4, "diamonds"), (5, "spades")],
            "player_3": [(6, "hearts"), (7, "diamonds")],
            "player_4": [(8, "clubs"), (9, "spades")],
            "player_5": [(10, "hearts"), (11, "diamonds")],
        }
        game_animations.deal_player_cards(player_hands)

    def on_deal_flop():
        if game_animations.state == GameState.PRE_FLOP:
            # Example flop cards
            flop_cards = [(10, "hearts"), (11, "diamonds"), (12, "clubs")]
            game_animations.deal_community_cards(flop_cards, "flop")

    def on_deal_turn():
        if game_animations.state == GameState.FLOP:
            # Example turn card
            turn_card = [(13, "spades")]
            game_animations.deal_community_cards(turn_card, "turn")

    def on_deal_river():
        if game_animations.state == GameState.TURN:
            # Example river card
            river_card = [(1, "hearts")]
            game_animations.deal_community_cards(river_card, "river")


        print(f"Round {i+1} of {rounds}")
        next_scene = env.play()
        return next_scene
        env.rotate()
        print("=====================================")    

    return env.play()
