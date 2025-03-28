from django import forms
from django.forms import fields
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import gettext_lazy as _
from utilities.forms.rendering import FieldSet
from netbox_security.choices import FirewallRuleFromSettingChoices, FirewallRuleThenSettingChoices
from netbox_security.models import FirewallRuleFromSetting, FirewallRuleThenSetting


class FilterRuleSettingBase:
    MODEL = None
    CHOICE = None
    NAME = None

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def _clean_fieldset(self):
        pass

    def _parse_key(self, key, label, field_type):
        initial = None
        if hasattr(self, 'instance'):
            setting = self.MODEL.objects.filter(
                assigned_object_type=ContentType.objects.get_for_model(self.Meta.model),
                assigned_object_id=self.instance.pk,
                key=key
            ).first()
            if setting:
                initial = setting.value
        if field_type == 'string':
            self.fields[key] = fields.CharField(
                label=label,
                required=False,
                initial=initial,
                max_length=128,
            )
            css = self.fields[key].widget.attrs.get('class', '')
            self.fields[key].widget.attrs['class'] = f'{css} form-control'
        elif field_type == 'integer':
            self.fields[key] = fields.IntegerField(
                label=label,
                required=False,
                initial=initial,
                min_value=0,
                max_value=65535
            )
            css = self.fields[key].widget.attrs.get('class', '')
            self.fields[key].widget.attrs['class'] = f'{css} form-control'
        elif field_type == 'boolean':
            choices = (
                (None, '---------'),
                (True, _('True')),
                (False, _('False')),
            )
            self.fields[key] = fields.NullBooleanField(
                label=label,
                required=False,
                initial=initial,
                widget=forms.Select(choices=choices)
            )
            css = self.fields[key].widget.attrs.get('class', '')
            self.fields[key].widget.attrs['class'] = f'{css} form-control'

    def save(self, *args, **kwargs):
        settings = {}
        for key, _ in self.CHOICE.CHOICES:
            if key in self.cleaned_data:
                settings[key] = self.cleaned_data.pop(key)
        obj = super().save(*args, **kwargs)

        for key, _ in self.CHOICE.CHOICES:
            value = settings.get(key, None)
            setting = self.MODEL.objects.filter(
                assigned_object_type=self.get_assigned_object_type(),
                assigned_object_id=self.get_assigned_object_id(),
                key=key
            ).first()
            if setting and value:
                setting.value = settings.get(key)
                setting.clean()
                setting.save()
            elif value:
                setting = self.MODEL(
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


class FilterRuleFromSettingMixin(FilterRuleSettingBase):
    MODEL = FirewallRuleFromSetting
    CHOICE = FirewallRuleFromSettingChoices
    NAME = 'From Settings'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._append_settings_fields()

    def _append_settings_fields(self):
        assigned_fields = []
        fieldset = FieldSet(*self.CHOICE.values(), name=_(self.NAME))
        for key, label in self.CHOICE.CHOICES:
            self._parse_key(key, label, self.CHOICE.FIELD_TYPES[key])
            assigned_fields.append(key)
        if fieldset not in self.fieldsets:
            self.fieldsets = (*self.fieldsets, fieldset)


class FilterRuleThenSettingMixin(FilterRuleSettingBase):
    MODEL = FirewallRuleThenSetting
    CHOICE = FirewallRuleThenSettingChoices
    NAME = 'Then Settings'

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._append_settings_fields()

    def _append_settings_fields(self):
        assigned_fields = []
        fieldset = FieldSet(*self.CHOICE.values(), name=_(self.NAME))
        for key, label in self.CHOICE.CHOICES:
            self._parse_key(key, label, self.CHOICE.FIELD_TYPES[key])
            assigned_fields.append(key)
        if fieldset not in self.fieldsets:
            self.fieldsets = (*self.fieldsets, fieldset)
