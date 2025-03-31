class Service:
    """Class representing a hotel service"""
    
    def __init__(self, service_id, name, price):
        """
        Initialize a Service object
        
        Args:
            service_id: Unique service identifier
            name: Name of the service
            price: Price of the service
        """
        self._service_id = service_id
        self._name = name
        self._price = price
        self._is_available = True
    
    def get_service_id(self):
        """Get the service ID"""
        return self._service_id
    
    def get_name(self):
        """Get the service name"""
        return self._name
    
    def get_price(self):
        """Get the service price"""
        return self._price
    
    def set_price(self, value):
        """Set the service price"""
        if not isinstance(value, (int, float)) or value <= 0:
            raise ValueError("Price must be a positive number")
        self._price = float(value)
    
    def is_available(self):
        """Check if the service is available"""
        return self._is_available
    
    def set_availability(self, available):
        """Set the availability of the service"""
        self._is_available = available
    
    def __str__(self):
        """String representation of the Service"""
        status = "Available" if self._is_available else "Unavailable"
        return f"Service {self._service_id}: {self._name} (${self._price:.2f}) - {status}"


class ServiceRequest:
    """Class representing a guest's service request"""
    
    def __init__(self, guest, service):
        """
        Initialize a ServiceRequest object
        
        Args:
            guest: Guest making the request
            service: Service being requested
        """
        self._request_id = self._generate_request_id()
        self._guest = guest
        self._service = service
        self._status = "Pending"
    
    def _generate_request_id(self):
        """Generate a unique request ID"""
        import random
        import string
        chars = string.ascii_uppercase + string.digits
        return 'SR-' + ''.join(random.choice(chars) for _ in range(6))
    
    def get_request_id(self):
        """Get the request ID"""
        return self._request_id
    
    def get_guest(self):
        """Get the guest"""
        return self._guest
    
    def get_service(self):
        """Get the service"""
        return self._service
    
    def get_status(self):
        """Get the request status"""
        return self._status
    
    def fulfill_request(self):
        """Mark the request as fulfilled"""
        self._status = "Fulfilled"
    
    def cancel_request(self):
        """Cancel the request"""
        self._status = "Cancelled"
    
    def __str__(self):
        """String representation of the ServiceRequest"""
        return (f"Request ID: {self._request_id}\n"
                f"Guest: {self._guest.get_name()}\n"
                f"Service: {self._service.get_name()}\n"
                f"Status: {self._status}")