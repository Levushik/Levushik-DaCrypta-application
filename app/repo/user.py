"""
Client user data operations
"""

from app import models, schemas
from app.repo.default import CRUDBase


class UserRepo(CRUDBase[models.User, schemas.UserCreate, schemas.UserUpdate]):
    """
    Data operations for user client
    """


user = UserRepo(models.User)
