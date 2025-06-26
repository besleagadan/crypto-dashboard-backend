import secrets
from fastapi import APIRouter, Request, HTTPException, Depends
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from authlib.integrations.starlette_client import OAuthError
from app.models.user import User
from app.db.postgres import get_db
from app.services.oauth_service import oauth
from app.core.security import create_access_token

router = APIRouter()

@router.get("/login/google")
async def login_with_google(request: Request):
    """
    Initiates Google OAuth2 login by redirecting the user to Google's consent screen.
    """
    nonce = secrets.token_urlsafe(16)
    request.session["nonce"] = nonce
    redirect_uri = request.url_for("auth_callback_google")
    return await oauth.google.authorize_redirect(request, redirect_uri, nonce=nonce)

def save_or_create_user(user_info: dict, db: Session, provider: str = "google") -> User:
    email = user_info.get("email")
    full_name = user_info.get("name")
    provider_id = user_info.get("sub")

    if not email or not provider_id:
        raise ValueError("Missing email or provider ID")

    user = db.query(User).filter_by(provider=provider, provider_id=provider_id).first()

    if not user:
        user = User(
            email=email,
            username=email.split("@")[0],
            full_name=full_name,
            provider=provider,
            provider_id=provider_id,
            is_verified=True,
        )
        db.add(user)
        db.commit()
        db.refresh(user)

    return user

@router.get("/callback/google")
async def google_auth_callback(request: Request, db: Session = Depends(get_db)):
    """
    Handles the OAuth2 callback from Google, validates the ID token, and sets the access token cookie.
    """
    try:
        token = await oauth.google.authorize_access_token(request)
        nonce = request.session.get("nonce")

        if not nonce:
            raise HTTPException(status_code=400, detail="Missing nonce in session")

        user_info = await oauth.google.parse_id_token(token, nonce)

        if not user_info or "email" not in user_info:
            raise HTTPException(status_code=400, detail="Invalid user info received from Google")

        user = save_or_create_user(user_info, db)
        access_token = create_access_token(data={"sub": str(user.id)})
        return {"access_token": access_token, "token_type": "bearer"}

        # access_token = create_access_token({"sub": user_info["email"]})
        # response = RedirectResponse(url="/docs")
        # response.set_cookie(key="access_token", value=f"Bearer {access_token}", httponly=True)
        # return response

    except OAuthError as e:
        raise HTTPException(status_code=400, detail=f"OAuth Error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Authentication failed")

@router.get("/logout")
async def logout():
    response = RedirectResponse(url="/")
    response.delete_cookie("access_token")
    return response

@router.get("/me")
async def me(request: Request):
    token = request.cookies.get("access_token", "").replace("Bearer ", "")
    return {"token": token}

