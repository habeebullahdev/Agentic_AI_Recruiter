from typing import Optional, List, Callable
from fastapi import Depends, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.user import User, UserRole
from app.core.security import decode_token
from app.core.exceptions import AuthenticationFailedException, PermissionDeniedException
from app.core.config import settings

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_PREFIX}/auth/login",
    auto_error=False
)


def get_current_user(
    token: Optional[str] = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    """
    Dependency that extracts, verifies JWT token and loads the authenticated User model.
    """
    if not token:
        raise AuthenticationFailedException("Authentication token required.")

    payload = decode_token(token)
    if not payload or "sub" not in payload:
        raise AuthenticationFailedException("Invalid or expired authentication token.")

    user_id = payload.get("sub")
    try:
        user = db.query(User).filter(User.id == int(user_id)).first()
    except (ValueError, TypeError):
        user = db.query(User).filter(User.email == str(user_id)).first()

    if not user:
        raise AuthenticationFailedException("User corresponding to token no longer exists.")

    if not user.is_active:
        raise PermissionDeniedException("User account is inactive or disabled.")

    return user


def get_optional_current_user(
    token: Optional[str] = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> Optional[User]:
    """
    Dependency that optionally extracts the current authenticated user if token is present.
    """
    if not token:
        return None
    try:
        return get_current_user(token=token, db=db)
    except Exception:
        return None


def require_roles(allowed_roles: List[UserRole]) -> Callable[[User], User]:
    """
    Role-Based Access Control (RBAC) dependency factory.
    """
    def role_checker(current_user: User = Depends(get_current_user)) -> User:
        if current_user.role not in allowed_roles and current_user.role != UserRole.ADMIN:
            role_names = [r.value for r in allowed_roles]
            raise PermissionDeniedException(
                f"Action requires one of the following roles: {role_names}. Your role is '{current_user.role.value}'."
            )
        return current_user
    return role_checker
