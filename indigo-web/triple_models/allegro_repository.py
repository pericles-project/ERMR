""""Triple UI views

Copyright 2015 Archive Analytics Solutions

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

from django.conf import settings
import requests
import urllib
from requests.exceptions import ConnectionError
import logging
import paho.mqtt.publish as publish
import json
from indigo.util import datetime_serializer



def mqtt_get_state(name):
    payload = dict()
    payload['name'] = name

    return payload

def add_repository_statements(name, data, content_type, empty_first=True):
    """Add statements to an existing repository
    
    - data can be an opened stream or a string
    - The content_type is used by allegro to determine how to parse the data
        "text/plain" for ntriple
        "application/rdf+xml" for RDF
    - when empty_first is True the repository is emptied before adding new
    statements"""
    url, auth = allegro_infos()
    try:
        pre_state = mqtt_get_state(name)
        if empty_first:
            r = requests.put("{}/repositories/{}/statements".format(
                                 url,
                                 name
                             ),
                             auth=auth,
                             data=data,
                             headers={"content-type" : content_type}
                            )
        else:
            r = requests.post("{}/repositories/{}/statements".format(
                                 url,
                                 name
                             ),
                             auth=auth,
                             data=data,
                             headers={"content-type" : content_type}
                            )
        updated = r.status_code==200
        if updated:
            post_state = mqtt_get_state(name)
            mqtt_publish(name, 'update', pre_state, post_state)
        return (updated, {}, r.status_code, r.text)
    except ConnectionError as e:
        return (False, [], 503, "Triple Store server is down")


def allegro_infos():
    """Get the allegro information for the connection. The information is
    stored in indigo_ui/settings.py as all Django config variables"""
    return (settings.ALLEGRO_SERVER['url'],
            (settings.ALLEGRO_SERVER['user'],settings.ALLEGRO_SERVER['pwd']))


def create_repository(name):
    """Create a new repository"""
    try:
        url, auth = allegro_infos()
        r = requests.put("{}/repositories/{}".format(
                             url,
                             name
                         ),
                         auth=auth)
        created = r.status_code==204
        if created:
            state = mqtt_get_state(name)
            mqtt_publish(name, 'create', {}, state)
        return (created, {}, r.status_code, r.text)
    except ConnectionError as e:
        return (False, [], 503, "Triple Store server is down")


def delete_repository(name):
    """Delete a repository"""
    try:
        url, auth = allegro_infos()
        r = requests.delete("{}/repositories/{}".format(url, name),
                            auth=auth)
        deleted = r.status_code==200
        if deleted:
            state = mqtt_get_state(name)
            mqtt_publish(name, 'delete', state, {})
        return (deleted, {}, r.status_code, r.text)
    except ConnectionError as e:
        return (False, [], 503, "Triple Store server is down")


def delete_repository_statements(name):
    """Delete all statements of a repository"""
    url, auth = allegro_infos()
    try:
        pre_state = mqtt_get_state(name)
        r = requests.delete("{}/repositories/{}/statements".format(
                                url,
                                name
                            ),
                            auth=auth)
        updated = r.status_code==200
        if updated:
            post_state = mqtt_get_state(name)
            mqtt_publish(updated, 'update', pre_state, post_state)
        return (r.status_code==200, {}, r.status_code, r.text)
    except ConnectionError as e:
        return (False, [], 503, "Triple Store server is down")


def get_repository_statements(name):
    """Get all statements of a repository"""
    url, auth = allegro_infos()
    try:
        r = requests.get("{}/repositories/{}/statements".format(
                             url,
                             name
                         ),
                         headers={"accept" : "application/json"},
                         auth=auth)
        
        if r.status_code == 200:
            return (True, r.json(), r.status_code, "Success")
        else:
            return (False, [], r.status_code, r.text)
    except ConnectionError as e:
        return (False, [], 503, "Triple Store server is down")


def list_repositories():
    url, auth = allegro_infos()
    try:
        r = requests.get("{}/repositories".format(url),
                         headers={"accept" : "application/json"},
                         auth=auth)
        if r.status_code == 200:
            return (True, r.json(), r.status_code, "Success")
        else:
            return (False, [], r.status_code, r.text)
    except ConnectionError as e:
        return (False, [], 503, "Triple Store server is down")


def list_statements(name, accept="application/json"):
    url, auth = allegro_infos()
    try:
        r = requests.get("{}/repositories/{}/statements".format(url,
                                                                name),
                         headers={"accept" : accept},
                         auth=auth)
        if r.status_code == 200:
            #return (True, r.json(), r.status_code, "Success")
            return (True, r, r.status_code, "Success")
        else:
            return (False, [], r.status_code, r.text)
    except ConnectionError as e:
        return (False, [], 503, "Triple Store server is down")


def mqtt_publish(repository, operation, pre_state, post_state):
    payload = dict()
    payload['pre'] = pre_state
    payload['post'] = post_state
    topic = u'{0}/repository/{1}'.format(operation, repository)
    # Remove MQTT wildcards from the topic. Corner-case: If the repository name
    # is made entirely of # and + and a script is set to run on such a
    # repository name. But that's what you get if you use stupid names for
    # things.
    topic = topic.replace('#', '').replace('+', '')
    logging.info(u'Publishing on topic "{0}"'.format(topic))
    try:
        publish.single(topic, json.dumps(payload, default=datetime_serializer))
    except:
        logging.error(u'Problem while publishing on topic "{0}"'.format(topic))


def query_repository(name, query, accept="application/json", method="GET"):
    url, auth = allegro_infos()
    try:
        if method == "GET":
            r = requests.get("{}/repositories/{}?query={}".format(
                                url,
                                name,
                                urllib.quote_plus(query)
                             ),
                             headers={"accept" : accept},
                             auth=auth)
        elif method == "POST":
            r = requests.post("{}/repositories/{}?query={}".format(
                                url,
                                name,
                                urllib.quote_plus(query)
                               ),
                               headers={"accept" : accept},
                               auth=auth)
        if r.status_code == 200:
            return (True, r, r.status_code, "Success")
        else:
            return (False, [], r.status_code, r.text)
    except ConnectionError as e:
        return (False, [], 503, "Triple Store server is down")


def list_public_images(name, accept="application/json"):
    """Return a list of the images that have 
    http://www.pericles-project.eu/ns/DEM-Scenario#releaseState as 
    public.
    """
    query_str ="""SELECT  DISTINCT ?url_definition
WHERE {
    ?image rdf:type <http://www.pericles-project.eu/ns/DEM-Core#DigitalObject> .
    ?image <http://www.pericles-project.eu/ns/DEM-Scenario#releaseState> ?release .
    ?image <http://xrce.xerox.com/LRM#url> ?url_location .
    ?url_location rdf:type <http://xrce.xerox.com/LRM#Location> .
    ?url_location <http://xrce.xerox.com/LRM#definition> ?url_definition .
 FILTER (?release = "public")
}"""
    return query_repository(name, query_str, accept, "GET")


