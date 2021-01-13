# python 3 headers, required if submitting to Ansible
from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = """
        module: icinga2_config_generator
        author:
          - Lennart Betz (lennart.betz@netways.de)
          - Thilo Wening (thilo.wening@netways.de
        version_added: "0.1"
        short_description: generate icinga2 objects
        description:
            - | This module should generate icinga 2 objects to deploy on the
                monitoring hosts
        notes:
          - if read in variable context, the file can be interpreted as YAML if the content is valid to the parser.
          - this lookup does not understand globing --- use the fileglob lookup instead.
        options:
          object_name:
            description: Name of the host object
            required: true
            type: string
          object_type:
            description: Icinga 2 object type.
            required: true
            type: string
          state:
            description: |
              Choose which state the config should be in - object|template|apply
            required: true
            type: string
          constants:
            description: A dict including all constants.
            required: true
            type: dict
          attrs:
            description: A dict with all object attributes and custom attributes listed below the "vars" key.
            required: false
            type: dict
          imports:
            description: A list including template imports for the object
            required: false
            type: list
"""

EXAMPLES = r'''
# Create Host
- name: generate Host configuration
  icinga_config_generator:
    object_name: agent.localdomain
    object_type: Host
    state: object
    constants: "{{ icinga2_constants }}"
    imports:
      - "basic-host"
    attrs:
      address: "127.0.0.1"
      check_interval: "300"
      check_command: "hostalive"
      vars:
        os: Linux
        application: Apache

- name: generate service configuration
  icinga_config_generator:
    object_name: ping4
    object_type: Service
    state: object
    constants: "{{ icinga2_constants }}"
    imports:
      - generic-service
    attrs:
      host_name: agent.localdomain
      check_command: ping4
      vars:
        ping_wrta: 100
        ping_crta: 200

'''

RETURN = r'''
 Return String with Object
'''

from ansible.module_utils.basic import AnsibleModule
from ansible_collections.icinga.icinga.plugins.module_utils.parse import Icinga2Parser
import re

class Icinga2Objects(object):

  def __init__(self):
      self.attrs={}
      self.object_type = module.params.get('object_type')
      self.object_name = module.params.get('object_name')
      self.state = module.params.get('state')
      self.imports = module.params.get('imports')
      self.attrs = module.params.get('attrs')
      self.assign = module.params.get('assign')
      self.apply = module.params.get('apply')
      self.apply_target = module.params.get('apply_target')
      self.constants = module.params.get('constants')



  def run(self):
      cfg = Icinga2Parser()
      # config.parse(terms[0], constants+reserved, indent)
      config = ''
      indent = 0

      # Is this a service?
      if (re.search(r'(object|template|apply)', self.state) and not
          (self.apply_target and self.apply)):
          config += '%s %s "%s" {\n' % (self.state, self.object_type, self.object_name)
      elif self.state == 'apply' and self.object_type == 'Service':
          config += 'apply Service "%s " for (%s)' % (self.object_name, self.apply)
      elif self.state == 'apply' and re.match(r'^(Notification|Dependency)$', self.object_type):
          config += 'apply %s "%s" to %s' % (self.object_type, self.object_name, self.apply_target)
      else:
        module.fail_json(msg=('Type ' + self.object_type + ' and/or state '
          + self.state + ' not supported'))
      for imp in self.imports:
          config += '  import "%s"\n' % (imp)
          config += '\n'
      if self.attrs:
          config += '  %s' % (re.sub('\n','\n  ',cfg.parse(self.attrs, self.constants, indent)))
          config += '\n'
      config += "}"

      obj = dict(changed=True, ansible_module_results="object generated", object=config)

      return obj

def main():
  global module
  object_types = [
      'Host',
      'Service',
      'ApiUser',
      'CheckCommand',
      'Dependency',
      'Endpoint',
      'EventCommand',
      'HostGroup',
      'Notification',
      'NotificationCommand',
      'ScheduledDowntime',
      'ServiceGroup',
      'TimePeriod',
      'User',
      'UserGroup',
      'Zone',
      'ApiListener',
      'CheckerComponent',
      'CheckResultReader',
      'CompatLogger',
      'ElasticsearchWriter',
      'ExternalCommandListener',
      'FileLogger',
      'GelfWriter',
      'GraphiteWriter',
      'IcingaApplication',
      'IcingaDB',
      'IdoMysqlConnection',
      'IdoPgsqlConnection',
      'InfluxdbWriter',
      'LivestatusListener',
      'NotificationComponent',
      'OpenTsdbWriter',
      'PerfdataWriter',
      'StatusDataWriter',
      'SyslogLogger'
  ]

  module = AnsibleModule(
      argument_spec=dict(
          object_name=dict(required=True),
          object_type=dict(required=True, choices=object_types),
          state=dict(required=True, choices=['template','object','apply','absent']),
          attrs=dict(type=dict),
          imports=dict(type=list),
          assign=dict(type=dict),
          apply=dict(type=str),
          apply_target=dict(type=str, choices=['Host','Service']),
          constants=dict(type=dict, required=True)
      ),
      supports_check_mode=False,
      add_file_common_args=True,
  )

  result = Icinga2Objects().run()
  module.exit_json(**result)

if __name__ == '__main__':
      main()
