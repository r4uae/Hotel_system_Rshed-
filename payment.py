class Payment:
    """Class representing a payment for a booking"""
    
    def __init__(self, booking, amount, method):
        """
        Initialize a Payment object
        
        Args:
            booking: Booking being paid for
            amount: Payment amount
            method: Payment method (e.g., "Credit Card", "Debit Card", "Cash")
        """
        self._payment_id = self._generate_payment_id()
        self._booking = booking
        self._amount = amount
        self._method = method
        self._status = "Pending"
    
    def _generate_payment_id(self):
        """Generate a unique payment ID"""
        import random
        import string
        chars = string.ascii_uppercase + string.digits
        return 'PAY-' + ''.join(random.choice(chars) for _ in range(8))
    
    def get_payment_id(self):
        """Get the payment ID"""
        return self._payment_id
    
    def get_booking(self):
        """Get the booking"""
        return self._booking
    
    def get_amount(self):
        """Get the payment amount"""
        return self._amount
    
    def get_method(self):
        """Get the payment method"""
        return self._method
    
    def get_status(self):
        """Get the payment status"""
        return self._status
    
    def process_payment(self):
        """Process the payment"""
        if self._status == "Completed":
            return
        
        # In a real system, this would integrate with a payment gateway
        self._status = "Completed"
        self._booking.set_status("Confirmed")
    
    def refund_payment(self, amount=None):
        """Process a refund"""
        if amount is None:
            amount = self._amount
        
        if amount > self._amount:
            raise ValueError("Refund amount cannot exceed original payment")
        
        # In a real system, this would process the refund
        self._status = "Refunded"
        if amount == self._amount:
            self._booking.set_status("Cancelled")
    
    def __str__(self):
        """String representation of the Payment"""
        return (f"Payment ID: {self._payment_id}\n"
                f"Booking ID: {self._booking.get_booking_id()}\n"
                f"Amount: ${self._amount:.2f}\n"
                f"Method: {self._method}\n"
                f"Status: {self._status}")


class Invoice:
    """Class representing an invoice for a booking"""
    
    def __init__(self, payment):
        """
        Initialize an Invoice object
        
        Args:
            payment: Payment to generate invoice for
        """
        self._invoice_id = self._generate_invoice_id()
        self._payment = payment
        self._tax_rate = 0.10  # 10% tax for example
        self._calculate_totals()
    
    def _generate_invoice_id(self):
        """Generate a unique invoice ID"""
        import random
        import string
        chars = string.ascii_uppercase + string.digits
        return 'INV-' + ''.join(random.choice(chars) for _ in range(8))
    
    def _calculate_totals(self):
        """Calculate invoice totals"""
        booking = self._payment.get_booking()
        self._room_charges = booking.get_total_cost() - sum(
            s.get_price() for s in booking.get_additional_services())
        self._service_charges = sum(s.get_price() for s in booking.get_additional_services())
        self._tax = (self._room_charges + self._service_charges) * self._tax_rate
        self._total = self._room_charges + self._service_charges + self._tax
    
    def get_invoice_id(self):
        """Get the invoice ID"""
        return self._invoice_id
    
    def get_payment(self):
        """Get the payment"""
        return self._payment
    
    def get_room_charges(self):
        """Get the room charges"""
        return self._room_charges
    
    def get_service_charges(self):
        """Get the service charges"""
        return self._service_charges
    
    def get_tax(self):
        """Get the tax amount"""
        return self._tax
    
    def get_total(self):
        """Get the total amount"""
        return self._total
    
    def generate_invoice(self):
        """Generate a formatted invoice string"""
        booking = self._payment.get_booking()
        invoice_lines = [
            f"Invoice ID: {self._invoice_id}",
            f"Guest: {booking.get_guest().get_name()}",
            f"Room: {booking.get_room().get_room_number()} ({booking.get_room().get_room_type().get_type_name()})",
            f"Dates: {booking.get_check_in()} to {booking.get_check_out()}",
            "",
            "Charges:",
            f"  Room ({booking.get_room().get_price():.2f}/night x {(booking.get_check_out() - booking.get_check_in()).days} nights): ${self._room_charges:.2f}",
        ]
        
        if booking.get_additional_services():
            invoice_lines.append("  Additional Services:")
            for service in booking.get_additional_services():
                invoice_lines.append(f"    {service.get_name()}: ${service.get_price():.2f}")
        
        invoice_lines.extend([
            "",
            "Summary:",
            f"  Room Charges: ${self._room_charges:.2f}",
            f"  Service Charges: ${self._service_charges:.2f}",
            f"  Tax ({self._tax_rate*100:.1f}%): ${self._tax:.2f}",
            f"  Total: ${self._total:.2f}",
            "",
            f"Payment Method: {self._payment.get_method()}",
            f"Payment Status: {self._payment.get_status()}",
        ])
        
        return "\n".join(invoice_lines)
    
    def __str__(self):
        """String representation of the Invoice"""
        return self.generate_invoice()