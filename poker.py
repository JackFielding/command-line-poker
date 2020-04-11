import argparse

from players.human_player import HumanPlayer
from players.random_player import RandomPlayer
from setup.action import Action
from setup.deck import Deck
from setup.hand_ranking import rank_hand, HandRank

parser = argparse.ArgumentParser(description="play a game of poker against the computer")
parser.add_argument("--name", required=True, help="your name to be displayed throughout the game")
parser.add_argument("--num-hands", required=True, help="number of hands you want to play", type=int)
args = parser.parse_args()

deck = Deck()

computer_name = "Maniac"

human = HumanPlayer(args.name)
computer = RandomPlayer(computer_name)

starting_chips = 100
blind = 1

name_width = max(len(args.name), len(computer_name))
rank_width = max(len(str(x)) for x in HandRank)
action_width = max(len(str(x)) for x in Action)

winner_template = "{{:{}}} wins the pot of: {{}}".format(name_width)
show_template = "{{:{}}} shows cards: {{}}, hand: {{:{}}}, {{}}".format(name_width, rank_width)
action_template = "Pot: {{:3}}, Player: {{:{}}}, Action: {{:{}}}, Size: {{}}".format(name_width, action_width)

human_results = 0


def play_street(board, pot, player1, player2, to_call=0):
    winner = None
    action, pot, to_call = player_act(board, pot, None, to_call, player1)
    if action is Action.FOLD:
        winner = player2
    else:
        while True:
            action, pot, to_call = player_act(board, pot, action, to_call, player2)
            if action in [Action.CHECK, Action.CALL, Action.FOLD, Action.DO_NOTHING]:
                if action is Action.FOLD:
                    winner = player1
                break
            action, pot, to_call = player_act(board, pot, action, to_call, player1)
            if action in [Action.CHECK, Action.CALL, Action.FOLD, Action.DO_NOTHING]:
                if action is Action.FOLD:
                    winner = player2
                break
    return pot, winner


def player_act(board, pot, opposing_action, to_call, player):
    action, amount = player.act(board, pot, opposing_action, to_call)
    if action in [Action.CALL, Action.BET, Action.RAISE]:
        pot += amount
        player.balance -= amount
        to_call = amount - to_call
    print(action_template.format(pot, player.name, action, amount))
    return action, pot, to_call


for i in range(1, args.num_hands + 1):
    print(f"starting hand {i}, {human.name} is: {human_results:+,} chips overall")
    deck.reset()
    board = []
    pot = 0
    human.reset(starting_chips, deck.deal(2))
    computer.reset(starting_chips, deck.deal(2))

    small_blind = human if i % 2 == 0 else computer
    big_blind = computer if i % 2 == 0 else human

    print("posting blinds, {} is BB".format(big_blind.name))
    small_blind.post_blind(blind)
    big_blind.post_blind(2 * blind)
    pot += 3 * blind

    print("{}'s cards are: {}".format(human.name, human.cards))
    pot, winner = play_street(board, pot, small_blind, big_blind, to_call=1)
    if winner is None:
        for street, num_cards in zip(["flop ", "turn ", "river"], [3, 1, 1]):
            board += deck.deal(num_cards)
            print(f"{street}: {board}")
            pot, winner = play_street(board, pot, big_blind, small_blind)
            if winner is not None:
                break
    if winner is None:
        human_hand_rank = rank_hand(board + human.cards)
        computer_hand_rank = rank_hand(board + computer.cards)
        print(show_template.format(computer.name, computer.cards, computer_hand_rank[0], computer_hand_rank[1]))
        print(show_template.format(human.name, human.cards, human_hand_rank[0], human_hand_rank[1]))
        if human_hand_rank > computer_hand_rank:  # comparing as tuples should compare hand rank then 5 card hand
            print(winner_template.format(human.name, pot))
            human.balance += pot
        elif computer_hand_rank > human_hand_rank:
            print(winner_template.format(human.name, pot))
            computer.balance += pot
        else:
            print(f"split pot, each person gets {pot / 2} chips")
            computer.balance += pot / 2
            human.balance += pot / 2
    else:
        print(winner_template.format(winner.name, pot))
        winner.balance += pot
    assert human.balance + computer.balance == 2 * starting_chips

    human_results += human.balance - starting_chips

print("finished {:,} hands, you are: {:+,} chips overall, average chips won per hand: {:.1f}".format(
    args.num_hands, human_results, human_results / args.num_hands))