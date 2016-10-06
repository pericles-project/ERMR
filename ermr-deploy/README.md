# ERMR Deployment

The following steps describe how to deploy ERMR to a remote (or local)
server.

[ Note, if you intend to run multiple servers, know beforehand the details of
the networks, as it is best to set up the system with the 'real' network rather
than using localhost. ]

####  PREREQUISTES
Ansible expects a user _indigo_ to exist with sudo rights.  
e.g. 

```
sudo adduser  indigo
sudo usermod -G sudo,adm indigo
# If you want to propagate ssh certificates
sudo mkdir ~indigo/.ssh
sudo cat ~/.ssh/authorized_keys >> ~indigo/.ssh/authorized_keys 
```

#### Access

* Make sure you have access to the server via SSH

#### Pre-requisites

-- Install Ansible and GIT on the host from which you are installing (not the 
target).

```
sudo apt-get install software-properties-common
sudo apt-add-repository ppa:ansible/ansible
sudo apt-get update
sudo apt-get install ansible git
```
-- Fetch _this_ package
```
git clone https://github.com/pericles-project/ERMR.git
```

#### Configuration

* By default the user account on the server should be 'indigo' who should have 
sudo access.  If different then the user field in deploy-standalone.yml should 
be changed.

* Cassandra stores it data by default in /var/lib/cassandra -- this may be 
redirected to an appropriate storage volume, either via a symbolic link or 
using something like
```
mkdir /var/lib/cassandra
mount --bind <target> /var/lib/cassandra
mkdir /var/lib/cassandra/data
# Ensure that permissions and ownership are appropriately set
chown -R casssandra:cassandra /var/lib/cassandra
```

* Create a ```hosts``` file containing the IP address of the servers.  It should look like..

```
[indigo-databases]
192.168.20.20 cassandra_interface=eth0

[indigo-webservers]
192.168.20.20

[indigo:children]
indigo-databases
indigo-webservers
```

Where the IP addresses should be replaced with the host name/IP address of each 
machine. For each [indigo-databases] you must provide the Ethernet interface on 
which Cassandra communicates. Usually this is eth0, but it may be something 
different on more complex topologies.

* The default behavior is to use HTTPS. If needed this can be changed in the
webservers.yml file with the variable https_mode. The nginx server is using the
SSL certificate in /etc/nginx/ssl/nginx.crt. If they are not present a self-signed
version is created during deployment.

* The deployment is configured to use upstart by default. If you need to use
systemd there's a script that can be used and deployed during install. This is
commented in the main.yml task for indigo-web and indigo-listener role.

#### Deploying


Run the deployment with the following command:

```
ansible-playbook deploy_standalone.yml -i hosts --ask-become-pass
```

This command is used to deploy ERMR on a test server named loc-ermr 
(see staging/staging)

```
ansible-playbook deploy_standalone.yml -i staging/staging --ask-become-pass
```

* Once started the script will ask for some details. The sudo-password for the 
user specified in deploy-standalone.yml.

* Make a cup of tea.


#### Problems

Unfortunately Cassandra can take a while to start. The process list will show 
the Java process running although Cassandra is still not available. To resolve 
this the script pauses once the Cassandra installation is complete.

On some occasions the indigo-node fails to start after installation.  This is 
being investigated.
** As a temporary workaround execute
```sudo service indigo-web start```
on the target machine if the web-service fails to work. **

### Install on lxc container

For some reasons Cassandra configuration is failing when trying to deploy on a
lxc container. If you experiment a connection error when ansible is trying to 
finish Cassandra initialization you can try to log on the container, and restart
cassandra manually, it should now listen on eth0 correctly rather than 127.0.0.1.

For the listener the Docker install is failing on the first time but works if
ansible is restarted

