class OntologyBuilder:
    def __init__(self, filepath=None):
        self.TRAVEL = URIRef("http://example.org/travel/")
        self.graph = Graph()
        self.filepath = filepath

        if filepath and os.path.exists(filepath):
            self.graph.parse(filepath, format=guess_format(filepath))
        else:
            self._create_base_ontology()

    def _uri(self, name):
        return URIRef(self.TRAVEL + quote(name.replace(" ", "_")))

    def _create_base_ontology(self):
        self.graph.bind("travel", self.TRAVEL)
        self.graph.bind("owl", OWL)
        self.graph.bind("rdf", RDF)
        self.graph.bind("rdfs", RDFS)
        self.graph.bind("foaf", FOAF)
        self.graph.bind("xsd", XSD)

        classes = ["City", "Country", "Continent", "PlaceOfInterest"]
        for c in classes:
            class_uri = self._uri(c)
            self.graph.add((class_uri, RDF.type, OWL.Class))
            self.graph.add((class_uri, RDFS.label, Literal(c, lang="en")))

        props = [
            ("locatedIn", "City", "Country"),
            ("hasCapital", "Country", "City"),
            ("locatedInContinent", "Country", "Continent"),
            ("hasPlaceOfInterest", "City", "PlaceOfInterest"),
            ("category", "PlaceOfInterest", RDFS.Literal),
        ]
        for prop, domain, range_ in props:
            prop_uri = self._uri(prop)
            self.graph.add((prop_uri, RDF.type, RDF.Property))
            self.graph.add((prop_uri, RDFS.label, Literal(prop.replace("In", " in"), lang="en")))
            self.graph.add((prop_uri, RDFS.domain, self._uri(domain)))
            self.graph.add((prop_uri, RDFS.range, self._uri(range_) if isinstance(range_, str) else range_))

    def save(self, filepath=None):
        path = filepath or self.filepath
        if path:
            self.graph.serialize(path, format="turtle")
            print(f"Saved ontology to {path}")
        else:
            raise ValueError("No filepath specified.")

    def get_graph(self):
        return self.graph

    def get_uri(self, name):
        return self._uri(name)
