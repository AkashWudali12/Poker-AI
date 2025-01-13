from .base_agent import BaseAgent
import random

class RandomAgent(BaseAgent):
    def __init__(self, name, reasoning_engine):
        super().__init__(name, reasoning_engine)

    def decide_action(self, game_state):
        """
        Make a decision based on current betting state in a No-Limit Texas Hold'em game.
        Ensures the returned action is always legal (fold, check, call, or raise),
        given the current bet, how much we've already put in (agent_current_bet),
        and how many chips we have left (self.stack).
        """

        previous_table_action = game_state["previous_action"]     # e.g. ("raise", 20)
        current_bet_on_table  = game_state["current_bet"]         # e.g. 20 chips
        agent_stack           = self.stack                        # Our remaining chips
        agent_current_bet     = self.current_bet                  # How much we've put in this round

        # How much more we need to put in to *match* the highest current bet
        call_amount = max(0, current_bet_on_table - agent_current_bet)

        legal_actions = []
        amount = 0  # Default bet size (updated below if needed)

        # ----------------------------------------------------------
        # 1. If we've already matched the table's current bet:
        #    -> We have no outstanding chips to call, so we can check or raise.
        # ----------------------------------------------------------
        if call_amount == 0:
            # 'check' is a valid action if there's nothing to call.
            legal_actions.append("check")

            # 'raise' is allowed if we have chips left to raise.
            if agent_stack > 0:
                legal_actions.append("raise")

            # (Optional) If you want to allow folding with no bet, add "fold":
            # legal_actions.append("fold")

        # ----------------------------------------------------------
        # 2. If we *have not* matched the table's current bet:
        #    -> We can fold, call (possibly all-in), or raise.
        # ----------------------------------------------------------
        else:
            # 'fold' is always available when facing a bet.
            legal_actions.append("fold")

            # If we have enough chips to call at least the required amount...
            if agent_stack >= call_amount:
                legal_actions.append("call")
                
                # If we still have chips beyond calling, we can raise.
                if agent_stack > call_amount:
                    legal_actions.append("raise")
            else:
                # If we don't have enough chips to fully call, we can only call all-in or fold.
                # (In typical poker, that's effectively "call" for your remaining stack.)
                legal_actions.append("call")  # This is effectively an all-in call.

        # ----------------------------------------------------------
        # Choose a random legal action among the computed set.
        # ----------------------------------------------------------
        chosen_action = random.choice(legal_actions)

        # ----------------------------------------------------------
        # Determine the bet or raise amount according to the chosen action.
        # ----------------------------------------------------------
        if chosen_action == "check":
            amount = 0  # No chips needed to check

        elif chosen_action == "fold":
            amount = 0  # No chips added, agent is folding

        elif chosen_action == "call":
            # If agent can't fully match the bet, treat it as an all-in call.
            amount = min(call_amount, agent_stack)

        elif chosen_action == "raise":
            # Minimal approach for No-Limit:
            #    * If call_amount > 0, we must put in at least `call_amount + previous_bet_increment`.
            #    * But for simplicity, let's define a min_raise as current_bet_on_table*2 if there's a bet,
            #      or something small (like 2) if there's no bet.
            if current_bet_on_table == 0:
                min_raise = 2
            else:
                # For a "proper" raise, we usually need at least *previous raise size* more than call.
                # As a very simplified rule, let's say double the current bet on the table:
                min_raise = current_bet_on_table * 2

            max_raise = agent_stack  # We can always go all-in

            if min_raise <= max_raise:
                amount = random.randint(min_raise, max_raise)
            else:
                # If we can't meet the min raise, just call all-in
                chosen_action = "call"
                amount = min(call_amount, agent_stack)

        # ----------------------------------------------------------
        # Optionally store our chosen action in self.previous_action
        # ----------------------------------------------------------
        self.previous_action = (chosen_action, amount)

        return (chosen_action, amount)