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

from rdflib import Graph, URIRef
from rdflib.namespace import RDF, RDFS
from rdflib.plugins.sparql import prepareQuery

class TravelGuideQuery:
    def __init__(self, ontology_file="travel_guide_ontology.owl"):
        """
        Initialize the query engine with the ontology file.
        
        Args:
            ontology_file (str): Path to the OWL ontology file
        """
        self.graph = Graph()
        self.graph.parse(ontology_file, format="xml")
        self.TRAVEL = URIRef("http://example.org/travel/")
        
    def _prepare_travel_uri(self, name):
        """Helper method to create URIs in the travel namespace"""
        return URIRef(self.TRAVEL + name.replace(" ", "_"))
    
    def get_all_cities(self):
        """
        Get all cities in the ontology.
        
        Returns:
            list: List of dictionaries with city info
        """
        query = """
        SELECT ?city ?name
        WHERE {
            ?city a travel:City .
            ?city rdfs:label ?name .
        }
        """
        q = prepareQuery(query, initNs={"travel": self.TRAVEL, "rdfs": RDFS})
        
        results = []
        for row in self.graph.query(q):
            results.append({
                "uri": str(row.city),
                "name": str(row.name)
            })
        return results
    
    def get_city_details(self, city_name):
        """
        Get detailed information about a specific city.
        
        Args:
            city_name (str): Name of the city to query
            
        Returns:
            dict: City details including country, capital, continent
        """
        city_uri = self._prepare_travel_uri(city_name)
        
        query = """
        SELECT ?name ?country ?countryName ?capital ?capitalName ?continent ?continentName
        WHERE {
            BIND(?city_uri AS ?city)
            ?city a travel:City ;
                  rdfs:label ?name .
            OPTIONAL {
                ?city travel:locatedIn ?country .
                ?country rdfs:label ?countryName .
                
                OPTIONAL {
                    ?country travel:hasCapital ?capital .
                    ?capital rdfs:label ?capitalName .
                }
                
                OPTIONAL {
                    ?country travel:locatedInContinent ?continent .
                    ?continent rdfs:label ?continentName .
                }
            }
        }
        """
        q = prepareQuery(query, initNs={"travel": self.TRAVEL, "rdfs": RDFS})
        
        result = {}
        for row in self.graph.query(q, initBindings={'city_uri': city_uri}):
            result = {
                "name": str(row.name),
                "country": {
                    "uri": str(row.country),
                    "name": str(row.countryName)
                } if row.country else None,
                "capital": {
                    "uri": str(row.capital),
                    "name": str(row.capitalName)
                } if row.capital else None,
                "continent": {
                    "uri": str(row.continent),
                    "name": str(row.continentName)
                } if row.continent else None
            }
        return result
    
    def get_pois_for_city(self, city_name):
        """
        Get all points of interest for a city.
        
        Args:
            city_name (str): Name of the city
            
        Returns:
            list: List of POI dictionaries with name, description, and category
        """
        city_uri = self._prepare_travel_uri(city_name)
        
        query = """
        SELECT ?poi ?name ?description ?category
        WHERE {
            BIND(?city_uri AS ?city)
            ?city travel:hasPlaceOfInterest ?poi .
            ?poi rdfs:label ?name .
            OPTIONAL { ?poi rdfs:comment ?description }
            OPTIONAL { ?poi travel:category ?category }
        }
        """
        q = prepareQuery(query, initNs={"travel": self.TRAVEL, "rdfs": RDFS})
        
        results = []
        for row in self.graph.query(q, initBindings={'city_uri': city_uri}):
            results.append({
                "uri": str(row.poi),
                "name": str(row.name),
                "description": str(row.description) if row.description else None,
                "category": str(row.category) if row.category else None
            })
        return results
    
    def get_cities_in_country(self, country_name):
        """
        Get all cities located in a specific country.
        
        Args:
            country_name (str): Name of the country
            
        Returns:
            list: List of city names
        """
        country_uri = self._prepare_travel_uri(country_name)
        
        query = """
        SELECT ?city ?name
        WHERE {
            BIND(?country_uri AS ?country)
            ?city travel:locatedIn ?country .
            ?city rdfs:label ?name .
        }
        """
        q = prepareQuery(query, initNs={"travel": self.TRAVEL, "rdfs": RDFS})
        
        return [str(row.name) for row in self.graph.query(q, initBindings={'country_uri': country_uri})]
    

    def search_pois_by_category(self, category_keyword):
        """
        Search points of interest by category keyword.
        
        Args:
            category_keyword (str): Keyword to search in POI categories
            
        Returns:
            list: List of POIs matching the category
        """
        query = """
        # SELECT ?poi ?name ?description ?category ?city ?cityName
        SELECT ?name
        WHERE {
            ?poi a travel:PlaceOfInterest ;
                rdfs:label ?name ;
                travel:locatedIn ?city .
            ?city rdfs:label ?cityName .
            OPTIONAL { ?poi rdfs:comment ?description }
            OPTIONAL { ?poi travel:category ?category }
            FILTER(CONTAINS(LCASE(COALESCE(?category, "")), ?keyword))
        }
        """
        try:
            q = prepareQuery(query, initNs={"travel": self.TRAVEL, "rdfs": RDFS})
            results = []
            for row in self.graph.query(q, initBindings={'keyword': Literal(category_keyword.lower())}):
                results.append({
                    # "poi": str(row.poi),
                    "name": str(row.name),
                    # "description": str(row.description) if row.description else None,
                    # "category": str(row.category) if row.category else None,
                    # "city": str(row.cityName)
                })
            return results
        except Exception as e:
            print(f"Error executing query: {e}")
            return []


if __name__ == "__main__":
    # wikidata_endpoint = "https://query.wikidata.org/sparql"
    # ontology_file = "travel_guide_ontology.ttl"
    
    # # List of city Wikidata IDs to process
    # city_ids = [
    #     "wd:Q1355",  # Bengaluru
    #     "wd:Q60",    # New York City
    #     "wd:Q84",    # London
    #     "wd:Q90",    # Paris
    #     "wd:Q1490"    # Tokyo
    # ]
    
    # # Load existing graph or create new one
    # travel_graph = load_existing_graph(ontology_file)
    
    # # Process each city
    # for city_id in city_ids:
    #     travel_graph = process_city(city_id, travel_graph, wikidata_endpoint)
    
    # # Save the updated graph
    # travel_graph.serialize(ontology_file, format="turtle")
    # print(f"Knowledge graph data saved to {ontology_file}")

    # Initialize the query engine
    query_engine = TravelGuideQuery("travel_guide_ontology.owl")

    # # Get all cities
    # all_cities = query_engine.get_all_cities()
    # print("All cities:", all_cities)

    # # Get details for a specific city
    # city_details = query_engine.get_city_details("Bengaluru")
    # print("\nBengaluru details:", city_details)

    # # Get points of interest for a city
    # pois = query_engine.get_pois_for_city("Bengaluru")
    # print("\nPoints of interest in Bengaluru:", pois)

    # # Get cities in a country
    # cities_in_country = query_engine.get_cities_in_country("India")
    # print("\nCities in India:", cities_in_country)

    # Search POIs by category
    museum_pois = query_engine.search_pois_by_category("museum")
    print("\nMuseum POIs:", museum_pois)

    temples_pois = query_engine.search_pois_by_category("park")
    print("\nTemple POIs:", temples_pois)
