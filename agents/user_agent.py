import random
from .base_agent import BaseAgent


class UserAgent(BaseAgent):
    def __init__(self, name, reasoning_engine):
        super().__init__(name, reasoning_engine)

    def decide_action(self, game_state):
        """
        Prompt the user for an action (fold, check, call, or raise) and validate
        it against the current table state to ensure it's legal in a
        No-Limit Texas Hold'em context, *with special fallback rules for raises*.
        """

        # Extract relevant information from game_state
        current_bet_on_table  = game_state["current_bet"]  # The highest bet for this round
        agent_stack           = self.stack                 # Our remaining chips
        agent_current_bet     = self.current_bet           # How much we've contributed this round

        # The amount needed to match the highest bet on the table
        call_amount = max(0, current_bet_on_table - agent_current_bet)

        # --------------------------------------------------------
        # 1) Build a list of valid actions based on call_amount.
        # --------------------------------------------------------
        legal_actions = []

        # If call_amount == 0 => no outstanding bet: typical options are check/raise
        # If we want to allow folding with no bet, uncomment 'fold' below.
        if call_amount == 0:
            legal_actions.append("check")
            if agent_stack > 0:
                legal_actions.append("raise")
            # legal_actions.append("fold")  # Rare but possible

        else:
            # Facing a bet => fold/call always available; raise if we have enough to exceed call.
            legal_actions.append("fold")
            if agent_stack >= call_amount:
                legal_actions.append("call")
                if agent_stack > call_amount:
                    legal_actions.append("raise")
            else:
                # Not enough to call fully => call is effectively an all-in
                legal_actions.append("call")

        # --------------------------------------------------------
        # 2) Prompt user for an action from the legal_actions set.
        # --------------------------------------------------------
        action = None
        amount = 0

        while True:
            print(f"\nYour stack: {agent_stack}, call amount needed: {call_amount}")
            user_input = input(f"Enter an action {legal_actions}: ").strip().lower()

            if user_input not in legal_actions:
                print(f"'{user_input}' is not a valid action here. Please try again.")
                continue

            # -------------------------
            # (A) fold
            # -------------------------
            if user_input == "fold":
                action = "fold"
                amount = 0
                break

            # -------------------------
            # (B) check
            # -------------------------
            elif user_input == "check":
                action = "check"
                amount = 0
                break

            # -------------------------
            # (C) call
            # -------------------------
            elif user_input == "call":
                # If agent can't fully match the bet, this is all-in
                action = "call"
                amount = min(call_amount, agent_stack)
                break

            # -------------------------
            # (D) raise
            # -------------------------
            elif user_input == "raise":
                # Calculate minimum raise needed
                if current_bet_on_table > 0:
                    # A simplified rule: min raise = 2 * current_bet_on_table
                    min_raise = current_bet_on_table * 2
                else:
                    # If no bet on table, let's define 2 as a minimal opening bet
                    min_raise = 2

                max_raise = agent_stack  # can always go all-in

                # -- Check if we can afford the minimum raise --
                if min_raise > max_raise:
                    # The user cannot do a legal 'raise' at all
                    print(
                        f"You do not have enough chips to meet the minimum raise ({min_raise})."
                    )

                    # If the only other legal action is 'check', default to check
                    if set(legal_actions) == {"check", "raise"}:
                        print("Defaulting to 'check' since raise is not possible.\n")
                        action = "check"
                        amount = 0
                        break
                    # If the other legal actions are 'call' or 'fold', let the user choose:
                    elif {"call", "fold"}.issubset(legal_actions):
                        while True:
                            fallback_choice = input("You can only 'call' or 'fold'. Choose: ").strip().lower()
                            if fallback_choice in ["call", "fold"]:
                                action = fallback_choice
                                if action == "call":
                                    amount = min(call_amount, agent_stack)
                                else:
                                    amount = 0
                                break
                            else:
                                print("Invalid choice. Please enter 'call' or 'fold' only.")
                        break
                    else:
                        # Fallback if we got here in a less-expected scenario
                        # (like we had both 'check' and 'call' and user tried raise)
                        # We'll just pick 'call' if it's legal, otherwise 'check'.
                        if "call" in legal_actions:
                            action = "call"
                            amount = min(call_amount, agent_stack)
                        else:
                            action = "check"
                            amount = 0
                        break
                else:
                    # Prompt user for a specific raise amount
                    while True:
                        try:
                            raise_input = input(
                                f"Enter a raise amount between {min_raise} and {max_raise}: "
                            )
                            raise_amount = int(raise_input)
                            if min_raise <= raise_amount <= max_raise:
                                action = "raise"
                                amount = raise_amount
                                break
                            else:
                                print(f"Raise must be between {min_raise} and {max_raise}.")
                        except ValueError:
                            print("Please enter a valid integer for raise amount.")
                    break  # Done with the raise action

        # Store our chosen action for reference
        self.previous_action = (action, amount)

        return (action, amount)