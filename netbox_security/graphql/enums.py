import strawberry

from netbox_security.choices import (
    FamilyChoices,
    FirewallRuleFromSettingChoices,
    FirewallRuleThenSettingChoices,
    PoolTypeChoices,
    RuleDirectionChoices,
    NatTypeChoices,
    RuleStatusChoices,
    CustomInterfaceChoices,
    AddressTypeChoices,
    ActionChoices,
    LossPriorityChoices,
    ForwardingClassChoices,
    ProtocolChoices,
)

__all__ = (
    "NetBoxSecurityFamilyEnum",
    "NetBoxSecurityFirewallRuleFromSettingEnum",
    "NetBoxSecurityFirewallRuleThenSettingEnum",
    "NetBoxSecurityPoolTypeEnum",
    "NetBoxSecurityRuleDirectionEnum",
    "NetBoxSecurityNatTypeEnum",
    "NetBoxSecurityRuleStatusEnum",
    "NetBoxSecurityCustomInterfaceEnum",
    "NetBoxSecurityAddressTypeEnum",
    "NetBoxSecurityActionEnum",
    "NetBoxSecurityLossPriorityEnum",
    "NetBoxSecurityForwardingClassEnum",
    "NetBoxSecurityProtocolEnum",
)


NetBoxSecurityFamilyEnum = strawberry.enum(FamilyChoices.as_enum())
NetBoxSecurityFirewallRuleFromSettingEnum = strawberry.enum(
    FirewallRuleFromSettingChoices.as_enum()
)
NetBoxSecurityFirewallRuleThenSettingEnum = strawberry.enum(
    FirewallRuleThenSettingChoices.as_enum()
)
NetBoxSecurityPoolTypeEnum = strawberry.enum(PoolTypeChoices.as_enum())
NetBoxSecurityRuleDirectionEnum = strawberry.enum(RuleDirectionChoices.as_enum())
NetBoxSecurityNatTypeEnum = strawberry.enum(NatTypeChoices.as_enum())
NetBoxSecurityRuleStatusEnum = strawberry.enum(RuleStatusChoices.as_enum())
NetBoxSecurityCustomInterfaceEnum = strawberry.enum(CustomInterfaceChoices.as_enum())
NetBoxSecurityAddressTypeEnum = strawberry.enum(AddressTypeChoices.as_enum())
NetBoxSecurityActionEnum = strawberry.enum(ActionChoices.as_enum())
NetBoxSecurityLossPriorityEnum = strawberry.enum(LossPriorityChoices.as_enum())
NetBoxSecurityForwardingClassEnum = strawberry.enum(ForwardingClassChoices.as_enum())
NetBoxSecurityProtocolEnum = strawberry.enum(ProtocolChoices.as_enum())
