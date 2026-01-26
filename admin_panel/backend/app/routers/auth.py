from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from jose import jwt, JWTError

from ..database import get_db
from ..models.admin import AdminUser
from ..core.security import verify_password, create_access_token, settings
from ..schemas import AdminLogin, Token, AdminResponse

router = APIRouter()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

async def get_current_admin(token: str = Depends(oauth2_scheme), db: AsyncSession = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=[settings.algorithm])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
        
    result = await db.execute(select(AdminUser).where(AdminUser.email == email))
    admin = result.scalar_one_or_none()
    
    if admin is None:
        raise credentials_exception
    return admin

@router.post("/login", response_model=Token)
async def login(credentials: AdminLogin, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(AdminUser).where(AdminUser.email == credentials.username))
    admin = result.scalar_one_or_none()
    
    if not admin or not verify_password(credentials.password, admin.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
        )
    
    access_token = create_access_token(data={"sub": admin.email})
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me", response_model=AdminResponse)
async def read_users_me(current_admin: AdminUser = Depends(get_current_admin)):
    return current_admin
