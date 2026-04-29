ALLOWED_COLLECTIONS = {"memories", "tasks", "journals", "logs", "knowledge"}
ALLOWED_OPERATIONS = {
    "insert_one",
    "find_one",
    "find",
    "update_one",
    "delete_one",
    "list_collections",
}


def validate_operation(operation: str, collection: str | None = None) -> bool:
    if operation not in ALLOWED_OPERATIONS:
        return False
    if (
        collection
        and collection not in ALLOWED_COLLECTIONS
        and not collection.startswith("custom_")
    ):
        return False
    return True
