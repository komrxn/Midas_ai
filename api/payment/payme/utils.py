import base64
from fastapi import HTTPException, Request, Depends
from ...config import get_settings

settings = get_settings()

def get_auth_header(username: str = "Paycom", password: str = None) -> str:
    """Generate Basic Auth header string."""
    if not password:
        password = settings.payme_key
    auth_str = f"{username}:{password}"
    b64_auth = base64.b64encode(auth_str.encode()).decode()
    return f"Basic {b64_auth}"

async def verify_payme_auth(request: Request):
    """
    Verify Basic Auth header.
    Expects Authorization: Basic Base64('Paycom:KEY')
    """
    auth_header = request.headers.get("Authorization")
    if not auth_header:
        # raise HTTPException(status_code=401, detail="Missing Authorization header")
        return False
    
    expected = get_auth_header()
    if auth_header != expected:
        # raise HTTPException(status_code=401, detail="Invalid Authorization")
        return False
    
    return True
