from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional
from pathlib import Path
from dotenv import load_dotenv
import yaml


# TODO: The database here should be set to something like AgenticOps or similar
class MongoSettings(BaseSettings):
    mongodb_uri: str = "mongodb://localhost:27017"
    mongo_database: str = "agent_memory"
    agent_name: Optional[str] = None

    model_config = SettingsConfigDict(
        env_prefix="MONGO_",
        env_file=".env",
        extra="ignore",
    )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Auto-load from workspace if URI is still default
        workspace = Path("/workspace")
        if workspace.exists() and self.mongodb_uri == "mongodb://localhost:27017":
            # 1. Try .env files
            for env_file in [
                workspace / ".env",
                workspace / "mongo.env",
            ]:
                if env_file.exists():
                    load_dotenv(env_file)
                    # Re-init settings so env vars take effect
                    super().__init__(**kwargs)
                    break

            # 2. Try YAML config files
            if self.mongodb_uri == "mongodb://localhost:27017":
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
                                self.mongodb_uri = mongo_section["uri"]
                            if mongo_section.get("database"):
                                self.mongo_database = mongo_section["database"]
                            if mongo_section.get("agent_name"):
                                self.agent_name = mongo_section["agent_name"]
                        except Exception:
                            pass  # ignore malformed yaml

        # Auto-name database if agent_name is provided
        if self.agent_name and self.mongo_database == "agent_memory":
            self.mongo_database = f"agent_{self.agent_name}"

    def is_configured(self) -> bool:
        return self.mongodb_uri != "mongodb://localhost:27017"

    def get_config_error_message(self) -> str:
        return (
            "MongoDB URI not configured.\n"
            "Options:\n"
            "1. Pass -e MONGO_URI=... when running the container, or\n"
            "2. Create a .env file in your project root with MONGO_URI=..., or\n"
            "3. Create mongo.yaml in your project root with a 'mongo:' section.\n"
            "Make sure you mount your project: -v $(pwd):/workspace"
        )
