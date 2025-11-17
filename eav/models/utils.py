"""
Utility function for getting the swappable Attribute model.
Similar to Django's get_user_model() pattern.
"""

from django.apps import apps
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

from eav.settings import EAV_ATTRIBUTE_MODEL as DEFAULT_ATTRIBUTE_MODEL


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
