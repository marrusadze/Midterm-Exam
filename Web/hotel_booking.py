from __future__ import annotations

import json
import logging
import os
from datetime import datetime
from typing import List, Optional


LOG_FILE_PATH = os.path.join(os.path.dirname(__file__), "bookings.log")
HISTORY_FILE_PATH = os.path.join(os.path.dirname(__file__), "bookings_history.json")

logger = logging.getLogger("hotel_booking")
logger.setLevel(logging.INFO)

if not logger.handlers:
    file_handler = logging.FileHandler(LOG_FILE_PATH, encoding="utf-8")
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)



class Room:
    HIGH_SEASON_MONTHS = {6, 7, 8, 12}       # ზაფხული + დეკემბერი -> ძვირი
    LOW_SEASON_MONTHS = {1, 2, 11}           # ზამთრის მშვიდი პერიოდი -> იაფი
    HIGH_SEASON_MULTIPLIER = 1.3
    LOW_SEASON_MULTIPLIER = 0.85
    REGULAR_MULTIPLIER = 1.0

    def __init__(
        self,
        room_number: int,
        room_type: str,
        price_per_night: float,
        max_guests: int,
        is_available: bool = True,
    ):
        self.room_number = room_number
        self.room_type = room_type
        self.price_per_night = price_per_night
        self.is_available = is_available
        self.max_guests = max_guests

    def book_room(self) -> bool:
        # დაჯავშნისას is_available=False. აბრუნებს True თუ წარმატებული იყო
        if not self.is_available:
            return False
        self.is_available = False
        return True

    def release_room(self) -> None:
        # ოთახის გათავისუფლება (is_available=True).
        self.is_available = True

    def _get_seasonal_multiplier(self, reference_date: Optional[datetime] = None) -> float:
        # დააბრუნებს სეზონურ კოეფიციენტს მოცემული (ან მიმდინარე) თარიღისთვის.
        month = (reference_date or datetime.now()).month
        if month in self.HIGH_SEASON_MONTHS:
            return self.HIGH_SEASON_MULTIPLIER
        if month in self.LOW_SEASON_MONTHS:
            return self.LOW_SEASON_MULTIPLIER
        return self.REGULAR_MULTIPLIER

    def calculate_price(self, nights: int, reference_date: Optional[datetime] = None) -> float:
        # გამოთვლის ჯამურ ფასს ღამეების რაოდენობის და სეზონის მიხედვით.
        if nights <= 0:
            raise ValueError("ღამეების რაოდენობა უნდა იყოს დადებითი რიცხვი")

        multiplier = self._get_seasonal_multiplier(reference_date)
        total = self.price_per_night * nights * multiplier
        return round(total, 2)

    def __str__(self) -> str:
        status = "თავისუფალია" if self.is_available else "დაკავებულია"
        return (
            f"ოთახი #{self.room_number} | ტიპი: {self.room_type} | "
            f"ფასი: {self.price_per_night}$/ღამე | ტევადობა: {self.max_guests} სტუმარი | "
            f"სტატუსი: {status}"
        )

    def __repr__(self) -> str:
        return f"Room({self.room_number}, {self.room_type!r})"


class Customer:
    POINTS_PER_DOLLAR = 0.1  # 1 ქულა ყოველ 10$-ზე

    def __init__(self, name: str, budget: float):
        self.name = name
        self.budget = budget
        self.booked_rooms: List[Room] = []
        self.reward_points: int = 0

    def add_room(self, room: Room) -> None:
        # ოთახის დამატება მომხმარებლის დაჯავშნილ სიაში.
        if room not in self.booked_rooms:
            self.booked_rooms.append(room)

    def remove_room(self, room: Room) -> None:
        # ოთახის წაშლა მომხმარებლის დაჯავშნილი ოთახებიდან.
        if room in self.booked_rooms:
            self.booked_rooms.remove(room)

    def pay_for_booking(self, total_price: float) -> bool:
        if total_price < 0:
            raise ValueError("ფასი არ შეიძლება იყოს უარყოფითი")

        if self.budget < total_price:
            return False

        self.budget -= total_price
        earned_points = int(total_price * self.POINTS_PER_DOLLAR)
        self.reward_points += earned_points
        return True

    def refund_booking(self, refund_amount: float) -> None:
        # უბრუნებს მომხმარებელს თანხას და აკლებს შესაბამის ქულებს.
        self.budget += refund_amount
        lost_points = int(refund_amount * self.POINTS_PER_DOLLAR)
        self.reward_points = max(0, self.reward_points - lost_points)

    def show_booking_summary(self) -> str:
        if not self.booked_rooms:
            return f"{self.name}-ს არ აქვს დაჯავშნილი ოთახები."

        lines = [f"{self.name}-ს აქტიური დაჯავშნები:"]
        for room in self.booked_rooms:
            lines.append(f"  - {room}")
        lines.append(f"მიმდინარე ბიუჯეტი: {round(self.budget, 2)}$")
        lines.append(f"დაგროვილი ქულები: {self.reward_points}")
        return "\n".join(lines)

    def __str__(self) -> str:
        return f"Customer({self.name}, ბიუჯეტი: {self.budget}$, ქულები: {self.reward_points})"


class Hotel:
    def __init__(self, name: str, rooms: Optional[List[Room]] = None):
        self.name = name
        self.rooms: List[Room] = rooms if rooms is not None else []
        self.bookings_log: List[dict] = []

    def add_room(self, room: Room) -> None:
        """ოთახის დამატება სასტუმროში (დამხმარე მეთოდი)."""
        self.rooms.append(room)

    def find_room(self, room_number: int) -> Optional[Room]:
        """ოთახის მოძებნა ნომრით."""
        for room in self.rooms:
            if room.room_number == room_number:
                return room
        return None

    def show_available_rooms(self, room_type: Optional[str] = None) -> List[Room]:
        # აბრუნებს თავისუფალი ოთახების სიას, სურვილისამებრ გაფილტრულს ტიპის მიხედვით.
        available = [room for room in self.rooms if room.is_available]
        if room_type:
            available = [room for room in available if room.room_type.lower() == room_type.lower()]
        return available

    def calculate_total_booking(self, room_number: int, nights: int) -> float:
        # გამოთვლის ჯამურ ღირებულებას კონკრეტული ოთახისთვის.
        room = self.find_room(room_number)
        if room is None:
            raise ValueError(f"ოთახი ნომრით {room_number} ვერ მოიძებნა")
        return room.calculate_price(nights)

    def book_room_for_customer(self, customer: Customer, room_number: int, nights: int) -> bool:
        """
        ჯავშნის კონკრეტულ ოთახს მომხმარებლისთვის, თუ:
            1. ოთახი არსებობს და თავისუფალია
            2. მომხმარებელს აქვს საკმარისი ბიუჯეტი

        აბრუნებს True, თუ დაჯავშნა წარმატებით შესრულდა, სხვა შემთხვევაში False.
        """
        room = self.find_room(room_number)
        if room is None or not room.is_available:
            logger.warning(
                # წარუმატებელი დაჯავშნის მცდელობა: ოთახი #%s არ არის ხელმისაწვდომი (მომხმარებელი: %s)
                room_number,
                customer.name,
            )
            return False

        total_price = room.calculate_price(nights)

        if not customer.pay_for_booking(total_price):
            logger.warning(
                # წარუმატებელი დაჯავშნა - არასაკმარისი ბიუჯეტი: %s საჭიროებს %s$, აქვს %s$
                customer.name,
                total_price,
                customer.budget,
            )
            return False

        room.book_room()
        customer.add_room(room)
        self.log_booking(customer, room, total_price)
        return True

    def cancel_booking(self, customer: Customer, room_number: int) -> bool:
        room = self.find_room(room_number)
        if room is None or room not in customer.booked_rooms:
            logger.warning(
                # გაუქმების მცდელობა ვერ განხორციელდა: ოთახი #%s არ იძებნება მომხმარებელთან %s
                room_number,
                customer.name,
            )
            return False

        room.release_room()
        customer.remove_room(room)

        # ვეძებთ ბოლო აქტიურ ჩანაწერს ამ ოთახზე და მომხმარებელზე
        refund = next(
            (entry["total_price"] for entry in reversed(self.bookings_log)
             if entry["room_number"] == room_number and entry["customer"] == customer.name),
            0.0,
        )

        # ვიყენებთ ახალ მეთოდს ბიუჯეტის და ქულების კორექტირებისთვის
        customer.refund_booking(refund)

        logger.info(
            "დაჯავშნა გაუქმდა და ქულები დაკორექტირდა: ოთახი #%s, მომხმარებელი %s, დაბრუნებული თანხა: %s$",
            room_number,
            customer.name,
            refund,
        )
        return True

    def log_booking(self, customer: Customer, room: Room, total_price: float) -> None:
        # ლოგავს დაჯავშნას და ინახავს ისტორიაში (in-memory + JSON ფაილში).
        entry = {
            "timestamp": datetime.now().isoformat(),
            "customer": customer.name,
            "room_number": room.room_number,
            "room_type": room.room_type,
            "total_price": total_price,
        }
        self.bookings_log.append(entry)

        logger.info(
            # დაჯავშნა შესრულდა: მომხმარებელი=%s, ოთახი=#%s (%s), ჯამური ფასი=%s$
            customer.name,
            room.room_number,
            room.room_type,
            total_price,
        )

        self._save_history_to_file()

    def _save_history_to_file(self) -> None:
        # ინახავს bookings_log-ს JSON ფაილში.
        try:
            with open(HISTORY_FILE_PATH, "w", encoding="utf-8") as f:
                json.dump(self.bookings_log, f, ensure_ascii=False, indent=2)
        except OSError as exc:
            logger.error("ისტორიის ფაილში შენახვა ვერ მოხერხდა: %s", exc)

    def __str__(self) -> str:
        return f"Hotel({self.name}, ოთახები: {len(self.rooms)}, დაჯავშნები: {len(self.bookings_log)})"


if __name__ == "__main__":
    hotel = Hotel("Tbilisi Grand Hotel")
    hotel.add_room(Room(101, "Single", 50.0, max_guests=1))
    hotel.add_room(Room(102, "Double", 80.0, max_guests=2))
    hotel.add_room(Room(201, "Suite", 150.0, max_guests=4))

    print("=== ხელმისაწვდომი ოთახები ===")
    for r in hotel.show_available_rooms():
        print(r)

    customer = Customer("გიორგი მამულაძე", budget=300.0)

    print("\n=== დაჯავშნის მცდელობა ===")
    success = hotel.book_room_for_customer(customer, room_number=102, nights=2)
    print("დაჯავშნა წარმატებულია!" if success else "დაჯავშნა ვერ მოხერხდა.")

    print("\n" + customer.show_booking_summary())

    print("\n=== დაჯავშნის გაუქმება ===")
    hotel.cancel_booking(customer, room_number=102)
    print(customer.show_booking_summary())
