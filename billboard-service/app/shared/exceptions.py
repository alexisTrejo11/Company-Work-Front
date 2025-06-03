class DomainException(Exception):
    """Base class for all domain-specific exceptions."""
    def __init__(self, message: str = "A domain-specific error occurred."):
        self.message = message
        super().__init__(self.message)
