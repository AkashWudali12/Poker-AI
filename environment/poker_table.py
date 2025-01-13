class Node:
    """
    A Node in a poker table as an agent and pointer to the next node.
    """
    def __init__(self, agent):
        self.agent = agent
        self.next = None


class PokerTable:
    """
    A circular singly linked list implementation of a poker table.
    Ensures at least two players in the table.
    """
    def __init__(self, agents):
        """
        Constructor that takes a list of agents. Enforces that there are at least two agents.
        """
        if len(agents) < 2:
            raise ValueError("At least two players are required at a poker table.")

        self.head = None
        self._size = 0

        # Initialize the circular list
        for agent in agents:
            self.add(agent)

        # Set pointers: small_blind, big_blind, action
        self._update_positions()

    def _update_positions(self):
        """
        Update the three pointers (small_blind, big_blind, action) based on current list size.
        """
        # Small blind always points to head
        self.small_blind = self.head

        # Big blind is the next node from head (safe since _size >= 2)
        self.big_blind = self.head.next

        # Action pointer is the next node after big_blind
        self.action = self.big_blind.next
    
    def move_positions(self):
        """
        Move the action pointer to the next player.
        """
        self.small_blind = self.small_blind.next
        self.big_blind = self.big_blind.next
        self.action = self.action.next

    def add(self, agent):
        """
        Add a new node with 'agent' to the end of the circular list.
        """
        new_node = Node(agent)
        
        if self.head is None:
            # List is empty; new node points to itself
            self.head = new_node
            new_node.next = new_node
        else:
            # Traverse to the last node (one that links back to head)
            current = self.head
            while current.next != self.head:
                current = current.next
            
            # Insert the new node at the end
            current.next = new_node
            new_node.next = self.head

        self._size += 1

    def remove(self, agent):
        """
        Remove the node that contains 'agent' from the list.
        If the agent is not found, this method does nothing.

        Enforces that removing a node does not reduce the list size below 2.
        """
        if self.head is None:
            # List is empty, nothing to remove
            return
        
        current = self.head
        prev = None
        
        while True:
            if current.agent == agent:
                # Found the node to remove
                if prev is None:
                    # We're removing the head node
                    # Case 1: There's only one node in the list
                    if current.next == self.head:
                        # This would leave 0 players, not allowed
                        raise ValueError("Cannot remove. A poker table must have at least two players.")
                    else:
                        # We need to find the last node to fix its .next pointer
                        tail = self.head
                        while tail.next != self.head:
                            tail = tail.next
                        self.head = current.next
                        tail.next = self.head
                else:
                    # Removing a non-head node
                    prev.next = current.next
                
                self._size -= 1

                # Check if removing leaves fewer than 2 players
                if self._size < 2:
                    # Undo removal, restore node (to strictly enforce 2+ players):
                    if prev is None:
                        # Rare edge case (but we've already handled it above)
                        pass
                    else:
                        prev.next = current
                    self._size += 1
                    raise ValueError("Cannot remove. A poker table must have at least two players.")
                
                self._update_positions()
                return

            prev = current
            current = current.next
            
            # If we've looped back to head, the agent is not in the list
            if current == self.head:
                break

    def get(self, index):
        """
        Get the agent at position 'index' (0-based).
        Raises an IndexError if the index is out of range.
        """
        if index < 0 or index >= self._size:
            raise IndexError("Index out of range.")
        
        current = self.head
        for _ in range(index):
            current = current.next
        return current.agent
    
    def get_head(self):
        return self.head
    
    def get_action(self):
        return self.action

    def get_small_blind(self):
        return self.small_blind
    
    def get_big_blind(self):
        return self.big_blind

    def size(self):
        """
        Return the number of elements in the list.
        """
        return self._size

    def print_list(self):
        """
        Print the contents of the list in order (by agent's name).
        """
        if self.head is None:
            print("List is empty.")
            return
        
        current = self.head
        result = []
        while True:
            result.append(current.agent.name)
            current = current.next
            if current == self.head:
                break
        
        print(" -> ".join(result) + " (back to head)")

        # Optionally print the pointers for clarity:
        print(f"Small Blind: {self.small_blind.agent.name}")
        print(f"Big Blind: {self.big_blind.agent.name}")
        print(f"Action: {self.action.agent.name}")
