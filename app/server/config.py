import pathlib
import toml
import os


with open(pathlib.Path(__file__).parent / "config.toml", "r") as fh:
    CONFIG = toml.load(fh)


DB_CONFIG = CONFIG.get("database", {})


KEYCLOAK_CONFIG = {
    "url": os.getenv("KEYCLOAK_URL"),
    "realm": os.getenv("KEYCLOAK_REALM"),
    "openid-connect-url": os.getenv("KEYCLOAK_OPENID_CONNECT_URL"),
    "client-id": os.getenv("ML_BACKEND_KEYCLOAK_CLIENT_ID"),
    "client-secret": os.getenv("ML_BACKEND_KEYCLOAK_CLIENT_SECRET"),
    "scopes": os.getenv("ML_BACKEND_KEYCLOAK_SCOPES"),
    "client-id-swagger": os.getenv("ML_BACKEND_KEYCLOAK_CLIENT_ID_SWAGGER")
}