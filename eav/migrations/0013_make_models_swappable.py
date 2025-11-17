# Generated migration for swappable EAV models

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):
    """
    This migration makes the EAV models swappable.
    
    This allows users to customize the EAV models by:
    1. Creating models that inherit from Abstract* base classes
    2. Setting the appropriate EAV_*_MODEL settings
    
    Note: This migration does not alter the database schema.
    It only updates the model Meta options to make them swappable.
    """

    dependencies = [
        ('eav', '0012_add_value_uniqueness_checks'),
    ]

    operations = [
        # No database operations needed - swappable is a Meta option only
        # The actual swappable setting is now in the model's Meta class
    ]
