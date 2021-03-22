# -*- coding: utf8 -*-
# Filename: metahead.py
#
########################################################################
# This is a program to help in removing errors in
# the metahead.ttl file that mostly contains information
# about persons, organisations, places and publications.
#
# Currently missing acdh:hasTitle for resources of type acdh:Person
# are created.
#
# Filename has to be 'metahead.ttl'.
# Location must be at same place as this script.
#
########################################################################

from rdflib import Graph, URIRef, Literal
from rdflib.namespace import RDF

# parse the metahead.ttl
graph = Graph()
graph.parse('metahead.ttl', format='turtle')

# iterate trough all resources of type acdh:Person
for resource in graph[: RDF.type : URIRef('https://vocabs.acdh.oeaw.ac.at/schema#Person')]:
  # if there is not acdh:hasTitle but there is at least acdh:hasLastName, generate acdh:hasTitle
  if len(list(graph[resource : URIRef('https://vocabs.acdh.oeaw.ac.at/schema#hasTitle') : ])) == 0 and len(list(graph[resource : URIRef('https://vocabs.acdh.oeaw.ac.at/schema#hasLastName') : ])) > 0:
    # collect first names and last names by languages
    firstNames = {}
    for firstName in graph[resource : URIRef('https://vocabs.acdh.oeaw.ac.at/schema#hasFirstName') : ]:
      language = firstName.language if firstName.language is not None else 'en'
      if language not in firstNames:
        firstNames[language] = []
      firstNames[language].append(firstName.value)
    lastNames = {}
    for lastName in graph[resource : URIRef('https://vocabs.acdh.oeaw.ac.at/schema#hasLastName') : ]:
      language = lastName.language if lastName.language is not None else 'en'
      if language not in lastNames:
        lastNames[language] = []
      lastNames[language].append(lastName.value)
    # generate titles where there is a last name and only one last name in a given language exists
    for language, names in lastNames.items():
      if len(names) == 1 and (language not in firstNames or len(firstNames[language]) == 1):
        title = (firstNames[language][0] + ' ' if language in firstNames else '') + names[0]
        graph.add([resource, URIRef('https://vocabs.acdh.oeaw.ac.at/schema#hasTitle'), Literal(title, lang=language)])
      else:
        print('more than one acdh:hasLastName and/or acdh:hasFirstName in language %s for %s' % (language, resource.identifier))

# write the output
with open('metahead.ttl.out', 'w', encoding='utf-8') as f:
  output = graph.serialize(format='turtle')
  f.write(output.decode('utf-8'))
