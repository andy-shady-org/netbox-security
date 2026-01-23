from django.db.models.signals import post_save
from django.dispatch import receiver
from netbox_security.models import NatPoolMember


@receiver(post_save, sender=NatPoolMember)
def add_ipaddress_assignment_post_save(instance, **kwargs):
    if instance.address:
        instance.address.assigned_object = instance
        instance.address.save()
