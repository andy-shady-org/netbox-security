from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey
from netbox.models import PrimaryModel
from netbox_security.constants import FILTER_SETTING_ASSIGNMENT_MODELS
from netbox_security.choices import FirewallRuleSettingChoices


class FirewallRuleSettingMixin(PrimaryModel):
    assigned_object_type = models.ForeignKey(
        to=ContentType,
        limit_choices_to=FILTER_SETTING_ASSIGNMENT_MODELS,
        on_delete=models.PROTECT,
        related_name='+',
        blank=True,
        null=True
    )
    assigned_object_id = models.PositiveBigIntegerField(
        blank=True,
        null=True
    )
    assigned_object = GenericForeignKey(
        ct_field='assigned_object_type',
        fk_field='assigned_object_id'
    )
    key = models.CharField(
        choices=FirewallRuleSettingChoices,
    )
    value = models.CharField()

    class Meta:
        abstract = True

    def __str__(self):
        return f'{self.assigned_object}: {self.key}'
