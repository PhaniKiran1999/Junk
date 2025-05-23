# Import necessary libraries
from pyshacl import validate
from rdflib import Graph, Literal, URIRef
from rdflib.namespace import RDF, XSD

# --- 1. Define Sample Data Graph (RDF) ---
# This data will be validated against the SHACL shapes.
# We'll include examples that conform and examples that violate the constraint.
data_graph_ttl = """
@prefix ex: <http://example.com/data#> .
@prefix foaf: <http://xmlns.com/foaf/0.1/> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

# Conforming data: John Doe
ex:johnDoe a foaf:Person ;
    foaf:firstName "John" ;
    foaf:lastName "Doe" ;
    ex:age 30 .

# Conforming data: Jane Smith
ex:janeSmith a foaf:Person ;
    foaf:firstName "Jane" ;
    foaf:lastName "Smith" ;
    ex:age 25 .

# Violating data: Alice Alice (first and last names are identical)
ex:aliceAlice a foaf:Person ;
    foaf:firstName "Alice" ;
    foaf:lastName "Alice" ;
    ex:age 28 .

# Violating data: Bob Bob (first and last names are identical)
ex:bobBob a foaf:Person ;
    foaf:firstName "Bob" ;
    foaf:lastName "Bob" ;
    ex:age 45 .

# Data that doesn't have both first and last name, so it won't trigger the specific constraint
ex:charlieBrown a foaf:Person ;
    foaf:firstName "Charlie" .
"""

# --- 2. Define SHACL Shapes Graph with a SPARQL Constraint ---
# This SHACL graph defines a constraint that checks if a person's first name
# and last name are identical. If they are, it's a violation.
shapes_graph_ttl = """
@prefix sh: <http://www.w3.org/ns/shacl#> .
@prefix ex: <http://example.com/data#> .
@prefix foaf: <http://xmlns.com/foaf/0.1/> .
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

ex:PersonNameConstraint
    a sh:NodeShape ;
    sh:targetClass foaf:Person ;
    sh:message "First name and last name cannot be identical." ;
    sh:sparql [
        sh:select \"\"\"
            SELECT ?this ?firstName ?lastName
            WHERE {
                ?this a foaf:Person ;
                      foaf:firstName ?firstName ;
                      foaf:lastName ?lastName .
                FILTER (STR(?firstName) = STR(?lastName))
            }
        \"\"\" ;
    ] .
"""

# --- 3. Load Graphs ---
# Create RDFlib Graph objects from the Turtle strings.
data_graph = Graph()
data_graph.parse(data=data_graph_ttl, format="turtle")

shapes_graph = Graph()
shapes_graph.parse(data=shapes_graph_ttl, format="turtle")

print("--- Data Graph ---")
print(data_graph.serialize(format="turtle")) # Removed .decode("utf-8")
print("\n--- Shapes Graph ---")
print(shapes_graph.serialize(format="turtle")) # Removed .decode("utf-8")

# --- 4. Perform Validation with pyshacl ---
# The validate function returns:
# - conformance: True if the data conforms, False otherwise.
# - results_graph: An RDF graph containing the validation results.
# - results_text: A human-readable string summary of the results.
# - results_dict: A dictionary representation of the results.
try:
    conforms, results_graph, results_text = validate(
        data_graph,
        shacl_graph=shapes_graph,
        data_graph_format="turtle",
        shacl_graph_format="turtle",
        inference="rdfs", # Optional: Apply RDFS inference before validation
        debug=True # Optional: Enable debug output for more details
    )

    # --- 5. Print Validation Results ---
    print("\n--- Validation Results ---")
    print(f"Data Conforms: {conforms}")
    print("\nDetailed Results (Text):")
    print(results_text)

    print("\nDetailed Results (RDF Graph):")
    # You can further process results_graph to extract specific information
    # For example, iterate over sh:ValidationResult instances
    for s, p, o in results_graph.triples((None, RDF.type, URIRef("http://www.w3.org/ns/shacl#ValidationResult"))):
        print(f"  Violation for Node: {s}")
        for p_res, o_res in results_graph.predicate_objects(s):
            if p_res == URIRef("http://www.w3.org/ns/shacl#focusNode"):
                print(f"    Focus Node: {o_res}")
            elif p_res == URIRef("http://www.w3.org/ns/shacl#sourceShape"):
                print(f"    Source Shape: {o_res}")
            elif p_res == URIRef("http://www.w3.org/ns/shacl#resultMessage"):
                print(f"    Message: {o_res}")
            elif p_res == URIRef("http://www.w3.org/ns/shacl#resultSeverity"):
                print(f"    Severity: {o_res.split('#')[-1]}") # Get just the severity name
            elif p_res == URIRef("http://www.w3.org/ns/shacl#value"):
                print(f"    Value: {o_res}")
            elif p_res == URIRef("http://www.w3.org/ns/shacl#sourceConstraintComponent"):
                print(f"    Constraint Component: {o_res.split('#')[-1]}") # Get just the component name
            elif p_res == URIRef("http://www.w3.org/ns/shacl#detail"):
                print(f"    Detail: {o_res}") # Specific to SPARQL constraints, shows the query result
        print("-" * 20)

except Exception as e:
    print(f"An error occurred during validation: {e}")
