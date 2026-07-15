books = [
    {"name": "1984", "writer": "ჯორჯ ორუელი", "date": 1949},
    {"name": "ჰარი პოტერი და ფილოსოფიური ქვა", "writer": "ჯოან როულინგი", "date": 1997},
    {"name": "დანაშაული და სასჯელი", "writer": "ფიოდორ დოსტოევსკი", "date": 1866},
    {"name": "ომი და მშვიდობა", "writer": "ლევ ტოლსტოი", "date": 1869},
    {"name": "პატარა უფლისწული", "writer": "ანტუან დე სენტ-ეგზიუპერი", "date": 1943},
    {"name": "ვეფხისტყაოსანი", "writer": "შოთა რუსთაველი", "date": 1189},
    {"name": "დათა თუთაშხია", "writer": "ჩაბუა ამირეჯიბი", "date": 1975},
    {"name": "ჰობიტი", "writer": "ჯ.რ.რ. ტოლკინი", "date": 1937},
    {"name": "ალქიმიკოსი", "writer": "პაულო კოელიო", "date": 1988},
    {"name": "ბრძოლის კლუბი", "writer": "ჩაკ პალანიკი", "date": 1996}
]


def print_books():
    print("\n===== წიგნების სია =====")

    if len(books) == 0:
        print("წიგნები არ არის ხელმისაწვდომი.")
        return

    for number, item in enumerate(books, 1):
        print(
            f"{number}) {item['name']} - {item['writer']} ({item['date']})"
        )
    print("წიგნების რაოდენობა:", len(books))


def insert_book():
    data = input("შეიყვანეთ წიგნის სახელი და ავტორი (/): ")
    published = input("შეიყვანეთ გამოცემის წელი: ")

    try:
        book_name, book_author = data.split("/")
    except ValueError:
        print("არასწორი ფორმატი!")
        return

    books.append({
        "name": book_name.strip(),
        "writer": book_author.strip(),
        "date": published
    })

    print("წიგნი წარმატებით დაემატა.")


def take_book():
    if not books:
        print("ბიბლიოთეკა ცარიელია.")
        return

    print_books()

    try:
        selected = int(input("აირჩიეთ წიგნის ნომერი: "))
        removed = books.pop(selected - 1)

        print(
            f"თქვენ აიღეთ წიგნი: {removed['name']}"
        )

    except (ValueError, IndexError):
        print("ასეთი წიგნი არ არსებობს.")


def find_book():
    text = input("შეიყვანეთ სახელი: ")

    result = [
        book for book in books
        if text.lower() in book["name"].lower()
    ]

    if result:
        print("\nნაპოვნი წიგნები:")
        for book in result:
            print(
                f"{book['name']} / {book['writer']} ({book['date']})"
            )
    else:
        print("წიგნი ვერ მოიძებნა.")


def menu():
    print("""
===== ბიბლიოთეკის მენიუ =====
1 - წიგნების ნახვა
2 - წიგნის დამატება
3 - წიგნის აღება
4 - ძებნა
5 - დასრულება
""")


def run_library():

    while True:
        menu()
        action = input("აირჩიეთ მოქმედება: ")

        if action == "1":
            print_books()

        elif action == "2":
            insert_book()

        elif action == "3":
            take_book()

        elif action == "4":
            find_book()

        elif action == "5":
            print("პროგრამა დასრულდა.")
            break

        else:
            print("არასწორი არჩევანი.")

run_library()
