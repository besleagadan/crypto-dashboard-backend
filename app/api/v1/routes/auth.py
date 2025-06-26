import secrets
from fastapi import APIRouter, Request, HTTPException, Depends
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from authlib.integrations.starlette_client import OAuthError
from app.models.user import User
from app.db.postgres import get_db
from app.services.auth_service import oauth, save_or_create_user
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

@router.get("/callback/google", )
async def auth_callback_google(request: Request, db: Session = Depends(get_db)):
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

