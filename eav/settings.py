"""
EAV-Django settings configuration.

This module defines settings and constants used throughout the EAV-Django package.
"""

from typing import Final

CHARFIELD_LENGTH: Final = 100

# Swappable Model Settings
# -------------------------
# These settings allow you to swap out the default EAV models with custom implementations.
# This is similar to Django's AUTH_USER_MODEL setting.
#
# To use custom models, create your own models that inherit from the abstract base models
# in eav.models.abstract, then set the appropriate setting in your Django settings file:
#
# Example:
#   # In your Django settings.py:
#   EAV_ATTRIBUTE_MODEL = 'myapp.CustomAttribute'
#   EAV_VALUE_MODEL = 'myapp.CustomValue'
#   EAV_ENUM_GROUP_MODEL = 'myapp.CustomEnumGroup'
#   EAV_ENUM_VALUE_MODEL = 'myapp.CustomEnumValue'
#
# Note: These settings must be defined before running migrations and cannot be changed
# after you have created database tables.
