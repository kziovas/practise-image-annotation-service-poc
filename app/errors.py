class ImageNotFound(Exception):
    """Exception raised when an image is not found."""


class SecretKeyNotFoundError(Exception):
    """Raised when the secret key is not found in the Flask app config."""


class UserNotFound(Exception):
    """Exception raised when a user is not found."""
