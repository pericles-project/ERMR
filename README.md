# ERMR

## Presentation



The Entity Registry and Model Repository tool (ERMR) is an open-source 
middleware component designed to implement a long-term data preservation 
environment to manage large collections of scientific data, replicated across 
different research projects, which may form the basis of international 
collaborations.

The ERMR was developed in response to PERICLES user requirements, which 
highlight many challenges relating to access and curation of scientific data. 
The ERMR follows the project’s information model to depict the semantics of the 
data and their interrelationships, which may be used as the basis for 
automatically deriving and annotating links (LRM); and the QA approach to 
ensure that the right data is accessible easily, and the obsolete data gets 
removed or refreshed. The overall aim is not simply to place data in a data 
repository, but to share large quantities of raw data, pre-processed data, and 
post-processed data across many collaborators on a regular basis.

The ERMR is designed as a federated system, using the Apache Cassandra 
database, providing access to distributed repositories of scientific and 
experimental data. The design of this tool has evolved from mainly an 
iRODS-based system, to the latest version, which can support potentially any 
storage technology, including CEPH. Within the PERICLES project, the ERMR is 
used to in managing the data life cycle, or continuum, across shared 
collections in ways that might foster collaborations and data re-use.

The overall aim is not simply to place data in a data repository, but to share 
large quantities of raw data, pre-processed data, and post-processed data 
across many collaborators on a regular basis. This has required the 
incorporation of tables and fact stores, required for the LRM, which go 
further than object storage technologies in managing the data archive.

Features include:

* High performance network data transfer
* Easy back up and replication
* Metadata management
* Controlled access through ACLs
* Management of large collections, including audit trails
* Workflows executed as part of normal operation
* A listener that will invoke action scripts

ERMR was created for the PERICLES project (http://www.pericles-project.eu/).



## Installation

ERMR is deployed with Ansible, from a guest to a number of hosts. Ansible 
controls node configuration over SSH to connect to servers and run the 
configured tasks. The folder _./ermr-deploy_ contains the ansible playbook 
that can be used to deploy a working system to configured hosts. It has a 
specific documentation folder (_./ermr-deploy/docs_) with a precise 
description of the installation procedure. 

A quick summary of the install procedure :

* Install an ubuntu 14.04 LTS on a virtual machine. Indigo has been tested
successfully on ubuntu 16.04 but it may need some manual tweaking. It requires
an `indigo` user with sudo access.

* Configure the host so it can be accessed by SSH from the guest from which you 
are installing.

* Install ansible on the guest.

* Configure an ansible inventory file to describe the host(s) where ERMR will 
be deployed.

* Install with the command 
`ansible-playbook deploy_standalone.yml -i hosts --ask-become-pass`

* If all goes well you should have a running nginx server serving ERMR on port 
80 on the host.



## Usage


* ERMR web interface is accessible at http://<host-ip>

* Ansible creates a set of user you can use to experiment

  * pericles/Per1cles
  * pericles1/Per1cles
  * guest/guest

* ERMR RESTful APIs are accessible from other clients:

  * http://<host-ip>/api/cdmi for the CDMI API to access the object store
  
  * http://<host-ip>/api/triple for the triple store API to manage triples
  
* Some ERMR documentation is available in the _./docs_ folder.


