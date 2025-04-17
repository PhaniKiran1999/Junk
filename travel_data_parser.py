import json
from SPARQLWrapper import SPARQLWrapper, JSON
from rdflib import Graph, Literal, URIRef
from rdflib.namespace import RDF, RDFS, FOAF, XSD
from urllib.parse import quote

# Define a namespace for your travel guide ontology
TRAVEL = URIRef("http://example.org/travel/")

def execute_sparql_query(endpoint_url, query):
    """Executes a SPARQL query against the given endpoint and returns the results in JSON format."""
    sparql = SPARQLWrapper(endpoint_url)
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    try:
        results = sparql.query().convert()
        return results
    except Exception as e:
        print(f"Error executing SPARQL query: {e}")
        return None

def create_uri(name):
    """Creates a properly encoded URI from a name."""
    return URIRef(TRAVEL + quote(name.replace(" ", "_")))

def parse_city_info(results, graph):
    """Parses the results of Query 1 and adds triples to the RDF graph."""
    if results and "results" in results and "bindings" in results["results"]:
        for binding in results["results"]["bindings"]:
            city_name = binding.get("cityName", {}).get("value")
            country_name = binding.get("countryName", {}).get("value")
            capital_name = binding.get("capitalName", {}).get("value")
            continent_name = binding.get("continentName", {}).get("value")

            if city_name:
                city_uri = create_uri(city_name)
                graph.add((city_uri, RDF.type, create_uri("City")))
                graph.add((city_uri, RDFS.label, Literal(city_name, lang="en")))

                if country_name:
                    country_uri = create_uri(country_name)
                    graph.add((city_uri, create_uri("locatedIn"), country_uri))
                    if (country_uri, RDF.type, create_uri("Country")) not in graph:
                        graph.add((country_uri, RDF.type, create_uri("Country")))
                        graph.add((country_uri, RDFS.label, Literal(country_name, lang="en")))

                        if capital_name:
                            capital_uri = create_uri(capital_name)
                            graph.add((country_uri, create_uri("hasCapital"), capital_uri))
                            if (capital_uri, RDF.type, create_uri("City")) not in graph:
                                graph.add((capital_uri, RDF.type, create_uri("City")))
                                graph.add((capital_uri, RDFS.label, Literal(capital_name, lang="en")))

                        if continent_name:
                            continent_uri = create_uri(continent_name)
                            graph.add((country_uri, create_uri("locatedInContinent"), continent_uri))
                            if (continent_uri, RDF.type, create_uri("Continent")) not in graph:
                                graph.add((continent_uri, RDF.type, create_uri("Continent")))
                                graph.add((continent_uri, RDFS.label, Literal(continent_name, lang="en")))
    return graph

def parse_poi_info(results, graph):
    """Parses the results of Query 2 and adds triples to the RDF graph."""
    if results and "results" in results and "bindings" in results["results"]:
        for binding in results["results"]["bindings"]:
            city_name = binding.get("cityName", {}).get("value")
            poi_name = binding.get("poiName", {}).get("value")
            poi_description = binding.get("poiDescription", {}).get("value")
            poi_type = binding.get("instanceOfLabel", {}).get("value")

            if city_name and poi_name:
                city_uri = create_uri(city_name)
                poi_uri = create_uri(poi_name)
                graph.add((city_uri, create_uri("hasPlaceOfInterest"), poi_uri))
                graph.add((poi_uri, RDF.type, create_uri("PlaceOfInterest")))
                graph.add((poi_uri, RDFS.label, Literal(poi_name, lang="en")))
                graph.add((poi_uri, create_uri("locatedIn"), city_uri))

                if poi_description:
                    graph.add((poi_uri, RDFS.comment, Literal(poi_description, lang="en")))
                if poi_type:
                    graph.add((poi_uri, create_uri("category"), Literal(poi_type, lang="en")))
    return graph

def create_ontology():
    """Creates an initial RDF graph with the basic ontology terms."""
    graph = Graph()
    graph.bind("rdf", RDF)
    graph.bind("rdfs", RDFS)
    graph.bind("foaf", FOAF)
    graph.bind("xsd", XSD)
    graph.bind("travel", TRAVEL)

    # Define classes
    city_class = create_uri("City")
    country_class = create_uri("Country")
    continent_class = create_uri("Continent")
    place_of_interest_class = create_uri("PlaceOfInterest")

    graph.add((city_class, RDF.type, RDFS.Class))
    graph.add((city_class, RDFS.label, Literal("City", lang="en")))
    graph.add((country_class, RDF.type, RDFS.Class))
    graph.add((country_class, RDFS.label, Literal("Country", lang="en")))
    graph.add((continent_class, RDF.type, RDFS.Class))
    graph.add((continent_class, RDFS.label, Literal("Continent", lang="en")))
    graph.add((place_of_interest_class, RDF.type, RDFS.Class))
    graph.add((place_of_interest_class, RDFS.label, Literal("Place of Interest", lang="en")))

    # Define properties
    located_in_prop = create_uri("locatedIn")
    has_capital_prop = create_uri("hasCapital")
    located_in_continent_prop = create_uri("locatedInContinent")
    has_place_of_interest_prop = create_uri("hasPlaceOfInterest")
    category_prop = create_uri("category")

    graph.add((located_in_prop, RDF.type, RDF.Property))
    graph.add((located_in_prop, RDFS.label, Literal("located in", lang="en")))
    graph.add((located_in_prop, RDFS.domain, city_class))
    graph.add((located_in_prop, RDFS.range, country_class))

    graph.add((has_capital_prop, RDF.type, RDF.Property))
    graph.add((has_capital_prop, RDFS.label, Literal("has capital", lang="en")))
    graph.add((has_capital_prop, RDFS.domain, country_class))
    graph.add((has_capital_prop, RDFS.range, city_class))

    graph.add((located_in_continent_prop, RDF.type, RDF.Property))
    graph.add((located_in_continent_prop, RDFS.label, Literal("located in continent", lang="en")))
    graph.add((located_in_continent_prop, RDFS.domain, country_class))
    graph.add((located_in_continent_prop, RDFS.range, continent_class))

    graph.add((has_place_of_interest_prop, RDF.type, RDF.Property))
    graph.add((has_place_of_interest_prop, RDFS.label, Literal("has place of interest", lang="en")))
    graph.add((has_place_of_interest_prop, RDFS.domain, city_class))
    graph.add((has_place_of_interest_prop, RDFS.range, place_of_interest_class))

    graph.add((category_prop, RDF.type, RDF.Property))
    graph.add((category_prop, RDFS.label, Literal("category", lang="en")))
    graph.add((category_prop, RDFS.domain, place_of_interest_class))
    graph.add((category_prop, RDFS.range, RDFS.Literal))

    return graph

# if __name__ == "__main__":
#     wikidata_endpoint = "https://query.wikidata.org/sparql"
#     city_id = "wd:Q90"  # Example: Bengaluru's Wikidata ID

#     # Create the initial ontology graph
#     travel_graph = create_ontology()

#     # --- Execute and parse Query 1 ---
#     print("Executing city information query...")
#     query1 = f"""
#     SELECT ?cityName ?countryName ?capitalName ?continentName
#     WHERE {{
#       BIND({city_id} AS ?city)
#       ?city rdfs:label ?cityName .
#       ?city wdt:P17 ?country .
#       ?country rdfs:label ?countryName .
#       OPTIONAL {{ ?country wdt:P36 ?capital .
#                  ?capital rdfs:label ?capitalName .
#                  FILTER (LANG(?capitalName) = "en") }}
#       ?country wdt:P30 ?continent .
#       ?continent rdfs:label ?continentName .
#       FILTER (LANG(?cityName) = "en")
#       FILTER (LANG(?countryName) = "en")
#       FILTER (LANG(?continentName) = "en")
#     }}
#     LIMIT 1
#     """
#     results1 = execute_sparql_query(wikidata_endpoint, query1)
#     if not results1:
#         print("Failed to execute city information query")
#         exit(1)
    
#     travel_graph = parse_city_info(results1, travel_graph)

#     # --- Execute and parse Query 2 ---
#     print("Executing points of interest query...")
#     query2 = f"""
#     SELECT DISTINCT ?cityName ?poiName ?poiDescription ?instanceOfLabel
#     WHERE {{
#       BIND({city_id} AS ?city)
#       ?city rdfs:label ?cityName .
#       ?poi wdt:P131* ?city .  # Located in or part of
#       ?poi wdt:P31 ?instanceOf .
#       ?instanceOf rdfs:label ?instanceOfLabel .
#       FILTER (LANG(?instanceOfLabel) = "en" &&
#               (CONTAINS(LCASE(?instanceOfLabel), "landmark") ||
#                CONTAINS(LCASE(?instanceOfLabel), "museum") ||
#                CONTAINS(LCASE(?instanceOfLabel), "palace") ||
#                CONTAINS(LCASE(?instanceOfLabel), "temple") ||
#                CONTAINS(LCASE(?instanceOfLabel), "histor") ||
#                CONTAINS(LCASE(?instanceOfLabel), "memorial") ||
#                CONTAINS(LCASE(?instanceOfLabel), "park") ||
#                CONTAINS(LCASE(?instanceOfLabel), "garden") ||
#                CONTAINS(LCASE(?instanceOfLabel), "monument")))
#       ?poi rdfs:label ?poiName .
#       OPTIONAL {{ ?poi schema:description ?poiDescription . FILTER (LANG(?poiDescription) = "en") }}
#       FILTER (LANG(?cityName) = "en")
#       FILTER (LANG(?poiName) = "en")
#     }}
#     """
#     results2 = execute_sparql_query(wikidata_endpoint, query2)
#     if not results2:
#         print("Failed to execute points of interest query")
#         exit(1)
    
#     travel_graph = parse_poi_info(results2, travel_graph)

#     # Serialize the graph
#     ontology_file = "travel_guide_ontology.owl"
#     travel_graph.serialize(ontology_file, format="xml")
#     print(f"Knowledge graph data saved to {ontology_file}")

    

import os
from rdflib.util import guess_format

# ... [keep all your existing functions] ...

def load_existing_graph(filepath):
    """Loads an existing RDF graph from file if it exists, otherwise creates a new one."""
    graph = Graph()
    if os.path.exists(filepath):
        file_format = guess_format(filepath)
        graph.parse(filepath, format=file_format)
    else:
        graph = create_ontology()
    return graph

def process_city(city_id, travel_graph, wikidata_endpoint):
    """Processes a single city and adds its data to the graph."""
    # --- Execute and parse Query 1 ---
    print(f"Processing city {city_id}...")
    query1 = f"""
    SELECT ?cityName ?countryName ?capitalName ?continentName
    WHERE {{
      BIND({city_id} AS ?city)
      ?city rdfs:label ?cityName .
      ?city wdt:P17 ?country .
      ?country rdfs:label ?countryName .
      OPTIONAL {{ ?country wdt:P36 ?capital .
                 ?capital rdfs:label ?capitalName .
                 FILTER (LANG(?capitalName) = "en") }}
      ?country wdt:P30 ?continent .
      ?continent rdfs:label ?continentName .
      FILTER (LANG(?cityName) = "en")
      FILTER (LANG(?countryName) = "en")
      FILTER (LANG(?continentName) = "en")
    }}
    LIMIT 1
    """
    results1 = execute_sparql_query(wikidata_endpoint, query1)
    if not results1:
        print(f"Failed to execute city information query for {city_id}")
        return travel_graph
    
    travel_graph = parse_city_info(results1, travel_graph)

    # --- Execute and parse Query 2 ---
    query2 = f"""
    SELECT DISTINCT ?cityName ?poiName ?poiDescription ?instanceOfLabel
    WHERE {{
      BIND({city_id} AS ?city)
      ?city rdfs:label ?cityName .
      ?poi wdt:P131* ?city .
      ?poi wdt:P31 ?instanceOf .
      ?instanceOf rdfs:label ?instanceOfLabel .
      FILTER (LANG(?instanceOfLabel) = "en" &&
              (CONTAINS(LCASE(?instanceOfLabel), "landmark") ||
               CONTAINS(LCASE(?instanceOfLabel), "museum") ||
               CONTAINS(LCASE(?instanceOfLabel), "palace") ||
               CONTAINS(LCASE(?instanceOfLabel), "temple") ||
               CONTAINS(LCASE(?instanceOfLabel), "histor") ||
               CONTAINS(LCASE(?instanceOfLabel), "memorial") ||
               CONTAINS(LCASE(?instanceOfLabel), "park") ||
               CONTAINS(LCASE(?instanceOfLabel), "garden") ||
               CONTAINS(LCASE(?instanceOfLabel), "monument")))
      ?poi rdfs:label ?poiName .
      OPTIONAL {{ ?poi schema:description ?poiDescription . FILTER (LANG(?poiDescription) = "en") }}
      FILTER (LANG(?cityName) = "en")
      FILTER (LANG(?poiName) = "en")
    }}
    LIMIT 50
    """
    results2 = execute_sparql_query(wikidata_endpoint, query2)
    if results2:
        travel_graph = parse_poi_info(results2, travel_graph)
    
    return travel_graph

if __name__ == "__main__":
    wikidata_endpoint = "https://query.wikidata.org/sparql"
    ontology_file = "travel_guide_ontology.ttl"
    
    # List of city Wikidata IDs to process
    city_ids = [
        "wd:Q1355",  # Bengaluru
        "wd:Q60",    # New York City
        "wd:Q84",    # London
        "wd:Q90",    # Paris
        "wd:Q1490"    # Tokyo
    ]
    
    # Load existing graph or create new one
    travel_graph = load_existing_graph(ontology_file)
    
    # Process each city
    for city_id in city_ids:
        travel_graph = process_city(city_id, travel_graph, wikidata_endpoint)
    
    # Save the updated graph
    travel_graph.serialize(ontology_file, format="turtle")
    print(f"Knowledge graph data saved to {ontology_file}")