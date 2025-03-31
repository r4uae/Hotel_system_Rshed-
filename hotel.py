from datetime import date, timedelta
from typing import List, Dict
from booking import Booking
from payment import Payment, Invoice
from service import Service, ServiceRequest

class Hotel:
    """Main class representing the hotel management system"""
    
    def __init__(self, name):
        """
        Initialize the Hotel object
        
        Args:
            name: Name of the hotel
        """
        self._name = name
        self._rooms = []
        self._guests = {}
        self._staff = {}
        self._services = []
        self._room_types = []
        self._bookings = {}
        self._payments = {}
        self._invoices = {}
    
    def get_name(self):
        """Get the hotel name"""
        return self._name
    
    def add_room_type(self, room_type):
        """Add a room type to the hotel"""
        if room_type not in self._room_types:
            self._room_types.append(room_type)
    
    def add_room(self, room):
        """Add a room to the hotel"""
        if room not in self._rooms:
            self._rooms.append(room)
    
    def add_guest(self, guest):
        """Add a guest to the hotel system"""
        if guest.get_guest_id() not in self._guests:
            self._guests[guest.get_guest_id()] = guest
    
    def add_staff(self, staff):
        """Add a staff member to the hotel"""
        if staff.get_staff_id() not in self._staff:
            self._staff[staff.get_staff_id()] = staff
    
    def add_service(self, service):
        """Add a service to the hotel"""
        if service not in self._services:
            self._services.append(service)
    
    def find_available_rooms(self, check_in, check_out, room_type=None):
        """
        Find available rooms for given dates and optional room type
        """
        available_rooms = []
        for room in self._rooms:
            if room.check_availability(check_in, check_out):
                if room_type is None or room.get_room_type().get_type_name().lower() == room_type.lower():
                    available_rooms.append(room)
        return available_rooms
    
    def make_booking(self, guest_id, room_number, check_in, check_out):
        """
        Make a booking for a guest
        """
        guest = self._guests.get(guest_id)
        if guest is None:
            raise ValueError("Guest not found")
        
        room = next((r for r in self._rooms if r.get_room_number() == room_number), None)
        if room is None:
            raise ValueError("Room not found")
        
        if not room.check_availability(check_in, check_out):
            raise ValueError("Room not available for selected dates")
        
        booking = Booking(guest, room, check_in, check_out)
        self._bookings[booking.get_booking_id()] = booking
        
        # Add loyalty points (e.g., 10 points per night)
        nights = (check_out - check_in).days
        guest.add_loyalty_points(nights * 10)
        
        return booking
    
    def add_service_to_booking(self, booking_id, service_id):
        """
        Add a service to an existing booking
        """
        booking = self._bookings.get(booking_id)
        if booking is None:
            raise ValueError("Booking not found")
        
        service = next((s for s in self._services if s.get_service_id() == service_id), None)
        if service is None:
            raise ValueError("Service not found")
        
        booking.add_service(service)
    
    def process_payment(self, booking_id, amount, method):
        """
        Process payment for a booking
        
        Args:
            booking_id: Booking ID
            amount: Payment amount
            method: Payment method
            
        Returns:
            Payment: The payment object
        """
        booking = self._bookings.get(booking_id)
        if booking is None:
            raise ValueError("Booking not found")
        
        payment = Payment(booking, amount, method)
        payment.process_payment()
        self._payments[payment.get_payment_id()] = payment
        
        # Generate invoice
        invoice = Invoice(payment)
        self._invoices[invoice.get_invoice_id()] = invoice
        
        return payment
    
    def cancel_booking(self, booking_id):
        """
        Cancel a booking
        """
        booking = self._bookings.get(booking_id)
        if booking is None:
            raise ValueError("Booking not found")
        
        booking.cancel_booking()
        
        # Process refund if payment was made
        payment = next((p for p in self._payments.values() if p.get_booking().get_booking_id() == booking_id), None)
        if payment and payment.get_status() == "Completed":
            payment.refund_payment()
    
    def create_service_request(self, guest_id, service_id):
        """
        Create a service request for a guest
        
        Args:
            guest_id: Guest ID
            service_id: Service ID
            
        Returns:
            ServiceRequest: The created service request
        """
        guest = self._guests.get(guest_id)
        if guest is None:
            raise ValueError("Guest not found")
        
        service = next((s for s in self._services if s.get_service_id() == service_id), None)
        if service is None:
            raise ValueError("Service not found")
        
        if not service.is_available():
            raise ValueError("Service is not currently available")
        
        request = ServiceRequest(guest, service)
        return request
    
    def get_guest_bookings(self, guest_id):
        """
        Get all bookings for a guest
        
        Args:
            guest_id: Guest ID
            
        Returns:
            List[Booking]: List of bookings for the guest
        """
        guest = self._guests.get(guest_id)
        if guest is None:
            raise ValueError("Guest not found")
        
        return [b for b in self._bookings.values() if b.get_guest().get_guest_id() == guest_id]
    
    def get_invoice(self, booking_id):
        """
        Get invoice for a booking
        
        Args:
            booking_id: Booking ID
            
        Returns:
            Invoice: The invoice for the booking
        """
        payment = next((p for p in self._payments.values() if p.get_booking().get_booking_id() == booking_id), None)
        if payment is None:
            raise ValueError("No payment found for this booking")
        
        invoice = next((i for i in self._invoices.values() if i.get_payment().get_payment_id() == payment.get_payment_id()), None)
        return invoice
    
    def __str__(self):
        """String representation of the Hotel"""
        return (f"Hotel: {self._name}\n"
                f"Rooms: {len(self._rooms)}\n"
                f"Guests: {len(self._guests)}\n"
                f"Staff: {len(self._staff)}\n"
                f"Services: {len(self._services)}")