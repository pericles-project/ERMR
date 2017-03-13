# Cloud Data Management Interface API


The object store can be used to organize collections and digital objects in the 
store. It implements the Cloud Data Management Interface (CDMI) that defines 
the functional interface that applications may use to create, retrieve, 
update and delete data elements from the Object Store. In addition, metadata 
can be set on collections and their contained data elements through this 
interface.

When you have succesfully deployed ERMR on a host, the CDMI web service is 
accessible at http://host/api/cdmi.


## Collections


### Create a collection using HTTP


#### Synopsys

To create a new collection object, the following request shall be performed:

`PUT <root URI>/api/cdmi/<CollectionName>/<NewCollectionName>/`

where:
  * `<root URI>` is the path to the registry.
  * `<CollectionName>` is zero or more intermediate collection that already 
  exist, with one ‘/’ between each pair of collection names.
  * `<NewCollectionName>` is the name for the collection to be created.

#### Response Status

|HTTP Status     |Description                                          |
|----------------|-----------------------------------------------------|
|201 Created     |The new collection was created                       |
|401 Unauthorized|The authentication credentials are missing or invalid|
|403 Forbidden   |The client lacks the proper authorization            |
|404 Not Found   |The resource was not found at the specified URI      |


#### Example

PUT to the collection URI to create a collection:

```
PUT /api/cdmi/MyCollection/ HTTP/1.1
Host: 192.168.56.100

Response:
HTTP/1.1 201 Created
```


### Create a collection using CDMI

#### Synopsys

To create a new collection object, the following request shall be performed:

`PUT <root URI>/api/cdmi/<CollectionName>/<NewCollectionName>/`

Where:
  * `<root URI>` is the path to the registry.
  * `<CollectionName>` is zero or more intermediate collection that already 
  exist, with one slash (i.e., "/") between each pair of collection names.
  * `<NewCollectionName>` is the name specified for the collection to be 
  created.


#### Request Headers

|Header                      |Type         |Description                 |Requirement |
|----------------------------|-------------|----------------------------|------------|
|Accept                      |Header String|“application/cdmi-container”|Optional    |
|Content-Type                |Header String|“application/cdmi-container”|Mandatory   |
|X-CDMI-Specification-Version|Header String|“1.1”                       |Mandatory   |


#### Request Body

|Field Name|Type       |Description                       |Requirement|
|----------|-----------|----------------------------------|-----------|
|metadata  |JSON Object|Metadata for the collection object|Optional   |


#### Response Headers

|Header                      |Type         |Description                 |Requirement|
|----------------------------|-------------|----------------------------|-----------|
|Content-Type                |Header String|“application/cdmi-container”|Mandatory  |
|X-CDMI-Specification-Version|Header String|“1.1”                       |Mandatory  |


#### Response Message Body

|Field Name|Type       |Description                    |Requirement|
|----------|-----------|-------------------------------|-----------|
|objectType|JSON String|“application/cdmi-container”   |Mandatory  |
|objectID  |JSON String|ObjectID of the object         |Mandatory  |
|objectName|JSON String|Name of the object             |Mandatory  |
|parentURI |JSON String|URI for the parent object      |Mandatory  |
|parentID  |JSON String|Object ID of the parent object |Mandatory  |
|metadata  |JSON Object|Metadata for the object        |Mandatory  |


#### Response Status

|HTTP Status     |Description                                          |
|----------------|-----------------------------------------------------|
|201 Created     |The new collection was created                       |
|400 Bad Request |The request contains invalid parameters              |
|401 Unauthorized|The authentication credentials are missing or invalid|
|403 Forbidden   |The client lacks the proper authorization            |
|404 Not Found   |The resource was not found at the specified URI      |


#### Example

PUT to the URI the collection object name and metadata:

```
PUT /api/cdmi/MyCollection/ HTTP/1.1
Host: 192.168.56.100
Accept: application/cdmi-container
Content-Type: application/cdmi-container
X-CDMI-Specification-Version: 1.1

{
    “metadata”: {}
}

Response:
HTTP/1.1 201 Created
Content-Type: application/cdmi-container
X-CDMI-Specification-Version: 1.1

{
    "objectType" : "application/cdmi-container",
    "objectID" : "00007ED900104E1D14771DC67C27BF8B",
    "objectName" : "MyCollection/",
    "parentURI" : "/",
    "parentID" : "00007E7F0010128E42D87EE34F5A6560",
    "metadata" : {
                  ...
                 },
}
```


###  Delete a collection using HTTP


#### Synopsys

To delete an existing container object, including all contained children, the following request shall be performed:

`DELETE <root URI>/api/cdmi/<CollectionName>/<TheCollectionName>/`

Where:
  * `<root URI>` is the path to the registry.
  * `<CollectionName>` is zero or more intermediate collection objects.
  * `<TheCollectionName>` is the name of the collection object to be deleted.


#### Response Status

|HTTP Status     |Description                                          |
|----------------|-----------------------------------------------------|
|204 No Content  |The collection was deleted                           |
|401 Unauthorized|The authentication credentials are missing or invalid|
|403 Forbidden   |The client lacks the proper authorization            |
|404 Not Found   |The resource was not found at the specified URI      |


#### Example

DELETE to the collection URI:

```
DELETE /api/cdmi/MyCollection/ HTTP/1.1
Host: 192.168.56.100

Response:
HTTP/1.1 204 No Content
```


### Delete a collection using CDMI


#### Synopsys


To delete an existing container object, including all contained children, the
following request shall be performed:

`DELETE <root URI>/api/cdmi/<CollectionName>/<TheCollectionName>/`

Where:
  * `<root URI>` is the path to the registry.
  * `<CollectionName>` is zero or more intermediate collection names.
  * `<TheCollectionName>` is the name of the collection to be deleted.


#### Request Headers


|Header                      |Type         |Description|Requirement|
|----------------------------|-------------|-----------|-----------|
|X-CDMI-Specification-Version|Header String|“1.1”      |Mandatory  |


#### Response Status


|HTTP Status     |Description                                          |
|----------------|-----------------------------------------------------|
|204 No Content  |The collection was deleted                           |
|401 Unauthorized|The authentication credentials are missing or invalid|
|403 Forbidden   |The client lacks the proper authorization            |
|404 Not Found   |The resource was not found at the specified URI      |


#### Example

DELETE the collection at URI:

```
DELETE /api/cdmi/MyCollection/ HTTP/1.1
Host: 192.168.56.100

Response:
HTTP/1.1 204 No Content
```


### Read a collection using CDMI


#### Synopsys


To read all fields from an existing collection object, the following request shall be performed:

`GET <root URI>/api/cdmi/<CollectionName>/<TheCollectionName>/`

Where:
  * `<root URI>` is the path to the registry.
  * `<CollectionName>` is zero or more intermediate collection objects.
  * `<TheCollectionName>` is the name specified for the collection object to 
  be read from.


#### Request Headers


|Header                      |Type         |Description                 |Requirement|
|----------------------------|-------------|----------------------------|-----------|
|Accept                      |Header String|“application/cdmi-container”|Optional   |
|X-CDMI-Specification-Version|Header String|“1.1”                       |Mandatory  |


#### Response Headers


|Header                      |Type         |Description                 |Requirement|
|----------------------------|-------------|----------------------------|-----------|
|Content-Type                |Header String|“application/cdmi-container”|Mandatory  |
|X-CDMI-Specification-Version|Header String|1.1”                        |Mandatory  |


#### Response Message Body


|Field Name|Type                      |Description                                          |Requirement|
|----------|--------------------------|-----------------------------------------------------|-----------|
|objectType|JSON String               |“application/cdmi-container”                         |Mandatory  |
|objectID  |JSON String               |ObjectID of the object                               |Mandatory  |
|objectName|JSON String               |Name of the object                                   |Mandatory  |
|parentURI |JSON String               |URI for the parent object                            |Mandatory  |
|parentID  |JSON String               |Object ID of the parent object                       |Mandatory  |
|metadata  |JSON Object               |Metadata for the object                              |Mandatory  |
|children  |JSON Array of JSON Strings|Name of the children objects in the collection object|Mandatory  |


#### Response Status


|HTTP Status     |Description                                                    |
|----------------|---------------------------------------------------------------|
|200 OK          |The metadata for the collection is provided in the message body|
|400 Bad Request |The request contains invalid parameters or field names         |
|401 Unauthorized|The authentication credentials are missing or invalid          |
|403 Forbidden   |The client lacks the proper authorization                      |
|404 Not Found   |The resource was not found at the specified URI                |


#### Example


GET to the collection object URI to read all the fields of the collection object:

```
GET /api/cdmi/MyCollection/ HTTP/1.1
Host: 192.168.56.100
Accept: application/cdmi-container
X-CDMI-Specification-Version: 1.1

Response:
HTTP/1.1 200 OK
Content-Type: application/cdmi-container
X-CDMI-Specification-Version: 1.1

{
    "objectType" : "application/cdmi-container",
    "objectID" : "00007ED900104E1D14771DC67C27BF8B",
    "objectName" : "MyCollection/",
    "parentURI" : "/",
    "parentID" : "00007E7F0010128E42D87EE34F5A6560",
    "metadata" : {
                    ...
                 },
    "children" : [
                   "child1",
                   “child2”,
                   …
                 ]
}
```


### Update a collection using CDMI


#### Synopsys


To update some or all fields in an existing collection object, the following
request shall be performed:

`PUT <root URI>/api/cdmi/<CollectionName>/<TheCollectionName>/`

To add, update, and remove specific metadata items of an existing collection 
object, the following request shall be performed:

`PUT <root URI> /api/cdmi/ <CollectionName> / <TheCollectionName> / ?metadata:<metadataname>`

Where:
  * `<root URI>` is the path to the registry.
  * `<CollectionName>` is zero or more intermediate collection objects.
  * `<TheCollectionName>` is the name of the collection object to be updated.


#### Request Headers


|Header                      |Type         |Description                 |Requirement|
|----------------------------|-------------|----------------------------|-----------|
|Accept                      |Header String|“application/cdmi-container”|Optional   |
|X-CDMI-Specification-Version|Header String|“1.1”                       |Mandatory  |


#### Request Body


|Field Name|Type       |Description                       |Requirement|
|----------|-----------|----------------------------------|-----------|
|metadata  |JSON Object|Metadata for the collection object|Optional   |


#### Response Status


|HTTP Status     |Description                                          |
|----------------|-----------------------------------------------------|
|204 No Content  |The collection content was updated                   |
|400 Bad Request |The request contains invalid parameters              |
|401 Unauthorized|The authentication credentials are missing or invalid|
|403 Forbidden   |The client lacks the proper authorization            |
|404 Not Found   |The resource was not found at the specified URI      |


#### Example


PUT to the collection object URI to set new metadata :

```
PUT /api/cdmi/MyCollection/ HTTP/1.1
Host: 192.168.56.100
Content-Type: application/cdmi-container
X-CDMI-Specification-Version: 1.1

{
"metadata" : { ...
             }
}

Response:
HTTP/1.1 204 No Content
```


## Data Objects


### Create an object using HTTP


#### Synopsys


The following HTTP PUT creates a new data object at the specified URI:

`PUT <root URI>/api/cdmi/<CollectionName>/<DataObjectName>`

Where:
  * `<root URI>` is the path to the CDMI cloud.
  * `<CollectionName>` is zero or more intermediate collections that already 
  exist, with one slash (i.e., "/") between each pair of collection names.
  * `<DataObjectName>` is the name specified for the data object to be created


#### Request Headers


|Header       |Type         |Description                                               |Requirement|
|-------------|-------------|----------------------------------------------------------|-----------|
|Content-Type |Header String|The content type of the data to be stored as a data object|Optional   |
|Content-Range|Header String|A valid range-specifier                                   |Optional   |


#### Request Body


The request message body contains the data to be stored.


#### Response Status


|HTTP Status     |Description                                          |
|----------------|-----------------------------------------------------|
|201 Created     |The new data object was created                      |
|401 Unauthorized|The authentication credentials are missing or invalid|
|403 Forbidden   |The client lacks the proper authorization            |
|404 Not Found   |The resource was not found at the specified URI      |


#### Example


PUT to the collection URI the data object name and contents:

```
PUT /api/cdmi/MyCollection/MyDataObject.txt HTTP/1.1
Host: 192.168.56.100
Content-Type: text/plain;charset=utf-8
Content-Length: 37

This is the Value of this Data Object

Response:
HTTP/1.1 201 Created
```


### Create an object using CDMI


#### Synopsys


To create a new data object, the following request shall be performed:

`PUT <root URI>/api/cdmi/<CollectionName>/<DataObjectName>`

Where:
  * `<root URI>` is the path to the registry.
  * `<CollectionName>` is zero or more intermediate collections that already 
  exist, with one slash (i.e., "/") between each pair of collection names.
  * `<DataObjectName>` is the name specified for the data object to be created.


#### Request Headers

|Header                      |Type         |Description              |Requirement|
|----------------------------|-------------|-------------------------|-----------|
|Accept                      |Header String|“application/cdmi-object”|Optional   |
|Content-Type                |Header String|“application/cdmi-object”|Mandatory  |
|X-CDMI-Specification-Version|Header String|“1.1”                    |Mandatory  |


#### Request Message Body


|Field Name|Type       |Description                                           |Requirement|
|----------|-----------|------------------------------------------------------|-----------|
|mimetype  |JSON String|Mime type of the data contained within the value field|Optional   |
|metadata  |JSON Object|Metadata for the data object                          |Optional   |
|value     |JSON String|The data object value                                 |Optional   |


#### Response Headers


|Header                      |Type         |Description              |Requirement|
|----------------------------|-------------|-------------------------|-----------|
|Content-Type                |Header String|“application/cdmi-object”|Mandatory  |
|X-CDMI-Specification-Version|Header String|“1.1”                    |Mandatory  |


#### Response Message Body


|Field Name|Type       |Description                              |Requirement|
|----------|-----------|-----------------------------------------|-----------|
|objectType|JSON String|“application/cdmi-object”                |Mandatory  |
|objectID  |JSON String|ObjectID of the object                   |Mandatory  |
|objectName|JSON String|Name of the object                       |Mandatory  |
|parentURI |JSON String|URI for the parent object                |Mandatory  |
|parentID  |JSON String|Object ID of the parent object           |Mandatory  |
|mimetype  |JSON String|MIME type of the value of the data object|Mandatory  |
|metadata  |JSON Object|Metadata for the object                  |Mandatory  |


#### Response Status


|HTTP Status     |Description                                          |
|----------------|-----------------------------------------------------|
|201 Created     |The new data object was created                      |
|400 Bad Request |The request contains invalid parameters              |
|401 Unauthorized|The authentication credentials are missing or invalid|
|403 Forbidden   |The client lacks the proper authorization            |
|404 Not Found   |The resource was not found at the specified URI      |


#### Example


PUT to the collection URI the data object name and contents:

```
PUT /api/cdmi/MyCollection/MyDataObject.txt HTTP/1.1
Host: 192.168.56.100
Accept: application/cdmi-object
Content-Type: application/cdmi-object
X-CDMI-Specification-Version: 1.1

{
    "mimetype" : "text/plain",
    "metadata" : { ...
    },
    "value" : "This is the Value of this Data Object"
}

Response:
HTTP/1.1 201 Created
Content-Type: application/cdmi-object
X-CDMI-Specification-Version: 1.1
{
    "objectType" : "application/cdmi-object",
    "objectID" : "00007ED90010D891022876A8DE0BC0FD",
    "objectName" : "MyDataObject.txt",
    "parentURI" : "/MyContainer/",
    "parentID" : "00007E7F00102E230ED82694DAA975D2",
    "mimetype" : "text/plain",
    "metadata" : {
        "cdmi_size" : "37"
    }
}
```


### Delete an object using HTTP


#### Synopsys

The following HTTP DELETE deletes an existing data object at the specified URI:

`DELETE <root URI>/api/cdmi/<CollectionName>/<DataObjectName>`

Where:
  * `<root URI>` is the path to the CDMI cloud.
  * `<CollectionName>` is zero or more intermediate collections.
  * `<DataObjectName>` is the name of the data object to be deleted.


#### Response Status

|HTTP Status     |Description                                          |
|----------------|-----------------------------------------------------|
|204 No Content  |The data object was deleted                          |
|400 Bad Request |The request contains invalid parameters              |
|401 Unauthorized|The authentication credentials are missing or invalid|
|403 Forbidden   |The client lacks the proper authorization            |
|404 Not Found   |The resource was not found at the specified URI      |


#### Example


DELETE to the data object URI:

```
DELETE /api/cdmi/MyCollection/MyDataObject.txt HTTP/1.1
Host: 192.168.56.100

Response:
HTTP/1.1 204 No Content
```


### Delete an object using CDMI


#### Synopsys


The following HTTP DELETE deletes an existing data object at the specified URI:

`DELETE <root URI>/api/cdmi/<CollectionName>/<DataObjectName>`

Where:
  * `<root URI>` is the path to the CDMI cloud.
  * `<CollectionName>` is zero or more intermediate collections.
  * `<DataObjectName>` is the name of the data object to be deleted.


#### Request Headers


|Header                      |Type         |Description|Requirement|
|----------------------------|-------------|-----------|-----------|
|X-CDMI-Specification-Version|Header String|“1.1”      |Mandatory  |


#### Response Status


|HTTP Status     |Description                                          |
|----------------|-----------------------------------------------------|
|204 No Content  |The data object was deleted                          |
|400 Bad Request |The request contains invalid parameters              |
|401 Unauthorized|The authentication credentials are missing or invalid|
|403 Forbidden   |The client lacks the proper authorization            |
|404 Not Found   |The resource was not found at the specified URI      |


#### Example


DELETE the data object URI:

```
DELETE /api/cdmi/MyCollection/MyDataObject.txt HTTP/1.1
Host: 192.168.56.100
X-CDMI-Specification-Version: 1.1

Response:
HTTP/1.1 204 No Content
```


### Read an object using HTTP


#### Synopsys


The following HTTP GET reads from an existing data object at the specified URI:

`GET <root URI>/api/cdmi/<CollectionName>/<DataObjectName>`

Where:
  * `<root URI>` is the path to the registry.
  * `<CollectionName>` is zero or more intermediate collections.
  * `<DataObjectName>` is the name of the data object to be read from


#### Request Headers


|Header|Type         |Description            |Requirement|
|------|-------------|-----------------------|-----------|
|Range |Header String|A valid range specifier|Optional   |


#### Response Headers


|Header      |Type         |Description                    |Requirement|
|------------|-------------|-------------------------------|-----------|
|Content-Type|Header String|The mimetype of the data object|Mandatory  |


#### Response Message Body


The response message body is the content of the data object.


#### Response Status


|HTTP Status     |Description                                          |
|----------------|-----------------------------------------------------|
|20O OK          |The data object content was returned in the response |
|401 Unauthorized|The authentication credentials are missing or invalid|
|403 Forbidden   |The client lacks the proper authorization            |
|404 Not Found   |The resource was not found at the specified URI      |


#### Example 1


GET to the data object URI to read the value of the data object:

```
GET /api/cdmi/MyCollection/MyDataObject.txt HTTP/1.1
Host: 192.168.56.100

Response:
HTTP/1.1 200 OK
Content-Type: text/plain
Content-Length: 37

This is the Value of this Data Object
```


#### Example 2


GET to the data object URI to read the first 11 bytes of the value of the data
object:

```
GET /api/cdmi/MyContainer/MyDataObject.txt HTTP/1.1
Host: 192.168.56.100
Range: bytes=0-10

Response:
HTTP/1.1 206 Partial Content
Content-Type: text/plain
Content-Range: bytes 0-10/37
Content-Length: 11

This is the
```


### Read an object using CDMI


#### Synopsys


The following HTTP GET reads from an existing data object at the specified URI:

`GET <root URI>/api/cdmi/<CollectionName>/<DataObjectName>`

`GET <root URI>/api/cdmi/<CollectionName>/<DataObjectName> ?value:<range>;...`

`GET <root URI>/api/cdmi/<CollectionName>/<DataObjectName> ?metadata:<prefix>;...`

Where:
  * `<root URI>` is the path to the CDMI cloud.
  * `<CollectionName>` is zero or more intermediate collections.
  * `<DataObjectName>` is the name of the data object to be read from.
  * `<range>` is a byte range of the data object value to be returned in the 
  value field.
  * `<prefix>` is a matching prefix that returns all metadata items that start 
  with the prefix value.


#### Request Headers


|Header                      |Type         |Description              |Requirement|
|----------------------------|-------------|-------------------------|-----------|
|Accept                      |Header String|“application/cdmi-object”|Optional   |
|X-CDMI-Specification-Version|Header String|“1.1”                    |Mandatory  |


#### Response Headers


|Header                      |Type         |Description              |Requirement|
|----------------------------|-------------|-------------------------|-----------|
|Content-Type                |Header String|“application/cdmi-object”|Mandatory  |
|X-CDMI-Specification-Version|Header String|“1.1”                    |Mandatory  |


#### Response Message Body


|Field Name|Type       |Description                              |Requirement|
|----------|-----------|-----------------------------------------|-----------|
|objectType|JSON String|“application/cdmi-object”                |Mandatory  |
|objectID  |JSON String|ObjectID of the object                   |Mandatory  |
|objectName|JSON String|Name of the object                       |Mandatory  |
|parentURI |JSON String|URI for the parent object                |Mandatory  |
|parentID  |JSON String|Object ID of the parent object           |Mandatory  |
|mimetype  |JSON String|MIME type of the value of the data object|Mandatory  |
|metadata  |JSON Object|Metadata for the object                  |Mandatory  |
|value     |JSON String|data object value                        |Conditional|


#### Response Status


|HTTP Status     |Description                                          |
|----------------|-----------------------------------------------------|
|20O OK          |The data object content was returned in the response |
|401 Unauthorized|The authentication credentials are missing or invalid|
|403 Forbidden   |The client lacks the proper authorization            |
|404 Not Found   |The resource was not found at the specified URI      |


#### Example


GET to the data object URI to read all fields of the data object:

```
GET /api/cdmi/MyCollection/MyDataObject.txt HTTP/1.1
Host: 192.168.56.100
Accept: application/cdmi-object
X-CDMI-Specification-Version: 1.1

Response:
HTTP/1.1 200 OK
X-CDMI-Specification-Version: 1.1
Content-Type: application/cdmi-object

{
    "objectType" : "application/cdmi-object",
    "objectID" : "00007ED90010D891022876A8DE0BC0FD",
    "objectName" : "MyDataObject.txt",
    "parentURI" : "/MyCollection/",
    "parentID" : "00007E7F00102E230ED82694DAA975D2",
    "mimetype" : "text/plain",
    "metadata" : {
        "cdmi_size" : "37"
    },
    "valuerange" : "0-36",
    "value" : "This is the Value of this Data Object"
}
```


### Update an object using HTTP


####Synopsys


The following HTTP PUT updates an existing data object at the specified URI:

`PUT <root URI>/api/cdmi/<CollectionName>/<DataObjectName>`

Where:
  * `<root URI>` is the path to the CDMI cloud.
  * `<CollectionName>` is zero or more intermediate collections.
  * `<DataObjectName>` is the name of the data object to be updated.


#### Request Headers


|Header       |Type         |Description                                            |Requirement|
|-------------|-------------|-------------------------------------------------------|-----------|
|Content-Type |Header String|The mime type of the data to be stored as a data object|Optional   |
|Content-Range|Header String|A valid range-specifier                                |Optional   |


#### Request Body


The request message body contains the data to be stored.


#### Response Status


|HTTP Status     |Description                                          |
|----------------|-----------------------------------------------------|
|204 No Content  |The data object content was updated                  |
|401 Unauthorized|The authentication credentials are missing or invalid|
|403 Forbidden   |The client lacks the proper authorization            |
|404 Not Found   |The resource was not found at the specified URI      |


#### Example


PUT to the data object URI to update the value of the data object:

```
PUT /api/cdmi/MyCollection/MyDataObject.txt HTTP/1.1
Host: 192.168.56.100
Content-Type: text/plain
Content-Length: 37

This is the value of this data object

Response:
HTTP/1.1 204 No Content
```


### Update an object using CDMI


#### Synopsys


The following HTTP PUT updates an existing data object at the specified URI:

`PUT <root URI>/api/cdmi/<CollectionName>/<DataObjectName>`

`PUT <root URI>/api/cdmi/<CollectionName>/<DataObjectName> ?value:<range>`

`PUT <root URI>/api/cdmi/<CollectionName>/<DataObjectName> ?metadata:<metadataname>`

Where:
  * `<root URI>` is the path to the registry.
  * `<CollectionName>` is zero or more intermediate collections that already 
  exist, with one slash (i.e., "/") between each pair of collection names.
  * `<DataObjectName>` is the name specified for the data object to be 
  created.
  * `<range>` is a byte range for the data object value to be updated.


#### Request Headers


|Header                      |Type         |Description              |Requirement|
|----------------------------|-------------|-------------------------|-----------|
|Content-Type                |Header String|“application/cdmi-object”|Mandatory  |
|X-CDMI-Specification-Version|Header String|“1.1”                    |Mandatory  |


#### Request Message Body


|Field Name|Type       |Description                                           |Requirement|
|----------|-----------|------------------------------------------------------|-----------|
|mimetype  |JSON String|Mime type of the data contained within the value field|Optional   |
|metadata  |JSON Object|Metadata for the data object                          |Optional   |
|value     |JSON String|The data object value                                 |Optional   |


#### Response Status


|HTTP Status     |Description                                          |
|----------------|-----------------------------------------------------|
|204 No Content  |The data object was updated                          |
|400 Bad Request |The request contains invalid parameters              |
|401 Unauthorized|The authentication credentials are missing or invalid|
|403 Forbidden   |The client lacks the proper authorization            |
|404 Not Found   |The resource was not found at the specified URI      |


#### Example


PUT to the data object URI to set new field values:

```
PUT /api/cdmi/MyCollection/MyDataObject.txt HTTP/1.1
Host: 192.168.56.100
Accept: application/cdmi-object
Content-Type: application/cdmi-object
X-CDMI-Specification-Version: 1.1
{
    "mimetype" : "text/plain",
    "metadata" : {
       "colour": "red",
    },
    "value" : "This is the Value of this Data Object"
}


Response:
HTTP/1.1 204 No Content
```