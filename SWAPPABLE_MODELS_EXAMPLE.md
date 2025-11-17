# Swappable Models Example

This document provides a complete example of how to use the swappable models feature in EAV-Django.

## Problem Statement

We want to add an additional field to the Attribute model to specify whether to return the attribute to our front-end application.

## Solution

Use the swappable models feature to create a custom Attribute model.

## Step-by-Step Implementation

### 1. Create Custom Model

In your Django app (e.g., `myapp/models.py`):

```python
from django.db import models
from eav.models import AbstractAttribute


class CustomAttribute(AbstractAttribute):
    """
    Custom Attribute model with frontend visibility flag.
    """
    
    # Add the custom field
    show_in_frontend = models.BooleanField(
        default=True,
        verbose_name="Show in Frontend",
        help_text="Whether to return this attribute to the frontend application"
    )
    
    class Meta(AbstractAttribute.Meta):
        swappable = 'EAV_ATTRIBUTE_MODEL'
        verbose_name = "Attribute"
        verbose_name_plural = "Attributes"
```

### 2. Configure Settings

In your Django `settings.py`:

```python
# Point to your custom model
EAV_ATTRIBUTE_MODEL = 'myapp.CustomAttribute'
```

### 3. Create and Run Migrations

```bash
python manage.py makemigrations myapp
python manage.py migrate
```

### 4. Use the Custom Model

#### In your code:

```python
# Always use the helper function to get the model
from eav import get_attribute_model

Attribute = get_attribute_model()

# Create attributes with the custom field
color_attr = Attribute.objects.create(
    name='Favorite Color',
    slug='fav_color',
    datatype=Attribute.TYPE_TEXT,
    show_in_frontend=True  # Custom field!
)

internal_attr = Attribute.objects.create(
    name='Internal Note',
    slug='internal_note',
    datatype=Attribute.TYPE_TEXT,
    show_in_frontend=False  # Hidden from frontend!
)
```

#### In your API views:

```python
from rest_framework import serializers
from eav import get_attribute_model

Attribute = get_attribute_model()


class AttributeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attribute
        fields = ['name', 'slug', 'datatype', 'show_in_frontend']


def get_frontend_attributes(request):
    """Get only attributes that should be shown in the frontend."""
    attributes = Attribute.objects.filter(show_in_frontend=True)
    serializer = AttributeSerializer(attributes, many=True)
    return Response(serializer.data)
```

### 5. Customize Admin (Optional)

In your `myapp/admin.py`:

```python
from django.contrib import admin
from eav import get_attribute_model

Attribute = get_attribute_model()


@admin.register(Attribute)
class CustomAttributeAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'datatype', 'show_in_frontend', 'required')
    list_filter = ('datatype', 'show_in_frontend', 'required')
    search_fields = ('name', 'slug', 'description')
    prepopulated_fields = {'slug': ('name',)}
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'datatype', 'description')
        }),
        ('Frontend Configuration', {
            'fields': ('show_in_frontend',)
        }),
        ('Advanced Options', {
            'fields': ('required', 'entity_ct', 'enum_group', 'display_order'),
            'classes': ('collapse',)
        }),
    )
```

## Complete Working Example

Here's a complete example with a Django app:

```python
# myproject/myapp/models.py
from django.db import models
from eav.models import AbstractAttribute


class FrontendAttribute(AbstractAttribute):
    """
    Attribute model with frontend visibility control.
    """
    
    # Frontend visibility
    show_in_frontend = models.BooleanField(
        default=True,
        db_index=True,
        verbose_name="Show in Frontend",
        help_text="Whether to return this attribute to the frontend application"
    )
    
    # Optional: Add category for better organization
    category = models.CharField(
        max_length=50,
        blank=True,
        default='general',
        choices=[
            ('general', 'General'),
            ('personal', 'Personal'),
            ('system', 'System'),
            ('internal', 'Internal'),
        ],
        help_text="Category for grouping attributes"
    )
    
    class Meta(AbstractAttribute.Meta):
        swappable = 'EAV_ATTRIBUTE_MODEL'
        verbose_name = "Frontend Attribute"
        verbose_name_plural = "Frontend Attributes"
    
    def __str__(self):
        visibility = "✓" if self.show_in_frontend else "✗"
        return f"{self.name} ({self.get_datatype_display()}) [{visibility}]"
```

```python
# myproject/settings.py
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    
    'eav',
    'myapp',  # Your app with custom model
]

# Configure swappable model
EAV_ATTRIBUTE_MODEL = 'myapp.FrontendAttribute'
```

```python
# myproject/myapp/views.py
from django.http import JsonResponse
from eav import get_attribute_model

Attribute = get_attribute_model()


def api_attributes(request):
    """
    API endpoint that returns only frontend-visible attributes.
    """
    attributes = Attribute.objects.filter(
        show_in_frontend=True
    ).values('name', 'slug', 'datatype', 'description', 'required')
    
    return JsonResponse({
        'attributes': list(attributes)
    })


def all_attributes_with_visibility(request):
    """
    Internal endpoint that returns all attributes with visibility info.
    """
    attributes = Attribute.objects.all().values(
        'name', 
        'slug', 
        'datatype', 
        'show_in_frontend',
        'category'
    )
    
    return JsonResponse({
        'attributes': list(attributes)
    })
```

```python
# myproject/myapp/management/commands/setup_attributes.py
from django.core.management.base import BaseCommand
from eav import get_attribute_model

Attribute = get_attribute_model()


class Command(BaseCommand):
    help = 'Set up initial attributes'

    def handle(self, *args, **options):
        # Frontend attributes
        Attribute.objects.get_or_create(
            slug='username',
            defaults={
                'name': 'Username',
                'datatype': Attribute.TYPE_TEXT,
                'show_in_frontend': True,
                'category': 'personal',
                'required': True,
            }
        )
        
        Attribute.objects.get_or_create(
            slug='age',
            defaults={
                'name': 'Age',
                'datatype': Attribute.TYPE_INT,
                'show_in_frontend': True,
                'category': 'personal',
            }
        )
        
        # Internal attribute (not shown in frontend)
        Attribute.objects.get_or_create(
            slug='internal_notes',
            defaults={
                'name': 'Internal Notes',
                'datatype': Attribute.TYPE_TEXT,
                'show_in_frontend': False,
                'category': 'internal',
            }
        )
        
        self.stdout.write(
            self.style.SUCCESS('Successfully created attributes')
        )
```

## Usage in Your Application

```python
# Example: Using EAV with custom attribute model

import eav
from django.contrib.auth.models import User
from eav import get_attribute_model

# Register User model with EAV
eav.register(User)

# Get the custom attribute model
Attribute = get_attribute_model()

# Create a user
user = User.objects.create_user(username='john_doe')

# Get frontend attributes
frontend_attrs = Attribute.objects.filter(show_in_frontend=True)

# Set attribute values
for attr in frontend_attrs:
    if attr.slug == 'age':
        user.eav.age = 25
    elif attr.slug == 'username':
        user.eav.username = 'johndoe'

user.save()

# Get internal attributes (not shown in frontend)
internal_attrs = Attribute.objects.filter(show_in_frontend=False)
for attr in internal_attrs:
    if attr.slug == 'internal_notes':
        user.eav.internal_notes = 'This is an internal note'

user.save()

# API response example
def get_user_frontend_data(user):
    """Get user data including only frontend-visible EAV attributes."""
    data = {
        'id': user.id,
        'username': user.username,
        'email': user.email,
        'attributes': {}
    }
    
    # Get all frontend attributes
    frontend_attrs = Attribute.objects.filter(show_in_frontend=True)
    
    for attr in frontend_attrs:
        value = getattr(user.eav, attr.slug, None)
        if value is not None:
            data['attributes'][attr.slug] = {
                'name': attr.name,
                'value': value,
                'type': attr.datatype,
            }
    
    return data
```

## Benefits

1. **Flexibility**: Add custom fields without modifying the core package
2. **Maintainability**: Keep your customizations separate from the package code
3. **Upgradability**: Update EAV-Django without losing your customizations
4. **Type Safety**: Use Django's ORM features with your custom fields
5. **Reusability**: Share your custom models across projects

## Testing

```python
# tests.py
from django.test import TestCase
from eav import get_attribute_model

Attribute = get_attribute_model()


class CustomAttributeTest(TestCase):
    def test_custom_field_exists(self):
        """Test that custom field is accessible."""
        attr = Attribute.objects.create(
            name='Test',
            slug='test',
            datatype=Attribute.TYPE_TEXT,
            show_in_frontend=True
        )
        
        self.assertTrue(hasattr(attr, 'show_in_frontend'))
        self.assertTrue(attr.show_in_frontend)
    
    def test_filter_frontend_attributes(self):
        """Test filtering by frontend visibility."""
        Attribute.objects.create(
            name='Visible',
            slug='visible',
            datatype=Attribute.TYPE_TEXT,
            show_in_frontend=True
        )
        
        Attribute.objects.create(
            name='Hidden',
            slug='hidden',
            datatype=Attribute.TYPE_TEXT,
            show_in_frontend=False
        )
        
        frontend_attrs = Attribute.objects.filter(show_in_frontend=True)
        self.assertEqual(frontend_attrs.count(), 1)
        self.assertEqual(frontend_attrs.first().slug, 'visible')
```

## Migration from Default Models

If you already have an EAV installation and want to add custom fields:

1. Create a backup of your database
2. Create the custom model using the **same table name**:

```python
class CustomAttribute(AbstractAttribute):
    show_in_frontend = models.BooleanField(default=True)
    
    class Meta(AbstractAttribute.Meta):
        swappable = 'EAV_ATTRIBUTE_MODEL'
        db_table = 'eav_attribute'  # Use existing table!
```

3. Update settings
4. Run `makemigrations` - it should only add the new field
5. Run `migrate`

## Troubleshooting

### Issue: "Table already exists"

**Solution**: Use the `db_table` Meta option to point to the existing table.

### Issue: "Model not found"

**Solution**: Ensure:
- Your app is in `INSTALLED_APPS`
- The setting format is correct: `'app_label.ModelName'`
- You're using the helper function: `get_attribute_model()`

### Issue: "Foreign key constraint violation"

**Solution**: When creating migrations, ensure they depend on EAV migrations:

```python
class Migration(migrations.Migration):
    dependencies = [
        ('eav', '0013_make_models_swappable'),
        ('myapp', '0001_initial'),
    ]
```

## Summary

The swappable models feature allows you to:

1. ✅ Add custom fields to EAV models
2. ✅ Override model methods
3. ✅ Add custom validation
4. ✅ Integrate with your application's specific needs
5. ✅ Maintain upgradability of the core package

This example demonstrates exactly what was requested: adding a field to the Attribute model to control frontend visibility, just like Django's swappable User model pattern.
