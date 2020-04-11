import random

from players.player import Player
from setup.action import Action


class RandomPlayer(Player):
    def __init__(self, name):
        super().__init__(name)

    def act(self, board, pot, opposing_action, to_call):
        assert len(board) in {0, 3, 4, 5}
        if self.balance == 0:
            return Action.DO_NOTHING, None
        if to_call > 0:
            if to_call == self.balance:
                action = random.choices([Action.CALL, Action.FOLD], weights=[0.7, 0.3])[0]
            else:
                action = random.choices([Action.RAISE, Action.CALL, Action.FOLD], weights=[0.4, 0.4, 0.2])[0]
        else:
            if opposing_action is Action.CALL:
                # we are in the big blind and the opponent has limped pre-flop
                action = random.choices([Action.RAISE, Action.CHECK], weights=[0.6, 0.4])[0]
            else:
                action = random.choices([Action.BET, Action.CHECK], weights=[0.6, 0.4])[0]
        if action in [Action.BET, Action.RAISE]:
            amount = random.randint(max(1, min(self.balance, 2 * to_call)), self.balance)
        elif action is Action.CALL:
            amount = to_call
        else:
            amount = None
        return action, amount
