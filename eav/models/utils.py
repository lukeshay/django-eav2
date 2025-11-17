"""
Utility functions for getting swappable EAV models.
Similar to Django's get_user_model() pattern.
"""

from django.apps import apps
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

from eav.settings import (
    EAV_ATTRIBUTE_MODEL as DEFAULT_ATTRIBUTE_MODEL,
    EAV_ENUM_GROUP_MODEL as DEFAULT_ENUM_GROUP_MODEL,
    EAV_ENUM_VALUE_MODEL as DEFAULT_ENUM_VALUE_MODEL,
    EAV_VALUE_MODEL as DEFAULT_VALUE_MODEL,
)


def get_attribute_model():
    """
    Return the Attribute model that is active in this project.
    
    Returns:
        The Attribute model class.
    
    Raises:
        ImproperlyConfigured: If the model cannot be found or is not configured correctly.
    """
    model_name = getattr(settings, "EAV_ATTRIBUTE_MODEL", DEFAULT_ATTRIBUTE_MODEL)
    try:
        return apps.get_model(model_name, require_ready=False)
    except ValueError:
        raise ImproperlyConfigured(
            "EAV_ATTRIBUTE_MODEL must be of the form 'app_label.model_name'"
        )
    except LookupError:
        raise ImproperlyConfigured(
            f"EAV_ATTRIBUTE_MODEL refers to model '{model_name}' "
            "that has not been installed"
        )


def get_value_model():
    """
    Return the Value model that is active in this project.
    
    Returns:
        The Value model class.
    
    Raises:
        ImproperlyConfigured: If the model cannot be found or is not configured correctly.
    """
    model_name = getattr(settings, "EAV_VALUE_MODEL", DEFAULT_VALUE_MODEL)
    try:
        return apps.get_model(model_name, require_ready=False)
    except ValueError:
        raise ImproperlyConfigured(
            "EAV_VALUE_MODEL must be of the form 'app_label.model_name'"
        )
    except LookupError:
        raise ImproperlyConfigured(
            f"EAV_VALUE_MODEL refers to model '{model_name}' "
            "that has not been installed"
        )


def get_enum_group_model():
    """
    Return the EnumGroup model that is active in this project.
    
    Returns:
        The EnumGroup model class.
    
    Raises:
        ImproperlyConfigured: If the model cannot be found or is not configured correctly.
    """
    model_name = getattr(settings, "EAV_ENUM_GROUP_MODEL", DEFAULT_ENUM_GROUP_MODEL)
    try:
        return apps.get_model(model_name, require_ready=False)
    except ValueError:
        raise ImproperlyConfigured(
            "EAV_ENUM_GROUP_MODEL must be of the form 'app_label.model_name'"
        )
    except LookupError:
        raise ImproperlyConfigured(
            f"EAV_ENUM_GROUP_MODEL refers to model '{model_name}' "
            "that has not been installed"
        )


def get_enum_value_model():
    """
    Return the EnumValue model that is active in this project.
    
    Returns:
        The EnumValue model class.
    
    Raises:
        ImproperlyConfigured: If the model cannot be found or is not configured correctly.
    """
    model_name = getattr(settings, "EAV_ENUM_VALUE_MODEL", DEFAULT_ENUM_VALUE_MODEL)
    try:
        return apps.get_model(model_name, require_ready=False)
    except ValueError:
        raise ImproperlyConfigured(
            "EAV_ENUM_VALUE_MODEL must be of the form 'app_label.model_name'"
        )
    except LookupError:
        raise ImproperlyConfigured(
            f"EAV_ENUM_VALUE_MODEL refers to model '{model_name}' "
            "that has not been installed"
        )
