from pydantic import Json
from fastapi import Depends, FastAPI
from authentication import get_current_user
from server.routes.libraries import LibrariesRouter

import os

from dotenv import load_dotenv
load_dotenv()

url_prefix = ""
app = FastAPI(
    openapi_url=f"{url_prefix}/openapi.json",
    docs_url=f"{url_prefix}/docs",
    swagger_ui_oauth2_redirect_url=f"{url_prefix}/docs/oauth2-redirect",
    swagger_ui_init_oauth={
        "clientId": os.getenv("ML_BACKEND_KEYCLOAK_CLIENT_ID_SWAGGER"),
        "realm": os.getenv("ML_BACKEND_KEYCLOAK_REALM"),
        "appName": "AIoD Marketplace backend",
        "usePkceWithAuthorizationCodeGrant": True,
        "scopes": os.getenv("ML_BACKEND_KEYCLOAK_SCOPES"),
    },
)

app.include_router(LibrariesRouter, tags=["Libraries"], prefix="/api/libraries")

# Note: this function is a copy of the one available in the AIoD REST API repository: 
#     https://github.com/aiondemand/AIOD-rest-api 
@app.get(url_prefix + "/authorization_test")
def test_authorization(user: Json = Depends(get_current_user)) -> dict:
    """
    Returns the user, if authenticated correctly.
    """
    return {"msg": "success", "user": user}


