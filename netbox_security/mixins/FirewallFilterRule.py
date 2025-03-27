from django.contrib.contenttypes.models import ContentType
from django import forms
from django.forms import fields
from django.utils.translation import gettext as _

from netbox_security.choices import FirewallRuleFromSettingChoices, FirewallRuleThenSettingChoices
from netbox_security.models import FirewallRuleSetting


class FilterRuleFromSettingMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._append_from_settings_fields()
        self._append_then_settings_fields()

    def _append_from_settings_fields(self):
        assigned_fields = []
        fieldset = (
            _('From Settings'), [
                'address',
            ]
        )
        for key, label in FirewallRuleFromSettingChoices.CHOICES:
            initial = None
            if hasattr(self, 'instance'):
                setting = FirewallRuleSetting.objects.filter(
                        assigned_object_type=ContentType.objects.get_for_model(self.Meta.model),
                        assigned_object_id=self.instance.pk,
                        key=key
                ).first()
                if setting:
                    initial = setting.value
            if FirewallRuleFromSettingChoices.FIELD_TYPES[key] == 'ipaddr':
                self.fields[key] = fields.CharField(
                    label=label,
                    required=False,
                    initial=initial,
                    max_length=128
                )
                css = self.fields[key].widget.attrs.get('class', '')
                self.fields[key].widget.attrs['class'] = f'{css} form-control'
            elif FirewallRuleFromSettingChoices.FIELD_TYPES[key] == 'integer':
                self.fields[key] = fields.IntegerField(
                    label=label,
                    required=False,
                    initial=initial,
                    min_value=0,
                    max_value=65535
                )
                css = self.fields[key].widget.attrs.get('class', '')
                self.fields[key].widget.attrs['class'] = f'{css} form-control'
            elif FirewallRuleFromSettingChoices.FIELD_TYPES[key] == 'boolean':
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
            assigned_fields.append(key)
            if key not in fieldset[1]:
                fieldset[1].append(key)
        if fieldset not in self.fieldsets:
            self.fieldsets.append(fieldset)

    def _append_then_settings_fields(self):
        assigned_fields = []
        fieldset = (
            _('Then Settings'), [
                'address',
            ]
        )
        for key, label in FirewallRuleFromSettingChoices.CHOICES:
            initial = None
            if hasattr(self, 'instance'):
                setting = FirewallRuleSetting.objects.filter(
                        assigned_object_type=ContentType.objects.get_for_model(self.Meta.model),
                        assigned_object_id=self.instance.pk,
                        key=key
                ).first()
                if setting:
                    initial = setting.value
            if FirewallRuleThenSettingChoices.FIELD_TYPES[key] == 'ipaddr':
                self.fields[key] = fields.CharField(
                    label=label,
                    required=False,
                    initial=initial,
                    max_length=128
                )
                css = self.fields[key].widget.attrs.get('class', '')
                self.fields[key].widget.attrs['class'] = f'{css} form-control'
            elif FirewallRuleThenSettingChoices.FIELD_TYPES[key] == 'integer':
                self.fields[key] = fields.IntegerField(
                    label=label,
                    required=False,
                    initial=initial,
                    min_value=0,
                    max_value=65535
                )
                css = self.fields[key].widget.attrs.get('class', '')
                self.fields[key].widget.attrs['class'] = f'{css} form-control'
            elif FirewallRuleThenSettingChoices.FIELD_TYPES[key] == 'boolean':
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
            assigned_fields.append(key)
            if key not in fieldset[1]:
                fieldset[1].append(key)
        if fieldset not in self.fieldsets:
            self.fieldsets.append(fieldset)

    def _clean_fieldset(self):
        pass

    def save(self, *args, **kwargs):
        from_settings = {}
        then_settings = {}
        for key, _ in FirewallRuleFromSettingChoices.CHOICES:
            if key in self.cleaned_data:
                from_settings[key] = self.cleaned_data.pop(key)
        for key, _ in FirewallRuleThenSettingChoices.CHOICES:
            if key in self.cleaned_data:
                then_settings[key] = self.cleaned_data.pop(key)
        obj = super().save(*args, **kwargs)

        for key, _ in FirewallRuleFromSettingChoices.CHOICES:
            value = from_settings.get(key, None)
            setting = FirewallRuleSetting.objects.filter(
                    assigned_object_type=self.get_assigned_object_type(),
                    assigned_object_id=self.get_assigned_object_id(),
                    key=key
            ).first()
            if setting and value:
                setting.value = from_settings.get(key)
                setting.clean()
                setting.save()
            elif value:
                setting = FirewallRuleSetting(
                    assigned_object=self.instance,
                    key=key,
                    value=from_settings.get(key, None)
                )
                setting.clean()
                setting.save()
            elif setting:
                setting.delete()
        for key, _ in FirewallRuleThenSettingChoices.CHOICES:
            value = then_settings.get(key, None)
            setting = FirewallRuleSetting.objects.filter(
                    assigned_object_type=self.get_assigned_object_type(),
                    assigned_object_id=self.get_assigned_object_id(),
                    key=key
            ).first()
            if setting and value:
                setting.value = then_settings.get(key)
                setting.clean()
                setting.save()
            elif value:
                setting = FirewallRuleSetting(
                    assigned_object=self.instance,
                    key=key,
                    value=then_settings.get(key, None)
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
