import logging

logging.basicConfig(
    filename="atm_log.log",
    level=logging.INFO,
    format="%(asctime)s - %(message)s",
    encoding="utf-8",
)

balance = 10000

MAX_DEPOSIT = 1000


def check_balance():
    print(f"თქვენი ბალანსია: {balance} ₾")
    logging.info(f"ბალანსის შემოწმება. მიმდინარე ბალანსი: {balance} ₾")


def withdraw(amount):
    global balance
    if amount > balance:
        print(f"შეცდომა: თანხის გატანა ვერ მოხერხდა. ბალანსზე მეტის გატანა არ შეიძლება (ბალანსი: {balance} ₾).")
        logging.info(f"წარუმატებელი გატანა: მოთხოვნილი {amount} ₾, ბალანსი {balance} ₾")
        return

    balance -= amount
    print(f"წარმატებით გაიტანეთ {amount} ₾. ახალი ბალანსი: {balance} ₾")
    logging.info(f"გატანა: {amount} ₾. ახალი ბალანსი: {balance} ₾")


def deposit(amount):
    global balance
    if amount > MAX_DEPOSIT:
        print(f"შეცდომა: ერთჯერადად ვერ შემოიტანთ {MAX_DEPOSIT} ₾-ზე მეტს.")
        logging.info(f"წარუმატებელი შემოტანა: მოთხოვნილი {amount} ₾ (ლიმიტი {MAX_DEPOSIT} ₾)")
        return

    balance += amount
    print(f"წარმატებით შემოიტანეთ {amount} ₾. ახალი ბალანსი: {balance} ₾")
    logging.info(f"შემოტანა: {amount} ₾. ახალი ბალანსი: {balance} ₾")


def show_menu():
    print("\n===== ბანკომატი =====")
    print("1. ბალანსის ნახვა")
    print("2. თანხის გატანა")
    print("3. თანხის შემოტანა")
    print("4. გასვლა")


def main():
    logging.info("ბანკომატის სესია დაიწყო")
    while True:
        show_menu()
        choice = input("აირჩიეთ მოქმედება (1-4): ")

        if choice == "1":
            check_balance()
        elif choice == "2":
            amount = float(input("შეიყვანეთ გასატანი თანხა (₾): "))
            withdraw(amount)
        elif choice == "3":
            amount = float(input("შეიყვანეთ შესატანი თანხა (₾): "))
            deposit(amount)
        elif choice == "4":
            print("მადლობთ, რომ სარგებლობთ ჩვენი ბანკომატით!")
            logging.info("ბანკომატის სესია დასრულდა")
            break
        else:
            print("გთხოვთ, აირჩიოთ 1-დან 4-მდე მნიშვნელობა.")


if __name__ == "__main__":
    main()
