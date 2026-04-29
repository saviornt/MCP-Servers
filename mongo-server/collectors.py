from pymongo.asynchronous.mongo_client import AsyncMongoClient
from pymongo.operations import SearchIndexModel
from config import MongoSettings
from models import MongoStatusModel, CommandResultModel, ConfigErrorModel

config = MongoSettings()


async def mongo_get_status(database: str | None = None):
    if not config.is_configured():
        return ConfigErrorModel(
            error="MongoDB not configured", message=config.get_config_error_message()
        )
    db_name = database or config.mongo_database
    try:
        client = AsyncMongoClient(config.mongo_uri)
        await client.admin.command("ping")
        collections = await client[db_name].list_collection_names()
        return MongoStatusModel(
            connected=True,
            database=db_name,
            collections=collections,
            message="Connected successfully",
        )
    except Exception as e:
        return MongoStatusModel(
            connected=False, database=db_name, collections=[], message=str(e)
        )


async def mongo_list_collections(database: str | None = None):
    if not config.is_configured():
        return ConfigErrorModel(
            error="MongoDB not configured", message=config.get_config_error_message()
        )
    db_name = database or config.mongo_database
    try:
        client = AsyncMongoClient(config.mongo_uri)
        collections = await client[db_name].list_collection_names()
        return CommandResultModel(
            success=True, message="Collections listed", data=collections
        )
    except Exception as e:
        return CommandResultModel(success=False, message=str(e))


async def mongo_insert_one(
    collection: str, document: dict, database: str | None = None
):
    if not config.is_configured():
        return ConfigErrorModel(
            error="MongoDB not configured", message=config.get_config_error_message()
        )
    db_name = database or config.mongo_database
    try:
        client = AsyncMongoClient(config.mongo_uri)
        result = await client[db_name][collection].insert_one(document)
        return CommandResultModel(
            success=True,
            message="Inserted",
            data={"inserted_id": str(result.inserted_id)},
        )
    except Exception as e:
        return CommandResultModel(success=False, message=str(e))


async def mongo_find_one(collection: str, query: dict, database: str | None = None):
    if not config.is_configured():
        return ConfigErrorModel(
            error="MongoDB not configured", message=config.get_config_error_message()
        )
    db_name = database or config.mongo_database
    try:
        client = AsyncMongoClient(config.mongo_uri)
        result = await client[db_name][collection].find_one(query)
        return CommandResultModel(success=True, message="Found", data=result)
    except Exception as e:
        return CommandResultModel(success=False, message=str(e))


async def mongo_find(
    collection: str, query: dict, limit: int = 50, database: str | None = None
):
    if not config.is_configured():
        return ConfigErrorModel(
            error="MongoDB not configured", message=config.get_config_error_message()
        )
    db_name = database or config.mongo_database
    try:
        client = AsyncMongoClient(config.mongo_uri)
        cursor = client[db_name][collection].find(query).limit(limit)
        results = await cursor.to_list(length=limit)
        return CommandResultModel(success=True, message="Found", data=results)
    except Exception as e:
        return CommandResultModel(success=False, message=str(e))


async def mongo_update_one(
    collection: str, query: dict, update: dict, database: str | None = None
):
    if not config.is_configured():
        return ConfigErrorModel(
            error="MongoDB not configured", message=config.get_config_error_message()
        )
    db_name = database or config.mongo_database
    try:
        client = AsyncMongoClient(config.mongo_uri)
        result = await client[db_name][collection].update_one(query, update)
        return CommandResultModel(
            success=True,
            message="Updated",
            data={"modified_count": result.modified_count},
        )
    except Exception as e:
        return CommandResultModel(success=False, message=str(e))


async def mongo_delete_one(collection: str, query: dict, database: str | None = None):
    if not config.is_configured():
        return ConfigErrorModel(
            error="MongoDB not configured", message=config.get_config_error_message()
        )
    db_name = database or config.mongo_database
    try:
        client = AsyncMongoClient(config.mongo_uri)
        result = await client[db_name][collection].delete_one(query)
        return CommandResultModel(
            success=True,
            message="Deleted",
            data={"deleted_count": result.deleted_count},
        )
    except Exception as e:
        return CommandResultModel(success=False, message=str(e))


async def mongo_ensure_vector_index(
    collection: str = "memories", path: str = "content", model: str = "voyage-4"
):
    if not config.mongo_vector_search:
        return CommandResultModel(
            success=False, message="MONGO_VECTOR_SEARCH flag is disabled"
        )
    if not config.is_configured():
        return ConfigErrorModel(
            error="MongoDB not configured", message=config.get_config_error_message()
        )
    db_name = config.mongo_database
    try:
        client = AsyncMongoClient(config.mongo_uri)
        coll = client[db_name][collection]
        index_model = SearchIndexModel(
            definition={
                "fields": [
                    {
                        "type": "autoEmbed",
                        "modality": "text",
                        "path": path,
                        "model": model,
                    },
                    {"type": "filter", "path": "memory_type"},
                ]
            },
            name="vector_index",
            type="vectorSearch",
        )
        await coll.create_search_index(model=index_model)

        cursor = await coll.list_search_indexes("vector_index")
        indexes = await cursor.to_list(length=10)
        if indexes and indexes[0].get("queryable") is True:
            return CommandResultModel(
                success=True,
                message="Vector index ready",
                data={"index": "vector_index"},
            )
        return CommandResultModel(
            success=True, message="Index created (still warming up)"
        )
    except Exception as e:
        return CommandResultModel(success=False, message=str(e))


async def mongo_semantic_search(
    collection: str, query: str, limit: int = 10, path: str = "content"
):
    """Semantic vector search using Auto-Embedding index."""
    if not config.mongo_vector_search:
        return CommandResultModel(
            success=False, message="MONGO_VECTOR_SEARCH flag is disabled"
        )
    if not config.is_configured():
        return ConfigErrorModel(
            error="MongoDB not configured", message=config.get_config_error_message()
        )
    db_name = config.mongo_database
    try:
        client = AsyncMongoClient(config.mongo_uri)
        coll = client[db_name][collection]

        pipeline = [
            {
                "$vectorSearch": {
                    "index": "vector_index",
                    "path": path,  # now correctly passed
                    "queryVector": query,  # text query (auto-embedded by the index)
                    "limit": limit,
                    "numCandidates": limit * 10,
                }
            },
            {"$project": {"_id": 0, "score": {"$meta": "vectorSearchScore"}}},
        ]

        cursor = await coll.aggregate(pipeline)  # ← missing await fixed
        results = await cursor.to_list(length=limit)  # ← now correct async cursor
        return CommandResultModel(
            success=True, message="Semantic search complete", data=results
        )
    except Exception as e:
        return CommandResultModel(success=False, message=str(e))
