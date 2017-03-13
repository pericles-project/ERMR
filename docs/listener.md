# ERMR Listener


## Synopsis


The listener is a daemon that executes user-created Python scripts when events 
trigger on the ERMR.


## Overview of operation

When *create*, *update*, or *delete* operations are performed on either a 
*collection* or a *resource*, a message is sent to a broker running on the 
local machine containing information about the operation and resource. 
The listener checks its cache of user-defined scripts to determine if any
script matches that message. If a script does match, it is passed the message 
and executed in a sandbox environment as a separate process. The 
user-defined script is free to do as it wants, given tight constraints over 
file-system access and the packages that are available. The scripts are stored 
within a special collection, and only the machine that performsthe operation 
executes the script. So for any one operation, a given script will execute 
exactly once.


## Messages

Because the application that interacts with ERMR is running as a different 
process (or possibly on a different machine), normal intra-process 
communication will not work, so some form of inter-process or network 
communication is needed. Indigo uses MQTT for this communication, which is an
 example of a publish/subscribe model. MQTT has a central "broker" that 
 receives all messages and forwards them on to clients who have subscribed to a
 topic or topics. In the case of MQTT, topics are a text string in the form of 
 a UNIX-style path or URI, which defines a hierarchy. E.g.:

`create/resource/something`

The format of topics used in the listener is:

`<operation>/<type>/<collection>/<collection>/.../<resource>`

Where `<operation>/<type>/` represents the root *collection*.

Subscribers can match all or part of a topic using the wildcards `#` and `+`,
 where `+` matches a single level of the hierarchy and `#` matches a complete 
 sub-tree of the hierarchy and must be the last character in the topic if it is
used. For example:

`+/resource/somepath/someresource`

Matches any operation on that particular *resource*.

`create/+/somepath/#`

Matches a *create* operation on any *resource* or *collection* below `/somepath`

User-defined scripts can currently subscribe to one topic (including wildcards).
This is defined in Indigo by giving it the metadata key "topic" and the
matching topic string as its value. If this metadata isn't present, the listener
ignores the script. Note, scripts cannot trigger off changes to the 
`/scripts` collection.


## Sandbox


When a user-defined script is triggered, it is passed the topic as a command 
line argument, and metadata about the object is given in JSON format through 
`stdin`. The script itself can be any Python script that can be called through
the command line, e.g: `/usr/bin/python myscript.py`

The environment the script is executed in is a Docker container running 
Python 3.4.3 The script is executed as the user `nobody` and the entire file
 system within the container is read-only. Any output to `stdout` or `stderr` 
 is directed to `/dev/null` TCP/IP ports 80, 443, 21, 22, 25, 587, 465 are 
 open for HTTP/HTTPS/FTP/SFTP/SSH/SMTP access. Note, these ports are mapped 
 directly onto the server's ports, so they are subject to the same 
 firewall/iptables rules as the server.

Long-running scripts (currently > 12 seconds) are terminated, and each script 
is given only a limited amount of memory (currently this isn't true, but I need 
to settle on a reasonable default).


## Script example


This a script which automatically adds metadata to a file which is uploaded to
the object store.

To use it you can upload it to the */scripts* collection and add a metadata to
it : *topic*: *create/+/TestCollection/#*

```
import sys
import json
import requests

# Name of the script that got executed
script_name = sys.argv[0]
# MQTT topic associated to the notification
topic = sys.argv[1]
# Payload of the message
payload = json.loads(sys.argv[2])

cdmi_path = "{}/{}".format(payload["post"]["container"], 
                           payload["post"]["name"])

auth = ("guest", "guest")
req_url = "https://192.168.56.100/api/cdmi{}".format(cdmi_path)

headers = {'X-CDMI-Specification-Version': "1.1"}
if cdmi_path.endswith('/'):
    headers['Content-type'] = 'application/cdmi-container'
else:
    headers['Content-type'] = 'application/cdmi-object'

metadata =  payload["post"]["metadata"]
metadata["auto"] = "meta"
data = { "metadata": metadata }

res = requests.put(req_url, headers=headers, auth=auth,
                   data=json.dumps(data), verify=False)
```