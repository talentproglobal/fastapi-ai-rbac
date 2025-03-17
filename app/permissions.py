from oso import Oso
from fastapi import Depends, HTTPException, status
from app.db import get_user
from app.auth import get_current_user  # ✅ Fix Import Path

# Initialize Oso
oso = Oso()

# Define and Load Policies
oso.load_str("""
    allow(actor: String, action: String, resource: String) if
        role_allow(actor, action, resource);

    role_allow("admin", "read", "all");
    role_allow("admin", "write", "all");
    role_allow("admin", "delete", "all");
    role_allow("user", "read", "all");
    role_allow("user", "write", "all");
""")

def get_user_role(username: str):
    """ Retrieve the user's role from the database """
    user = get_user(username)
    if not user:
        return None
    return user.get("role", "user")  # Default to 'user' if role is missing

async def check_permission(action: str, current_user: dict = Depends(get_current_user)):
    """ Enforce RBAC using Oso to check if a user has the right permission """
    username = current_user["username"]
    role = get_user_role(username)
    
    if not role:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="User role not found")
    
    if not oso.is_allowed(role, action):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Access denied")
    
    return True  # Access granted