from app.auth.auth_schema import LoginRequest, TokenResponse
from app.security.jwt import create_access_token
from app.security.password import verify_password
from app.users.user_repository import UserRepository
from core.exceptions import InvalidCredentialsException
from core.messages import AuthMessages


class AuthService:

    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    def login(self, login_data: LoginRequest) -> TokenResponse:
        user = self.user_repository.find_by_email(
            login_data.email
        )

        if user is None:
            raise InvalidCredentialsException(
                AuthMessages.INVALID_CREDENTIALS
            )

        if not verify_password(
            login_data.password,
            user.password_hash
        ):
            raise InvalidCredentialsException(
                AuthMessages.INVALID_CREDENTIALS
            )

        access_token = create_access_token(user.id)

        return TokenResponse(
            access_token=access_token,
            token_type="bearer"
        )