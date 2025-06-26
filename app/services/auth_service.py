from authlib.integrations.starlette_client import OAuth
from sqlalchemy.orm import Session
from app.models.user import User
from app.core.config import settings

oauth = OAuth()
oauth.register(
    name="google",
    client_id=settings.GOOGLE_CLIENT_ID,
    client_secret=settings.GOOGLE_CLIENT_SECRET,
    server_metadata_url="https://accounts.google.com/.well-known/openid-configuration",
    client_kwargs={"scope": "openid email profile", "id_token": ""},
)


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
