# Ansible Integration Test

Create a collection folder where this collection resides. Include the path to the COLLECTIONS_PATH env and then run the `ansible-test` command.

```
mkdir -p ~/dev/ansible/collections/ansible_collections/icinga
git clone https://github.com/Icinga/ansible-collection-icinga.git ~/dev/ansible/collections/ansible_collections/icinga/icinga

export COLLECTIONS_PATH=~/dev/ansible/collections

cd ~/dev/ansible/collections/ansible_collections/icinga/icinga

ansible-test integration icinga2_object --docker fedora32 --python 3.8
```

## Extend the tests

To extend the tests just add another tasks file in folder `tasks/` and use the module
`include` to include the test in the `main.yml`

```
- include: icinga2_host.yml
```
