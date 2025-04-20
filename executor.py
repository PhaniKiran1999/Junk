class SPARQLExecutor:
    def __init__(self, endpoint_url):
        self.endpoint_url = endpoint_url

    def run_query(self, query):
        sparql = SPARQLWrapper(self.endpoint_url)
        sparql.setQuery(query)
        sparql.setReturnFormat(JSON)
        try:
            return sparql.query().convert()
        except Exception as e:
            print(f"[SPARQL Error] {e}")
            return None
