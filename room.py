from datetime import date, timedelta

class RoomType:
    """Class representing types of rooms available"""
    
    def __init__(self, type_name, description, capacity):
        """
        Initialize a RoomType object
        
        Args:
            type_name: Name of the room type (e.g., "Single", "Double")
            description: Description of the room type
            capacity: Maximum number of occupants
        """
        self._type_name = type_name
        self._description = description
        self._capacity = capacity
    
    def get_type_name(self):
        """Get the room type name"""
        return self._type_name
    
    def get_description(self):
        """Get the room type description"""
        return self._description
    
    def get_capacity(self):
        """Get the room capacity"""
        return self._capacity
    
    def __str__(self):
        """String representation of the RoomType"""
        return f"{self._type_name} Room (Capacity: {self._capacity}): {self._description}"


class Room:
    """Class representing a hotel room"""
    
    def __init__(self, room_number, room_type, amenities, price):
        """
        Initialize a Room object
        
        Args:
            room_number: Room number/identifier
            room_type: Type of room
            amenities: List of amenities
            price: Price per night
        """
        self._room_number = room_number
        self._room_type = room_type
        self._amenities = amenities.copy()
        self._price = price
        self._is_available = True
        self._booked_dates = []
    
    def get_room_number(self):
        """Get the room number"""
        return self._room_number
    
    def get_room_type(self):
        """Get the room type"""
        return self._room_type
    
    def get_amenities(self):
        """Get the room amenities"""
        return self._amenities.copy()
    
    def add_amenity(self, amenity):
        """Add an amenity to the room"""
        if amenity not in self._amenities:
            self._amenities.append(amenity)
    
    def remove_amenity(self, amenity):
        """Remove an amenity from the room"""
        if amenity in self._amenities:
            self._amenities.remove(amenity)
    
    def get_price(self):
        """Get the room price per night"""
        return self._price
    
    def set_price(self, value):
        """Set the room price per night"""
        if not isinstance(value, (int, float)) or value <= 0:
            raise ValueError("Price must be a positive number")
        self._price = float(value)
    
    def is_available(self):
        """Check if the room is currently available"""
        return self._is_available
    
    def check_availability(self, check_in, check_out):
        """
        Check if the room is available for specific dates
        
        Args:
            check_in: Check-in date
            check_out: Check-out date
            
        Returns:
            bool: True if available, False otherwise
        """
        if check_in >= check_out:
            raise ValueError("Check-in date must be before check-out date")
            
        for booked_in, booked_out in self._booked_dates:
            if not (check_out <= booked_in or check_in >= booked_out):
                return False
        return True
    
    def book_room(self, check_in, check_out):
        """
        Book the room for specific dates
        
        Args:
            check_in: Check-in date
            check_out: Check-out date
        """
        if not self.check_availability(check_in, check_out):
            raise ValueError("Room not available for the selected dates")
        
        self._booked_dates.append((check_in, check_out))
        self._is_available = False
    
    def release_room(self):
        """Mark the room as available"""
        self._is_available = True
    
    def __str__(self):
        """String representation of the Room"""
        status = "Available" if self._is_available else "Booked"
        return (f"Room {self._room_number} - {self._room_type.get_type_name()} "
                f"(Price: ${self._price:.2f}/night, Status: {status}) "
                f"Amenities: {', '.join(self._amenities)}")