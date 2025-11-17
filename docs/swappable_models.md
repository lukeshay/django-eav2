# Swappable EAV Models

EAV-Django now supports swappable models, similar to Django's `AUTH_USER_MODEL`. This feature allows you to customize the EAV models by adding your own fields and methods.

## Table of Contents

1. [Overview](#overview)
2. [Quick Start](#quick-start)
3. [Available Models](#available-models)
4. [Step-by-Step Guide](#step-by-step-guide)
5. [Best Practices](#best-practices)
6. [Migration Guide](#migration-guide)

## Overview

The swappable models feature allows you to extend the built-in EAV models with custom functionality. This is useful when you need to:

- Add custom fields to EAV models
- Override model methods
- Add custom validation
- Integrate with other parts of your application

## Quick Start

Here's a simple example of customizing the `Attribute` model:

```python
# myapp/models.py
from eav.models import AbstractAttribute

class CustomAttribute(AbstractAttribute):
    """Custom Attribute model with an additional field."""
    
    # Add your custom fields
    is_frontend_visible = models.BooleanField(
        default=True,
        help_text="Whether to return this attribute to the frontend"
    )
    
    class Meta(AbstractAttribute.Meta):
        swappable = 'EAV_ATTRIBUTE_MODEL'
```

```python
# settings.py
EAV_ATTRIBUTE_MODEL = 'myapp.CustomAttribute'
```

## Available Models

You can swap out any of the following EAV models:

### 1. Attribute Model

**Setting**: `EAV_ATTRIBUTE_MODEL`  
**Abstract Base**: `AbstractAttribute`  
**Default**: `eav.Attribute`

Stores attribute definitions (the "A" in EAV).

### 2. Value Model

**Setting**: `EAV_VALUE_MODEL`  
**Abstract Base**: `AbstractValue`  
**Default**: `eav.Value`

Stores attribute values for entities (the "V" in EAV).

### 3. EnumGroup Model

**Setting**: `EAV_ENUM_GROUP_MODEL`  
**Abstract Base**: `AbstractEnumGroup`  
**Default**: `eav.EnumGroup`

Groups enum values for multiple-choice attributes.

### 4. EnumValue Model

**Setting**: `EAV_ENUM_VALUE_MODEL`  
**Abstract Base**: `AbstractEnumValue`  
**Default**: `eav.EnumValue`

Stores individual enum value choices.

## Step-by-Step Guide

### 1. Create Your Custom Model

Create a new model that inherits from the appropriate abstract base class:

```python
# myapp/models.py
from django.db import models
from eav.models import AbstractAttribute

class CustomAttribute(AbstractAttribute):
    """
    Custom Attribute model with additional fields.
    """
    
    # Add custom fields
    is_frontend_visible = models.BooleanField(
        default=True,
        verbose_name="Frontend Visible",
        help_text="Whether to return this attribute to the frontend application"
    )
    
    category = models.CharField(
        max_length=100,
        blank=True,
        default="",
        help_text="Attribute category for grouping"
    )
    
    # Override methods if needed
    def save(self, *args, **kwargs):
        # Custom save logic
        super().save(*args, **kwargs)
    
    class Meta(AbstractAttribute.Meta):
        swappable = 'EAV_ATTRIBUTE_MODEL'
        verbose_name = "Custom Attribute"
        verbose_name_plural = "Custom Attributes"
```

### 2. Update Settings

Add the swappable model setting to your Django settings:

```python
# settings.py

# Swappable EAV model settings
EAV_ATTRIBUTE_MODEL = 'myapp.CustomAttribute'
# EAV_VALUE_MODEL = 'myapp.CustomValue'  # if needed
# EAV_ENUM_GROUP_MODEL = 'myapp.CustomEnumGroup'  # if needed
# EAV_ENUM_VALUE_MODEL = 'myapp.CustomEnumValue'  # if needed
```

**Important**: This setting must be defined before you create your first migration and cannot be changed after you've created database tables.

### 3. Create Migrations

Create and apply migrations for your custom model:

```bash
python manage.py makemigrations myapp
python manage.py migrate
```

### 4. Use Your Custom Model

The custom model will be used automatically throughout the application:

```python
from eav.conf import get_attribute_model

Attribute = get_attribute_model()

# Create an attribute with custom fields
attr = Attribute.objects.create(
    name='User Color Preference',
    slug='color_preference',
    datatype=Attribute.TYPE_TEXT,
    is_frontend_visible=True,  # Custom field!
    category='preferences'  # Custom field!
)
```

### 5. Register with Admin (Optional)

If you want to customize the admin interface:

```python
# myapp/admin.py
from django.contrib import admin
from eav.conf import get_attribute_model
from eav.admin import AttributeAdmin

Attribute = get_attribute_model()

class CustomAttributeAdmin(AttributeAdmin):
    list_display = AttributeAdmin.list_display + ('is_frontend_visible', 'category')
    list_filter = ('is_frontend_visible', 'category')
    
    fieldsets = (
        (None, {
            'fields': ('name', 'slug', 'datatype', 'description')
        }),
        ('Custom Fields', {
            'fields': ('is_frontend_visible', 'category')
        }),
        ('Advanced', {
            'fields': ('required', 'entity_ct', 'enum_group', 'display_order'),
            'classes': ('collapse',)
        }),
    )

# Unregister the default admin (if already registered)
try:
    admin.site.unregister(Attribute)
except admin.sites.NotRegistered:
    pass

# Register with custom admin
admin.site.register(Attribute, CustomAttributeAdmin)
```

## Complete Example

Here's a complete example showing how to customize the Attribute model for a multi-tenant application:

```python
# myapp/models.py
from django.db import models
from django.conf import settings
from eav.models import AbstractAttribute

class TenantAttribute(AbstractAttribute):
    """
    Attribute model with multi-tenant support.
    """
    
    # Multi-tenant field
    tenant = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='attributes',
        help_text="Owner of this attribute"
    )
    
    # Frontend visibility
    is_frontend_visible = models.BooleanField(
        default=True,
        help_text="Whether to return this attribute to the frontend"
    )
    
    # Categorization
    category = models.CharField(
        max_length=100,
        blank=True,
        default="",
        db_index=True,
        help_text="Category for grouping attributes"
    )
    
    # Access control
    is_public = models.BooleanField(
        default=False,
        help_text="Whether this attribute is public across tenants"
    )
    
    class Meta(AbstractAttribute.Meta):
        swappable = 'EAV_ATTRIBUTE_MODEL'
        verbose_name = "Tenant Attribute"
        verbose_name_plural = "Tenant Attributes"
        # Add unique constraint
        constraints = [
            models.UniqueConstraint(
                fields=['tenant', 'slug'],
                name='unique_tenant_slug'
            )
        ]
    
    def __str__(self):
        return f"{self.tenant.username}: {self.name}"
```

```python
# settings.py
EAV_ATTRIBUTE_MODEL = 'myapp.TenantAttribute'
```

```python
# Usage example
from eav.conf import get_attribute_model
from django.contrib.auth.models import User

Attribute = get_attribute_model()
user = User.objects.first()

# Create tenant-specific attribute
attr = Attribute.objects.create(
    tenant=user,
    name='Favorite Color',
    slug='fav_color',
    datatype=Attribute.TYPE_TEXT,
    is_frontend_visible=True,
    category='preferences',
    is_public=False
)
```

## Best Practices

### 1. Always Use Helper Functions

Instead of importing models directly, use the helper functions:

```python
# ❌ Don't do this
from eav.models import Attribute

# ✅ Do this instead
from eav.conf import get_attribute_model
Attribute = get_attribute_model()
```

### 2. Set Swappable Settings Early

Configure your swappable model settings before running your first migration:

```python
# settings.py - Set this BEFORE first migration
EAV_ATTRIBUTE_MODEL = 'myapp.CustomAttribute'
```

### 3. Inherit Meta Properly

Always inherit from the abstract model's Meta class:

```python
class CustomAttribute(AbstractAttribute):
    # ... your fields ...
    
    class Meta(AbstractAttribute.Meta):  # ← Important!
        swappable = 'EAV_ATTRIBUTE_MODEL'
```

### 4. Use Abstract Base Classes

Always inherit from the abstract base classes, not the concrete models:

```python
# ✅ Correct
from eav.models import AbstractAttribute
class CustomAttribute(AbstractAttribute):
    pass

# ❌ Wrong - Don't inherit from concrete models
from eav.models import Attribute
class CustomAttribute(Attribute):  # This won't work!
    pass
```

### 5. Update Foreign Keys

When referencing EAV models in your own models, use string references:

```python
from django.db import models
from eav.conf import get_attribute_model_string

class MyModel(models.Model):
    # Use string reference for swappable models
    attribute = models.ForeignKey(
        get_attribute_model_string(),  # Returns 'eav.Attribute' or your custom model
        on_delete=models.CASCADE
    )
```

## Migration Guide

### Migrating Existing Projects

If you have an existing project using the default EAV models and want to add custom fields:

**⚠️ Warning**: This process requires careful planning and may result in data migration.

#### Option 1: Fresh Start (Recommended for New Projects)

1. Create your custom models
2. Set the swappable settings
3. Delete existing EAV migrations
4. Create fresh migrations
5. Migrate your database

#### Option 2: Data Migration (For Existing Projects)

This is more complex and requires:

1. Create your custom models
2. Create a data migration to copy data from old tables to new tables
3. Update all foreign keys
4. Remove old tables

For existing projects with data, we recommend consulting with a Django expert or the EAV-Django community.

### Example: Adding a Field to Existing Database

If you already have EAV tables and want to add a custom field:

```python
# Step 1: Create custom model
from eav.models import AbstractAttribute

class CustomAttribute(AbstractAttribute):
    is_frontend_visible = models.BooleanField(default=True)
    
    class Meta(AbstractAttribute.Meta):
        swappable = 'EAV_ATTRIBUTE_MODEL'
        db_table = 'eav_attribute'  # Use existing table!
```

```python
# Step 2: Update settings
# settings.py
EAV_ATTRIBUTE_MODEL = 'myapp.CustomAttribute'
```

```bash
# Step 3: Create migration for new field
python manage.py makemigrations myapp
python manage.py migrate
```

## Troubleshooting

### Issue: "ImproperlyConfigured" Error

**Problem**: Getting an error about the model not being found.

**Solution**: Make sure:
- The model is defined in your app's `models.py`
- The app is in `INSTALLED_APPS`
- The setting uses the correct format: `'app_label.ModelName'`

### Issue: Migration Conflicts

**Problem**: Migrations are creating duplicate tables.

**Solution**: Use the `db_table` Meta option to point to the existing table:

```python
class CustomAttribute(AbstractAttribute):
    class Meta(AbstractAttribute.Meta):
        swappable = 'EAV_ATTRIBUTE_MODEL'
        db_table = 'eav_attribute'  # Point to existing table
```

### Issue: Foreign Key Errors

**Problem**: Foreign keys to EAV models are breaking.

**Solution**: Use string references and helper functions:

```python
from eav.conf import get_attribute_model_string

class MyModel(models.Model):
    attribute = models.ForeignKey(
        get_attribute_model_string(),
        on_delete=models.CASCADE
    )
```

## API Reference

### Helper Functions

All helper functions are available in `eav.conf`:

```python
from eav.conf import (
    get_attribute_model,
    get_value_model,
    get_enum_group_model,
    get_enum_value_model,
    get_attribute_model_string,
    get_value_model_string,
    get_enum_group_model_string,
    get_enum_value_model_string,
)
```

#### `get_attribute_model()`
Returns the Attribute model class that is active in the project.

#### `get_value_model()`
Returns the Value model class that is active in the project.

#### `get_enum_group_model()`
Returns the EnumGroup model class that is active in the project.

#### `get_enum_value_model()`
Returns the EnumValue model class that is active in the project.

#### `get_*_model_string()`
Returns the string representation of the model (e.g., `'eav.Attribute'` or `'myapp.CustomAttribute'`).
Useful for ForeignKey definitions.

## Additional Resources

- [Django Swappable Models Documentation](https://docs.djangoproject.com/en/stable/topics/auth/customizing/#substituting-a-custom-user-model)
- [EAV-Django Main Documentation](../README.md)
- [Contributing Guide](../CONTRIBUTING.md)

## Support

If you encounter issues with swappable models:

1. Check this documentation
2. Review the example code in `/examples/` (if available)
3. Open an issue on GitHub with:
   - Your custom model code
   - Your settings configuration
   - The full error traceback
   - Django and EAV-Django versions
