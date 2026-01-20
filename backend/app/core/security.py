import hmac
import hashlib
from typing import Optional
from datetime import datetime, timedelta
from urllib.parse import parse_qsl

from jose import JWTError, jwt
from fastapi import HTTPException, status

from app.core.config import settings


def verify_telegram_web_app_data(init_data: str) -> dict:
    """
    Verify Telegram Web App initData signature

    Args:
        init_data: The initData string from Telegram Web App

    Returns:
        dict: Parsed and verified data

    Raises:
        HTTPException: If signature is invalid
    """
    try:
        # Parse the init_data
        parsed_data = dict(parse_qsl(init_data))

        # Get hash from data
        received_hash = parsed_data.pop('hash', None)
        if not received_hash:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Hash not found in init data"
            )

        # Sort data keys and create data_check_string
        data_check_arr = [f"{k}={v}" for k, v in sorted(parsed_data.items())]
        data_check_string = '\n'.join(data_check_arr)

        # Create secret key
        secret_key = hmac.new(
            key="WebAppData".encode(),
            msg=settings.TELEGRAM_BOT_TOKEN.encode(),
            digestmod=hashlib.sha256
        ).digest()

        # Calculate hash
        calculated_hash = hmac.new(
            key=secret_key,
            msg=data_check_string.encode(),
            digestmod=hashlib.sha256
        ).hexdigest()

        # Compare hashes
        if not hmac.compare_digest(calculated_hash, received_hash):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid hash"
            )

        # Check auth_date (data should not be older than 1 hour)
        auth_date = int(parsed_data.get('auth_date', 0))
        current_timestamp = int(datetime.utcnow().timestamp())

        if current_timestamp - auth_date > 3600:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Init data is too old"
            )

        return parsed_data

    except Exception as e:
        if isinstance(e, HTTPException):
            raise
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=f"Failed to verify init data: {str(e)}"
        )


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """Create JWT access token"""
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(
            minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES
        )

    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(
        to_encode,
        settings.SECRET_KEY,
        algorithm=settings.ALGORITHM
    )

    return encoded_jwt


def decode_access_token(token: str) -> dict:
    """Decode JWT access token"""
    try:
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        return payload
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
