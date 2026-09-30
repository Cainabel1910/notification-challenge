class UserMessages:
    NOT_FOUND = "User not found"
    EMAIL_ALREADY_REGISTERED = "Email already registered"


class AuthMessages:
    INVALID_CREDENTIALS = "Invalid email or password"
    INVALID_TOKEN = "Invalid or expired token"


class NotificationMessages:
    NOT_FOUND = "Notification not found"
    INVALID_CHANNEL = "Invalid notification channel"
    INVALID_EMAIL_RECIPIENT = "Invalid email recipient"
    INVALID_SMS_RECIPIENT = "Invalid SMS recipient"
    INVALID_PUSH_RECIPIENT = "Invalid push recipient" 
    SMS_CONTENT_TOO_LONG = (
        "SMS content must not exceed {max_length} characters"
    )