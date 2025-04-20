class TravelDataProcessor:
    def __init__(self, graph, uri_func):
        self.graph = graph
        self.uri = uri_func

    def parse_city_info(self, results):
        for binding in results.get("results", {}).get("bindings", []):
            city_name = binding.get("cityName", {}).get("value")
            country_name = binding.get("countryName", {}).get("value")
            capital_name = binding.get("capitalName", {}).get("value")
            continent_name = binding.get("continentName", {}).get("value")

            if city_name:
                city_uri = self.uri(city_name)
                self.graph.add((city_uri, RDF.type, self.uri("City")))
                self.graph.add((city_uri, RDFS.label, Literal(city_name, lang="en")))

                if country_name:
                    country_uri = self.uri(country_name)
                    self.graph.add((city_uri, self.uri("locatedIn"), country_uri))
                    self.graph.add((country_uri, RDF.type, self.uri("Country")))
                    self.graph.add((country_uri, RDFS.label, Literal(country_name, lang="en")))

                    if capital_name:
                        capital_uri = self.uri(capital_name)
                        self.graph.add((country_uri, self.uri("hasCapital"), capital_uri))
                        self.graph.add((capital_uri, RDF.type, self.uri("City")))
                        self.graph.add((capital_uri, RDFS.label, Literal(capital_name, lang="en")))

                    if continent_name:
                        continent_uri = self.uri(continent_name)
                        self.graph.add((country_uri, self.uri("locatedInContinent"), continent_uri))
                        self.graph.add((continent_uri, RDF.type, self.uri("Continent")))
                        self.graph.add((continent_uri, RDFS.label, Literal(continent_name, lang="en")))

    def parse_poi_info(self, results):
        for binding in results.get("results", {}).get("bindings", []):
            city_name = binding.get("cityName", {}).get("value")
            poi_name = binding.get("poiName", {}).get("value")
            poi_description = binding.get("poiDescription", {}).get("value")
            poi_type = binding.get("instanceOfLabel", {}).get("value")

            if city_name and poi_name:
                city_uri = self.uri(city_name)
                poi_uri = self.uri(poi_name)

                self.graph.add((poi_uri, RDF.type, self.uri("PlaceOfInterest")))
                self.graph.add((poi_uri, RDFS.label, Literal(poi_name, lang="en")))
                self.graph.add((city_uri, self.uri("hasPlaceOfInterest"), poi_uri))
                self.graph.add((poi_uri, self.uri("locatedIn"), city_uri))

                if poi_description:
                    self.graph.add((poi_uri, RDFS.comment, Literal(poi_description, lang="en")))
                if poi_type:
                    self.graph.add((poi_uri, self.uri("category"), Literal(poi_type, lang="en")))

    def process_city(self, city_id, executor):
        print(f"Processing city {city_id}...")

        query1 = f"""SELECT ?cityName ?countryName ?capitalName ?continentName
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
        LIMIT 1"""
        results1 = executor.run_query(query1)
        if results1:
            self.parse_city_info(results1)

        query2 = f"""SELECT DISTINCT ?cityName ?poiName ?poiDescription ?instanceOfLabel
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
        LIMIT 50"""
        results2 = executor.run_query(query2)
        if results2:
            self.parse_poi_info(results2)
