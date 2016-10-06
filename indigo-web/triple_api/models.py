from django.db import models

import re
import json

from triple_models.allegro_repository import (
    query_repository
)



def getLabelOfInstanceFromRepository(repository, instance):
    query = "SELECT DISTINCT ?label WHERE { <" + instance + "> rdfs:label ?label .}"
    ok, resp, status, msg = query_repository(repository, query)
    if ok:
        result = resp['values']
        if len(result) != 0:
            return re.sub("\"", "", result[0][0]) # removes quote symbol (") from result

    return False


def getAssociatedDependencyURIsOfResource(resource):
    # TODO: prefix changed to uri
    query = "SELECT ?dependency WHERE " \
            "{ " \
                "{ " \
                "?dependency <http://xrce.xerox.com/LRM#from> <" + resource.uri + "> ." \
                "} " \
            "UNION " \
                "{ " \
                "?dependency <http://xrce.xerox.com/LRM#to> <" + resource.uri + "> ." \
                "} " \
            "}"
    dependencies = []
    ok, resp, status, msg = query_repository(resource.repository, query)
    if ok:
        for result in resp['values']:
            dependencies.append(re.sub("[<>]", "", result[0])) # removes < > symbols from result
        return dependencies

    return dependencies


def getToResourceURIsOfDependency(dependency):

    # TODO: prefix changed to uri
    query = "SELECT ?resource WHERE " \
            "{ " \
                "<" + dependency.uri + "> <http://xrce.xerox.com/LRM#to> ?resource ." \
            "}"
    resource_uris = []
    ok, resp, status, msg = query_repository(dependency.repository, query)
    if ok:
        for result in resp['values']:
            resource_uris.append(re.sub("[<>]", "", result[0])) # removes < > symbols from result
        return resource_uris

    return resource_uris


def getFromResourceURIsOfDependency(dependency):

    # TODO: prefix changed to uri
    query = "SELECT ?resource WHERE " \
            "{ " \
                "<" + dependency.uri + "> <http://xrce.xerox.com/LRM#from> ?resource ." \
            "}"
    resource_uris = []
    ok, resp, status, msg = query_repository(dependency.repository, query)
    if ok:
        for result in resp['values']:
            resource_uris.append(re.sub("[<>]", "", result[0])) # removes < > symbols from result
        return resource_uris

    return resource_uris


def getConjunctiveOrDisjunctiveTypeOfDependency(dependency):

    # TODO: prefix changed to uri
    query = "SELECT DISTINCT ?dependency_type WHERE" \
            "{ " \
                "<" + dependency.uri + "> rdf:type ?dependency_type . " \
                "FILTER(" \
                    "?dependency_type = <http://xrce.xerox.com/LRM#ConjunctiveDependency> || " \
                    "?dependency_type = <http://xrce.xerox.com/LRM#DisjunctiveDependency>" \
                ") " \
            "}"
    resource_uris = []
    ok, resp, status, msg = query_repository(dependency.repository, query)
    if ok:
        result = resp['values']
        dependency_type = re.sub("[<>]", "", result[0][0]) # removes < > symbols from result
        if dependency_type == 'http://xrce.xerox.com/LRM#DisjunctiveDependency':
            return 'Disjunctive'
        else:
            return 'Conjunctive'

    return None


def getIntentionOfDependency(dependency):
    intention_value = ''

    # TODO: change prefix to URI
    query = "SELECT ?intention_value WHERE" \
            "{ " \
                "<" + dependency.uri + "> <http://xrce.xerox.com/LRM#intention> ?intention . " \
                "?intention rdfs:label ?intention_value " \
            "}"
    resource_uris = []
    ok, resp, status, msg = query_repository(dependency.repository, query)
    if ok:
        result = resp['values']
        intention_value = re.sub("\"", "", re.sub("\^\^<.*?>", '', result[0][0])) # removes unwanted content from a result like e.g. "Functional"^^<http://www.w3.org/2001/XMLSchema#string>

    return intention_value


def getPredicateBetweenResourceAndDependency(resource, dependency):
    predicate = 'to'

    query = "SELECT ?predicate WHERE" \
            "{ " \
                "<" + dependency.uri + "> ?predicate <" + resource.uri + "> . " \
            "}"

    resource_uris = []
    ok, resp, status, msg = query_repository(resource.repository, query)
    if ok:
        result = resp['values']

        retrieved_predicate = re.sub('[<>]', '', result[0][0]) # removes < > symbols from result
    
        if retrieved_predicate == 'http://xrce.xerox.com/LRM#from':
            predicate = 'from'
    
    return predicate


class Dependency:
    def __init__(self, uri, tree, parent_resource):
        self.repository = tree.repository
        self.uri = uri
        self.tree = tree
        self.parent_resource = parent_resource

        self.tree.dependency_nodes_uris.append(self.uri)

        self.from_resource_uris = []
        self.to_resource_uris = []
        self.children_resource_nodes = []

        # Label
        self.label = getLabelOfInstanceFromRepository(self.repository, self.uri)
        if self.label == False:
            self.label = ''

        # Intention
        self.intention = getIntentionOfDependency(self)

        # Conjunctive or disjunctive
        self.type = getConjunctiveOrDisjunctiveTypeOfDependency(self)

        # Find to resources
        self.findToResources()

        # # Find from resources
        self.findFromResources()

    def findToResources(self):
        resource_uris = getToResourceURIsOfDependency(self)

        for uri in resource_uris:
            self.to_resource_uris.append(uri)

            if uri not in self.tree.resource_nodes_uris:

                new_resource = Resource(uri, self.tree, self)

                self.children_resource_nodes.append(new_resource)
                self.tree.resource_nodes.append(new_resource)

    def findFromResources(self):
        resource_uris = getFromResourceURIsOfDependency(self)

        for uri in resource_uris:
            self.from_resource_uris.append(uri)

            if uri not in self.tree.resource_nodes_uris:

                new_resource = Resource(uri, self.tree, self)

                self.children_resource_nodes.append(new_resource)
                self.tree.resource_nodes.append(new_resource)

    def createDictionaryOfDependency(self):
        d = {}
        d['name'] = self.label
        d['type'] = 'Dependency'
        d['dependencyType'] = self.type
        d['intention'] = self.intention

        d['link'] = {'label': getPredicateBetweenResourceAndDependency(self.parent_resource, self), 'direction': 'parent'}

        children_list_of_dicts = []

        for child_resource in self.children_resource_nodes:
            children_list_of_dicts.append(child_resource.createDictionaryOfResource())

        if children_list_of_dicts != []:
            d['children'] = children_list_of_dicts

        return d


class Resource:
    def __init__(self, uri, tree, parent_dependency):
        self.uri = uri
        self.repository = tree.repository
        self.tree = tree
        self.parent_dependency = parent_dependency

        self.tree.resource_nodes_uris.append(self.uri)

        # Search for label
        self.label = getLabelOfInstanceFromRepository(self.repository, self.uri)

        # If label not found, set empty label string
        if self.label == False:
            self.label = ''

        # # Find associated dependencies
        self.associated_dependency_uris = []
        self.children_dependency_nodes = []
        self.findAssociatedDependencies()

    def findAssociatedDependencies(self):

        # Search for associated dependencies
        associated_dependency_uris = getAssociatedDependencyURIsOfResource(self)

        for dependency_uri in associated_dependency_uris:
            self.associated_dependency_uris.append(dependency_uri)

            if dependency_uri not in self.tree.dependency_nodes_uris:

                # Create a dependency
                new_dependency = Dependency(dependency_uri, self.tree, self)

                # Append to lists
                self.children_dependency_nodes.append(new_dependency)
                self.tree.dependency_nodes.append(new_dependency)

    def createDictionaryOfResource(self):
        d = {}
        d['name'] = self.label
        d['type'] = 'Resource'

        if self.parent_dependency != None:
            to_or_from_predicate = getPredicateBetweenResourceAndDependency(self, self.parent_dependency)
            d['link'] = {'label': to_or_from_predicate, 'direction': 'self'}

        # if self.parent_dependency == None:
        #     d['impacted'] = True
        #     d['change'] = self.tree.change_description
        # elif self.parent_dependency.type == 'Conjunctive' and to_or_from_predicate == 'to':
        #     d['impacted'] = True
        # else:
        #     d['impacted'] = False


        children_list_of_dicts = []

        for child_dependency in self.children_dependency_nodes:
            children_list_of_dicts.append(child_dependency.createDictionaryOfDependency())

        if children_list_of_dicts != []:
            d['children'] = children_list_of_dicts

        return d


class Tree():
    def __init__(self, repository , changed_resource_uri, change_description):

        self.change_description = change_description
        self.repository = repository
        self.resource_nodes = []
        self.dependency_nodes = []
        self.resource_nodes_uris = []
        self.dependency_nodes_uris = []

        # Create an instance of Processor
        self.changed_resource = Resource(changed_resource_uri, self, None)

        self.resource_nodes.append(self.changed_resource)

        # print 'Number of dependencies created', len(self.dependency_nodes_uris)
        # for uri in self.dependency_nodes_uris:
        #     print uri
        #
        # print 'Number of resources created', len(self.resource_nodes)
        # for uri in self.resource_nodes_uris:
        #     print uri


    def build_json(self):
        return self.changed_resource.createDictionaryOfResource()
