import random
from datetime import datetime, timedelta

class TravelGraphGenerator:
    def __init__(self):
        self.cities = ["London", "Paris", "New York", "Tokyo", "Rome", "Sydney", "Berlin", "Barcelona", "Amsterdam", "Dubai", "Bengaluru"]
        self.countries = ["United Kingdom", "France", "United States", "Japan", "Italy", "Australia", "Germany", "Spain", "Netherlands", "United Arab Emirates", "India"]
        self.states_india = ["Karnataka", "Maharashtra", "Tamil Nadu", "Delhi"]
        self.modes_of_transport = ["flight", "train", "bus", "car", "cruise", "metro"]
        self.travel_apps = ["MakeMyTrip", "Goibibo", "Booking.com", "Airbnb", "Expedia", "IRCTC Rail Connect"]
        self.airlines = ["Emirates", "Qatar Airways", "Singapore Airlines", "Air India", "British Airways", "IndiGo"]
        self.hotels = ["The Ritz-Carlton", "Four Seasons", "Mandarin Oriental", "Taj Hotels", "Hyatt", "The Leela Palace"]
        self.events_bengaluru = ["Bengaluru International Film Festival", "Namma Bengaluru Habba", "Karaga Festival"]
        self.local_attractions_bengaluru = ["Bangalore Palace", "Lalbagh Botanical Garden", "Vidhana Soudha", "Cubbon Park"]
        self.regions_europe = ["Tuscany", "Bavaria", "Andalusia"]
        self.user = "user:me"

        # Define a simple ontology (dictionary representation)
        self.ontology = {
            "classes": {
                "User": {"description": "Represents a user of the system."},
                "Trip": {"description": "Represents a travel event or journey.",
                         "subclassOf": ["Event"]},
                "Destination": {"description": "Represents a location of travel.",
                              "subclassOf": ["Place"]},
                "City": {"description": "A specific city.", "subclassOf": ["Destination"]},
                "Country": {"description": "A country.", "subclassOf": ["Destination"]},
                "State": {"description": "A state.", "subclassOf": ["Destination"]},
                "Event": {"description": "A general event."},
                "Booking": {"description": "A travel booking.",
                             "subclassOf": ["Event"]},
                "Application": {"description": "A software application.",
                                "subclassOf": ["Software"]},
                "Airline": {"description": "An airline company.",
                            "subclassOf": ["Organization"]},
                "Hotel": {"description": "A hotel.", "subclassOf": ["Place"]},
                "Place": {"description": "A general place."},
                "Organization": {"description": "A general organization."},
                "Software": {"description": "A general software."},
                "TransportMode": {"description": "A mode of transportation."},
                "Attraction": {"description": "A tourist attraction.", "subclassOf": ["Place"]}
            },
            "properties": {
                "hasDestination": {"domain": "Trip", "range": "Destination",
                                   "description": "Relates a trip to its destination."},
                "hasTravelDate": {"domain": "Trip", "range": "xsd:date",  # Using xsd:date for clarity
                                   "description": "Relates a trip to its date."},
                "notifiedBy": {"domain": "Trip", "range": "Application",
                               "description": "Relates a trip to the application that notified the user."},
                "mentionedTravelTo": {"domain": "User", "range": "Destination",
                                     "description": "Indicates a destination a user mentioned."},
                "discussedTravelWith": {"domain": "User", "range": "User",
                                        "description": "Indicates a user with whom travel was discussed."},
                "discussedTravelModeFor": {"domain": "User", "range": "TransportMode",
                                            "description": "Mode of transport discussed for a destination"},
                "mentionedTravelDateFor": {"domain": "User", "range": "xsd:date",
                                            "description": "Date mentioned for travel to a destination"},
                "askedAboutHotelIn": {"domain": "User", "range": "Destination",
                                      "description": "User asked about hotel in a destination"},
                "bookedTravelTo": {"domain": "User", "range": "Destination",
                                   "description": "Indicates a destination a user booked travel to."},
                "bookedVia": {"domain": "Booking", "range": "Application",
                              "description": "Relates a booking to the application used."},
                "uses": {"domain": "Booking", "range": "TransportMode",
                         "description": "Relates a booking to the mode of transport."},
                "onAirline": {"domain": "Booking", "range": "Airline",
                              "description": "Relates a booking to the airline."},
                "operatedBy": {"domain": "Booking", "range": "Organization",
                               "description": "Company operating the transport."},
                "includesStayAt": {"domain": "Booking", "range": "Hotel",
                                   "description": "Hotel included in the booking"},
                "browsedAbout": {"domain": "User", "range": "Destination",
                              "description": "Indicates a destination a user browsed about."},
                "searchedFor": {"domain": "User", "range": "xsd:string", # Using xsd:string
                               "description": "Indicates a search query."},
                "showedInterestIn": {"domain": "User", "range": "Attraction",
                                     "description": "Indicates an attraction a user showed interest in."},
                "researchedRegion": {"domain": "User", "range": "Destination",
                                     "description": "Region researched by user"},
                "hasCalendarEvent": {"domain": "User", "range": "Event",
                                     "description": "Relates a user to a calendar event."},
                "locatedAt": {"domain": "Event", "range": "Destination",
                              "description": "Relates an event to its location."},
                "onDate": {"domain": "Event", "range": "xsd:date",
                           "description": "Relates an event to its date."},
                "isRelatedTo": {"domain": "Event", "range": "xsd:string",
                                 "description": "Local event"},
                "sharedPostAbout": {"domain": "User", "range": "Destination",
                                    "description": "User shared post about"},
                "mentionsLocation": {"domain": "xsd:string", "range": "Destination", # changed domain
                                     "description": "Post mentions a location"},
                "interactedWithFriendAbout": {"domain": "User", "range": "User",
                                            "description": "User interacted with friend about a location"},
                "alsoInterestedIn": {"domain": "User", "range": "Destination",
                                     "description": "Friend also interested in location"},
                "checkedInAt": {"domain": "User", "range": "Attraction",
                               "description": "User checked in at"},
                "performedLocalSearch": {"domain": "User", "range": "xsd:string",
                                         "description": "User performed local search"},
                "hasSearchResult": {"domain": "xsd:string", "range": "xsd:string",
                                      "description": "Search result for a query"},
                "receivedNotificationAbout": {"domain": "User", "range": "Trip", "description": "User received notification about a trip"}
            }
        }

        self.triples = {
            "notification": self._generate_notification_triples(),
            "messages": self._generate_message_triples(),
            "travel_app": self._generate_travel_app_triples(),
            "browsing_history": self._generate_browsing_history_triples(),
            "calendar_events": self._generate_calendar_event_triples(),
            "social_media": self._generate_social_media_triples(),
            "local_search": self._generate_local_search_triples(),
        }

        self.triples["ontology_triples"] = self._generate_ontology_triples() # added ontology triples

    def _get_random_location(self):
        location_type = random.choice(["city", "country", "state"])
        if location_type == "city":
            return random.choice(self.cities)
        elif location_type == "country":
            return random.choice(self.countries)
        else:
            return random.choice(self.states_india)

    def _generate_notification_triples(self):
        triples = []
        for _ in range(10):
            location = self._get_random_location()
            travel_date = datetime.now() + timedelta(days=random.randint(1, 60))
            formatted_date = travel_date.strftime("%Y-%m-%d")
            trip_id = f"trip:{location.replace(' ', '_')}_{formatted_date}"
            triples.append((self.user, "receivedNotificationAbout", trip_id))
            triples.append((trip_id, "hasDestination", location))
            triples.append((trip_id, "hasTravelDate", formatted_date))
            if random.random() < 0.5:
                app = random.choice(self.travel_apps)
                triples.append((trip_id, "notifiedBy", f"app:{app.replace(' ', '_')}"))
            if random.random() < 0.3:
                mode = random.choice(self.modes_of_transport)
                triples.append((trip_id, "uses", mode))
        return triples

    def _generate_message_triples(self):
        triples = []
        for _ in range(10):
            person = f"contact:{random.randint(1000, 9999)}"
            location = self._get_random_location()
            if random.random() < 0.7:
                triples.append((self.user, "mentionedTravelTo", location))
                triples.append((person, "discussedTravelWith", self.user))
            if random.random() < 0.4:
                mode = random.choice(self.modes_of_transport)
                triples.append((self.user, "discussedTravelModeFor", location))
            if random.random() < 0.3:
                travel_date = datetime.now() + timedelta(days=random.randint(1, 90))
                formatted_date = travel_date.strftime("%Y-%m-%d")
                triples.append((self.user, "mentionedTravelDateFor", location))
            if random.random() < 0.2:
                hotel = random.choice(self.hotels)
                triples.append((self.user, "askedAboutHotelIn", location))
        return triples

    def _generate_travel_app_triples(self):
        triples = []
        app = random.choice(self.travel_apps)
        for _ in range(10):
            location = self._get_random_location()
            travel_date = datetime.now() + timedelta(days=random.randint(1, 120))
            formatted_date = travel_date.strftime("%Y-%m-%d")
            booking_id = f"booking:{random.randint(100, 999)}"
            triples.append((self.user, "bookedTravelTo", location))
            triples.append((booking_id, "hasDestination", location))
            triples.append((booking_id, "hasTravelDate", formatted_date))
            triples.append((booking_id, "bookedVia", f"app:{app.replace(' ', '_')}"))
            if random.random() < 0.6:
                mode = random.choice(self.modes_of_transport)
                triples.append((booking_id, "uses", mode))
                if mode == "flight" and random.random() < 0.5:
                    airline = random.choice(self.airlines)
                    triples.append((booking_id, "onAirline", f"airline:{airline.replace(' ', '_')}"))
                elif mode in ["train", "bus"] and random.random() < 0.4:
                    company = f"transport_company:{random.randint(1, 20)}"
                    triples.append((booking_id, "operatedBy", company))
            if random.random() < 0.4:
                hotel = random.choice(self.hotels)
                triples.append((booking_id, "includesStayAt", f"hotel:{hotel.replace(' ', '_')}"))
                triples.append((f"hotel:{hotel.replace(' ', '_')}", "locatedIn", location))
        return triples

    def _generate_browsing_history_triples(self):
        triples = []
        for _ in range(10):
            location = self._get_random_location()
            if random.random() < 0.8:
                triples.append((self.user, "browsedAbout", location))
            if random.random() < 0.5:
                search_term = random.choice([f"things to do in {location}", f"best hotels {location}", f"flights to {location}", f"train tickets to {location}"])
                triples.append((self.user, "searchedFor", search_term))
            if random.random() < 0.3:
                attraction_name = f"attraction:{location.replace(' ', '_')}_{random.randint(1, 5)}"
                triples.append((self.user, "showedInterestIn", attraction_name))
                triples.append((attraction_name, "locatedIn", location))
            if random.random() < 0.2:
                region = random.choice(self.regions_europe)
                triples.append((self.user, "researchedRegion", region))
        return triples

    def _generate_calendar_event_triples(self):
        triples = []
        for _ in range(5):
            location = self._get_random_location()
            event_date = datetime(2025, 5, random.randint(1, 31)) # Assuming events in May 2025
            formatted_date = event_date.strftime("%Y-%m-%d")
            event_name = f"event:{location.replace(' ', '_')}_{random.randint(1, 3)}"
            triples.append((self.user, "hasCalendarEvent", event_name))
            triples.append((event_name, "locatedAt", location))
            triples.append((event_name, "onDate", formatted_date))
            if location == "Bengaluru" and random.random() < 0.6:
                local_event = random.choice(self.events_bengaluru)
                triples.append((event_name, "isRelatedTo", local_event.replace(" ", "_")))
        return triples

    def _generate_social_media_triples(self):
        triples = []
        for _ in range(7):
            location = self._get_random_location()
            if random.random() < 0.6:
                post_id = f"post:{random.randint(10000, 99999)}"
                triples.append((self.user, "sharedPostAbout", location))
                triples.append((post_id, "mentionsLocation", location))
            if random.random() < 0.4:
                friend = f"friend:{random.randint(100, 500)}"
                triples.append((self.user, "interactedWithFriendAbout", location))
                triples.append((friend, "alsoInterestedIn", location))
            if location == "Bengaluru" and random.random() < 0.3:
                attraction = random.choice(self.local_attractions_bengaluru)
                triples.append((self.user, "checkedInAt", attraction.replace(" ", "_")))
                triples.append((attraction.replace(" ", "_"), "locatedIn", "Bengaluru"))
        return triples

    def _generate_local_search_triples(self):
        triples = []
        if datetime.now().month == 4 and datetime.now().year == 2025 and datetime.now().day >= 18: # Context aware
            for _ in range(5):
                query = random.choice([f"restaurants near me", f"hotels in {random.choice(self.states_india)}", f"tourist places in {random.choice(self.cities)}"])
                result = random.choice([f"restaurant:{random.randint(1, 20)}", f"hotel:{random.randint(100, 300)}", f"attraction:local_{random.randint(1, 10)}"])
                location = "Bengaluru" # Since the current location is Bengaluru
                triples.append((self.user, "performedLocalSearch", query))
                triples.append((query, "hasSearchResult", result))
                if "hotel" in query:
                    triples.append((result, "locatedIn", random.choice(self.states_india)))
                elif "tourist places" in query:
                    triples.append((result, "locatedIn", random.choice(self.cities)))
                elif "restaurants" in query:
                    triples.append((result, "locatedIn", location))
        return triples

    def _generate_ontology_triples(self):
        """
        Generates RDF triples representing the ontology defined in self.ontology.
        """
        ontology_triples = []
        for class_name, class_def in self.ontology["classes"].items():
            class_uri = f"class:{class_name.replace(' ', '_')}"
            ontology_triples.append((class_uri, "rdf:type", "rdfs:Class"))  # Define as a class
            if "description" in class_def:
                ontology_triples.append((class_uri, "rdfs:comment", f'"{class_def["description"]}"'))
            if "subclassOf" in class_def:
                for parent_class_name in class_def["subclassOf"]:
                    parent_class_uri = f"class:{parent_class_name.replace(' ', '_')}"
                    ontology_triples.append((class_uri, "rdfs:subClassOf", parent_class_uri))

        for prop_name, prop_def in self.ontology["properties"].items():
            prop_uri = f"property:{prop_name.replace(' ', '_')}"
            ontology_triples.append((prop_uri, "rdf:type", "rdf:Property"))  # Define as a property
            if "description" in prop_def:
                ontology_triples.append((prop_uri, "rdfs:comment", f'"{prop_def["description"]}"'))
            if "domain" in prop_def:
                domain_uri = f"class:{prop_def["domain"].replace(' ', '_')}" if "class:" not in prop_def["domain"] else prop_def["domain"]
                ontology_triples.append((prop_uri, "rdfs:domain", domain_uri))
            if "range" in prop_def:
                range_uri = f"class:{prop_def["range"].replace(' ', '_')}" if "class:" not in prop_def["range"]  else prop_def["range"]
                ontology_triples.append((prop_uri, "rdfs:range", range_uri))
        return ontology_triples

    def get_random_triples_by_category(self, category, n=5):
        if category not in self.triples:
            return f"Category '{category}' not found."
        return random.sample(self.triples[category], min(n, len(self.triples[category])))

    def add_triples_to_graph(self, triples_to_add, existing_graph=None):
        if existing_graph is None:
            existing_graph = []
        existing_graph.extend(triples_to_add)
        return existing_graph

# Example Usage
generator = TravelGraphGenerator()

# Print the ontology triples
print("Ontology Triples:")
for triple in generator.triples["ontology_triples"]:
    print(triple)

# Get some random triples from different categories
print("\nRandom triples from notification:", generator.get_random_triples_by_category("notification", 2))
print("\nRandom triples from messages:", generator.get_random_triples_by_category("messages", 2))
print("\nRandom triples from travel_app:", generator.get_random_triples_by_category("travel_app", 2))
print("\nRandom triples from browsing_history:", generator.get_random_triples_by_category("browsing_history", 2))
print("\nRandom triples from calendar_events:", generator.get_random_triples_by_category("calendar_events", 2))
print("\nRandom triples from social_media:", generator.get_random_triples_by_category("social_media", 2))
print("\nRandom triples from local_search:", generator.get_random_triples_by_category("local_search", 2))

# Add all generated triples to a single knowledge graph
all_triples = []
for category in generator.triples:
    all_triples.extend(generator.triples[category])

knowledge_graph = generator.add_triples_to_graph(all_triples)
print(f"\nTotal number of triples in the generated knowledge graph: {len(knowledge_graph)}")


