from fastapi import APIRouter, Depends, status, Request
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
from app.database.session import get_db
from app.models.user import User, UserRole
from app.schemas.user import UserCreate, UserOut, UserLogin, TokenResponse
from app.schemas.common import APIResponse
from app.core.security import verify_password, get_password_hash, create_access_token
from app.core.dependencies import get_current_user
from app.core.exceptions import DuplicateResourceException, AuthenticationFailedException
from app.core.logging import logger

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post(
    "/register",
    response_model=APIResponse[UserOut],
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
    description="Registers a new candidate, recruiter, or admin with email and hashed password."
)
def register_user(user_in: UserCreate, db: Session = Depends(get_db)):
    # Check if email is already registered
    existing_user = db.query(User).filter(User.email == user_in.email.lower().strip()).first()
    if existing_user:
        raise DuplicateResourceException(f"Email '{user_in.email}' is already registered.")

    # Create new user
    new_user = User(
        name=user_in.name.strip(),
        email=user_in.email.lower().strip(),
        password_hash=get_password_hash(user_in.password),
        role=user_in.role or UserRole.CANDIDATE,
        is_active=True
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    logger.info(f"New user registered: {new_user.email} (Role: {new_user.role})")
    return APIResponse(
        success=True,
        message="User registered successfully.",
        data=UserOut.model_validate(new_user)
    )


@router.post(
    "/login",
    response_model=TokenResponse,
    summary="User login and JWT token generation",
    description="Authenticates user credentials (email & password) and returns a JWT access token."
)
def login_user(
    credentials: UserLogin,
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.email == credentials.email.lower().strip()).first()
    if not user or not verify_password(credentials.password, user.password_hash):
        raise AuthenticationFailedException("Incorrect email or password.")

    if not user.is_active:
        raise AuthenticationFailedException("User account is inactive.")

    token = create_access_token(subject=user.id, role=user.role.value)
    logger.info(f"User logged in: {user.email}")

    return TokenResponse(
        access_token=token,
        token_type="bearer",
        user=UserOut.model_validate(user)
    )


@router.post(
    "/token",
    response_model=TokenResponse,
    include_in_schema=False,
    summary="OAuth2 compatible token login for Swagger UI authorization"
)
def login_oauth2(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.email == form_data.username.lower().strip()).first()
    if not user or not verify_password(form_data.password, user.password_hash):
        raise AuthenticationFailedException("Incorrect email or password.")

    token = create_access_token(subject=user.id, role=user.role.value)
    return TokenResponse(
        access_token=token,
        token_type="bearer",
        user=UserOut.model_validate(user)
    )


@router.get(
    "/me",
    response_model=APIResponse[UserOut],
    summary="Get current user profile",
    description="Returns profile details of the currently authenticated user."
)
def get_me(current_user: User = Depends(get_current_user)):
    return APIResponse(
        success=True,
        message="Current user profile retrieved successfully.",
        data=UserOut.model_validate(current_user)
    )
