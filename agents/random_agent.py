from .base_agent import BaseAgent
import random
import time

class RandomAgent(BaseAgent):
    def __init__(self, name, reasoning_engine):
        super().__init__(name, reasoning_engine)

    def decide_action(self, game_state):
        """
        Make a decision based on current betting state in a No-Limit Texas Hold'em game.
        Ensures the returned action is always legal (fold, check, call, or raise),
        given the current bet (game_state["current_bet"]), how much we've already put in
        (self.current_bet), and how many chips we have left (self.stack).
        """

        previous_table_action = game_state["previous_action"]     # e.g. ("raise", 20)
        current_bet_on_table  = game_state["current_bet"]         # e.g. 20 chips
        agent_stack           = self.stack                        # Our remaining chips
        agent_current_bet     = self.current_bet                  # How much we've already put in this round

        # How much more we need to match the highest current bet
        call_amount = max(0, current_bet_on_table - agent_current_bet)

        legal_actions = []

        # ---------------------------
        # CASE 1: No outstanding bet
        # ---------------------------
        if call_amount == 0:
            # There's nothing to call, so we can CHECK or RAISE
            legal_actions.append("check")

            # RAISE is legal only if we have some chips left
            if agent_stack > 0:
                legal_actions.append("raise")
            
            # Folding here is legal in most rulesets, but almost never done
            # If you want to forbid folding with no bet, do nothing
            # If you'd like to allow it, uncomment below:
            # legal_actions.append("fold")

        # ----------------------------------
        # CASE 2: There's an outstanding bet
        # ----------------------------------
        else:
            # 1) FOLD is always an option if facing a bet
            legal_actions.append("fold")

            # 2) CALL (or all-in if we don't have enough)
            if agent_stack >= call_amount:
                # We can fully call
                legal_actions.append("call")
                # 3) RAISE is possible only if we still have chips beyond the call_amount
                if agent_stack > call_amount:
                    legal_actions.append("raise")
            else:
                # We don't have enough to fully call, so this is effectively an all-in call
                legal_actions.append("call")

        # ----------------------------------------------------------
        # Choose a random legal action among the computed set
        # ----------------------------------------------------------
        chosen_action = random.choice(legal_actions)
        amount = 0  # Default

        # ----------------------------------------------------------
        # Determine the final bet/raise amount based on the chosen action
        # ----------------------------------------------------------
        if chosen_action == "check":
            amount = 0  # Checking requires no additional chips

        elif chosen_action == "fold":
            amount = 0  # Folding doesn't add chips

        elif chosen_action == "call":
            # If we can't fully match the bet, treat it as an all-in call
            amount = min(call_amount, agent_stack)

        elif chosen_action == "raise":
            # ----------------------------------------
            # Minimal no-limit logic for a raise:
            # - If there's no existing bet on the table (call_amount == 0),
            #   we define a min first bet (e.g. 2).
            # - If there's an existing bet (call_amount > 0),
            #   the min raise is typically "current_bet_on_table + (some increment)".
            #   For simplicity, let's do a "double the current bet" approach.
            # ----------------------------------------
            if call_amount == 0:
                # No bet on the table, define a minimal bet
                min_raise = 2
            else:
                # Minimal raise: at least double the current bet on the table
                min_raise = current_bet_on_table * 2

            max_raise = agent_stack  # We can go up to all-in

            # Ensure our min_raise is at least enough to cover the call
            # i.e., min total contribution must be >= current_bet_on_table + the increment
            if min_raise < (call_amount * 2):
                # A safer (though simplified) approach is: min_raise >= call_amount + (current_bet_on_table - agent_current_bet)
                # But let's keep it consistent with "double the bet" logic
                min_raise = call_amount * 2

            # If we can't meet the min_raise, we must fall back to either calling or folding
            # But in no-limit, you can always jam all-in, which might be less than the typical 'min raise' if your stack is short.
            # So we handle that below:
            if min_raise <= max_raise:
                # We can pick a random raise between min_raise and max_raise
                amount = random.randint(min_raise, max_raise)
            else:
                # We can't meet the min raise fully, so let's either go all-in (call_amount + partial) or just call.
                # Typically, you'd do an all-in for your entire stack. Let's do that.
                if agent_stack > call_amount:
                    amount = agent_stack  # all-in
                else:
                    # We can't raise at all, so revert to call or fold
                    if agent_stack >= call_amount:
                        chosen_action = "call"
                        amount = call_amount
                    else:
                        chosen_action = "fold"
                        amount = 0

        # Store the chosen action & amount
        self.previous_action = (chosen_action, amount)

        time.sleep(random.randint(1, 3))

        return (chosen_action, amount)
