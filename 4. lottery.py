import random
import logging

logging.basicConfig(
    filename="lottery_log.log",
    level=logging.INFO,
    format="%(asctime)s - %(message)s",
    encoding="utf-8",
)

JACKPOT = 1000000


def generate_computer_numbers():
    return sorted(random.sample(range(1, 50), 6))


def get_player_numbers():
    raw = input("შეიყვანეთ თქვენი 6 რიცხვი (1-49), გამოყავით space-ით: ")
    numbers = [int(n) for n in raw.split()]
    return numbers


def count_matches(player_numbers, winning_numbers):
    return len(set(player_numbers) & set(winning_numbers))


def calculate_prize(matches):
    if matches == 6:
        return JACKPOT
    elif matches == 5:
        return JACKPOT * (1 - 0.40)
    elif matches == 4:
        return JACKPOT * (1 - 0.60)
    elif matches == 3:
        return JACKPOT * (1 - 0.80)
    else:
        return 0


def play_round():
    winning_numbers = generate_computer_numbers()
    player_numbers = get_player_numbers()

    matches = count_matches(player_numbers, winning_numbers)
    prize = calculate_prize(matches)

    print(f"\nგამარჯვებული რიცხვები: {winning_numbers}")
    print(f"თქვენი რიცხვები: {sorted(player_numbers)}")
    print(f"დამთხვევების რაოდენობა: {matches}")

    if prize > 0:
        print(f"გილოცავთ! თქვენ მოიგეთ: {prize:,.0f} ₾")
    else:
        print("სამწუხაროდ, ამჯერად ვერაფერს ვერ მოიგებთ.")

    logging.info(
        f"გათამაშება - გამარჯვებული: {winning_numbers}, მოთამაშის რიცხვები: {sorted(player_numbers)}, "
        f"დამთხვევა: {matches}, მოგება: {prize:,.0f} ₾"
    )


def show_menu():
    print("\n===== ლატარიის სიმულატორი =====")
    print("1. გათამაშებაში მონაწილეობა")
    print("2. გასვლა")


def main():
    logging.info("ლატარიის სესია დაიწყო")
    while True:
        show_menu()
        choice = input("აირჩიეთ მოქმედება (1-2): ")

        if choice == "1":
            play_round()
        elif choice == "2":
            print("ნახვამდის!")
            logging.info("ლატარიის სესია დასრულდა")
            break
        else:
            print("გთხოვთ, აირჩიოთ 1 ან 2.")


if __name__ == "__main__":
    main()
