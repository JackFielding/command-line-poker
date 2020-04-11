
class Player:
    def __init__(self, name):
        self.name = name
        self.starting_balance = None
        self.balance = None
        self.cards = None

    def act(self, board, pot, opposing_action, to_call):
        raise NotImplementedError

    def reset(self, amount, cards):
        self.balance = amount
        self.starting_balance = amount
        self.cards = cards

    def post_blind(self, blind):
        self.balance -= blind
