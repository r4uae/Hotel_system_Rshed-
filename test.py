# testing.py
from person import Guest, Staff
from room import Room, RoomType
from service import Service
from booking import Booking
from payment import Payment, Invoice
from hotel import Hotel

# Constants for discounts and taxes
LOYALTY_POINTS_PER_NIGHT = 10
LOYALTY_REDEMPTION_RATE = 0.05  # 5% discount per 100 points
TAX_RATE = 0.10  # 10% tax

# Create room types
single_type = RoomType("Single", "Single bed room", 1)
double_type = RoomType("Double", "Double bed room", 2)
suite_type = RoomType("Suite", "Luxury suite with living area", 4)

# Create rooms
room101 = Room("101", single_type, ["Wi-Fi", "TV"], 99.99)
room201 = Room("201", double_type, ["Wi-Fi", "TV", "Mini-bar"], 149.99)
room301 = Room("301", suite_type, ["Wi-Fi", "TV", "Mini-bar", "Jacuzzi"], 299.99)

# Create services
room_service = Service("SRV001", "Room Service", 15.99)
laundry = Service("SRV002", "Laundry", 9.99)
airport_transfer = Service("SRV003", "Airport Transfer", 29.99)

# Create a hotel
royal_stay = Hotel("Royal Stay Hotel")

# Add room types to hotel
royal_stay.add_room_type(single_type)
royal_stay.add_room_type(double_type)
royal_stay.add_room_type(suite_type)

# Add rooms to hotel
royal_stay.add_room(room101)
royal_stay.add_room(room201)
royal_stay.add_room(room301)

# Add services to hotel
royal_stay.add_service(room_service)
royal_stay.add_service(laundry)
royal_stay.add_service(airport_transfer)

# Create guests
guest1 = Guest("Alyazia Saeed", "555-0101", "alyazia@email.com", "G001")  # Regular guest
guest2 = Guest("Mariam Abdulla", "555-0102", "mariam@email.com", "G002")  # Loyal guest with points

# Add loyalty points to guest2
guest2.add_loyalty_points(500)  # 500 points = 25% discount (500 * 0.05)

# Register guests to hotel
royal_stay.add_guest(guest1)
royal_stay.add_guest(guest2)

# Create staff
staff1 = Staff("Salama Ali", "555-0201", "salama@royalstay.com", "S001", "Receptionist", "Front Desk")
staff2 = Staff("Mohammed Ahmed", "555-0202", "mohammed@royalstay.com", "S002", "Manager", "Management")

# Add staff to hotel
royal_stay.add_staff(staff1)
royal_stay.add_staff(staff2)

# Test dates
from datetime import date, timedelta
today = date.today()
tomorrow = today + timedelta(days=1)
next_week = today + timedelta(days=7)

# Make bookings
# Booking 1: Regular guest, single room
booking1 = royal_stay.make_booking("G001", "101", tomorrow, tomorrow + timedelta(days=3))

# Booking 2: Loyal guest, suite with services
booking2 = royal_stay.make_booking("G002", "301", tomorrow, tomorrow + timedelta(days=2))
royal_stay.add_service_to_booking(booking2._booking_id, "SRV001")  # Room service
royal_stay.add_service_to_booking(booking2._booking_id, "SRV003")  # Airport transfer

# Booking 3: Long stay with multiple services
booking3 = royal_stay.make_booking("G002", "201", next_week, next_week + timedelta(days=5))
royal_stay.add_service_to_booking(booking3._booking_id, "SRV001")  # Room service
royal_stay.add_service_to_booking(booking3._booking_id, "SRV002")  # Laundry
royal_stay.add_service_to_booking(booking3._booking_id, "SRV002")  # Laundry again

# Process payments
# Payment for booking1 (no discount)
payment1 = royal_stay.process_payment(booking1._booking_id, booking1._total_cost, "Credit Card")

# Payment for booking2 (loyalty discount)
# Calculate discount (500 points * 0.05 = 25% discount)
discounted_amount2 = booking2._total_cost * 0.75
payment2 = royal_stay.process_payment(booking2._booking_id, discounted_amount2, "Debit Card")

# Payment for booking3 (bulk discount for long stay)
discounted_amount3 = booking3._total_cost * 0.90  # 10% discount
payment3 = royal_stay.process_payment(booking3._booking_id, discounted_amount3, "Cash")

# Create service requests
request1 = royal_stay.create_service_request("G001", "SRV002")  # Laundry request
request2 = royal_stay.create_service_request("G002", "SRV001")  # Room service request

# Fulfill some requests
request1.fulfill_request()

# Display information
print("----- Hotel Information -----")
print(royal_stay)
print("\n----- Staff Members -----")
print(staff1)
print(staff2)

print("\n----- Guest Information -----")
print(guest1)
print(guest2)

print("\n----- Booking Details -----")
print(f"Booking 1:\n{booking1}")
print(f"\nBooking 2:\n{booking2}")
print(f"\nBooking 3:\n{booking3}")

print("\n----- Payment Information -----")
print(f"Payment 1:\n{payment1}")
print(f"\nPayment 2:\n{payment2}")
print(f"\nPayment 3:\n{payment3}")

print("\n----- Invoices -----")
invoice1 = royal_stay.get_invoice(booking1._booking_id)
print(f"Invoice for Booking 1:\n{invoice1.generate_invoice()}")

invoice2 = royal_stay.get_invoice(booking2._booking_id)
print(f"\nInvoice for Booking 2:\n{invoice2.generate_invoice()}")

invoice3 = royal_stay.get_invoice(booking3._booking_id)
print(f"\nInvoice for Booking 3:\n{invoice3.generate_invoice()}")

print("\n----- Service Requests -----")
print(f"Request 1:\n{request1}")
print(f"\nRequest 2:\n{request2}")

print("\n----- Room Availability -----")
available_rooms = royal_stay.find_available_rooms(tomorrow, next_week)
print(f"Available rooms between {tomorrow} and {next_week}:")
for room in available_rooms:
    print(f"- {room._room_number} ({room._room_type._type_name})")

# Test cancellation
print("\n----- Testing Cancellation -----")
print(f"Before cancellation - Room 101 available: {room101.is_available}")
royal_stay.cancel_booking(booking1._booking_id)
print(f"After cancellation - Room 101 available: {room101.is_available}")
print(f"Booking 1 status: {booking1._status}")
print(f"Payment 1 status: {payment1._status}")