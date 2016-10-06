# ERMR

## Presentation


## Install

ERMR is deployed using ansible. The folder ermr-deploy contains the ansible
playbook that can be used to deploy a working system to a node accessible by ssh.
Its specific README.md file describes the procedure. To summarize the steps:

* Install an ubuntu 14.04 LTS on a virtual machine. Indigo has been tested
successfully on ubuntu 16.04 but it may need some manual tweaking. It requires
an `indigo` user with sudo access.

* Configure it so it can be used from the host from which you are installing.

* Install ansible on the host.

* Configure an ansible host file to describe the target where you plan to install
ERMR

* Install with the command 
`ansible-playbook deploy_standalone.yml -i hosts --ask-become-pass`

* If all goes well you should have a running nginx server serving ERMR on HTTPS
on the target.

