from typing import List
from fastapi import APIRouter, Body, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from server.models.library import AssetModel, DeleteAssetModel
from authentication import get_current_user

from server.database import (
    add_assets_to_library,
    delete_asset_from_library,
    retrieve_libraries,
    retrieve_library,
    retrieve_library_assets
)   

from server.models.response import (
    ErrorResponseModel,
    ResponseModel,
)

from server.routes.user_validation import (
    is_allowed_user,
    is_valid_admin_user
)

LibrariesRouter = APIRouter()

@LibrariesRouter.get("/", response_description="Retrieve all items")
async def get_libraries(user: dict = Depends(get_current_user)):
    if not is_valid_admin_user(user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to get all user libraries.",
        )
    items = await retrieve_libraries()
    if items:
        return ResponseModel(items)
    return ResponseModel(items)

@LibrariesRouter.get("/{id_user}", response_description="Retrieve user's library")
async def get_library(
    id_user,
    user: dict = Depends(get_current_user)
):
    if not is_allowed_user(user, id_user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to get a user's library",
        )
    library = await retrieve_library(id_user)
    if library:
        return ResponseModel(library)
    return ErrorResponseModel("Not found error", 404, "User library not found.")

@LibrariesRouter.get(
    "/{id_user}/assets", 
    response_description="Retrieve assets of user's library"
)
async def get_library_assets(
    id_user,
    user: dict = Depends(get_current_user)
):
    if not is_allowed_user(user, id_user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to get library assets.",
        )
    assets = await retrieve_library_assets(id_user)
    if assets or assets == []:
        return ResponseModel(assets)
    return ErrorResponseModel("Not found error", 404, "User library not found.")

@LibrariesRouter.delete(
    "/{id_user}/assets", 
    response_description="Delete asset from the user's library"
)
async def delete_library_asset(
    id_user, 
    delete_asset: DeleteAssetModel = Body(...),
    user: dict = Depends(get_current_user)
):
    if not is_allowed_user(user, id_user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to delete items",
        )
    deleted_item = await delete_asset_from_library(id_user, jsonable_encoder(delete_asset))
    if deleted_item:
        return ResponseModel([])
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST, 
        detail="Asset could not be removed from library. "
    ) 
                     
@LibrariesRouter.post(
    "/{id_user}/purchases", 
    response_description="Add new items to a user's library. \
        If this is the first time a user acquires items, the library is created"
)
async def add_purchase_to_library(
    id_user,
    user_email: str,
    assets_data: List[AssetModel] = Body(...),
    user: dict = Depends(get_current_user)
):
    if not is_allowed_user(user, id_user):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You do not have permission to purchase AIoD resources.",
        )

    library = await add_assets_to_library(id_user, user_email, assets_data)
    return ResponseModel(library, 201)
