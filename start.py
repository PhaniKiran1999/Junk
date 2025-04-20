if __name__ == "__main__":
    city_ids = ["wd:Q1355", "wd:Q60", "wd:Q84", "wd:Q90", "wd:Q1490"]
    endpoint = "https://query.wikidata.org/sparql"
    file_path = "travel_guide_ontology.ttl"

    ontology = OntologyBuilder(file_path)
    graph = ontology.get_graph()
    processor = TravelDataProcessor(graph, ontology.get_uri)
    executor = SPARQLExecutor(endpoint)

    for cid in city_ids:
        processor.process_city(cid, executor)

    ontology.save(file_path)
    query_engine = TravelGuideQuery(file_path)
