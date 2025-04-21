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

        # Define a more structured ontology
        self.ontology = {
            "classes": {
                "User": {"description": "Represents a user of the system.",
                         "properties": ["hasNotification", "hasMessage", "hasBooking", "hasBrowsingHistory",
                                        "hasCalendarEvent", "hasSocialMediaActivity", "hasLocalSearch", "hasBankAccount"]},  # Non-travel
                "Notification": {"description": "Represents a notification.",
                                 "properties": ["aboutTrip"],
                                 "subclassOf": ["Event"]},
                "Message": {"description": "Represents a message.",
                            "properties": ["mentionsTravel", "discussesTravelWith"]},
                "TravelAppBooking": {"description": "Represents a booking made through a travel app.",
                                     "properties": ["hasBookingDetails"],
                                     "subclassOf": ["Booking"]},
                "BrowsingHistory": {"description": "Represents user's browsing history.",
                                    "properties": ["browsedFor"]},
                "CalendarEvent": {"description": "Represents an event from user's calendar.",
                                  "properties": ["atLocation", "onEventDate"]},
                "SocialMediaActivity": {"description": "Represents user's activity on social media.",
                                        "properties": ["sharedPost", "interactedWithFriend"]},
                "LocalSearch": {"description": "Represents user's local search activity.",
                                "properties": ["searchQuery", "hasResult"]},
                "Trip": {"description": "Represents a travel event or journey.",
                         "properties": ["hasDestination", "hasTravelDate", "usesModeOfTransport"],
                         "subclassOf": ["Event"]},
                "Destination": {"description": "Represents a location of travel.",
                              "subclassOf": ["Place"]},
                "City": {"description": "A specific city.", "subclassOf": ["Destination"]},
                "Country": {"description": "A country.", "subclassOf": ["Destination"]},
                "State": {"description": "A state.", "subclassOf": ["Destination"]},
                "Event": {"description": "A general event."},
                "Booking": {"description": "A travel booking.",
                             "properties": ["bookingId"],
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
                "Attraction": {"description": "A tourist attraction.", "subclassOf": ["Place"]},
                "BankAccount": {"description": "User's bank account.", "properties": ["accountNumber"]} # Non-travel
            },
            "properties": {
                "hasNotification": {"domain": "User", "range": "Notification",
                                    "description": "Relates a user to a notification."},
                "aboutTrip": {"domain": "Notification", "range": "Trip",
                             "description": "Relates a notification to a trip."},
                "hasMessage": {"domain": "User", "range": "Message",
                             "description": "Relates a user to a message."},
                "mentionsTravel": {"domain": "Message", "range": "Destination",
                                     "description": "Indicates a destination mentioned in a message."},
                "discussesTravelWith": {"domain": "Message", "range": "User",
                                        "description": "Indicates a user with whom travel is discussed."},
                "hasBooking": {"domain": "User", "range": "TravelAppBooking",
                               "description": "Relates a user to a travel app booking."},
                "hasBookingDetails": {"domain": "TravelAppBooking", "range": "Booking",
                                      "description": "Relates a travel app booking to booking details"},
                "hasDestination": {"domain": "Trip", "range": "Destination",
                                   "description": "Relates a trip to its destination."},
                "hasTravelDate": {"domain": "Trip", "range": "xsd:date",
                                   "description": "Relates a trip to its date."},
                "usesModeOfTransport": {"domain": "Trip", "range": "TransportMode",
                                        "description": "Mode of transport used for the trip"},
                "bookedVia": {"domain": "Booking", "range": "Application",
                              "description": "Relates a booking to the application used."},
                "onAirline": {"domain": "Booking", "range": "Airline",
                              "description": "Relates a booking to the airline."},
                "operatedBy": {"domain": "Booking", "range": "Organization",
                               "description": "Company operating the transport."},
                "includesStayAt": {"domain": "Booking", "range": "Hotel",
                                   "description": "Hotel included in the booking"},
                "bookingId": {"domain": "Booking", "range": "xsd:string",
                              "description": "Booking Identifier"},
                "hasBrowsingHistory": {"domain": "User", "range": "BrowsingHistory",
                                     "description": "Relates a user to their browsing history."},
                "browsedFor": {"domain": "BrowsingHistory", "range": "Destination",
                              "description": "Indicates a destination a user browsed for."},
                "hasCalendarEvent": {"domain": "User", "range": "CalendarEvent",
                                     "description": "Relates a user to a calendar event."},
                "atLocation": {"domain": "CalendarEvent", "range": "Destination",
                             "description": "Location of Calendar Event"},
                "onEventDate": {"domain": "CalendarEvent", "range": "xsd:date",
                              "description": "Date of Calendar Event"},
                "hasSocialMediaActivity": {"domain": "User", "range": "SocialMediaActivity",
                                          "description": "User's social media activity"},
                "sharedPost": {"domain": "SocialMediaActivity", "range": "Destination",
                                    "description": "Destination shared in social media post"},
                "interactedWithFriend": {"domain": "SocialMediaActivity", "range": "User",
                                            "description": "User interacted with friend"},
                "hasLocalSearch": {"domain": "User", "range": "LocalSearch",
                                   "description": "User performed local search"},
                "searchQuery": {"domain": "LocalSearch", "range": "xsd:string",
                                    "description": "Local Search query"},
                "hasResult": {"domain": "LocalSearch", "range": "xsd:string",
                                 "description": "Result of local search"},
                "hasBankAccount": {"domain": "User", "range": "BankAccount", # Non-travel
                                 "description": "User has a bank account"},
                "accountNumber": {"domain": "BankAccount", "range": "xsd:string", # Non-travel
                                  "description": "Bank account number"}
            }
        }

        self.instances = { # added instances.
            "user": {
                "user:me": {"class": "User", "properties": {"hasNotification": [], "hasMessage": [], "hasBooking": [], "hasBrowsingHistory": [], "hasCalendarEvent": [], "hasSocialMediaActivity": [], "hasLocalSearch": [], "hasBankAccount": "bankaccount:12345"}},
                "user:john_doe": {"class": "User", "properties": {"hasBankAccount": "bankaccount:67890"}}, # Non-travel user
            },
            "notification": {
                "notification:trip1": {"class": "Notification", "properties": {"aboutTrip": "trip:london_2025-05-20"}},
                "notification:promo1": {"class": "Notification", "properties": {}}, # Non-travel notification
            },
            "message": {
                "message:london_trip": {"class": "Message", "properties": {"mentionsTravel": "London", "discussesTravelWith": "user:contact1"}},
                "message:meeting_reminder": {"class": "Message", "properties": {}}, # Non-travel message
            },
            "booking": {
                "booking:123": {"class": "TravelAppBooking", "properties": {"hasBookingDetails": "booking_details:123"}},
                "booking:non_travel": {"class": "Booking", "properties": {}} # Non-travel booking
            },
            "browsing_history": {
                "browsing_history:london": {"class": "BrowsingHistory", "properties": {"browsedFor": "London"}},
                "browsing_history:recipes": {"class": "BrowsingHistory", "properties": {}} # Non-travel
            },
            "calendar_event": {
                "calendar_event:london_trip": {"class": "CalendarEvent", "properties": {"atLocation": "London", "onEventDate": "2025-05-20"}},
                "calendar_event:doctor_appt": {"class": "CalendarEvent", "properties": {}} # Non-travel
            },
            "social_media_activity":{
                "social_media_activity:london_post": {"class": "SocialMediaActivity", "properties": {"sharedPost": "London"}},
                "social_media_activity:general_post": {"class": "SocialMediaActivity", "properties": {}} # Non-travel
            },
            "local_search": {
                "local_search:restaurants": {"class": "LocalSearch", "properties": {"searchQuery": "restaurants near me", "hasResult": "restaurant:1"}},
                "local_search:directions": {"class": "LocalSearch", "properties": {}} # Non-travel
            },
            "trip":{
                "trip:london_2025-05-20": {"class": "Trip", "properties": {"hasDestination": "London", "hasTravelDate": "2025-05-20", "usesModeOfTransport": "flight"}},
            },
            "destination":{
                "destination:london": {"class": "City", "properties": {}},
                "destination:uk": {"class": "Country", "properties": {}},
                "destination:karnataka": {"class": "State", "properties": {}},
            },
            "application":{
                "application:makemytrip": {"class": "Application", "properties": {}},
            },
            "airline": {
                "airline:emirates": {"class": "Airline", "properties": {}},
            },
            "hotel":{
                "hotel:ritz_london": {"class": "Hotel", "properties": {}},
            },
            "transportmode":{
                "transportmode:flight": {"class": "TransportMode", "properties": {}},
            },
            "attraction":{
                "attraction:london_eye": {"class": "Attraction", "properties": {}},
            },
            "bankaccount": { # Non-travel
                "bankaccount:12345": {"class": "BankAccount", "properties": {"accountNumber": "12345"}},
                "bankaccount:67890": {"class": "BankAccount", "properties": {"accountNumber": "67890"}}
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
            "ontology_triples": self._generate_ontology_triples(),
            "instance_triples": self._generate_instance_triples() # added instance triples
        }

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
            triples.append((self.user, "hasNotification", f"notification:notification{random.randint(1,10)}"))
            triples.append((f"notification:notification{random.randint(1,10)}", "aboutTrip", trip_id))
            triples.append((trip_id, "hasDestination", location))
            triples.append((trip_id, "hasTravelDate", formatted_date))
            if random.random() < 0.5:
                app = random.choice(self.travel_apps)
                triples.append((trip_id, "bookedVia", f"application:{app.replace(' ', '_')}"))
            if random.random() < 0.3:
                mode = random.choice(self.modes_of_transport)
                triples.append((trip_id, "usesModeOfTransport", mode))
        return triples

    def _generate_message_triples(self):
        triples = []
        for _ in range(10):
            person = f"contact:{random.randint(1000, 9999)}"
            location = self._get_random_location()
            if random.random() < 0.7:
                triples.append((self.user, "hasMessage", f"message:message{random.randint(1,10)}"))
                triples.append((f"message:message{random.randint(1,10)}", "mentionsTravel", location))
                triples.append((f"message:message{random.randint(1,10)}", "discussesTravelWith", person))
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
            triples.append((self.user, "hasBooking", f"booking:{booking_id}"))
            triples.append((f"booking:{booking_id}", "hasBookingDetails", f"booking_details:{booking_id}"))
            triples.append((f"booking:{booking_id}", "hasDestination", location))
            triples.append((f"booking:{booking_id}", "hasTravelDate", formatted_date))
            triples.append((f"booking:{booking_id}", "bookedVia", f"application:{app.replace(' ', '_')}"))
            if random.random() < 0.6:
                mode = random.choice(self.modes_of_transport)
                triples.append((f"booking:{booking_id}", "usesModeOfTransport", mode))
                if mode == "flight" and random.random() < 0.5:
                    airline = random.choice(self.airlines)
                    triples.append((f"booking:{booking_id}", "onAirline", f"airline:{airline.replace(' ', '_')}"))
                elif mode in ["train", "bus"] and random.random() < 0.4:
                    company = f"transport_company:{random.randint(1, 20)}"
                    triples.append((f"booking:{booking_id}", "operatedBy", company))
            if random.random() < 0.4:
                hotel = random.choice(self.hotels)
                triples.append((f"booking:{booking_id}", "includesStayAt", f"hotel:{hotel.replace(' ', '_')}"))
                triples.append((f"hotel:{hotel.replace(' ', '_')}", "locatedIn", location))
        return triples

    def _generate_browsing_history_triples(self):
        triples = []
        for _ in range(10):
            location = self._get_random_location()
            triples.append((self.user, "hasBrowsingHistory", f"browsing_history:browsing{random.randint(1,10)}"))
            triples.append((f"browsing_history:browsing{random.randint(1,10)}", "browsedFor", location))
            if random.random() < 0.5:
                search_term = random.choice([f"things to do in {location}", f"best hotels {location}", f"flights to {location}", f"train tickets to {location}"])
                triples.append((f"browsing_history:browsing{random.randint(1,10)}", "searchedFor", search_term))
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
            event_date = datetime(2025, 5, random.randint(1, 31))
            formatted_date = event_date.strftime("%Y-%m-%d")
            event_name = f"event:{location.replace(' ', '_')}_{random.randint(1, 3)}"
            triples.append((self.user, "hasCalendarEvent", event_name))
            triples.append((event_name, "atLocation", location))
            triples.append((event_name, "onEventDate", formatted_date))
            if location == "Bengaluru" and random.random() < 0.6:
                local_event = random.choice(self.events_bengaluru)
                triples.append((event_name, "isRelatedTo", local_event.replace(" ", "_")))
        return triples

    def _generate_social_media_triples(self):
        triples = []
        for _ in range(7):
            location = self._get_random_location()
            post_id = f"post:{random.randint(10000, 99999)}"
            triples.append((self.user, "hasSocialMediaActivity", f"social_media_activity:social_media{random.randint(1,10)}"))
            triples.append((f"social_media_activity:social_media{random.randint(1,10)}", "sharedPost", location))
            triples.append((post_id, "mentionsLocation", location))
            if random.random() < 0.4:
                friend = f"friend:{random.randint(100, 500)}"
                triples.append((f"social_media_activity:social_media{random.randint(1,10)}", "interactedWithFriend", friend))
                triples.append((friend, "alsoInterestedIn", location))
            if location == "Bengaluru" and random.random() < 0.3:
                attraction = random.choice(self.local_attractions_bengaluru)
                triples.append((self.user, "checkedInAt", attraction.replace(" ", "_")))
                triples.append((attraction.replace(" ", "_"), "locatedIn", "Bengaluru"))
        return triples

    def _generate_local_search_triples(self):
        triples = []
        if datetime.now().month == 4 and datetime.now().year == 2025 and datetime.now().day >= 18:
            for _ in range(5):
                query = random.choice([f"restaurants near me", f"hotels in {random.choice(self.states_india)}", f"tourist places in {random.choice(self.cities)}"])
                result = random.choice([f"restaurant:{random.randint(1, 20)}", f"hotel:{random.randint(100, 300)}", f"attraction:local_{random.randint(1, 10)}"])
                location = "Bengaluru"
                triples.append((self.user, "hasLocalSearch", f"local_search:search{random.randint(1,10)}"))
                triples.append((f"local_search:search{random.randint(1,10)}", "searchQuery", query))
                triples.append((f"local_search:search{random.randint(1,10)}", "hasResult", result))
                if "hotel" in query:
                    triples.append((result, "locatedIn", random.choice(self.states_india)))
                elif "tourist places" in query:
                    triples.append((result, "locatedIn", random.choice(self.cities)))
                elif "restaurants" in query:
                    triples.append((result, "locatedIn", location))
        return triples

    def _generate_ontology_triples(self):
        """Generates RDF triples representing the ontology defined in self.ontology."""
        ontology_triples = []
        for class_name, class_def in self.ontology["classes"].items():
            class_uri = f"class:{class_name.replace(' ', '_')}"
            ontology_triples.append((class_uri, "rdf:type", "rdfs:Class"))
            if "description" in class_def:
                ontology_triples.append((class_uri, "rdfs:comment", f'"{class_def["description"]}"'))
            if "subclassOf" in class_def:
                for parent_class_name in class_def["subclassOf"]:
                    parent_class_uri = f"class:{parent_class_name.replace(' ', '_')}"
                    ontology_triples.append((class_uri, "rdfs:subClassOf", parent_class_uri))
            if "properties" in class_def:
                for prop_name in class_def["properties"]:
                    prop_uri = f"property:{prop_name.replace(' ', '_')}"
                    ontology_triples.append((class_uri, "rdfs:domain", prop_uri))

        for prop_name, prop_def in self.ontology["properties"].items():
            prop_uri = f"property:{prop_name.replace(' ', '_')}"
            ontology_triples.append((prop_uri,"rdf:type", "rdf:Property"))
            if "description" in prop_def:
                ontology_triples.append((prop_uri, "rdfs:comment", f'"{prop_def["description"]}"'))
            if "domain" in prop_def:
                domain_uri = f"class:{prop_def["domain"].replace(' ', '_')}" if "class:" not in prop_def["domain"] else prop_def["domain"]
                ontology_triples.append((prop_uri, "rdfs:domain", domain_uri))
            if "range" in prop_def:
                range_uri = f"class:{prop_def["range"].replace(' ', '_')}" if "class:" not in prop_def["range"]  else prop_def["range"]
                ontology_triples.append((prop_uri, "rdfs:range", range_uri))
        return ontology_triples

    def _generate_instance_triples(self):
        """Generates RDF triples for instances of classes defined in self.ontology."""
        instance_triples = []
        for instance_type, instances in self.instances.items():
            for instance_name, instance_data in instances.items():
                class_name = instance_data["class"]
                class_uri = f"class:{class_name.replace(' ', '_')}"
                instance_triples.append((instance_name, "rdf:type", class_uri))
                if "properties" in instance_data:
                    for prop_name, prop_value in instance_data["properties"].items():
                        prop_uri = f"property:{prop_name.replace(' ', '_')}"
                        if isinstance(prop_value, list):
                           for val in prop_value:
                                instance_triples.append((instance_name, prop_uri, val))
                        else:
                            instance_triples.append((instance_name, prop_uri, prop_value))
        return instance_triples

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

print("\nInstance Triples:")
for triple in generator.triples["instance_triples"]:
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

