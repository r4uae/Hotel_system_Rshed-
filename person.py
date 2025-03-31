class Person:
    """Base class representing a person with basic information"""
    
    def __init__(self, name, contact, email):
        """
        Initialize a Person object
        
        Args:
            name: Full name of the person
            contact: Phone number or contact information
            email: Email address
        """
        self._name = name
        self._contact = contact
        self._email = email
    
    def get_name(self):
        """Get the person's name"""
        return self._name
    
    def set_name(self, value):
        """Set the person's name"""
        if not isinstance(value, str) or len(value.strip()) == 0:
            raise ValueError("Name must be a non-empty string")
        self._name = value.strip()
    
    def get_contact(self):
        """Get the contact information"""
        return self._contact
    
    def set_contact(self, value):
        """Set the contact information"""
        if not isinstance(value, str) or len(value.strip()) == 0:
            raise ValueError("Contact must be a non-empty string")
        self._contact = value.strip()
    
    def get_email(self):
        """Get the email address"""
        return self._email
    
    def set_email(self, value):
        """Set the email address"""
        if "@" not in value or "." not in value:
            raise ValueError("Invalid email format")
        self._email = value.strip()
    
    def __str__(self):
        """String representation of the Person"""
        return f"Person: {self._name}, Contact: {self._contact}, Email: {self._email}"


class Guest(Person):
    """Class representing a hotel guest, inherits from Person"""
    
    def __init__(self, name, contact, email, guest_id):
        """
        Initialize a Guest object
        
        Args:
            name: Full name of the guest
            contact: Phone number
            email: Email address
            guest_id: Unique guest identifier
        """
        super().__init__(name, contact, email)
        self._guest_id = guest_id
        self._loyalty_points = 0
        self._preferences = []
        self._reservation_history = []
    
    def get_guest_id(self):
        """Get the guest ID"""
        return self._guest_id
    
    def get_loyalty_points(self):
        """Get the loyalty points"""
        return self._loyalty_points
    
    def add_loyalty_points(self, points):
        """Add loyalty points to the guest's account"""
        if not isinstance(points, int) or points <= 0:
            raise ValueError("Points must be a positive integer")
        self._loyalty_points += points
    
    def redeem_loyalty_points(self, points):
        """Redeem loyalty points from the guest's account"""
        if not isinstance(points, int) or points <= 0:
            raise ValueError("Points must be a positive integer")
        if points > self._loyalty_points:
            raise ValueError("Not enough loyalty points")
        self._loyalty_points -= points
    
    def get_preferences(self):
        """Get the guest's preferences"""
        return self._preferences.copy()
    
    def add_preference(self, preference):
        """Add a preference to the guest's profile"""
        if preference not in self._preferences:
            self._preferences.append(preference)
    
    def add_reservation(self, reservation):
        """Add a reservation to the guest's history"""
        self._reservation_history.append(reservation)
    
    def get_reservation_history(self):
        """Get the guest's reservation history"""
        return self._reservation_history.copy()
    
    def __str__(self):
        """String representation of the Guest"""
        return (f"Guest ID: {self._guest_id}, {super().__str__()}, "
                f"Loyalty Points: {self._loyalty_points}")


class Staff(Person):
    """Class representing hotel staff, inherits from Person"""
    
    def __init__(self, name, contact, email, staff_id, position, department):
        """
        Initialize a Staff object
        
        Args:
            name: Full name
            contact: Phone number
            email: Email address
            staff_id: Unique staff identifier
            position: Job position
            department: Department
        """
        super().__init__(name, contact, email)
        self._staff_id = staff_id
        self._position = position
        self._department = department
    
    def get_staff_id(self):
        """Get the staff ID"""
        return self._staff_id
    
    def get_position(self):
        """Get the position"""
        return self._position
    
    def get_department(self):
        """Get the department"""
        return self._department
    
    def __str__(self):
        """String representation of the Staff"""
        return (f"Staff ID: {self._staff_id}, {super().__str__()}, "
                f"Position: {self._position}, Department: {self._department}")