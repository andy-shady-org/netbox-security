from django.contrib.contenttypes.models import ContentType
from django.utils.translation import gettext_lazy as _
from utilities.forms.rendering import FieldSet
from netbox_security.choices import FirewallRuleFromSettingChoices, FirewallRuleThenSettingChoices
from netbox_security.models import FirewallRuleFromSetting, FirewallRuleThenSetting


class FilterRuleSettingFormMixin:
    FROM_MODEL = FirewallRuleFromSetting
    FROM_CHOICE = FirewallRuleFromSettingChoices
    FROM_NAME = None
    THEN_MODEL = FirewallRuleThenSetting
    THEN_CHOICE = FirewallRuleThenSettingChoices
    THEN_NAME = 'Then Settings'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._append_from_settings_fields()
        self._append_then_settings_fields()

    def _clean_fieldset(self):
        pass

    def _append_from_settings_fields(self):
        assigned_fields = []
        fieldset = FieldSet(*self.FROM_CHOICE.values(), name=_(self.FROM_NAME))
        for key, label in self.FROM_CHOICE.CHOICES:
            self._parse_key(key, label, self.FROM_CHOICE.FIELD_TYPES[key])
            assigned_fields.append(key)
        if fieldset not in self.fieldsets:
            self.fieldsets = (*self.fieldsets, fieldset)

    def _append_then_settings_fields(self):
        assigned_fields = []
        fieldset = FieldSet(*self.THEN_CHOICE.values(), name=_(self.THEN_NAME))
        for key, label in self.THEN_CHOICE.CHOICES:
            self._parse_key(key, label, self.THEN_CHOICE.FIELD_TYPES[key])
            assigned_fields.append(key)
        if fieldset not in self.fieldsets:
            self.fieldsets = (*self.fieldsets, fieldset)

    def save(self, *args, **kwargs):
        settings = {}
        for key, _ in self.FROM_CHOICE.CHOICES:
            if key in self.cleaned_data:
                settings[key] = self.cleaned_data.pop(key)
        for key, _ in self.THEN_CHOICE.CHOICES:
            if key in self.cleaned_data:
                settings[key] = self.cleaned_data.pop(key)
        obj = super().save(*args, **kwargs)

        for key, _ in self.FROM_CHOICE.CHOICES:
            value = settings.get(key, None)
            setting = self.FROM_MODEL.objects.filter(
                assigned_object_type=self.get_assigned_object_type(),
                assigned_object_id=self.get_assigned_object_id(),
                key=key
            ).first()
            if setting and value:
                setting.value = settings.get(key)
                setting.clean()
                setting.save()
            elif value:
                setting = self.FROM_MODEL(
                    assigned_object=self.instance,
                    key=key,
                    value=settings.get(key, None)
                )
                setting.clean()
                setting.save()
            elif setting:
                setting.delete()
        for key, _ in self.THEN_CHOICE.CHOICES:
            value = settings.get(key, None)
            setting = self.THEN_MODEL.objects.filter(
                assigned_object_type=self.get_assigned_object_type(),
                assigned_object_id=self.get_assigned_object_id(),
                key=key
            ).first()
            if setting and value:
                setting.value = settings.get(key)
                setting.clean()
                setting.save()
            elif value:
                setting = self.THEN_MODEL(
                    assigned_object=self.instance,
                    key=key,
                    value=settings.get(key, None)
                )
                setting.clean()
                setting.save()
            elif setting:
                setting.delete()
        return obj

    def get_assigned_object_type(self):
        return ContentType.objects.get_for_model(self.instance).pk

    def get_assigned_object_id(self):
        return self.instance.pk

