import platform
from models import MongoCapabilitiesModel


def collect_capabilities():
    """Return structured capabilities (includes vector search flag)."""
    return MongoCapabilitiesModel(
        platform=platform.system(),
        pymongo_version="4.17.0",
        configured=False,  # updated at runtime
        vector_search_enabled=False,  # updated at runtime from config
    )
