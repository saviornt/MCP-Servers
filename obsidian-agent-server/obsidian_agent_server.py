from mcp.server.fastmcp import FastMCP
from pathlib import Path
import os
from datetime import datetime, timezone

mcp = FastMCP("agentos-obsidian")

# ==================================================
# VAULT ROOT
# ==================================================
def get_vault_root() -> Path:
    # Optional override for full control
    env_override = os.environ.get("AGENTOS_VAULT_PATH")
    if env_override:
        return Path(env_override)

    # Unified AgentOS convention
    return Path.home() / "Documents" / "Vaults"

VAULT_ROOT = get_vault_root()


# ==================================================
# DYNAMIC VAULT DISCOVERY
# ==================================================
def list_vaults():
    if not VAULT_ROOT.exists():
        return []
    return [p.name for p in VAULT_ROOT.iterdir() if p.is_dir()]


# ==================================================
# SAFE PATH RESOLUTION
# ==================================================
def resolve(vault: str, path: str) -> Path:
    return VAULT_ROOT / vault / path


# ==================================================
# TOOL CAPABILITY MANIFEST (NO MORE STATIC DICT)
# ==================================================
def tool_manifest(tool_name: str):
    return {
        "tool": tool_name,
        "available_vaults": list_vaults(),
        "source": "agentos-obsidian-mcp",
        "generated_at": datetime.now(timezone.utc).isoformat(),
    }


# ==================================================
# READ NOTE
# ==================================================
@mcp.tool()
def read_note(vault: str, path: str):
    file = resolve(vault, path)

    if not file.exists():
        return None

    return {
        "content": file.read_text(encoding="utf-8"),
        "meta": tool_manifest("read_note"),
        "vault": vault,
    }


# ==================================================
# WRITE NOTE
# ==================================================
@mcp.tool()
def write_note(vault: str, path: str, content: str):
    file = resolve(vault, path)
    file.parent.mkdir(parents=True, exist_ok=True)
    file.write_text(content, encoding="utf-8")

    return {
        "status": "written",
        "file": str(file),
        "meta": tool_manifest("write_note"),
        "vault": vault,
    }


# ==================================================
# APPEND NOTE
# ==================================================
@mcp.tool()
def append_note(vault: str, path: str, content: str):
    file = resolve(vault, path)
    file.parent.mkdir(parents=True, exist_ok=True)

    with open(file, "a", encoding="utf-8") as f:
        f.write("\n" + content)

    return {"status": "appended", "meta": tool_manifest("append_note"), "vault": vault}


# ==================================================
# LIST NOTES (VAULT-AWARE)
# ==================================================
@mcp.tool()
def list_notes(vault: str, subpath: str = ""):
    base = VAULT_ROOT / vault / subpath

    if not base.exists():
        return []

    return [str(p.relative_to(VAULT_ROOT / vault)) for p in base.rglob("*.md")]


# ==================================================
# SEARCH VAULT (basic first-pass index)
# ==================================================
@mcp.tool()
def search_vault(vault: str, query: str):
    base = VAULT_ROOT / vault
    results = []

    for file in base.rglob("*.md"):
        try:
            text = file.read_text(encoding="utf-8")
            if query.lower() in text.lower():
                results.append(str(file.relative_to(base)))
        except Exception:
            continue

    return {"results": results, "meta": tool_manifest("search_vault"), "vault": vault}


# ==================================================
# SYSTEM IDENTITY (AgentOS self-definition)
# ==================================================
@mcp.tool()
def get_identity():
    file = VAULT_ROOT / "system" / "identity.md"
    if not file.exists():
        return None
    return file.read_text(encoding="utf-8")


@mcp.tool()
def set_identity(content: str):
    file = VAULT_ROOT / "system" / "identity.md"
    file.parent.mkdir(parents=True, exist_ok=True)
    file.write_text(content, encoding="utf-8")
    return "identity updated"


# ==================================================
# SYSTEM LOGGING (agent memory trace)
# ==================================================
@mcp.tool()
def log_event(event: str):
    file = VAULT_ROOT / "system" / "logs.md"
    file.parent.mkdir(parents=True, exist_ok=True)

    entry = f"- {datetime.now(timezone.utc).isoformat()} {event}\n"

    with open(file, "a", encoding="utf-8") as f:
        f.write(entry)

    return {"status": "logged"}
