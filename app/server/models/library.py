from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field, constr, create_model

class AssetModel(BaseModel):
    identifier: constr(strict=True) = Field(...)
    name: str = Field(...)
    category: str = Field(...)
    url_metadata: str = Field(...)
    price: int = Field(default=0)
    added_at: int = Field(default=0)

    class config:
        schema_extra = {
            "example": {
                "identifier": "1",
                "name": "name",
                "category": "dataset",
                "url_metadata": "http://example.com",
                "price": 0,
                "added_at": 1324560
            }
        }
    
    @classmethod
    def as_optional(cls):
        annonations = cls.__fields__
        fields = {
            attribute: (Optional[data_type.type_], None)
            for attribute, data_type in annonations.items()
        }
        OptionalModel = create_model(f"Optional{cls.__name__}", **fields)
        return OptionalModel


class LibraryModel(BaseModel):
    id_user: constr(strict=True) = Field(...)
    user_email: EmailStr = Field(...)
    assets: List[AssetModel] = Field(default=[])
    created_at: int = Field(default=0)
    modified_at: int = Field(default=0)

    class config:
        schema_extra = {
            "example": {
                "id_user": "12a12b12-aa45-2nn2-5t6mss123q5a",
                "user_email": "user@foo.com",
                "assets": [
                    {
                        "identifier": "1",
                        "name": "name",
                        "url_metadata": "http://example.com",
                        "price": 0,
                        "added_at": 1324560
                    }
                ],
                "created_at": 1324560,
                "modified_at": 1324560
            }
        }
    
    @classmethod
    def as_optional(cls):
        annonations = cls.__fields__
        fields = {
            attribute: (Optional[data_type.type_], None)
            for attribute, data_type in annonations.items()
        }
        OptionalModel = create_model(f"Optional{cls.__name__}", **fields)
        return OptionalModel
    
class DeleteAssetModel(BaseModel):
    identifier: constr(strict=True) = Field(...)
    category: str = Field(...)

    class config:
        schema_extra = {
            "example": {
                "identifier": "1",
                "category": "dataset"
            }
        }