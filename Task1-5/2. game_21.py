import random

SUITS = ["ყვავი", "ჯვარი", "გული", "აგური"]
RANKS = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King", "Ace"]


def create_deck():
    deck = [(rank, suit) for suit in SUITS for rank in RANKS]
    random.shuffle(deck)
    return deck


def card_value(rank):
    if rank in ("Jack", "Queen", "King"):
        return 10
    if rank == "Ace":
        return 11
    return int(rank)


def calculate_score(hand):
    return sum(card_value(rank) for rank, suit in hand)


def show_hand(name, hand):
    cards_str = ", ".join(f"{rank} {suit}" for rank, suit in hand)
    print(f"{name}: {cards_str}  (ქულა: {calculate_score(hand)})")


def player_turn(deck, player_hand):
    while True:
        show_hand("თქვენი ბარათები", player_hand)
        score = calculate_score(player_hand)

        if score > 21:
            print("თქვენ გადააჭარბეთ 21-ს!")
            return

        choice = input("გსურთ კიდევ ბარათის აღება? (add/stop): ")
        if choice == "stop":
            return
        else:
            player_hand.append(deck.pop())


def computer_turn(deck, computer_hand):
    while calculate_score(computer_hand) < 17:
        computer_hand.append(deck.pop())
    show_hand("კომპიუტერის ბარათები", computer_hand)


def determine_winner(player_hand, computer_hand):
    player_score = calculate_score(player_hand)
    computer_score = calculate_score(computer_hand)

    print(f"\nთქვენი საბოლოო ქულა: {player_score}")
    print(f"კომპიუტერის საბოლოო ქულა: {computer_score}")

    if player_score > 21:
        print("თქვენ წააგეთ")
    elif computer_score > 21:
        print("თქვენ მოიგეთ")
    elif player_score > computer_score:
        print("თქვენ მოიგეთ")
    elif player_score < computer_score:
        print("თქვენ წააგეთ")
    else:
        print("ფრეზე ვართ - ხელახლა ვარიგებთ!")


def play_round():
    deck = create_deck()

    player_hand = [deck.pop(), deck.pop()]
    computer_hand = [deck.pop(), deck.pop()]

    print("\n===== ახალი რაუნდი =====")

    player_turn(deck, player_hand)

    if calculate_score(player_hand) <= 21:
        computer_turn(deck, computer_hand)

    determine_winner(player_hand, computer_hand)


def main():
    while True:
        play_round()
        again = input("\nგსურთ თამაშის თავიდან დაწყება? (კი/არა): ")
        if again == "არა":
            print("ნახვამდის!")
            break


if __name__ == "__main__":
    main()
