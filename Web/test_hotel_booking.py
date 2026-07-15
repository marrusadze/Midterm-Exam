import unittest

from hotel_booking import Room, Customer, Hotel


class TestCustomerPayForBooking(unittest.TestCase):
    def setUp(self):
        self.customer = Customer(name="ნინო", budget=500.0)

    def test_successful_payment_reduces_budget_correctly(self):
        result = self.customer.pay_for_booking(200.0)
        self.assertTrue(result)
        self.assertEqual(self.customer.budget, 300.0)

    def test_payment_fails_when_budget_is_insufficient(self):
        result = self.customer.pay_for_booking(1000.0)
        self.assertFalse(result)
        self.assertEqual(self.customer.budget, 500.0)

    def test_exact_budget_amount_is_allowed(self):
        result = self.customer.pay_for_booking(500.0)
        self.assertTrue(result)
        self.assertEqual(self.customer.budget, 0.0)


class TestHotelBookRoomForCustomer(unittest.TestCase):

    def setUp(self):
        self.hotel = Hotel("Test Hotel")
        self.available_room = Room(1, "Single", 50.0, max_guests=1, is_available=True)
        self.booked_room = Room(2, "Double", 90.0, max_guests=2, is_available=False)
        self.hotel.add_room(self.available_room)
        self.hotel.add_room(self.booked_room)
        self.customer = Customer("დავითი", budget=1000.0)

    def test_booking_succeeds_for_available_room(self):
        result = self.hotel.book_room_for_customer(self.customer, room_number=1, nights=2)
        self.assertTrue(result)
        self.assertFalse(self.available_room.is_available)
        self.assertIn(self.available_room, self.customer.booked_rooms)

    def test_booking_fails_for_already_booked_room(self):
        result = self.hotel.book_room_for_customer(self.customer, room_number=2, nights=1)
        self.assertFalse(result)
        self.assertFalse(self.booked_room.is_available)
        self.assertNotIn(self.booked_room, self.customer.booked_rooms)

    def test_booking_fails_for_nonexistent_room(self):
        result = self.hotel.book_room_for_customer(self.customer, room_number=999, nights=1)
        self.assertFalse(result)


if __name__ == "__main__":
    unittest.main(verbosity=2)
