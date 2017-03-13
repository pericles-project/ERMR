# Entity Registry and Model Repository

These document describe the Entity Registry Model Registry. ERMR is a central
component to manage digital ecosystems, it can keep track of entities and 
relationships. The registry we present is a translation layer that provides an 
accessible and well structured set of access methods to the data management
 system. Access methods comes in the form of RESTful services, accessible via 
 the base url of the registry. The registry is divided in two main components, 
 the object store and the triple store. Each components providing its own set
 of services.


The object store is used to store and register digital objects in the registry. 
The data model is that of a hierarchical object store, i.e. objects are chunks 
of data that are stored in selected containers and may have associated metadata 
in the form of name/value pairs. Agreed metadata conventions will be used to
provide the necessary registry functionality, that is to say the repository is 
agnostic to the data and metadata it stores, and the interpretation of both is 
the responsibility of the various applications, interpreters and engines that 
use the store as a registry. The object store provides a CDMI implementation 
for HTTP access to digital objects in the registry. The CDMI standard is fairly 
well designed, and the richest of the available “standards”. We layer a CDMI 
interface to provide remote (https) based access to the objects and metadata.


The triple store is a database for the storage and retrieval of triples through 
semantic queries. ERMR provides a service layer on top of the triple store, it 
can be used to access a virtualized triple store (Allegro Graph). It can also 
act as a mediator between other semantic services like LRM to extend its 
reasoning capabilities. The triple store provides a simple RESTful API for 
HTTP access to the registry. It can interpret queries expressed in the standard 
SPARQL query language to retrieve and manipulate data stored in the triple 
store. In order to link entities described as triples to the actual digital 
objects, the object store uses unique identifier that can be used to create a 
unique CDMI URL for that object. This URL can be used in a triple to link the 
two stores.


