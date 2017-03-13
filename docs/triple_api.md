# Triple Store API


The ERMR triple store API acts as a mediator between clients and the internal 
triple store we are using. It interprets the requests of the client and forward 
a request in the correct format for the triple store.


When you have succesfully deployed ERMR on a host, the CDMI web service is 
accessible at http://host/api/triple.


### List repositories


#### Synopsys


To list existing repositories, the following request shall be performed:

`GET <root URI>/api/triple`

where:
  * `<root URI>` is the path to the registry.


#### Response Message Body


The response message contains a JSON list of repositories informations (to be 
refined).


#### Response Status


|HTTP Status|Description         |
|-----------|--------------------|
|200 OK     |The list is returned|


#### Example


GET a list of repositories:

```
GET /api/triple HTTP/1.1
Host: 192.168.56.100

Response:
HTTP/1.1 200 Ok

[ { "title": "DemoLondon", "writable": true, "id": "DemoLondon" }, 
  { "title": "Test", "writable": true, "id": "Test" } ]
```


### Create a repository


#### Synopsys


To create a new repository, the following request shall be performed:

`PUT <root URI>/api/triple/<NewRepositoryName>`

where:
  * `<root URI>` is the path to the registry.
  * `<NewRepositoryName>` is the name for the repository to be created.


#### Response Status


|HTTP Status|Description                   |
|-----------|------------------------------|
|201 Created|The new repository was created|


#### Example


PUT to the triple store URI to create a repository:

```
PUT /api/triple/MyRepository HTTP/1.1
Host: 192.168.56.100

Response:
HTTP/1.1 201 Created
```


### Delete a repository


#### Synopsys


To delete a repository, the following request shall be performed:

`DELETE <root URI>/api/triple/<repositoryName>`

where:
  * `<root URI>` is the path to the registry.
  * `<repositoryName>` is the name of the repository to be deleted.


#### Response Status


|HTTP Status   |Description               |
|--------------|--------------------------|
|204 No Content|The repository was deleted|


#### Example


DELETE a repository:

```
Delete /api/triple/MyRepository HTTP/1.1
Host: 192.168.56.100

Response:
HTTP/1.1 204 No Content
```


### Add triples to a repository


#### Synopsys


The following HTTP PUT/POST requests add triples to a repository. A PUT request 
empty the repository first while a POST request add triples.


`PUT <root URI>/api/triple/<repositoryName>/statements`

`POST <root URI>/api/triple/<repositoryName>/statements`

Where:
  * `<root URI>` is the path to the registry.
  * `<repositoryName>` is the name of the repository.


#### Request Headers


|Header      |Type         |Description                    |Requirement|
|------------|-------------|-------------------------------|-----------|
|Content-Type|Header String|The content type of the triples|Mandatory  |
|            |             |“text/plain” for ntriples      |           |
|            |             |“application/rdf+xml” for RDF  |           |
|            |             |“text/turtle” for Turtle       |           |


#### Request Body


The request message body contains the data to be stored.


#### Response Status


|HTTP Status|Description           |
|-----------|----------------------|
|201 Created|The triples were added|


#### Example


PUT triples to the repository URI:

```
PUT /api/triple/MyRepository/statements HTTP/1.1
Host: 192.168.56.100
Content-Type: text/plain

<http://www.pericles.org/models#process1> <http://www.pericles.org/models#name> "Ingest" .
<http://www.pericles.org/models#process1> <http://www.pericles.org/models#description> "Ingest documents in the registry" .
<http://www.pericles.org/models#process1> <http://www.pericles.org/models#identity> "7d4e14c8-1adf-4cfd-b0b8-ede46944b006" .
<http://www.pericles.org/models#process1> <http://www.pericles.org/models#version> "0.1" .

Response:
HTTP/1.1 201 Created
```


### List triples of a repository


#### Synopsys


To list triples contained in an existing repository, the following request 
shall be performed:

`GET <root URI>/api/triple/<repositoryName>`

`GET <root URI>/api/triple/<repositoryName>/statements`

where:
  * `<root URI>` is the path to the registry.
  * `<repositoryName>` is the name of the repository to list.


#### Request Headers


|Header|Type         |Description          |Requirement|
|------|-------------|---------------------|-----------|
|Accept|Header String|“application/json”   |Optional   |
|      |             |“application/rdf+xml”|           |


#### Response Message Body


By default the response message contains a JSON list of triples. Specifying 
“application/rdf+xml” as the Accept header can be used to obtain the result in 
XML.


#### Response Status


|HTTP Status|Description         |
|-----------|--------------------|
|200 OK     |The list is returned|


#### Example


GET a list of repository triples:

```
GET /api/triple/MyRepository HTTP/1.1
Host: 192.168.56.100

Response:
HTTP/1.1 200 Ok

[
    [
        "<http://www.pericles.org/models#process3>",
        "<http://www.pericles.org/models#version>",
        "\"1.0\""
    ],
    [
        "<http://www.pericles.org/models#process3>",
        "<http://www.pericles.org/models#identity>",
        "\"3ecdb028-40ec-453a-b4eb-21ad9234ac5e\""
    ],
    [
        "<http://www.pericles.org/models#process3>",
        "<http://www.pericles.org/models#description>",
        "\"Extract metadata in a document of the registry\""
    ],
    [
        "<http://www.pericles.org/models#process3>",
        "<http://www.w3.org/1999/02/22-rdf-syntax-ns#type>",
        "<http://www.pericles.org/models#process>"
    ],
...
]
```


### Delete all triples of a repository


#### Synopsys


To delete all triples of a repository, the following request shall be performed:

`DELETE <root URI>/api/triple/<repositoryName>/statements`

where:
  * `<root URI>` is the path to the registry.
  * `<repositoryName>` is the name of the repository that contains triples 
  to be deleted.


#### Response Status


|HTTP Status   |Description             |
|--------------|------------------------|
|204 No Content|The triples were deleted|


#### Example


DELETE a repository:

```
Delete /api/triple/MyRepository/statements HTTP/1.1
Host: 192.168.56.100

Response:
HTTP/1.1 204 No Content
```


### Query a repository


#### Synopsys


To send a SPARQL query to a repository, the following request shall be performed:

`GET <root URI>/api/triple/<repositoryName>?query=<SparqlQuery>`

where:
  * `<root URI>` is the path to the registry.
  * `<repositoryName>` is the name of the repository to query.
  * `<SparqlQuery>` is a sparql query encoded as a URI.


#### Request Headers


|Header|Type         |Description                      |Requirement|
|------|-------------|---------------------------------|-----------|
|Accept|Header String|“application/json”               |Optional   |
|      |             |“application/sparql-results+xml” |           |
|      |             |“application/sparql-results+json”|           |


#### Response Message Body


By default the response message contains a JSON dictionary (“application/json”):
* “values stores a list of tuples
* “name” stores a list of names for the returned tuples

Specifying “application/sparql-results+xml”  or “application/sparql-results+json” 
can be used to obtain these outputs : 
* https://www.w3.org/TR/rdf-sparql-XMLres/
* https://www.w3.org/2001/sw/DataAccess/json-sparql/


#### Response Status


|HTTP Status|Description           |
|-----------|----------------------|
|200 OK     |The result is returned|


#### Example


GET to evaluate a SPARQL query on a repository:

````
GET /api/triple/MyRepo?query=select%20?s%20?p%20?o%20%7B?s%20?p%20?o%7D HTTP/1.1
Host: 192.168.56.100

Response:
HTTP/1.1 200 Ok

{
    "values": [
        [
            "<http://www.pericles.org/models#version>",
            "\"1.0\""
        ],
        [
            "<http://www.pericles.org/models#identity>",
            "\"3ecdb028-40ec-453a-b4eb-21ad9234ac5e\""
        ],
        [
            "<http://www.pericles.org/models#name>",
            "\"Convert\""
        ],
...
    ],
    "names": [
        "p",
        "o"
    ]
}
````