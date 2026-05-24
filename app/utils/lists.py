def normalize_string_list(value: object) -> list[str]:
    """Normaliza un valor a lista de strings no vacíos."""
    if value is None:
        return []
    if isinstance(value, list):
        items = value
    elif isinstance(value, str):
        items = value.split(",")
    else:
        return []

    return [str(item).strip() for item in items if str(item).strip()]
