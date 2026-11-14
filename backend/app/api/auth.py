
from fastapi import APIRouter, HTTPException, status

from app.schemas import UserRegister, UserLogin, TokenResponse
from app.services.auth_service import register_user, authenticate_user
from app.services.jwt_service import create_access_token

router = APIRouter(
    prefix="/auth",
    tags=["Authentication"]
)


@router.post("/register", status_code=status.HTTP_201_CREATED)
def register(request: UserRegister):
    try:
        result = register_user(
            username=request.username,
            email=request.email,
            password=request.password
        )
        return result

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=str(e)
        )


@router.post("/login", response_model=TokenResponse)
def login(request: UserLogin):

    user = authenticate_user(
        email=request.email,
        password=request.password
    )

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"}
        )

    access_token = create_access_token(
        data={"sub": str(user["id"])}
    )

    return {
        "access_token": access_token,
        "token_type": "bearer"
    }
