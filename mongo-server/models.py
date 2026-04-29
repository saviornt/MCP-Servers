from pydantic import BaseModel
from typing import List, Optional, Any


class MongoStatusModel(BaseModel):
    connected: bool
    database: str
    collections: List[str]
    message: str


class MongoCapabilitiesModel(BaseModel):
    platform: str
    pymongo_version: str
    configured: bool
    vector_search_enabled: bool


class CommandResultModel(BaseModel):
    success: bool
    message: str
    data: Optional[Any] = None


class ConfigErrorModel(BaseModel):
    error: str
    message: str
    action_needed: bool = True
