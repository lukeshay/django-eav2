"""
EAV-Django: Entity-Attribute-Value implementation for Django.

This package provides a flexible EAV implementation with swappable models.
"""

def register(model_cls, config_cls=None):
    """Register a model with EAV."""
    from eav.registry import Registry

    Registry.register(model_cls, config_cls)


def unregister(model_cls):
    """Unregister a model from EAV."""
    from eav.registry import Registry

    Registry.unregister(model_cls)


# Export swappable model helper functions for easy access
from eav.conf import (  # noqa: E402
    get_attribute_model,
    get_enum_group_model,
    get_enum_value_model,
    get_value_model,
)

__all__ = [
    'register',
    'unregister',
    'get_attribute_model',
    'get_value_model',
    'get_enum_group_model',
    'get_enum_value_model',
]
