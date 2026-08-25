from app.services.official_sources import list_official_sources


def available_connectors() -> dict:
    sources = list_official_sources()
    return {
        "status": "catalog",
        "connectors": [
            {
                "name": item["name"],
                "category": category,
                "url": item["url"],
                "purpose": item["purpose"],
                "mode": "manual_or_api_adapter_required",
            }
            for category, items in sources.items()
            for item in items
        ],
    }
