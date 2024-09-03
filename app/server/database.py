import time
import motor.motor_asyncio

from server.config import DB_CONFIG
from dotenv import load_dotenv
from bson.objectid import ObjectId
from fastapi.encoders import jsonable_encoder


load_dotenv()

try:
    client = motor.motor_asyncio.AsyncIOMotorClient(DB_CONFIG.get('url'))
except Exception as e:
    raise SystemExit(f"Could not connect to MongoDB: {e}")
    
database = client.mylibrary
libraries_collection = database.get_collection(
    DB_CONFIG.get('collection')
)

## Library

def library_helper(library) -> dict:
    assets = []
    if "assets" in library:
        assets = library["assets"]

    return {
        "id_user": str(library["id_user"]),
        "user_email": library["user_email"],
        "assets": assets_helper(assets),
        "created_at": library["created_at"],
        "modified_at": library["modified_at"],
    }

def assets_helper(assets) :
    list_assets = []
    for asset in assets:
        list_assets.append(asset_helper(asset))
    return list_assets

def asset_helper(asset) -> dict:
    return {
        "identifier": str(asset["identifier"]),
        "name": asset["name"],
        "category": asset["category"],
        "url_metadata": asset["url_metadata"],
        "price": asset["price"],
        "added_at": asset["added_at"],
    }

# Buscar todes les socies de la base de datos
async def retrieve_libraries():
    libraries = []
    async for library in libraries_collection.find():
        libraries.append(library_helper(library))
    return libraries

# Get library associated to a user
# ToDo: return error if library not found
async def retrieve_library(id_user: str) -> dict:
    library = await libraries_collection.find_one({"id_user": id_user})
    if library:
        return library_helper(library)
    else:
        return False    

# Get library associated to a user
async def retrieve_library_assets(id_user: str) -> dict:
    library = await libraries_collection.find_one({"id_user": id_user})
    if library:
        return assets_helper(library['assets'])
    else:
        return False
    
# Add a new library to the database
async def add_library(library_data: dict):
    library = await libraries_collection.insert_one(library_data)
    updated_data = {
        "created_at": int(time.time()), # timestamp in seconds
        "modified_at": int(time.time())
    }
    updated_library = await libraries_collection.update_one(
        {"_id": ObjectId(library.inserted_id)}, {"$set": updated_data}
    )
    new_library = await libraries_collection.find_one({"_id": library.inserted_id})

    return library_helper(new_library)

# ToDo: 
# - refactor code
# - update assets added date?
async def add_assets_to_library(
        id_user: str, 
        user_email: str, 
        new_assets_data
    ) -> dict:

    res = await libraries_collection.find_one({"id_user": id_user})

    if res is None:
        library_data = {
            "id_user": id_user,
            "user_email": user_email,
            "assets": new_assets_data,
            "created_at": int(time.time()),
            "modified_at": int(time.time())
        }
        library = await libraries_collection.insert_one(jsonable_encoder(library_data))
        new_library = await libraries_collection.find_one({"_id": library.inserted_id})
        
        return library_helper(new_library)
    else:
        existing_assets = res['assets']
        updated_assets = existing_assets.copy()
        print(existing_assets)
        
        for new_asset in new_assets_data:
            if not any(existing_asset['identifier'] == new_asset.identifier for existing_asset in existing_assets):
                updated_assets.append(new_asset.dict())
        
        if len(updated_assets) > len(existing_assets):
            updated_data = {
                "assets": updated_assets,
                "modified_at": int(time.time())
            }
            await libraries_collection.update_one(
                { "id_user": id_user }, { "$set": updated_data }
            )
            updated_library = await libraries_collection.find_one({ "id_user": id_user })

            return library_helper(updated_library)
    
async def delete_asset_from_library(
        id_user: str, 
        delete_asset: dict
):
    res = await libraries_collection.find_one({"id_user": id_user})

    if res:
        current_assets = res['assets']
        asset_found = False
        index_of_asset = 0
        
        for asset in current_assets:
            if asset['identifier'] == delete_asset["identifier"] \
                and asset['category'] == delete_asset["category"]:
                asset_found = True
                break
            index_of_asset += 1
        
        if asset_found:
            updated_assets = current_assets.pop(index_of_asset)
            
            updated_data = { 
                "assets": current_assets
            }
            updated_result = await libraries_collection.update_one(
                {"id_user": id_user}, {"$set": updated_data}
            )

            return True
        return False
    return False
        


    

 