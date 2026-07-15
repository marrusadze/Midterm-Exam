library = [
    {"title": "1984", "author": "ჯორჯ ორუელი", "year": 1949},
    {"title": "ჰარი პოტერი და ფილოსოფიური ქვა", "author": "ჯოან როულინგი", "year": 1997},
    {"title": "დანაშაული და სასჯელი", "author": "ფიოდор დოსტოევსკი", "year": 1866},
    {"title": "ომი და მშვიდობა", "author": "ლევ ტოლსტოი", "year": 1869},
    {"title": "პატარა უფლისწული", "author": "ანტუან დე სენტ-ეგზიუპერი", "year": 1943},
    {"title": "ვეფხისტყაოსანი", "author": "შოთა რუსთაველი", "year": 1189},
    {"title": "დათა თუთაშხია", "author": "ჩაბუა ამირეჯიბი", "year": 1975},
    {"title": "ჰობიტი", "author": "ჯ.რ.რ. ტოლკინი", "year": 1937},
    {"title": "ალქიმიკოსი", "author": "პაულო კოელიო", "year": 1988},
    {"title": "ბრძოლის კლუბი", "author": "ჩაკ პალანიკი", "year": 1996},
]


def show_books():
    print("\n--- ბიბლიოთეკაში არსებული წიგნები ---")
    if not library:
        print("ბიბლიოთეკა ცარიელია.")
        return
    for i, book in enumerate(library, start=1):
        print(f"{i}. {book['title']} / {book['author']} ({book['year']})")
    print(f"სულ: {len(library)} წიგნი")


def add_book():
    raw = input("შეიყვანეთ წიგნი ფორმატით სახელი/ავტორი: ")
    year = input("შეიყვანეთ გამოცემის წელი: ")

    title, author = raw.split("/")

    new_book = {
        "title": title,
        "author": author,
        "year": year,
    }
    library.append(new_book)
    print(f"წიგნი „{new_book['title']}“ დაემატა ბიბლიოთეკას. ახლა ბიბლიოთეკაში სულ {len(library)} წიგნია.")


def borrow_book():
    if not library:
        print("ბიბლიოთეკა ცარიელია.")
        return

    show_books()
    choice = int(input("აირჩიეთ წიგნის ნომერი, რომლის წაღებაც გსურთ: "))

    index = choice - 1
    book = library.pop(index)
    print(f"წიგნი „{book['title']}“ გაიტანეთ წასაკითხად. სასიამოვნო კითხვას გისურვებთ!")


def search_book():
    print("\n--- წიგნის მოძებნა სათაურით ---")
    query = input("შეიყვანეთ წიგნის სათაური: ")

    found_books = []
    for book in library:
        if query in book["title"]:
            found_books.append(book)

    if not found_books:
        print("სამწუხაროდ, წიგნი ამ სათაურით ვერ მოიძებნა.")
    else:
        print(f"\nმოიძებნა {len(found_books)} წიგნი:")
        for i, book in enumerate(found_books, start=1):
            print(f"{i}. {book['title']} / {book['author']} ({book['year']})")


def show_menu():
    print("\n===== მინი-ბიბლიოთეკა =====")
    print("1. ყველა წიგნის ნახვა")
    print("2. ახალი წიგნის დამატება")
    print("3. წიგნის აღება წასაკითხად")
    print("4. წიგნის მოძებნა სათაურით")
    print("5. გასვლა")


def main():
    while True:
        show_menu()
        choice = input("აირჩიეთ მოქმედება (1-5): ")

        if choice == "1":
            show_books()
        elif choice == "2":
            add_book()
        elif choice == "3":
            borrow_book()
        elif choice == "4":
            search_book()
        elif choice == "5":
            print("ნახვამდის!")
            break
        else:
            print("გთხოვთ, აირჩიოთ 1-დან 5-მდე მნიშვნელობა.")


if __name__ == "__main__":
    main()