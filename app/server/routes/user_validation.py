import os
from dotenv import load_dotenv

load_dotenv()

def is_valid_auth_user(user):
    if "groups" not in user \
        or "groups" in user and os.getenv("KEYCLOAK_ROLE") not in user["groups"]:
        return False
    return True

# ToDo: validation should by user role, not by ID
def is_valid_admin_user(user):
    if not is_valid_auth_user(user):
        return False
    if user["sub"] != os.getenv("MKTPLC_ADMIN_ID"):
        return False
    return True

def is_same_user(user, id_user):
    return user['sub'] == id_user

# This function checks whether user can see/edit other user's library
def is_allowed_user(user, id_user):
    return is_valid_admin_user(user) \
        or is_valid_auth_user(user) and is_same_user(user, id_user)
 