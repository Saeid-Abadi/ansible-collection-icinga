## Module ServiceNow Import

Icinga Web Module to import data from ServiceNow into the Icinga Director.
It adds the import source type "ServiceNow Table API" to the Director.

**Important:** This module expects the [NETWAYS Extras repository](https://packages.netways.de/extras/) to be enabled on the system.
It can be enabled using the `repos` role.

## Configuration

The module has no configuration files of its own. Only the general module parameters `enabled` and `source` apply.

```yaml
icingaweb2_modules:
  servicenowimport:
    enabled: true
    source: package
```

Connection settings like the ServiceNow URL, authentication and proxy belong to the individual import source in the Director, not to the module.
They can be set in Icinga Web or with the `telekom_mms.icinga_director.icinga_importsource` module.
