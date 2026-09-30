class UserNotFoundException(Exception):
    pass


class EmailAlreadyRegisteredException(Exception):
    pass


class InvalidCredentialsException(Exception):
    pass


class InvalidTokenException(Exception):
    pass


class InvalidRecipientException(Exception):
    pass


class NotificationNotFoundException(Exception):
    pass


class InvalidNotificationContentException(Exception):
    pass