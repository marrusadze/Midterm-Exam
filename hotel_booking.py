import logging
from datetime import datetime


logging.basicConfig(
    filename="bookings.log",
    level=logging.INFO,
    format="%(asctime)s - %(message)s",
    encoding="utf-8"
)


class Room:
    def __init__(self, room_number, room_type, price_per_night, max_guests):
        self.room_number = room_number
        self.room_type = room_type
        self.price_per_night = price_per_night
        self.is_available = True
        self.max_guests = max_guests

    def book_room(self):
        if self.is_available:
            self.is_available = False
            return True
        return False

    def release_room(self):
        self.is_available = True

    def calculate_price(self, nights):
        month = datetime.now().month

        price = self.price_per_night * nights

        # მაღალი სეზონი
        if month in [6, 7, 8, 12]:
            price *= 1.3

        # დაბალი სეზონი
        elif month in [1, 2, 11]:
            price *= 0.85

        return round(price, 2)

    def __str__(self):
        status = "თავისუფალი" if self.is_available else "დაკავებული"

        return (
            f"ოთახი №{self.room_number} | "
            f"{self.room_type} | "
            f"{self.price_per_night}$/ღამე | "
            f"{self.max_guests} სტუმარი | "
            f"{status}"
        )


class Customer:
    def __init__(self, name, budget):
        self.name = name
        self.budget = budget
        self.booked_rooms = []
        self.reward_points = 0

    def add_room(self, room):
        self.booked_rooms.append(room)

    def remove_room(self, room):
        if room in self.booked_rooms:
            self.booked_rooms.remove(room)

    def pay_for_booking(self, total_price):
        if self.budget >= total_price:
            self.budget -= total_price

            # ყოველ 10$-ზე 1 ქულა
            self.reward_points += int(total_price / 10)
            return True
        return False

    def show_booking_summary(self):
        if not self.booked_rooms:
            return f"{self.name}-ს დაჯავშნები არ აქვს."

        result = f"მომხმარებელი: {self.name}\n"
        result += "დაჯავშნილი ოთახები:\n"

        for room in self.booked_rooms:
            result += str(room) + "\n"

        result += f"ბიუჯეტი: {self.budget}$\n"
        result += f"ქულები: {self.reward_points}"

        return result


class Hotel:
    def __init__(self, name):
        self.name = name
        self.rooms = []
        self.bookings_log = []

    def add_room(self, room):
        self.rooms.append(room)

    def show_available_rooms(self, room_type=None):
        available = []

        for room in self.rooms:
            if room.is_available:
                if room_type is None or room.room_type == room_type:
                    available.append(room)
        return available

    def find_room(self, room_number):
        for room in self.rooms:
            if room.room_number == room_number:
                return room
        return None

    def calculate_total_booking(self, room_number, nights):
        room = self.find_room(room_number)
        if room:
            return room.calculate_price(nights)
        return 0

    def book_room_for_customer(self, customer, room_number, nights):
        room = self.find_room(room_number)
        if room is None:
            return False
        if not room.is_available:
            return False
        total_price = self.calculate_total_booking(
            room_number,
            nights
        )

        if customer.pay_for_booking(total_price):
            room.book_room()
            customer.add_room(room)
            self.log_booking(
                customer,
                room,
                total_price
            )
            return True
        return False

    def log_booking(self, customer, room, total_price):
        booking = {
            "customer": customer.name,
            "room": room.room_number,
            "price": total_price,
            "date": datetime.now().strftime("%Y-%m-%d")
        }
        self.bookings_log.append(booking)

        logging.info(
            f"Booking: {customer.name}, "
            f"Room {room.room_number}, "
            f"Price {total_price}$"
        )

    def cancel_booking(self, customer, room_number):
        room = self.find_room(room_number)
        if room and room in customer.booked_rooms:
            room.release_room()
            customer.remove_room(room)

            logging.info(
                f"Cancelled: {customer.name}, "
                f"Room {room_number}"
            )
            return True
        return False


# პროგრამის ტესტირება

hotel = Hotel("Tbilisi Grand Hotel")

hotel.add_room(Room(101, "Single", 50, 1))

hotel.add_room(Room(102, "Double", 80, 2))

hotel.add_room(Room(201, "Suite", 150, 4))


print("=== თავისუფალი ოთახები ===")

for room in hotel.show_available_rooms():
    print(room)

customer = Customer("გიორგი", 300)

print("\n=== დაჯავშნა ===")

result = hotel.book_room_for_customer(customer, 102, 2)


if result:
    print("დაჯავშნა წარმატებულია")
else:
    print("დაჯავშნა ვერ შესრულდა")


print("\n=== მომხმარებლის ინფორმაცია ===")

print(customer.show_booking_summary())

print("\n=== გაუქმება ===")

hotel.cancel_booking(customer, 102)

print(customer.show_booking_summary())
