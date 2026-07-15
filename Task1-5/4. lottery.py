import random
import logging


logging.basicConfig(
    filename="lottery_history.log",
    level=logging.INFO,
    format="%(asctime)s - %(message)s",
    encoding="utf-8"
)

MAX_PRIZE = 1000000


def create_winning_numbers():

    numbers = random.sample(range(1, 50),6)
    return sorted(numbers)


def enter_numbers():
    while True:
        try:
            user_input = input(
                "შეიყვანეთ 6 რიცხვი (1-49) space-ით: "
            )
            chosen = [
                int(number)
                for number in user_input.split()
            ]

            if len(chosen) != 6:
                print("უნდა შეიყვანოთ ზუსტად 6 რიცხვი.")
                continue

            if any(number < 1 or number > 49 for number in chosen):
                print("რიცხვები უნდა იყოს 1-დან 49-მდე.")
                continue

            if len(set(chosen)) != 6:
                print("რიცხვები არ უნდა მეორდებოდეს.")
                continue
            return sorted(chosen)

        except ValueError:
            print("შეიყვანეთ მხოლოდ რიცხვები.")


def find_matches(player, computer):
    return len(
        set(player) & set(computer)
    )


def get_reward(matches):
    prizes = {
        6: MAX_PRIZE,
        5: MAX_PRIZE * 0.60,
        4: MAX_PRIZE * 0.40,
        3: MAX_PRIZE * 0.20
    }

    return prizes.get(matches, 0)


def play_lottery():
    lucky_numbers = create_winning_numbers()
    user_numbers = enter_numbers()
    matched = find_matches(
        user_numbers,
        lucky_numbers
    )

    reward = get_reward(matched)
    print("\n===== შედეგი =====")
    print("გამარჯვებული ნომრები:", lucky_numbers)
    print("თქვენი ნომრები:",user_numbers)
    print("დამთხვევები:",matched)

    if reward:
        print(f"გილოცავთ! თქვენი მოგებაა {reward:,.0f} ₾")
    else:
        print("სამწუხაროდ, ვერ მოიგეთ.")

    logging.info(
        f"კომპიუტერი: {lucky_numbers}; "
        f"მოთამაშე: {user_numbers}; "
        f"დამთხვევა: {matched}; "
        f"მოგება: {reward}"
    )


def menu():
    print("""===== ლატარიის თამაში =====
1. ახალი გათამაშება
2. გამოსვლა
""")

def lottery_app():
    logging.info("ლატარიის პროგრამა დაიწყო")

    while True:
        menu()
        choice = input("აირჩიეთ მოქმედება: ")

        if choice == "1":
            play_lottery()
        elif choice == "2":
            print("ნახვამდის!")

            logging.info("ლატარიის პროგრამა დასრულდა")
            break
        else:
            print("აირჩიეთ მხოლოდ 1 ან 2.")

lottery_app()
