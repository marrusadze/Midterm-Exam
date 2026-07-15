import unittest

from hotel_booking import Room, Customer, Hotel

class TestCustomerPayForBooking(unittest.TestCase):
    def setUp(self):
        self.customer = Customer("ნინო", 500.0)

    def test_payment_success(self):
        result = self.customer.pay_for_booking(200)
        self.assertTrue(result)
        self.assertEqual(self.customer.budget, 300)


    def test_payment_without_enough_money(self):
        result = self.customer.pay_for_booking(1000)
        self.assertFalse(result)
        self.assertEqual(self.customer.budget, 500)


    def test_payment_all_budget(self):
        result = self.customer.pay_for_booking(500)
        self.assertTrue(result)
        self.assertEqual(self.customer.budget, 0)


class TestHotelBooking(unittest.TestCase):
    def setUp(self):
        self.hotel = Hotel("Test Hotel")
        self.room = Room(1, "Single", 50, 1)

        self.busy_room = Room(2, "Double", 90, 2)

        self.busy_room.is_available = False
        self.hotel.add_room(self.room)
        self.hotel.add_room(self.busy_room)

        self.customer = Customer("დავითი", 1000)


    def test_booking_available_room(self):
        result = self.hotel.book_room_for_customer(self.customer, 1, 2)
        self.assertTrue(result)
        self.assertFalse(self.room.is_available)
        self.assertIn(self.room, self.customer.booked_rooms)


    def test_booking_busy_room_fails(self):
        result = self.hotel.book_room_for_customer(self.customer, 2, 1)
        self.assertFalse(result)
        self.assertNotIn(
            self.busy_room,
            self.customer.booked_rooms
        )


    def test_booking_unknown_room(self):
        result = self.hotel.book_room_for_customer(self.customer, 999, 1)
        self.assertFalse(result)


if __name__ == "__main__":
    unittest.main(verbosity=2)
