import re

stored_data = {
    "email": "user@mail.com",
    "nickname": "george777",
    "password": "password123",
}


def classify_input(raw):
    if raw == "":
        return "empty"

    if re.fullmatch(r"\s+", raw):
        return "only_spaces"

    if re.search(r"\s", raw):
        return "contains_spaces"

    if re.fullmatch(r"[0-9]+", raw):
        return "numeric"

    if re.fullmatch(r"[^a-zA-Zა-ჰА-Яа-я0-9]+", raw):
        return "symbols"

    if re.search(r"[ა-ჰ]", raw) or re.search(r"[а-яА-Я]", raw):
        return "other_language"

    if re.fullmatch(r"[A-Za-z0-9]+", raw) and re.search(r"[0-9]", raw) and re.search(r"[A-Za-z]", raw):
        return "mixed_alnum"

    if re.search(r"[A-Za-z]", raw) and re.search(r"[^a-zA-Z0-9]", raw):
        return "letters_with_symbols"

    if re.search(r"[A-Z]", raw):
        return "uppercase"

    if re.fullmatch(r"[a-z]+", raw):
        return "valid"

    return "unknown"


def get_error_message(category, raw):
    messages = {
        "empty": "ველი ცარიელია, გთხოვთ შემოიტანეთ string პატარა რეგისტრში.",
        "only_spaces": "შემოყვანილია მხოლოდ space, შემოიტანეთ მხოლოდ string პატარა რეგისტრში.",
        "contains_spaces": "ტექსტი შეიცავს space, შემოიტანეთ მხოლოდ გადაბმული string პატარა რეგისტრში.",
        "numeric": "შემოყვანილია რიცხვითი მნიშვნელობა, შემოიტანეთ მხოლოდ string პატარა რეგისტრში.",
        "symbols": "შემოყვანილია სიმბოლოები, შემოიტანეთ მხოლოდ string პატარა რეგისტრში.",
        "other_language": "შემოყვანილია სხვა ენის ასოები, გთხოვთ შემოიტანეთ მხოლოდ ლათინური ასოები პატარა რეგისტრში.",
        "mixed_alnum": "შემოყვანილია შერეული ტიპის მონაცემი (ასოები და ციფრები), შემოიტანეთ მხოლოდ string პატარა რეგისტრში.",
        "uppercase": "შემოყვანილია დიდი ასოები, გთხოვთ შემოიტანეთ მხოლოდ პატარა ლათინური ასოები.",
        "letters_with_symbols": "შემოყვანილია ასოები და სიმბოლოები ერთად, შემოიტანეთ მხოლოდ string პატარა რეგისტრში.",
        "unknown": "შემოყვანილია არასწორი ტიპის მონაცემი, შემოიტანეთ მხოლოდ string პატარა რეგისტრში.",
    }
    return messages[category]


def register_user():
    while True:
        raw = input("შეიყვანეთ სახელი: ")
        category = classify_input(raw)

        if category == "valid":
            print("\nრეგისტრაცია წარმატებით დასრულდა!")
            print("--- თქვენი მონაცემები ---")
            print(f"ელ-ფოსტა: {stored_data['email']}")
            print(f"სახელი: {raw}")
            print(f"ზედმეტსახელი: {stored_data['nickname']}")
            print(f"პაროლი: {stored_data['password']}")
            return
        else:
            print(get_error_message(category, raw))
            print("სცადეთ თავიდან.\n")


def main():
    print("===== რეგისტრაციის სიმულატორი =====")
    register_user()


if __name__ == "__main__":
    main()
