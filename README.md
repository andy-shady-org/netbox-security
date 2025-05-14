# NetBox Security Plugin
[Netbox](https://github.com/netbox-community/netbox) plugin for Security and NAT related objects documentation.

<div align="center">
<a href="https://pypi.org/project/netbox-security/"><img src="https://img.shields.io/pypi/v/netbox-security" alt="PyPi"/></a>
<a href="https://github.com/andy-shady-org/netbox-security/stargazers"><img src="https://img.shields.io/github/stars/andy-shady-org/netbox-security?style=flat" alt="Stars Badge"/></a>
<a href="https://github.com/andy-shady-org/netbox-security/network/members"><img src="https://img.shields.io/github/forks/andy-shady-org/netbox-security?style=flat" alt="Forks Badge"/></a>
<a href="https://github.com/andy-shady-org/netbox-security/issues"><img src="https://img.shields.io/github/issues/andy-shady-org/netbox-security" alt="Issues Badge"/></a>
<a href="https://github.com/andy-shady-org/netbox-security/pulls"><img src="https://img.shields.io/github/issues-pr/andy-shady-org/netbox-security" alt="Pull Requests Badge"/></a>
<a href="https://github.com/andy-shady-org/netbox-security/graphs/contributors"><img alt="GitHub contributors" src="https://img.shields.io/github/contributors/andy-shady-org/netbox-security?color=2b9348"></a>
<a href="https://github.com/andy-shady-org/netbox-security/blob/master/LICENSE"><img src="https://img.shields.io/github/license/andy-shady-org/netbox-security?color=2b9348" alt="License Badge"/></a>
<a href="https://github.com/psf/black"><img src="https://img.shields.io/badge/code%20style-black-000000.svg" alt="Code Style Black"/></a>
<a href="https://pepy.tech/project/netbox-security"><img alt="Downloads" src="https://static.pepy.tech/badge/netbox-security"></a>
<a href="https://pepy.tech/project/netbox-security"><img alt="Downloads/Week" src="https://static.pepy.tech/badge/netbox-security/month"></a>
<a href="https://pepy.tech/project/netbox-security"><img alt="Downloads/Month" src="https://static.pepy.tech/badge/netbox-security/week"></a>
</div>


## Features
This plugin provides following Models:
* Addresses
* Address Sets
* Address Lists
* Security Zones
* Security Zone Policies
* NAT Pools
* NAT Pool Members
* NAT Rule-sets
* NAT Rules
* Firewall Filters
* Firewall Filter Rules
* Firewall Policers

## Compatibility

| NetBox Version | NetBox Security Version |
|----------------|-------------------------|
| NetBox 4.2     | \>= 1.0.2               |
| NetBox 4.3     | \>= 1.1.0               |

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

Full documentation on using plugins with NetBox: [Using Plugins - NetBox Documentation](https://netbox.readthedocs.io/en/stable/plugins/)


## Configuration

The following options are available:
* `device_ext_page`: String (default left) Device related objects table position. The following values are available:  
left, right, full_width. Set empty value for disable.
* `virtual_ext_page`: String (default left) Virtual Context related objects table position. The following values are available:  
left, right, full_width. Set empty value for disable.
* `interface_ext_page`: String (default left) Interface related objects table position. The following values are available:  
left, right, full_width. Set empty value for disable.
* `address_ext_page`: String (default right) Address/Address Set related objects table position. The following values are available:  
left, right, full_width. Set empty value for disable.
* `top_level_menu`: Boolean (default True) Display plugin menu at the top level. The following values are available: True, False.


## Contribute

Contributions are always welcome! Please see the [Contribution Guidelines](CONTRIBUTING.md)


## Documentation

For further information, please refer to the full documentation: [Using NetBox Security](docs/using_netbox_security.md)


## Credits

- Thanks to Peter Eckel for providing some lovely examples which I've happily borrowed, and for providing excellent guidance.
- Thanks to Dan Sheppard for the abstracted field generation stuff which I also used.
- Thanks to Kris Beevers and Mark Coleman at Netbox Labs for encouragement and engagement.
