# NetBox Security Plugin
[Netbox](https://github.com/netbox-community/netbox) plugin for Security and NAT related objects documentation.

## Features
This plugin provides following Models:
* Addresses
* Security Zones
* Security Zone Policies
* NAT Pools
* NAT Pool Members
* NAT Rule-sets
* NAT Rules
* Firewall Filters
* Firewall Filter Rules

## Compatibility

|            |           |
|------------|-----------|
| NetBox 4.1 | \>= 1.0.0 |

## Installation

The plugin is available as a Python package in pypi and can be installed with pip  

```
pip install netbox-security
```
Enable the plugin in /opt/netbox/netbox/netbox/configuration.py:
```
PLUGINS = ['netbox_security']
```
Restart NetBox and add `netbox-security` to your local_requirements.txt

Perform database migrations:
```bash
cd /opt/netbox
source venv/bin/activate
python ./netbox/manage.py migrate netbox_security
python ./netbox/manage.py reindex netbox_security
```
See [NetBox Documentation](https://docs.netbox.dev/en/stable/plugins/#installing-plugins) for details

## Configuration

The following options are available:
* `device_ext_page`: String (default left) Device related objects table position. The following values are available:  
left, right, full_width. Set empty value for disable.
* `virtual_ext_page`: String (default left) Virtual Context related objects table position. The following values are available:  
left, right, full_width. Set empty value for disable.
* `interface_ext_page`: String (default left) Interface related objects table position. The following values are available:  
left, right, full_width. Set empty value for disable.
* `top_level_menu`: Boolean (default True) Display plugin menu at the top level. The following values are available: True, False.


## Credits

Thanks to Peter Eckel for providing some lovely examples which I've happily borrowed.
Thanks to Dan Sheppard for the abstracted field generation stuff which I also used.

Thanks to Kris and Mark at Netbox Labs for encouragement and engagement.

