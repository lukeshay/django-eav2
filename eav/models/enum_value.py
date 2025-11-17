from __future__ import annotations

from django.db import models
from django.utils.translation import gettext_lazy as _

from eav.logic.managers import EnumValueManager
from eav.logic.object_pk import get_pk_format
from eav.logic.slug import SLUGFIELD_MAX_LENGTH


class AbstractEnumValue(models.Model):
    """
    *EnumValue* objects are the value 'choices' to multiple choice *TYPE_ENUM*
    :class:`Attribute` objects. They have only one field, *value*, a
    ``CharField`` that must be unique.

    For example::

        yes = EnumValue.objects.create(value='Yes') # doctest: SKIP
        no = EnumValue.objects.create(value='No')
        unknown = EnumValue.objects.create(value='Unknown')

        ynu = EnumGroup.objects.create(name='Yes / No / Unknown')
        ynu.values.add(yes, no, unknown)

        Attribute.objects.create(name='has fever?',
            datatype=Attribute.TYPE_ENUM, enum_group=ynu)
        # = <Attribute: has fever? (Multiple Choice)>

    .. note::
       The same *EnumValue* objects should be reused within multiple
       *EnumGroups*.  For example, if you have one *EnumGroup* called: *Yes /
       No / Unknown* and another called *Yes / No / Not applicable*, you should
       only have a total of four *EnumValues* objects, as you should have used
       the same *Yes* and *No* *EnumValues* for both *EnumGroups*.
    """

    id = get_pk_format()

    value = models.CharField(
        _("Value"),
        db_index=True,
        unique=True,
        max_length=SLUGFIELD_MAX_LENGTH,
    )

    objects = EnumValueManager()

    class Meta:
        abstract = True
        verbose_name = _("EnumValue")
        verbose_name_plural = _("EnumValues")

    def __str__(self) -> str:
        """String representation of `EnumValue` instance."""
        return str(
            self.value,
        )

    def __repr__(self) -> str:
        """String representation of `EnumValue` object."""
        return f"<EnumValue {self.value}>"

    def natural_key(self) -> tuple[str]:
        """
        Retrieve the natural key for the EnumValue instance.

        The natural key for an EnumValue is defined by its `value`. This method returns
        the value of the instance as a single-element tuple.

        Returns
        -------
            tuple: A tuple containing the value of the EnumValue instance.
        """
        return (self.value,)


class EnumValue(AbstractEnumValue):
    """
    Default concrete implementation of AbstractEnumValue.
    
    This model can be swapped with a custom model by setting EAV_ENUM_VALUE_MODEL
    in your Django settings.
    """
    
    class Meta(AbstractEnumValue.Meta):
        abstract = False
        swappable = "EAV_ENUM_VALUE_MODEL"
