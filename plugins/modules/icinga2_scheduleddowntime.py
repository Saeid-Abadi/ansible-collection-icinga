#!/usr/bin/python


from ansible.module_utils.basic import AnsibleModule

def main():
    module = AnsibleModule(
        supports_check_mode=True,
        argument_spec = dict(
            state         = dict(default='present', choices=['present', 'absent']),
            name          = dict(required=True),
            order         = dict(default=10, type='int'),
            file          = dict(required=True, type='str'),
            template      = dict(default=False, type='bool'),
            imports       = dict(default=list(), type='list', elements='str'),
            apply         = dict(default=False, type='str'),
            display_name  = dict(type='str'),
            host_name     = dict(required=True, type='str'),
            service_name  = dict(type='str'),
            author        = dict(required=True, type='str'),
            comment       = dict(required=True, type='str'),
            fixed         = dict(default=True, type='bool'),
            duration      = dict(type='str'),
            ranges        = dict(required=True, type='dict'),
            child_options = dict(type='str'),
        )
    )

    args = module.params
    name = args.pop('name')
    order = args.pop('order')
    state = args.pop('state')
    file = args.pop('file')
    template = args.pop('template')
    imports = args.pop('imports')
    apply = args.pop('apply')

    module.exit_json(changed=False, args=args, name=name, order=str(order), state=state, file=file, template=template, imports=imports, apply=apply, apply_for=apply_for)

if __name__ == '__main__':
    main()