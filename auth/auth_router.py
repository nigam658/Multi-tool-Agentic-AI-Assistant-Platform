from fastapi import APIRouter
from datetime import datetime, timezone, timedelta

from auth.auth_schemas import SignupRequest, LoginRequest, RefreshTokenRequest, VerifyOTPRequest
from auth.auth_repository import (
    create_user,
    get_user_by_email
)
from auth.auth_service import hash_password, validate_password,verify_password,generate_otp
from auth.jwt_handler import create_access_token,create_refresh_token,verify_token
from session_manager import sessions as pending_users
from email_tool.email_service import send_email


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
    
    existing_pending = pending_users.get(request.email)
    if existing_pending:
        
        if datetime.now(timezone.utc) < existing_pending["expires_at"]:
            return {
                "success": False,
                "message": "OTP already sent. Please check your email."
            }
    
    otp = generate_otp()
    pending_users[request.email] = {
        "email": request.email,
        "password": hash_password(request.password),
        "otp": otp,
        "expires_at": datetime.now(timezone.utc) + timedelta(minutes=10)
    }
    try :
        send_email(
            recipient=request.email,
            subject="Verify your email - OTP",
            body=(
                f"Hello,\n\n"
                f"Your OTP for email verification is:\n\n"
                f"{otp}\n\n"
                f"This OTP expires in 10 minutes.\n\n"
                f"If you did not request this, please ignore this email."
            )
        )
    except Exception as e:
        print("OTP Email Error:", e)
        return {
            "success": False,
            "message": "Failed to send OTP. Please try again."
        }
    
    return {
        "success": True,
        "message": "OTP sent to your email. Please verify to complete signup."
    }


@router.post("/verify-otp")
def verify_otp(request: VerifyOTPRequest):

    # check the otp is sending or not 
    pending = pending_users.get(request.email)
 
    if not pending:
        return {
            "success": False,
            "message": "No signup request found. Please signup first."
        }
    
    # Step 2 - Check if OTP expired
    if datetime.now(timezone.utc) > pending["expires_at"]:
        del pending_users[request.email]
        return {
            "success": False,
            "message": "OTP expired. Please signup again."
        }
 
    # Step 3 - Check if OTP matches
    if pending["otp"] != request.otp:
        return {
            "success": False,
            "message": "Invalid OTP. Please try again."
        }
    
    # Step 4 - Create user in DB
    try:
        create_user(
            pending["email"],
            pending["password"]
        )
    except Exception as e:
        print("Create User Error:", e)
        return {
            "success": False,
            "message": "Failed to create account. Please try again."
        }
 
    # Step 5 - Remove from pending
    del pending_users[request.email]
 
    return {
        "success": True,
        "message": "Email verified successfully. You can now login."
    }

@router.post("/resend-otp")
def resend_otp(request: SignupRequest):
 
    # Check if pending user exists
    pending = pending_users.get(request.email)
 
    if not pending:
        return {
            "success": False,
            "message": "No signup request found. Please signup first."
        }
 
    # Generate new OTP
    new_otp = generate_otp()
 
    # Update pending user with new OTP
    pending_users[request.email]["otp"] = new_otp
    pending_users[request.email]["expires_at"] = datetime.now(timezone.utc) + timedelta(minutes=10)
 
    # Send new OTP email
    try:
        send_email(
            recipient=request.email,
            subject="Resend OTP - Email Verification",
            body=(
                f"Hello,\n\n"
                f"Your new OTP for email verification is:\n\n"
                f"{new_otp}\n\n"
                f"This OTP expires in 10 minutes.\n\n"
                f"If you did not request this, please ignore this email."
            )
        )
    except Exception as e:
        print("Resend OTP Error:", e)
        return {
            "success": False,
            "message": "Failed to resend OTP. Please try again."
        }
 
    return {
        "success": True,
        "message": "New OTP sent to your email."
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
    refresh_token = create_refresh_token(user["id"])

    return {
        "success": True,
        "token": token,
        "refresh_token":refresh_token
    }

@router.post("/refresh")
def refresh_token(refresh_token: RefreshTokenRequest):

    payload = verify_token(refresh_token.refresh_token)

    if not payload:
        return {
            "success": False,
            "message": "Invalid refresh token"
        }

    if payload["type"] != "refresh":
        return {
            "success": False,
            "message": "Invalid token type"
        }

    access_token = create_access_token(
        payload["user_id"]
    )

    return {
        "success": True,
        "access_token": access_token
    }