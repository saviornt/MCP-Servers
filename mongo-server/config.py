from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional
from pathlib import Path
from dotenv import load_dotenv
import yaml


class MongoSettings(BaseSettings):
    mongo_uri: str = "mongodb://localhost:27017"  # ← renamed for brevity
    mongo_database: str = "default_db"
    agent_name: Optional[str] = None
    mongo_vector_search: bool = False  # ← new flag

    model_config = SettingsConfigDict(
        env_prefix="MONGO_", env_file=".env", extra="ignore"
    )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        workspace = Path("/workspace")
        if workspace.exists() and self.mongo_uri == "mongodb://localhost:27017":
            # .env / mongo.env lookup + YAML lookup (same smart logic as before)
            for env_file in [workspace / ".env", workspace / "mongo.env"]:
                if env_file.exists():
                    load_dotenv(env_file)
                    super().__init__(**kwargs)
                    break
            if self.mongo_uri == "mongodb://localhost:27017":
                for yaml_file in [
                    workspace / "mongo.yaml",
                    workspace / "config.yaml",
                    workspace / "settings.yaml",
                ]:
                    if yaml_file.exists():
                        try:
                            with open(yaml_file, "r", encoding="utf-8") as f:
                                data = yaml.safe_load(f) or {}
                            mongo_section = data.get("mongo") or data
                            if mongo_section.get("uri"):
                                self.mongo_uri = mongo_section["uri"]
                            if mongo_section.get("database"):
                                self.mongo_database = mongo_section["database"]
                            if mongo_section.get("agent_name"):
                                self.agent_name = mongo_section["agent_name"]
                            if mongo_section.get("vector_search") is not None:
                                self.mongo_vector_search = mongo_section[
                                    "vector_search"
                                ]
                        except Exception:
                            pass
        if self.agent_name and self.mongo_database == "default_db":
            self.mongo_database = f"agent_{self.agent_name}"

    def is_configured(self) -> bool:
        return self.mongo_uri != "mongodb://localhost:27017"

    def get_config_error_message(self) -> str:
        return (
            "MongoDB URI not configured.\n"
            "1. Add -e MONGO_URI=... to docker run, or\n"
            "2. Create .env / mongo.env in workspace, or\n"
            "3. Create mongo.yaml / config.yaml in workspace.\n"
            "Mount with -v $(pwd):/workspace"
        )
