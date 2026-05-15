from controlforge.frameworks.framework_registry import (
    FRAMEWORK_REGISTRY
)


def get_framework_metadata(framework_code: str) -> dict:
    return FRAMEWORK_REGISTRY.get(
        framework_code,
        {
            "name": framework_code,
            "category": "Unknown",
            "description": "No framework metadata available.",
            "primary_domains": []
        }
    )