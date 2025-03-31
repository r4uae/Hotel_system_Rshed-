from datetime import date, timedelta
import random
import string

class Booking:
    """Class representing a room booking"""
    
    def __init__(self, guest, room, check_in, check_out):
        """
        Initialize a Booking object
        """
        self._booking_id = self._generate_booking_id()
        self._guest = guest
        self._room = room
        self._check_in = check_in
        self._check_out = check_out
        self._status = "Confirmed"
        self._additional_services = []
        
        # Calculate total cost - FIXED LINE
        nights = (check_out - check_in).days
        self._total_cost = room.get_price() * nights  # Changed from room.price to room.get_price()
        
        # Book the room
        room.book_room(check_in, check_out)
        
        # Add to guest's reservation history
        guest.add_reservation(self)
    
    def _generate_booking_id(self):
        """Generate a unique booking ID"""
        chars = string.ascii_uppercase + string.digits
        return ''.join(random.choice(chars) for _ in range(8))
    
    def get_booking_id(self):
        """Get the booking ID"""
        return self._booking_id
    
    def get_guest(self):
        """Get the guest"""
        return self._guest
    
    def get_room(self):
        """Get the room"""
        return self._room
    
    def get_check_in(self):
        """Get the check-in date"""
        return self._check_in
    
    def get_check_out(self):
        """Get the check-out date"""
        return self._check_out
    
    def get_status(self):
        """Get the booking status"""
        return self._status
    
    def set_status(self, value):
        """Set the booking status"""
        valid_statuses = ["Confirmed", "Cancelled", "Completed"]
        if value not in valid_statuses:
            raise ValueError(f"Status must be one of: {', '.join(valid_statuses)}")
        self._status = value
    
    def get_total_cost(self):
        """Get the total cost"""
        return self._total_cost
    
    def add_service(self, service):
        """Add an additional service to the booking"""
        self._additional_services.append(service)
        self._total_cost += service.get_price()  # Also changed from service.price
    
    def get_additional_services(self):
        """Get additional services"""
        return self._additional_services.copy()
    
    def cancel_booking(self):
        """Cancel the booking"""
        if self._status == "Cancelled":
            return
        
        self._status = "Cancelled"
        self._room.release_room()
    
    def __str__(self):
        """String representation of the Booking"""
        nights = (self._check_out - self._check_in).days
        services = ", ".join([s.get_name() for s in self._additional_services]) or "None"
        return (f"Booking ID: {self._booking_id}\n"
                f"Guest: {self._guest.get_name()}\n"
                f"Room: {self._room.get_room_number()} ({self._room.get_room_type().get_type_name()})\n"
                f"Dates: {self._check_in} to {self._check_out} ({nights} nights)\n"
                f"Status: {self._status}\n"
                f"Total Cost: ${self._total_cost:.2f}\n"
                f"Additional Services: {services}")