# NetBox Security
The NetBox Security plugin enables NetBox to manage operational security elements related to firewalls and possibly other devices.

## Objectives
NetBox Security is designed to be the 'Security Source of Truth' analogous to NetBox being the 'Network Source of Truth'.

The plugin stores information about Security Zones and Policies, Firewall Rules, NAT Pools and Rules, making it a data source for automatic provisioning of firewalls and other devices.

Main features include:

* Addresses, Address Sets and Address Lists, used in Security Policies.
* Security Zones and Security Policies
* NAT Pools, Pool Members, NAT Rule Sets and NAT Rules
* Firewall Filters and Firewall Filter Rules
* Device and Virtual Device Context association through various association tables


## Installation and Configuration
The installation of plugins in general is described in the [NetBox documentation](https://netbox.readthedocs.io/en/stable/plugins/).

### Requirements
The installation of NetBox Security requires a Python interpreter and a working NetBox deployment. The following versions are currently supported:

* NetBox 4.1.0 or higher
* Python 3.10 or higher

### Compatibility
NetBox Security is compatible with the following NetBox versions.

| NetBox Version | NetBox Security Version |
|----------------|-------------------------|
| NetBox 4.2     | \>= 1.0.0               |


### Installation of NetBox Security
NetBox Security is available as a PyPi module and can be installed using pip:

```
$ source /opt/netbox/venv/bin/activate
(venv) $ pip install netbox-security
```
This will install NetBox DNS and all prerequisites within the NetBox virtual environment.

### Adding NetBox Security to the local NetBox requirements
To ensure that NetBox Security is updated when a NetBox update is performed,  include it in the local requirements file for NetBox:

```
echo netbox-security >> /opt/netbox/local_requirements.txt
```
If the local requirements file does not exist, this command will create it.

This will guarantee that NetBox Security will be updated every time the update script provided with NetBox is executed.

### Enabling the Plugin
In configuration.py, add `netbox_security` to the PLUGINS list:

```
PLUGINS = [
    'netbox_security',
]
```

### Running the Django database migration procedure
NetBox Security requires some tables for its data models within the NetBox database to be present. Execute the following command to create and update these tables:

```
/opt/netbox/netbox/manage.py migrate
```

### Restarting NetBox
Restart the WSGI service and the request queue worker to load the new plugin:

```
systemctl restart netbox netbox-rq
```
Now NetBox Security should show up under "Security" at the bottom of the left-hand side of the NetBox web GUI. If you with the plugin to show up under the "Plugins" menu, you can set
the following settings within your Netbox Configuration:

```
PLUGINS_CONFIG = {
    'netbox_security': {
        'top_level_menu': False,
    },
}
```

### Reindexing Global Search
In order for existing NetBox Security objects to appear in the global search after the initial installation or some upgrades of NetBox Security, 
the search indices need to be rebuilt. This can be done with the command

```
/opt/netbox/netbox/manage.py reindex netbox_security
```
This can be done at any time, especially when items that should show up in the global search do not.


## Object types

NetBox Security can manage ten different object types: 

* Address
* AddressSet
* SecurityZone
* SecurityZonePolicy
* NatPool
* NatPoolMember
* NatRuleSet
* NatRule
* FirewallFilter
* FirewallFilterRule

In addition, further object types are using to handle Many-to-Many relationships with Netbox Device, VirtualDeviceContext and Interface object types. These assignment objects are:

* AddressList -> Address and AddressSet (used with security zone policy list items)
* AddressAssignment -> Device and VirtualDeviceContext
* AddressSetAssignment -> Device and VirtualDeviceContext
* SecurityZoneAssignment -> Device, VirtualDeviceContext and Interface (for assigning an interface to a security zone)
* NatPoolAssignment -> Device and VirtualDeviceContext
* NatRuleSetAssignment -> Device and VirtualDeviceContext
* NatRuleAssignment -> Interface (Used for outbound interface assignments)
* FirewallFilterAssignment -> Device and VirtualDeviceContext


### Addresses, Address Sets and Address Lists

Addresses and Address Sets are normally used by security zone policies as source and destination list elements. 
To ensure that both can be used, each Address and AddressSet object needs to be assigned to a unique AddressList object.
AddressList objects are then used as the list items for the relevant source and destination list fields within any given security zone policy.

#### Permissions

The following Django permissions are applicable to Address objects:

| Permission                       | Action                  |
|----------------------------------|-------------------------|
| `netbox_security.add_address`    | Create new view objects |
| `netbox_security.change_address` | Edit view information   |
| `netbox_security.delete_address` | Delete a view object    |
| `netbox_security.view_address`   | View view information   |

The following Django permissions are applicable to AddressSet objects:

| Permission                          | Action                  |
|-------------------------------------|-------------------------|
| `netbox_security.add_addressset`    | Create new view objects |
| `netbox_security.change_addressset` | Edit view information   |
| `netbox_security.delete_addressset` | Delete a view object    |
| `netbox_security.view_addressset`   | View view information   |

The following Django permissions are applicable to AddressList objects:

| Permission                           | Action                  |
|--------------------------------------|-------------------------|
| `netbox_security.add_addresslist`    | Create new view objects |
| `netbox_security.change_addresslist` | Edit view information   |
| `netbox_security.delete_addresslist` | Delete a view object    |
| `netbox_security.view_addresslist`   | View view information   |

#### ScreenShots

Addresses
![List Addresses](img/address_list.png)
![View Address](img/address.png)

Address Sets
![List Address Sets](img/address_set_list.png)
![View Address](img/address_set.png)


### Security Zones and Security Zone Policies

Firewall security zones are logical groupings of network interfaces used to control and log traffic flow, 
allowing administrators to define security policies based on zones rather than individual interfaces, 
enhancing security and simplifying management.

In Netbox Security, a security zone can be assigned to one or more devices or virtual device contexts. It can also be assigned to one or more interfaces.
Security zone assignments are stored within the SecurityZoneAssignment table.

#### Permissions

The following Django permissions are applicable to SecurityZone objects:

| Permission                            | Action                  |
|---------------------------------------|-------------------------|
| `netbox_security.add_securityzone`    | Create new view objects |
| `netbox_security.change_securityzone` | Edit view information   |
| `netbox_security.delete_securityzone` | Delete a view object    |
| `netbox_security.view_securityzone`   | View view information   |

The following Django permissions are applicable to SecurityZonePolicy objects:

| Permission                                  | Action                  |
|---------------------------------------------|-------------------------|
| `netbox_security.add_securityzonepolicy`    | Create new view objects |
| `netbox_security.change_securityzonepolicy` | Edit view information   |
| `netbox_security.delete_securityzonepolicy` | Delete a view object    |
| `netbox_security.view_securityzonepolicy`   | View view information   |


#### ScreenShots

Security Zones
![List Security Zones](img/security_zone_list.png)
![View Security Zone](img/security_zone.png)

Security Zone Policies
![List Security Zone Policies](img/policies_list.png)
![View Security Zone Policy](img/policy.png)


### NAT Pools and NAT Pool Members

NAT Pools are used as part of a NAT operation for forwarding traffic. Nat Pools consist of pool members that are used as the source or destination of the traffic.

In Netbox Security, a NAT pool can be assigned to one or more devices or virtual device contexts. 
NAT pool assignments are stored within the NatPoolAssignment table.

#### Permissions

The following Django permissions are applicable to NatPool objects:

| Permission                       | Action                  |
|----------------------------------|-------------------------|
| `netbox_security.add_natpool`    | Create new view objects |
| `netbox_security.change_natpool` | Edit view information   |
| `netbox_security.delete_natpool` | Delete a view object    |
| `netbox_security.view_natpool`   | View view information   |

The following Django permissions are applicable to NATPoolMember objects:

| Permission                              | Action                  |
|-----------------------------------------|-------------------------|
| `netbox_security.add_natpoolmember`     | Create new view objects |
| `netbox_security.change_natpoolmember`  | Edit view information   |
| `netbox_security.delete_natpoolmember`  | Delete a view object    |
| `netbox_security.view_natpoolmember`    | View view information   |


#### ScreenShots

NAT Pools
![List NAT Pools](img/nat-pool-list.png)
![View NAT Pool](img/nat-pool.png)

NAT Pool Members
![List NAT Pool Members](img/members.png)
![View NAT Pool Member](img/nat-pool-member.png)


### NAT Rule Sets and NAT Rules

NAT Rule Sets are collections of NAT rules. Nat Rules control the forwarding of NAT based traffic.

In Netbox Security, a NAT Rule Set can be assigned to one or more devices or virtual device contexts. 
NAT pool assignments are stored within the NatRuleSetAssignment table.

In addition, a NAT Rule may be assigned to an outbound interface, and therefore this assignment is achieved through the NatRuleAssignment table.

#### Permissions

The following Django permissions are applicable to NatPool objects:

| Permission                          | Action                  |
|-------------------------------------|-------------------------|
| `netbox_security.add_natruleset`    | Create new view objects |
| `netbox_security.change_natruleset` | Edit view information   |
| `netbox_security.delete_natruleset` | Delete a view object    |
| `netbox_security.view_natruleset`   | View view information   |

The following Django permissions are applicable to NATPoolMember objects:

| Permission                       | Action                  |
|----------------------------------|-------------------------|
| `netbox_security.add_natrule`    | Create new view objects |
| `netbox_security.change_natrule` | Edit view information   |
| `netbox_security.delete_natrule` | Delete a view object    |
| `netbox_security.view_natrule`   | View view information   |


#### ScreenShots

NAT Rule Sets
![List NAT Rule Sets](img/nat-rule-set-list.png)
![View NAT Rule Set](img/nat-rule-set.png)

NAT Rules
![List NAT Rules](img/nat-rule-list.png)
![View NAT Rule](img/nat-rule.png)


### Firewall Filters and Firewall Rules

Firewall filters are essentially containers for firewall rules. Different vendors have different types of firewall rules, and 
Cisco Access Lists has been covered in an alternate Netbox plugin.

In Netbox Security, a Firewall Filter can be assigned to one or more devices or virtual device contexts. 
Firewall Filter assignments are stored within the FirewallFilterAssignment table.

#### Permissions

The following Django permissions are applicable to NatPool objects:

| Permission                              | Action                  |
|-----------------------------------------|-------------------------|
| `netbox_security.add_firewallfilter`    | Create new view objects |
| `netbox_security.change_firewallfilter` | Edit view information   |
| `netbox_security.delete_firewallfilter` | Delete a view object    |
| `netbox_security.view_firewallfilter`   | View view information   |

The following Django permissions are applicable to NATPoolMember objects:

| Permission                                   | Action                  |
|----------------------------------------------|-------------------------|
| `netbox_security.add_firewallfilterrule`     | Create new view objects |
| `netbox_security.change_firewallfilterrule`  | Edit view information   |
| `netbox_security.delete_firewallfilterrule`  | Delete a view object    |
| `netbox_security.view_firewallfilterrule`    | View view information   |


#### ScreenShots

Firewall Filters
![List Firewall Filters](img/firewall-filter-list.png)
![View Firewall Filter](img/firewall-filter.png)

Firewall Filter Rules
![List Firewall Filter Rules](img/firewall-rule-list.png)
![View Firewall Filter Rule](img/firewall-rule.png)

