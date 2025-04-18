import rdflib
from rdflib import Graph, URIRef, Literal
from rdflib.namespace import RDF, XSD
from datetime import datetime, timedelta
import random

# Define the base URI for the 'kb' namespace
KB_BASE_URI = "http://example.org/knowledgebase/"  # You can change this if needed

class TravelGraphGenerator:
    def __init__(self):
        self.cities = ["London", "Paris", "New York", "Tokyo", "Rome", "Sydney", "Berlin", "Barcelona", "Amsterdam", "Dubai", "Bengaluru"]
        self.countries = ["United_Kingdom", "France", "United_States", "Japan", "Italy", "Australia", "Germany", "Spain", "Netherlands", "United_Arab_Emirates", "India"]
        self.states_india = ["Karnataka", "Maharashtra", "Tamil_Nadu", "Delhi"]
        self.modes_of_transport = ["flight", "train", "bus", "car", "cruise", "metro"]
        self.travel_apps = ["MakeMyTrip", "Goibibo", "Booking_com", "Airbnb", "Expedia", "IRCTC_Rail_Connect"]
        self.airlines = ["Emirates", "Qatar_Airways", "Singapore_Airlines", "Air_India", "British_Airways", "IndiGo"]
        self.hotels = ["The_Ritz-Carlton", "Four_Seasons", "Mandarin_Oriental", "Taj_Hotels", "Hyatt", "The_Leela_Palace"]
        self.events_bengaluru = ["Bengaluru_International_Film_Festival", "Namma_Bengaluru_Habba", "Karaga_Festival"]
        self.local_attractions_bengaluru = ["Bangalore_Palace", "Lalbagh_Botanical_Garden", "Vidhana_Soudha", "Cubbon_Park"]
        self.regions_europe = ["Tuscany", "Bavaria", "Andalusia"]
        self.user_uri = URIRef(f"{KB_BASE_URI}user/me")
        self.predicate_namespace = f"{KB_BASE_URI}ontology/"

        self.triples = {
            "notification": self._generate_notification_triples(),
            "messages": self._generate_message_triples(),
            "travel_app": self._generate_travel_app_triples(),
            "browsing_history": self._generate_browsing_history_triples(),
            "calendar_events": self._generate_calendar_event_triples(),
            "social_media": self._generate_social_media_triples(),
            "local_search": self._generate_local_search_triples(),
        }

    def _get_random_location_uri(self):
        location_type = random.choice(["city", "country", "state"])
        if location_type == "city":
            return URIRef(f"{KB_BASE_URI}location/{random.choice(self.cities).replace(' ', '_')}")
        elif location_type == "country":
            return URIRef(f"{KB_BASE_URI}country/{random.choice(self.countries)}")
        else:
            return URIRef(f"{KB_BASE_URI}state/{random.choice(self.states_india).replace(' ', '_')}")

    def _generate_notification_triples(self):
        triples = []
        for _ in range(10):
            location_uri = self._get_random_location_uri()
            location_name = location_uri.split('/')[-1]
            travel_date = datetime.now() + timedelta(days=random.randint(1, 60))
            formatted_date = travel_date.strftime("%Y-%m-%d")
            trip_uri = URIRef(f"{KB_BASE_URI}trip/{location_name}_{formatted_date}")
            triples.append((self.user_uri, URIRef(f"{self.predicate_namespace}receivedNotificationAbout"), trip_uri))
            triples.append((trip_uri, URIRef(f"{self.predicate_namespace}hasDestination"), location_uri))
            triples.append((trip_uri, URIRef(f"{self.predicate_namespace}hasTravelDate"), Literal(formatted_date, datatype=XSD.date)))
            if random.random() < 0.5:
                app = random.choice(self.travel_apps)
                app_uri = URIRef(f"{KB_BASE_URI}app/{app.replace('.', '_')}")
                triples.append((trip_uri, URIRef(f"{self.predicate_namespace}notifiedBy"), app_uri))
            if random.random() < 0.3:
                mode = random.choice(self.modes_of_transport)
                mode_uri = URIRef(f"{KB_BASE_URI}mode/{mode}")
                triples.append((trip_uri, URIRef(f"{self.predicate_namespace}usesModeOfTransport"), mode_uri))
        return triples

    def _generate_message_triples(self):
        triples = []
        for _ in range(10):
            person_uri = URIRef(f"{KB_BASE_URI}contact/{random.randint(1000, 9999)}")
            location_uri = self._get_random_location_uri()
            if random.random() < 0.7:
                triples.append((self.user_uri, URIRef(f"{self.predicate_namespace}mentionedTravelTo"), location_uri))
                triples.append((person_uri, URIRef(f"{self.predicate_namespace}discussedTravelWith"), self.user_uri))
            if random.random() < 0.4:
                mode = random.choice(self.modes_of_transport)
                mode_uri = URIRef(f"{KB_BASE_URI}mode/{mode}")
                triples.append((self.user_uri, URIRef(f"{self.predicate_namespace}discussedTravelModeFor"), location_uri))
            if random.random() < 0.3:
                travel_date = datetime.now() + timedelta(days=random.randint(1, 90))
                formatted_date = travel_date.strftime("%Y-%m-%d")
                triples.append((self.user_uri, URIRef(f"{self.predicate_namespace}mentionedTravelDateFor"), location_uri))
            if random.random() < 0.2:
                hotel = random.choice(self.hotels)
                hotel_uri = URIRef(f"{KB_BASE_URI}hotel/{hotel.replace('-', '_')}")
                triples.append((self.user_uri, URIRef(f"{self.predicate_namespace}askedAboutHotelIn"), location_uri))
        return triples

    def _generate_travel_app_triples(self):
        triples = []
        app = random.choice(self.travel_apps)
        app_uri = URIRef(f"{KB_BASE_URI}app/{app.replace('.', '_')}")
        for _ in range(10):
            location_uri = self._get_random_location_uri()
            location_name = location_uri.split('/')[-1]
            travel_date = datetime.now() + timedelta(days=random.randint(1, 120))
            formatted_date = travel_date.strftime("%Y-%m-%d")
            booking_uri = URIRef(f"{KB_BASE_URI}booking/{random.randint(100, 999)}")
            triples.append((self.user_uri, URIRef(f"{self.predicate_namespace}bookedTravelTo"), location_uri))
            triples.append((booking_uri, URIRef(f"{self.predicate_namespace}hasDestination"), location_uri))
            triples.append((booking_uri, URIRef(f"{self.predicate_namespace}hasTravelDate"), Literal(formatted_date, datatype=XSD.date)))
            triples.append((booking_uri, URIRef(f"{self.predicate_namespace}bookedVia"), app_uri))
            if random.random() < 0.6:
                mode = random.choice(self.modes_of_transport)
                mode_uri = URIRef(f"{KB_BASE_URI}mode/{mode}")
                triples.append((booking_uri, URIRef(f"{self.predicate_namespace}uses"), mode_uri))
                if mode == "flight" and random.random() < 0.5:
                    airline = random.choice(self.airlines)
                    airline_uri = URIRef(f"{KB_BASE_URI}airline/{airline.replace('_', '_')}")
                    triples.append((booking_uri, URIRef(f"{self.predicate_namespace}onAirline"), airline_uri))
                elif mode in ["train", "bus"] and random.random() < 0.4:
                    company_uri = URIRef(f"{KB_BASE_URI}transportCompany/{random.randint(1, 20)}")
                    triples.append((booking_uri, URIRef(f"{self.predicate_namespace}operatedBy"), company_uri))
            if random.random() < 0.4:
                hotel = random.choice(self.hotels)
                hotel_uri = URIRef(f"{KB_BASE_URI}hotel/{hotel.replace('-', '_')}")
                triples.append((booking_uri, URIRef(f"{self.predicate_namespace}includesStayAt"), hotel_uri))
                triples.append((hotel_uri, URIRef(f"{self.predicate_namespace}locatedIn"), location_uri))
        return triples

    def _generate_browsing_history_triples(self):
        triples = []
        for _ in range(10):
            location_uri = self._get_random_location_uri()
            location_name = location_uri.split('/')[-1].replace('_', ' ')
            if random.random() < 0.8:
                triples.append((self.user_uri, URIRef(f"{self.predicate_namespace}browsedAbout"), location_uri))
            if random.random() < 0.5:
                search_term = random.choice([f"things to do in {location_name}", f"best hotels {location_name}", f"flights to {location_name}", f"train tickets to {location_name}"])
                triples.append((self.user_uri, URIRef(f"{self.predicate_namespace}searchedFor"), Literal(search_term)))
            if random.random() < 0.3:
                attraction = f"attraction:{location_name.replace(' ', '_')}_{random.randint(1, 5)}"
                attraction_uri = URIRef(f"{KB_BASE_URI}attraction/{attraction}")
                triples.append((self.user_uri, URIRef(f"{self.predicate_namespace}showedInterestIn"), attraction_uri))
                triples.append((attraction_uri, URIRef(f"{self.predicate_namespace}locatedIn"), location_uri))
            if random.random() < 0.2:
                region = random.choice(self.regions_europe)
                region_uri = URIRef(f"{KB_BASE_URI}region/{region}")
                triples.append((self.user_uri, URIRef(f"{self.predicate_namespace}researchedRegion"), region_uri))
                # Implicitly, regions are associated with countries (can be added if needed)
        return triples

    def _generate_calendar_event_triples(self):
        triples = []
        for _ in range(5):
            location_uri = self._get_random_location_uri()
            location_name = location_uri.split('/')[-1]
            event_date = datetime(2025, 5, random.randint(1, 31)) # Assuming events in May 2025
            formatted_date = event_date.strftime("%Y-%m-%d")
            event = f"event:{location_name}_{random.randint(1, 3)}"
            event_uri = URIRef(f"{KB_BASE_URI}event/{event}")
            triples.append((self.user_uri, URIRef(f"{self.predicate_namespace}hasCalendarEvent"), event_uri))
            triples.append((event_uri, URIRef(f"{self.predicate_namespace}locatedAt"), location_uri))
            triples.append((event_uri, URIRef(f"{self.predicate_namespace}onDate"), Literal(formatted_date, datatype=XSD.date)))
            if location_name == "Bengaluru":
                if random.random() < 0.6:
                    local_event = random.choice(self.events_bengaluru)
                    local_event_uri = URIRef(f"{KB_BASE_URI}event/{local_event.replace(' ', '_')}")
                    triples.append((event_uri, URIRef(f"{self.predicate_namespace}isRelatedTo"), local_event_uri))
        return triples

    def _generate_social_media_triples(self):
        triples = []
        for _ in range(7):
            location_uri = self._get_random_location_uri()
            location_name = location_uri.split('/')[-1]
            if random.random() < 0.6:
                post_uri = URIRef(f"{KB_BASE_URI}post/{random.randint(10000, 99999)}")
                triples.append((self.user_uri, URIRef(f"{self.predicate_namespace}sharedPostAbout"), location_uri))
                triples.append((post_uri, URIRef(f"{self.predicate_namespace}mentionsLocation"), location_uri))
            if random.random() < 0.4:
                friend_uri = URIRef(f"{KB_BASE_URI}friend/{random.randint(100, 500)}")
                triples.append((self.user_uri, URIRef(f"{self.predicate_namespace}interactedWithFriendAbout"), location_uri))
                triples.append((friend_uri, URIRef(f"{self.predicate_namespace}alsoInterestedIn"), location_uri))
            if location_name == "Bengaluru":
                if random.random() < 0.3:
                    attraction = random.choice(self.local_attractions_bengaluru)
                    attraction_uri = URIRef(f"{KB_BASE_URI}attraction/{attraction.replace(' ', '_')}")
                    triples.append((self.user_uri, URIRef(f"{self.predicate_namespace}checkedInAt"), attraction_uri))
                    triples.append((attraction_uri, URIRef(f"{self.predicate_namespace}locatedIn"), URIRef(f"{KB_BASE_URI}location/Bengaluru")))
        return triples

    def _generate_local_search_triples(self):
        triples = []
        if datetime.now().month == 4 and datetime.now().year == 2025 and datetime.now().day >= 18: # Context aware
            for _ in range(5):
                location_bengaluru_uri = URIRef(f"{KB_BASE_URI}location/Bengaluru")
                query = random.choice([f"restaurants near me", f"hotels in {random.choice(self.states_india).replace('_', ' ')}", f"tourist places in {random.choice(self.cities).replace('_', ' ')}"])
                result_type = random.choice(["restaurant", "hotel", "attraction"])
                result_id = f"{result_type}_{random.randint(1, 300)}"
                result_uri = URIRef(f"{KB_BASE_URI}{result_type}/{result_id}")
                triples.append((self.user_uri, URIRef(f"{self.predicate_namespace}performedLocalSearch"), Literal(query)))
                triples.append((Literal(query), URIRef(f"{self.predicate_namespace}hasSearchResult"), result_uri))
                if "hotel" in query:
                    state = random.choice(self.states_india).replace(" ", "_")
                    state_uri = URIRef(f"{KB_BASE_URI}state/{state}")
                    triples.append((result_uri, URIRef(f"{self.predicate_namespace}locatedIn"), state_uri))
                elif "tourist places" in query:
                    city = random.choice(self.cities).replace(" ", "_")
                    city_uri = URIRef(f"{KB_BASE_URI}location/{city}")
                    triples.append((result_uri, URIRef(f"{self.predicate_namespace}locatedIn"), city_uri))
                elif "restaurants" in query:
                    triples.append((result_uri, URIRef(f"{self.predicate_namespace}locatedIn"), location_bengaluru_uri))
        return triples

    def get_random_triples_by_category(self, category, n=5):
        if category not in self.triples:
            return f"Category '{category}' not found."
        return random.sample(self.triples[category], min(n, len(self.triples[category])))

    def add_triples_to_graph(self, triples_to_add, existing_graph=None):
        if existing_graph is None:
            existing_graph = []
        existing_graph.extend(triples_to_add)
        return existing_graph

def add_triples_to_kg_and_save(triples, output_file="knowledge_graph.ttl"):
    """
    Adds a list of RDF triples to an rdflib Graph and saves it in TTL format.

    Args:
        triples: A list of triples, where each triple is a tuple of (subject, predicate, object).
        output_file: The name of the file to save the TTL output to.  Defaults to "knowledge_graph.ttl".
    """
    graph = Graph()
    # Bind the kb namespace
    graph.bind("kb", KB_BASE_URI)

    for s, p, o in triples:
        graph.add((s, p, o))

    try:
        graph.serialize(destination=output_file, format="ttl")
        print(f"Knowledge graph successfully saved to {output_file}")
    except Exception as e:
        print(f"Error saving knowledge graph: {e}")

if __name__ == "__main__":
    generator = TravelGraphGenerator()

    # Get all generated triples
    all_triples = []
    for category in generator.triples:
        all_triples.extend(generator.triples[category])

    # Add the triples to a knowledge graph and save to a file
    add_triples_to_kg_and_save(all_triples)


# sparql_query = """
# PREFIX kb: <http://example.org/knowledgebase/>
# PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
# PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
# PREFIX xsd: <http://www.w3.org/2001/XMLSchema#>

# SELECT ?subject ?predicate ?object
# WHERE {
#   ?subject ?predicate ?object .
#   FILTER (?predicate IN (
#     kb:ontology/receivedNotificationAbout,
#     kb:ontology/hasDestination,
#     kb:ontology/hasTravelDate,
#     kb:ontology/notifiedBy,
#     kb:ontology/usesModeOfTransport,
#     kb:ontology/mentionedTravelTo,
#     kb:ontology/discussedTravelWith,
#     kb:ontology/discussedTravelModeFor,
#     kb:ontology/mentionedTravelDateFor,
#     kb:ontology/askedAboutHotelIn,
#     kb:ontology/bookedTravelTo,
#     kb:ontology/bookedVia,
#     kb:ontology/uses,
#     kb:ontology/onAirline,
#     kb:ontology/operatedBy,
#     kb:ontology/includesStayAt,
#     kb:ontology/locatedIn,
#     kb:ontology/browsedAbout,
#     kb:ontology/searchedFor,
#     kb:ontology/showedInterestIn,
#     kb:ontology/researchedRegion,
#     kb:ontology/hasCalendarEvent,
#     kb:ontology/locatedAt,
#     kb:ontology/onDate,
#     kb:ontology/isRelatedTo,
#     kb:ontology/sharedPostAbout,
#     kb:ontology/mentionsLocation,
#     kb:ontology/interactedWithFriendAbout,
#     kb:ontology/alsoInterestedIn,
#     kb:ontology/checkedInAt,
#     kb:ontology/performedLocalSearch,
#     kb:ontology/hasSearchResult
#   ))
# }
# """
