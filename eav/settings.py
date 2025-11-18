from typing import Final

CHARFIELD_LENGTH: Final = 100

# Swappable model settings
# These can be overridden in your Django settings to use custom models
EAV_ATTRIBUTE_MODEL: Final = "eav.Attribute"
EAV_VALUE_MODEL: Final = "eav.Value"
