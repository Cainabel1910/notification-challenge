from uuid import UUID

from app.users.user_model import UserModel
from sqlalchemy import select
from sqlalchemy.orm import Session


class UserRepository:

    def __init__(self, db: Session):
        self.db = db
    
    def find_all(self) -> list[UserModel]:
        statement = select(UserModel)

        return list(self.db.scalars(statement).all())
    
        
    def find_by_id(self, user_id: UUID) -> UserModel | None:
        return self.db.get(UserModel, user_id)
    
    
    def find_by_email(self, email: str) -> UserModel | None:
        statement = select(UserModel).where(
            UserModel.email == email
        )

        return self.db.scalar(statement)


    def save(self, user: UserModel) -> UserModel:
        self.db.add(user)
        self.db.commit()
        self.db.refresh(user)

        return user