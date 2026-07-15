import random


SUITS = ["ყვავი", "ჯვარი", "გული", "აგური"]
CARDS = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King", "Ace"]


def make_deck():
    cards = []

    for suit in SUITS:
        for card in CARDS:
            cards.append((card, suit))

    random.shuffle(cards)
    return cards


def get_card_points(card):
    name = card[0]

    if name in ["Jack", "Queen", "King"]:
        return 10

    if name == "Ace":
        return 11

    return int(name)


def total_points(hand):
    points = sum(get_card_points(card) for card in hand)

    aces = sum(1 for card in hand if card[0] == "Ace")

    while points > 21 and aces:
        points -= 10
        aces -= 1

    return points


def print_cards(owner, cards):
    print("\n" + owner)

    for card in cards:
        print(f"{card[0]} - {card[1]}")

    print("სულ ქულა:", total_points(cards))


def player_move(deck, hand):

    while True:
        print_cards("თქვენი ბარათები:", hand)

        if total_points(hand) > 21:
            print("თქვენ გადააჭარბეთ 21 ქულას!")
            break

        answer = input(
            "აიღებთ კიდევ ერთ ბარათს? (კი/არა): "
        )

        if answer.lower() == "კი":
            hand.append(deck.pop())

        elif answer.lower() == "არა":
            break

        else:
            print("გთხოვთ დაწეროთ კი ან არა.")


def dealer_move(deck, hand):

    while total_points(hand) < 17:
        hand.append(deck.pop())
    print_cards("კომპიუტერის ბარათები:", hand)


def check_result(player, dealer):

    player_score = total_points(player)
    dealer_score = total_points(dealer)

    print("\n===== შედეგი =====")
    print("თქვენი ქულა:", player_score)
    print("კომპიუტერის ქულა:", dealer_score)


    if player_score > 21:
        print("კომპიუტერმა მოიგო.")

    elif dealer_score > 21:
        print("თქვენ მოიგეთ!")

    elif player_score > dealer_score:
        print("თქვენ მოიგეთ!")

    elif player_score < dealer_score:
        print("თქვენ წააგეთ.")

    else:
        print("ფრეა.")


def start_game():
    deck = make_deck()
    user_cards = [
        deck.pop(),
        deck.pop()
    ]
    computer_cards = [
        deck.pop(),
        deck.pop()
    ]

    print("\n===== Blackjack =====")

    player_move(deck, user_cards)

    if total_points(user_cards) <= 21:
        dealer_move(deck, computer_cards)

    check_result(user_cards, computer_cards)

def game_menu():

    while True:
        start_game()
        again = input(
            "\nგსურთ ახალი თამაში? (კი/არა): "
        )

        if again.lower() == "არა":
            print("თამაში დასრულდა.")
            break

game_menu()
