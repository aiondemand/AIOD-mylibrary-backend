"""
We use keycloak for authentication and authorization.

The overall idea is that:
- The frontend uses a public client (without a secret) and authenticates the user
- The frontend passes the token to the backend
- The backend (i.e. this project) decodes the token to obtain the username
- The backend performs an authorization request to Keycloak, obtaining the permissions. It uses a
    private client for this request.

The main reason to perform a separate authorization request in the backend is that the frontend
should not be responsible for keeping the permissions up to date. Explanation: instead of only
obtaining the permissions from the decoded token, the backend could also take the permissions.
This is perfectly safe (the token cannot be changed without knowing the private key of keycloak).
But then the frontend needs to make sure that the permissions are up-to-date. Every front-end
should therefor request a new token every X minutes. This is not needed when the back-end
performs a separate authorization request. The only downside is the overhead of the additional
keycloak requests - if that becomes prohibitive in the future, we should reevaluate this design.

Note: this file is a copy of the one available in the AIoD REST API repository: 
    https://github.com/aiondemand/AIOD-rest-api 
whose authors are:
- Antonis Ganios
- Íñigo Aréjula Aísa
- Jos van der Velde (email: j.d.v.d.velde@tue.nl)
- Pieter Gijsbers (email: p.gijsbers@tue.nl)
- Giannis Mouchakis
- Taniya Das (email: t.das@tue.nl)
"""


import logging
import os

from dotenv import load_dotenv
from fastapi import HTTPException, Security, status
from fastapi.security import OpenIdConnect
from keycloak import KeycloakOpenID, KeycloakError

load_dotenv()


oidc = OpenIdConnect(openIdConnectUrl=os.getenv("ML_BACKEND_KEYCLOAK_OPENID_CONNECT_URL"), auto_error=False)


client_secret = os.getenv("ML_BACKEND_KEYCLOAK_CLIENT_SECRET")
keycloak_openid = KeycloakOpenID(
    server_url=os.getenv("ML_BACKEND_KEYCLOAK_URL"),
    client_id=os.getenv("ML_BACKEND_KEYCLOAK_CLIENT_ID"),
    client_secret_key=client_secret,
    realm_name=os.getenv("ML_BACKEND_KEYCLOAK_REALM"),
    verify=True,
)


async def get_current_user(token=Security(oidc)) -> dict:
    if not client_secret:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="This instance is not configured correctly. You'll need to set the env var "
            "KEYCLOAK_CLIENT_SECRET (e.g. in src/.env). You need to obtain this secret "
            "from a Keycloak Administrator of AIoD.",
        )
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="This endpoint requires authorization. You need to be logged in.",
            headers={"WWW-Authenticate": "Bearer"},
        )
    try:
        token = token.replace("Bearer ", "")
        return keycloak_openid.userinfo(token)  # perform a request to keycloak
    except KeycloakError as e:
        logging.error(f"Error while checking the access token: '{e}'")
        error_msg = e.error_message
        if isinstance(error_msg, bytes):
            error_msg = error_msg.decode("utf-8")
        detail = "Invalid authentication token"
        if error_msg != "":
            detail += f": '{error_msg}'"
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=detail,
            headers={"WWW-Authenticate": "Bearer"},
        )
