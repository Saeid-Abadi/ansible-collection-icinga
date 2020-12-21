# python 3 headers, required if submitting to Ansible
from __future__ import (absolute_import, division, print_function)

__metaclass__ = type

DOCUMENTATION = """
        module: icinga2_config_generator
        author: Thilo Wening, Lennart Betz
        version_added: "0.1"
        short_description: generate icinga2 objects
        description:
            - | This module should generate icinga 2 objects to deploy on the
                monitoring hosts
        notes:
          - if read in variable context, the file can be interpreted as YAML if the content is valid to the parser.
          - this lookup does not understand globing --- use the fileglob lookup instead.
        options:
          name:
            description: Name of the host object
            required: true
            type: string
        state:
          description: |
            Choose between present or absent,
            whether the host should be created or deleted
          required: true
          type: string
"""

EXAMPLES = r'''
# Create Host
- name: Create Host at Director
  icinga2_director_host:
    name: agent.localdomain
    host: "http://icingaweb.localdomain/icingaweb2"
    username: 'icinga'
    password: 'icinga'
    state: 'present'
    templates:
      - "basic-host"
    host_vars:
      address: "127.0.0.1"
      check_interval: "300"
      check_command: "hostalive"
    custom_vars:
      os: "Linux"
      application: "Apache"
'''

RETURN = r'''
 test blubber
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

      if re.search(r'(object|template|apply)', self.state) and not (self.apply_target and self.apply):
          config += '%s %s "%s" {\n' % (self.state, self.object_type, self.object_name)
      elif self.state == 'apply' and self.object_type == 'Service':
          config += 'apply Service "%s " for (%s)' % (self.object_name, self.apply)
      elif self.state == 'apply' and re.match(r'^(Notification|Dependency)$', self.object_type):
          config += 'apply %s "%s" to %s' % (self.object_type, self.object_name, self.apply_target)
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
  )

  result = Icinga2Objects().run()
  module.exit_json(**result)

if __name__ == '__main__':
      main()
