from players.player import Player
from setup.action import Action


class HumanPlayer(Player):
    def __init__(self, name):
        super().__init__(name)

    def act(self, board, pot, opposing_action, to_call):
        assert len(board) in {0, 3, 4, 5}
        if self.balance == 0:
            return Action.DO_NOTHING, None
        while True:
            action_str = input("Your Turn: ")
            err_msg, action, amount = self._parse_command(action_str.upper())
            if err_msg:
                print(f"Failed to parse command, ERROR msg: {err_msg}")
                print("A command should be one of {}, followed by a number if RAISE or BET".format(
                    {a for a in Action if a is not Action.DO_NOTHING}))
                print("Please try again...")
                continue
            if action == Action.CALL:
                amount = to_call
            if amount is not None and amount > self.balance:
                print("bet amount cannot be more than balance: {} (found: {})".format(self.balance, amount))
                print("Please try again...")
                continue
            if to_call > 0:
                if to_call == self.balance:
                    allowed_actions = [Action.CALL, Action.FOLD]
                    if action not in allowed_actions:
                        print("If facing an all in action must be one of: {} (found: {})".format(allowed_actions,
                                                                                                 action))
                        print("Please try again...")
                        continue
                else:
                    allowed_actions = [Action.RAISE, Action.CALL, Action.FOLD]
                    if action not in allowed_actions:
                        print("If facing a bet action must be one of: {} (found: {})".format(allowed_actions, action))
                        print("Please try again...")
                        continue
                    if action is Action.RAISE and amount < min(self.balance, 2 * to_call):
                        print("The minimum raise is the smaller of (2x the previous raise) and all in, i.e. {}".format(
                            min(2 * to_call, self.balance)))
                        print("Please try again...")
                        continue
                break
            else:
                if opposing_action is Action.CALL:
                    # we are in the big blind and the opponent has limped pre-flop
                    allowed_actions = [Action.RAISE, Action.CHECK]
                    if action not in allowed_actions:
                        print("When opponent calls pre-flop, action must be one of: {} (found: {})".format(
                            allowed_actions, action
                        ))
                        print("Please try again...")
                        continue
                    break
                else:
                    allowed_actions = [Action.BET, Action.CHECK]
                    if action not in allowed_actions:
                        print("If not facing a bet action must be one of: {} (found: {})".format(allowed_actions,
                                                                                                 action))
                        print("Please try again...")
                        continue
                    break
        return action, amount

    def _parse_command(self, command):
        split = command.strip().split()
        if not split:
            return "empty command", None, None
        action_str = split[0]
        try:
            action = Action[action_str]
        except KeyError:
            allowed_actions = {a for a in Action if a is not Action.DO_NOTHING}
            return "action: {} is not in {}".format(action_str, allowed_actions), None, None
        if action not in [Action.BET, Action.RAISE]:
            if len(split) != 1:
                return "extra characters after {} (found words: {})".format(action, split[1:]), None, None
            return None, action, None
        if len(split) == 1:
            return "no amount specified for {}".format(action), None, None
        if len(split) > 2:
            return "extra characters after {} {} (found words: {})".format(action, split[1], split[2:]), None, None
        try:
            amount = int(split[1])
        except ValueError:
            return "could not parse amount {} as int".format(split[1]), None, None
        if amount <= 0:
            return "amount for bet must be > 0 (found: {})".format(amount), None, None
        return None, action, amount







