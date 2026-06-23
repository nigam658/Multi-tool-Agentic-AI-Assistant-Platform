from fastapi import APIRouter
from auth.auth_schemas import SignupRequest, LoginRequest
from auth.auth_repository import (
    create_user,
    get_user_by_email
)
from auth.auth_service import hash_password, validate_password,verify_password
from auth.jwt_handler import create_access_token



router = APIRouter()
 
@router.post("/signup")
def signup(request: SignupRequest):

    password_error = validate_password(
    request.password
    )

    if password_error:
        return {
            "success": False,
            "message": password_error
        }
  
    existing_user = get_user_by_email(
    request.email
    )

    if existing_user:
        return {
            "success": False,
            "message": "Email already exists."
        }
    
    hashed_password = hash_password(
        request.password
    )

    create_user(
        request.email,
        hashed_password
    )

    return {
        "success": True,
        "message": "User created successfully."
    }


@router.post("/login")
def login(request: LoginRequest):

    user = get_user_by_email(
        request.email
    )

    if not user:
        return {
            "success": False,
            "message": "Invalid email or password."
        }

    if not verify_password(
        request.password,
        user["password"]
    ):
        return {
            "success": False,
            "message": "Invalid email or password."
        }

    token = create_access_token(
        user["id"]
    )

    return {
        "success": True,
        "token": token
    }