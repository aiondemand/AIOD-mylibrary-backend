import os
from dotenv import load_dotenv

load_dotenv()

# ToDo: validation should by user role, not by ID
def is_valid_admin_user(user):
    if user["sub"] != os.getenv("MKTPLC_ADMIN_ID"):
        return False
    return True

def is_same_user(user, id_user):
    return user['sub'] == id_user

# This function checks whether user can see/edit other user's library
def is_allowed_user(user, id_user):
    # ToDo: Enhance user validation with roles
    return is_valid_admin_user(user) or is_same_user(user, id_user)
 