import logging

logging.basicConfig(
    filename="bank_operations.log",
    level=logging.INFO,
    format="%(asctime)s | %(message)s",
    encoding="utf-8"
)


account_money = 10000
DEPOSIT_LIMIT = 1000


def show_balance():
    print(f"\nმიმდინარე ბალანსი: {account_money} ₾")

    logging.info(
        f"ბალანსის შემოწმება: {account_money} ₾"
    )



def take_money(value):

    global account_money

    if value <= 0:
        print("თანხა უნდა იყოს დადებითი.")
        return


    if value > account_money:
        print("შეცდომა: არასაკმარისი თანხა ანგარიშზე.")
        logging.info(f"გატანის უარყოფა: {value} ₾, ბალანსი {account_money} ₾")
        return


    account_money -= value
    print(f"თქვენ გაიტანეთ {value} ₾")
    print(f"დარჩენილი თანხა: {account_money} ₾")

    logging.info(f"თანხის გატანა: {value} ₾. ახალი ბალანსი: {account_money} ₾")

def add_money(value):
    global account_money
    if value <= 0:
        print("თანხა უნდა იყოს დადებითი.")
        return

    if value > DEPOSIT_LIMIT:
        print(f"ერთჯერადად შეგიძლიათ შეიტანოთ მაქსიმუმ {DEPOSIT_LIMIT} ₾")

        logging.info(f"დეპოზიტის შეცდომა: {value} ₾")
        return

    account_money += value
    print(f"თქვენ შეიტანეთ {value} ₾")
    print(f"ახალი ბალანსი: {account_money} ₾")

    logging.info(f"თანხის შეტანა: {value} ₾. ახალი ბალანსი: {account_money} ₾")


def print_menu():

    print("""===== ბანკომატის სისტემა =====
1. ბალანსის ნახვა
2. თანხის გატანა
3. თანხის შეტანა
4. გასვლა
""")

def atm_program():

    logging.info("ATM პროგრამა ჩაირთო")

    while True:
        print_menu()
        option = input("აირჩიეთ ოპერაცია: ")

        if option == "1":
            show_balance()
        elif option == "2":
            try:
                money = float(input("რამდენის გატანა გსურთ? "))
                take_money(money)

            except ValueError:
                print("შეიყვანეთ მხოლოდ რიცხვი.")

        elif option == "3":
            try:
                money = float(input("რამდენის შეტანა გსურთ? "))
                add_money(money)
            except ValueError:
                print("შეიყვანეთ მხოლოდ რიცხვი.")

        elif option == "4":
            print("მადლობა სარგებლობისთვის!")
            logging.info("ATM პროგრამა დასრულდა")
            break
        else:
            print("არასწორი არჩევანი.")

atm_program()
