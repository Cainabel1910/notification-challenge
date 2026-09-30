from uuid import UUID

from app.security.password import hash_password
from app.users.user_model import UserModel
from app.users.user_repository import UserRepository
from app.users.user_schema import UserCreate
from core.exceptions import (
    EmailAlreadyRegisteredException,
    UserNotFoundException,
)
from core.messages import UserMessages


class UserService:

    def __init__(self, repository: UserRepository):
        self.repository = repository
        
        
    def get_all_users(self) -> list[UserModel]:
        return self.repository.find_all()
        
        
    def get_user_by_id(self, user_id: UUID) -> UserModel:
        user = self.repository.find_by_id(user_id)
        if user is None:
            raise UserNotFoundException(
                UserMessages.NOT_FOUND
            )

        return user
    
    
    def get_user_by_email(self, email: str) -> UserModel:
        user = self.repository.find_by_email(email)
        if user is None:
            raise UserNotFoundException(
                UserMessages.NOT_FOUND
            )
    
            return user


    def register_user(self, user_data: UserCreate) -> UserModel:
        existing_user = self.repository.find_by_email(user_data.email)

        if existing_user:
            raise EmailAlreadyRegisteredException(
                UserMessages.EMAIL_ALREADY_REGISTERED
            )

        user = UserModel(
            email=user_data.email,
            password_hash=hash_password(user_data.password)
        )

        return self.repository.save(user)