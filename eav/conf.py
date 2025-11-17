"""
Configuration module for swappable EAV models.

This module provides functions to retrieve swappable EAV models,
similar to Django's get_user_model() pattern.
"""

from django.apps import apps
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured


def get_attribute_model():
    """
    Return the Attribute model that is active in this project.
    
    Similar to Django's get_user_model(), this function returns the model
    specified in settings.EAV_ATTRIBUTE_MODEL, or the default Attribute model
    if the setting is not configured.
    
    Returns:
        Model class for Attribute
        
    Raises:
        ImproperlyConfigured: If the model specified in settings cannot be found
    """
    model_string = getattr(settings, 'EAV_ATTRIBUTE_MODEL', 'eav.Attribute')
    
    try:
        return apps.get_model(model_string, require_ready=False)
    except ValueError:
        raise ImproperlyConfigured(
            f"EAV_ATTRIBUTE_MODEL must be of the form 'app_label.model_name', "
            f"got '{model_string}'"
        )
    except LookupError:
        raise ImproperlyConfigured(
            f"EAV_ATTRIBUTE_MODEL refers to model '{model_string}' "
            f"that has not been installed"
        )


def get_value_model():
    """
    Return the Value model that is active in this project.
    
    Similar to Django's get_user_model(), this function returns the model
    specified in settings.EAV_VALUE_MODEL, or the default Value model
    if the setting is not configured.
    
    Returns:
        Model class for Value
        
    Raises:
        ImproperlyConfigured: If the model specified in settings cannot be found
    """
    model_string = getattr(settings, 'EAV_VALUE_MODEL', 'eav.Value')
    
    try:
        return apps.get_model(model_string, require_ready=False)
    except ValueError:
        raise ImproperlyConfigured(
            f"EAV_VALUE_MODEL must be of the form 'app_label.model_name', "
            f"got '{model_string}'"
        )
    except LookupError:
        raise ImproperlyConfigured(
            f"EAV_VALUE_MODEL refers to model '{model_string}' "
            f"that has not been installed"
        )


def get_enum_group_model():
    """
    Return the EnumGroup model that is active in this project.
    
    Similar to Django's get_user_model(), this function returns the model
    specified in settings.EAV_ENUM_GROUP_MODEL, or the default EnumGroup model
    if the setting is not configured.
    
    Returns:
        Model class for EnumGroup
        
    Raises:
        ImproperlyConfigured: If the model specified in settings cannot be found
    """
    model_string = getattr(settings, 'EAV_ENUM_GROUP_MODEL', 'eav.EnumGroup')
    
    try:
        return apps.get_model(model_string, require_ready=False)
    except ValueError:
        raise ImproperlyConfigured(
            f"EAV_ENUM_GROUP_MODEL must be of the form 'app_label.model_name', "
            f"got '{model_string}'"
        )
    except LookupError:
        raise ImproperlyConfigured(
            f"EAV_ENUM_GROUP_MODEL refers to model '{model_string}' "
            f"that has not been installed"
        )


def get_enum_value_model():
    """
    Return the EnumValue model that is active in this project.
    
    Similar to Django's get_user_model(), this function returns the model
    specified in settings.EAV_ENUM_VALUE_MODEL, or the default EnumValue model
    if the setting is not configured.
    
    Returns:
        Model class for EnumValue
        
    Raises:
        ImproperlyConfigured: If the model specified in settings cannot be found
    """
    model_string = getattr(settings, 'EAV_ENUM_VALUE_MODEL', 'eav.EnumValue')
    
    try:
        return apps.get_model(model_string, require_ready=False)
    except ValueError:
        raise ImproperlyConfigured(
            f"EAV_ENUM_VALUE_MODEL must be of the form 'app_label.model_name', "
            f"got '{model_string}'"
        )
    except LookupError:
        raise ImproperlyConfigured(
            f"EAV_ENUM_VALUE_MODEL refers to model '{model_string}' "
            f"that has not been installed"
        )


def get_attribute_model_string():
    """Return the string representation of the Attribute model."""
    return getattr(settings, 'EAV_ATTRIBUTE_MODEL', 'eav.Attribute')


def get_value_model_string():
    """Return the string representation of the Value model."""
    return getattr(settings, 'EAV_VALUE_MODEL', 'eav.Value')


def get_enum_group_model_string():
    """Return the string representation of the EnumGroup model."""
    return getattr(settings, 'EAV_ENUM_GROUP_MODEL', 'eav.EnumGroup')


def get_enum_value_model_string():
    """Return the string representation of the EnumValue model."""
    return getattr(settings, 'EAV_ENUM_VALUE_MODEL', 'eav.EnumValue')
