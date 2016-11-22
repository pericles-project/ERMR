""""view for the api/triple restful api

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

from rest_framework.decorators import (
    api_view,
    authentication_classes,
    renderer_classes
)
from rest_framework.authentication import (
    BasicAuthentication,
    exceptions
)
import urllib
import json
from django.http import JsonResponse
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from rest_framework.response import Response
from rest_framework_xml.renderers import XMLRenderer
from rest_framework.renderers import JSONRenderer
import cgi
import cStringIO
from rest_framework.status import (
    HTTP_200_OK,
    HTTP_201_CREATED,
    HTTP_204_NO_CONTENT,
    HTTP_400_BAD_REQUEST,
    HTTP_406_NOT_ACCEPTABLE,
    
)
import ldap
from django.http import StreamingHttpResponse
from indigo.models.user import User
from triple_models.allegro_repository import (
    add_repository_statements,
    create_repository,
    delete_repository,
    delete_repository_statements,
    list_repositories,
    list_statements,
    query_repository
)
from models import Tree


class CassandraAuthentication(BasicAuthentication):
    www_authenticate_realm = 'Indigo'

    def authenticate_credentials(self, userid, password):
        """
        Authenticate the userid and password against username and password.
        """
        user = User.find(userid)
        if user is None or not user.is_active():
            raise exceptions.AuthenticationFailed(_('User inactive or deleted.'))
        if not user.authenticate(password) and not ldapAuthenticate(userid, password):
            raise exceptions.AuthenticationFailed(_('Invalid username/password.'))
        return (user, None)

def ldapAuthenticate(username, password):
    if settings.AUTH_LDAP_SERVER_URI is None:
        return False

    if settings.AUTH_LDAP_USER_DN_TEMPLATE is None:
        return False

    try:
        connection = ldap.initialize(settings.AUTH_LDAP_SERVER_URI)
        connection.protocol_version = ldap.VERSION3
        user_dn = settings.AUTH_LDAP_USER_DN_TEMPLATE % {"user": username}
        connection.simple_bind_s(user_dn, password)
        return True
    except ldap.INVALID_CREDENTIALS:
        return False
    except ldap.SERVER_DOWN:
        return False


class RDFRenderer(XMLRenderer):
    """
    Renderer which serializes RDF content to XML.
    """
    media_type = 'application/rdf+xml'

class SPARQLXMLRenderer(XMLRenderer):
    """
    Renderer which serializes SPARQL result content to XML.
    """
    media_type = 'application/sparql-results+xml'


class SPARQLJSONRenderer(JSONRenderer):
    """
    Renderer which serializes SPARQL result content to JSON.
    """
    media_type = 'application/sparql-results+json'


@api_view(['GET', 'PUT', 'POST', 'DELETE'])
@authentication_classes([CassandraAuthentication,])
@renderer_classes((JSONRenderer, RDFRenderer,))
def statements(request, repository):
    accept = request.accepted_media_type
    if request.method == "GET":
        return list_stats(repository, accept)
    elif request.method in ["PUT", "POST"]:
        return add_statements(request, repository, request.method == "PUT")
    elif request.method == "DELETE":
        return delete_statements(repository)
    return Response(status=HTTP_406_NOT_ACCEPTABLE)


@api_view(['GET'])
@authentication_classes([CassandraAuthentication,])
def ls_repositories(request):
    ok, ls_infos, status, msg = list_repositories()
    return JsonResponse(ls_infos, safe=False, status=status)


@api_view(['GET', 'PUT', 'POST', 'DELETE'])
@authentication_classes([CassandraAuthentication,])
@renderer_classes((JSONRenderer, RDFRenderer, SPARQLXMLRenderer, SPARQLJSONRenderer))
def repository(request, repository):
    accept = request.accepted_media_type
    if request.method == "GET":
        if "query" in request.query_params:
            if not accept in ["application/json",
                              "application/sparql-results+xml",
                              "application/sparql-results+json"]:
                accept = "application/json"
            return query(repository,
                         request.query_params.get("query", ""),
                         accept)
        else:
            if not accept in ["application/json", "application/rdf+xml"]:
                accept = "application/json"
            return list_stats(repository,
                              accept)
    elif request.method == "PUT":
        return create_repo(repository)
    elif request.method == "POST":
        if "query" in request.query_params:
            if not accept in ["application/json",
                              "application/sparql-results+xml",
                              "application/sparql-results+json"]:
                accept = "application/json"
            return query(repository,
                         request.query_params.get("query", ""),
                         accept, "POST")
        else:
            return create_repo(repository)
    elif request.method == "DELETE":
        return delete_repo(repository)
    return Response(status=HTTP_406_NOT_ACCEPTABLE)

def create_repo(name):
    ok, ls_infos, status, msg = create_repository(name)
    if ok:
        return Response(status=HTTP_201_CREATED)
    else:
        return Response(msg, status=status)


def delete_repo(name):
    ok, _, status, msg = delete_repository(name)
    if ok:
        return Response(status=HTTP_204_NO_CONTENT)
    else:
        return Response(msg, status=status)


def list_stats(name, accept="application/json"):
    ok, stats, status, msg = list_statements(name, accept)
    if ok:
        return StreamingHttpResponse(streaming_content=stats,
                                     status=status)
    else:
        return Response(msg, status=status)


def query(name, query, accept, method="GET"):
    ok, resp, status, msg = query_repository(name, query, accept, method)
    if ok:
        #return JsonResponse(resp, safe=False)
        return StreamingHttpResponse(streaming_content=resp,
                                     status=status)
    else:
        return Response(msg, status=status)


def add_statements(request, name, empty_first=True):
    if request.content_type == "multipart/form-data":
        ctype, pdict = cgi.parse_header(self.request.META.get('content-type', ''))
        f = cStringIO.StringIO(request.body)
        if ctype == 'multipart/form-data':
            parts_dict = cgi.parse_multipart(f, pdict)
            for name, value in parts_dict.items():
                ok, _, status, msg = add_repository_statements(name,
                                                               value[0],
                                                               "text/plain",
                                                               empty_first)
                if not ok:
                    return Response(msg, status=status)
            return Response(status=HTTP_201_CREATED)

    ok, _, status, msg = add_repository_statements(name,
                                                   request.body,
                                                   request.content_type,
                                                   empty_first)
    if ok:
        return Response(status=HTTP_201_CREATED)
    else:
        return Response(msg, status=status)


def delete_statements(name):
    ok, _, status, msg = delete_repository_statements(name)
    if ok:
        return Response(status=HTTP_204_NO_CONTENT)
    else:
        return Response(msg, status=status)


@api_view(['POST'])
@authentication_classes([CassandraAuthentication,])
def dependency(request, repository):
    """Generate the dependency graph for the given uri.
    
    Sample Content to pass in the body:
    {
       "resource_uri" : "https://dl.dropboxusercontent.com/u/27469926/dva_t.owl#processor_1",
       "description" : "deletion: 1 GHz Processor"
    }
    """
    content = request.data
    if not isinstance(content, dict):
        return Response(msg="No JSON object could be decoded",
                        status=HTTP_400_BAD_REQUEST)
    if "resource_uri" in content:
        resource_uri = content["resource_uri"]
    else:
        return Response("Missing 'ressource_uri' in parameters",
                        status=HTTP_400_BAD_REQUEST)
    if "description" in content:
        description = content["description"]
    else:
        return Response("Missing 'description' in parameters",
                        status=HTTP_400_BAD_REQUEST)
    
    tree = Tree(repository, resource_uri, description)
    return JsonResponse(tree.build_json(), safe=False)


@api_view(['GET'])
@authentication_classes([CassandraAuthentication,])
def ls_public_images(request, repository):
    """Return a list of the images that have 
    http://www.pericles-project.eu/ns/DEM-Scenario#releaseState as 
    public.
    """
    query_str ="""SELECT ?url_definition
WHERE {
    ?image rdf:type <http://www.pericles-project.eu/ns/DEM-Core#DigitalObject> .
    ?image <http://www.pericles-project.eu/ns/DEM-Scenario#releaseState> ?release .
    ?image <http://xrce.xerox.com/LRM#url> ?url_location .
    ?url_location rdf:type <http://xrce.xerox.com/LRM#Location> .
    ?url_location <http://xrce.xerox.com/LRM#definition> ?url_definition .
 FILTER (?release = "public")
}"""
    accept = request.accepted_media_type    
    if not accept in ["application/json",
                      "application/sparql-results+xml",
                      "application/sparql-results+json"]:
        accept = "application/json"
    return query(repository,
                 query_str,
                 accept)

