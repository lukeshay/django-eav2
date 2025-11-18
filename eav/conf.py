from __future__ import annotations

from django.apps import apps
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

VALUE_MODEL_SETTING = "EAV_VALUE_MODEL"
DEFAULT_VALUE_MODEL = "eav.Value"


def get_value_model_name() -> str:
    """
    Return the dotted path for the configured Value model.

    Defaults to ``"eav.Value"`` unless the :data:`~django.conf.settings.EAV_VALUE_MODEL`
    setting overrides it.
    """

    return getattr(settings, VALUE_MODEL_SETTING, DEFAULT_VALUE_MODEL)


def get_value_model():
    """
    Return the configured Value model class.

    Raises
    ------
    ImproperlyConfigured
        If :data:`~django.conf.settings.EAV_VALUE_MODEL` is malformed or the
        referenced model cannot be found.
    """

    model_path = get_value_model_name()

    try:
        return apps.get_model(model_path, require_ready=False)
    except ValueError as err:  # pragma: no cover - defensive
        msg = (
            f"{VALUE_MODEL_SETTING} must be of the form 'app_label.ModelName', "
            f"but received '{model_path}'."
        )
        raise ImproperlyConfigured(msg) from err
    except LookupError as err:
        msg = (
            f"{VALUE_MODEL_SETTING} refers to '{model_path}', "
            "which has not been installed."
        )
        raise ImproperlyConfigured(msg) from err


def is_value_model_swapped() -> bool:
    """Return ``True`` when a custom Value model is configured."""

    return get_value_model_name() != DEFAULT_VALUE_MODEL
