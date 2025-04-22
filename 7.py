import rdflib
from rdflib import Graph, URIRef, Literal
from rdflib.namespace import RDF, XSD, OWL, RDFS
from datetime import datetime, timedelta
import random

# Define the base URI for the 'kb' namespace
KB_BASE_URI = "http://example.org/knowledgebase/"
# # Define the base URI for the 'ontology' namespace
# KB_BASE_URI = "http://example.org/knowledgebase/ontology/"

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

        # Define ontology URIs for classes
        self.onto_user = URIRef(f"{KB_BASE_URI}User")
        self.onto_location = URIRef(f"{KB_BASE_URI}Location")
        self.onto_trip = URIRef(f"{KB_BASE_URI}Trip")
        self.onto_travel_app = URIRef(f"{KB_BASE_URI}TravelApp")
        self.onto_mode_of_transport = URIRef(f"{KB_BASE_URI}ModeOfTransport")
        self.onto_booking = URIRef(f"{KB_BASE_URI}Booking")
        self.onto_airline = URIRef(f"{KB_BASE_URI}Airline")
        self.onto_transport_company = URIRef(f"{KB_BASE_URI}TransportCompany")
        self.onto_hotel = URIRef(f"{KB_BASE_URI}Hotel")
        self.onto_attraction = URIRef(f"{KB_BASE_URI}Attraction")
        self.onto_region = URIRef(f"{KB_BASE_URI}Region")
        self.onto_event = URIRef(f"{KB_BASE_URI}Event")
        self.onto_contact = URIRef(f"{KB_BASE_URI}Contact")
        self.onto_post = URIRef(f"{KB_BASE_URI}Post")
        self.onto_friend = URIRef(f"{KB_BASE_URI}Friend")
        self.onto_search_result = URIRef(f"{KB_BASE_URI}SearchResult")
        self.onto_notification = URIRef(f"{KB_BASE_URI}Notification")
        self.onto_message = URIRef(f"{KB_BASE_URI}Message")
        self.onto_calendar_event = URIRef(f"{KB_BASE_URI}CalendarEvent")
        self.onto_social_media_interaction = URIRef(f"{KB_BASE_URI}SocialMediaInteraction")
        self.onto_local_search_query = URIRef(f"{KB_BASE_URI}LocalSearchQuery")

        # Define ontology URIs for properties
        self.pred_received_notification = URIRef(f"{KB_BASE_URI}receivedNotificationAbout")
        self.pred_has_destination = URIRef(f"{KB_BASE_URI}hasDestination")
        self.pred_has_travel_date = URIRef(f"{KB_BASE_URI}hasTravelDate")
        self.pred_notified_by = URIRef(f"{KB_BASE_URI}notifiedBy")
        self.pred_uses_mode = URIRef(f"{KB_BASE_URI}usesModeOfTransport")
        self.pred_mentioned_travel_to = URIRef(f"{KB_BASE_URI}mentionedTravelTo")
        self.pred_discussed_travel_with = URIRef(f"{KB_BASE_URI}discussedTravelWith")
        self.pred_discussed_mode_for = URIRef(f"{KB_BASE_URI}discussedTravelModeFor")
        self.pred_mentioned_date_for = URIRef(f"{KB_BASE_URI}mentionedTravelDateFor")
        self.pred_asked_about_hotel_in = URIRef(f"{KB_BASE_URI}askedAboutHotelIn")
        self.pred_booked_travel_to = URIRef(f"{KB_BASE_URI}bookedTravelTo")
        self.pred_booked_via = URIRef(f"{KB_BASE_URI}bookedVia")
        self.pred_uses = URIRef(f"{KB_BASE_URI}uses")
        self.pred_on_airline = URIRef(f"{KB_BASE_URI}onAirline")
        self.pred_operated_by = URIRef(f"{KB_BASE_URI}operatedBy")
        self.pred_includes_stay_at = URIRef(f"{KB_BASE_URI}includesStayAt")
        self.pred_located_in = URIRef(f"{KB_BASE_URI}locatedIn")
        self.pred_browsed_about = URIRef(f"{KB_BASE_URI}browsedAbout")
        self.pred_searched_for = URIRef(f"{KB_BASE_URI}searchedFor")
        self.pred_showed_interest_in = URIRef(f"{KB_BASE_URI}showedInterestIn")
        self.pred_researched_region = URIRef(f"{KB_BASE_URI}researchedRegion")
        self.pred_has_calendar_event = URIRef(f"{KB_BASE_URI}hasCalendarEvent")
        self.pred_located_at = URIRef(f"{KB_BASE_URI}locatedAt")
        self.pred_on_date = URIRef(f"{KB_BASE_URI}onDate")
        self.pred_is_related_to = URIRef(f"{KB_BASE_URI}isRelatedTo")
        self.pred_shared_post_about = URIRef(f"{KB_BASE_URI}sharedPostAbout")
        self.pred_mentions_location = URIRef(f"{KB_BASE_URI}mentionsLocation")
        self.pred_interacted_with_friend_about = URIRef(f"{KB_BASE_URI}interactedWithFriendAbout")
        self.pred_also_interested_in = URIRef(f"{KB_BASE_URI}alsoInterestedIn")
        self.pred_checked_in_at = URIRef(f"{KB_BASE_URI}checkedInAt")
        self.pred_performed_local_search = URIRef(f"{KB_BASE_URI}performedLocalSearch")
        self.pred_has_search_result = URIRef(f"{KB_BASE_URI}hasSearchResult")

        self.triples = {
            "notification": self._generate_notification_triples(),
            "messages": self._generate_message_triples(),
            "travel_app": self._generate_travel_app_triples(),
            "browsing_history": self._generate_browsing_history_triples(),
            "calendar_events": self._generate_calendar_event_triples(),
            "social_media": self._generate_social_media_triples(),
            "local_search": self._generate_local_search_triples(),
        }

    def _create_instance_uri(self, class_name, identifier=None):
        if identifier is None:
            identifier = random.randint(1000, 9999)
        return URIRef(f"{KB_BASE_URI}{class_name.lower().replace(' ', '_')}/{identifier}")

    def _get_random_location_uri(self):
        location_type = random.choice(["city", "country", "state"])
        if location_type == "city":
            city_name = random.choice(self.cities).replace(' ', '_')
            city_uri = URIRef(f"{KB_BASE_URI}location/{city_name}")
            return city_uri, self.onto_location
        elif location_type == "country":
            country_name = random.choice(self.countries)
            country_uri = URIRef(f"{KB_BASE_URI}country/{country_name}")
            return country_uri, self.onto_location
        else:
            state_name = random.choice(self.states_india).replace(' ', '_')
            state_uri = URIRef(f"{KB_BASE_URI}state/{state_name}")
            return state_uri, self.onto_location

    def _generate_notification_triples(self):
        triples = []
        for i in range(10):
            notification_uri = self._create_instance_uri("Notification", f"notif_{i}")
            triples.append((notification_uri, RDF.type, self.onto_notification))
            triples.append((self.user_uri, self.pred_received_notification, notification_uri))

            # Add the 'whenReceived' property
            received_time = datetime.now() - timedelta(hours=random.randint(1, 72)) # Simulate different reception times
            triples.append((notification_uri, URIRef(f"{KB_BASE_URI}whenReceived"), Literal(received_time, datatype=XSD.dateTime)))

            # Make notification content more generic
            if random.random() < 0.6:
                thing_type = random.choice(["TravelOffer", "EventReminder", "GeneralInfo"])
                thing_uri = self._create_instance_uri(thing_type, f"{thing_type.lower()}_{i}")
                triples.append((notification_uri, URIRef(f"{KB_BASE_URI}hasSubject"), thing_uri))
                triples.append((thing_uri, RDF.type, URIRef(f"{KB_BASE_URI}{thing_type}")))

                if thing_type == "TravelOffer" and random.random() < 0.5:
                    location_uri, location_class = self._get_random_location_uri()
                    triples.append((thing_uri, self.pred_has_destination, location_uri))
                    triples.append((location_uri, RDF.type, location_class))
                    
                elif thing_type == "EventReminder" and random.random() < 0.3:
                    event_date = datetime.now() + timedelta(days=random.randint(1, 30))
                    formatted_date = event_date.strftime("%Y-%m-%d")
                    triples.append((thing_uri, self.pred_on_date, Literal(formatted_date, datatype=XSD.date)))
                elif thing_type == "GeneralInfo" and random.random() < 0.2:
                    content = random.choice(["New features available!", "Check out our latest blog post.", "Important security update."])
                    triples.append((thing_uri, RDFS.label, Literal(content)))
            else:
                content = random.choice(["New features available!", "Check out our latest blog post.", "Important security update."])
                triples.append((thing_uri, RDFS.label, Literal(content)))

            if random.random() < 0.3:
                app_name = random.choice(self.travel_apps).replace('.', '_')
                app_uri = URIRef(f"{KB_BASE_URI}travelapp/{app_name}")
                triples.append((app_uri, RDF.type, self.onto_travel_app))
                triples.append((notification_uri, self.pred_notified_by, app_uri))
        return triples
    
    def _generate_message_triples(self):
        triples = []
        for i in range(10):
            message_uri = self._create_instance_uri("Message", i)
            triples.append((message_uri, RDF.type, self.onto_message))

            person_uri = self._create_instance_uri("Contact", random.randint(1000, 9999))
            triples.append((person_uri, RDF.type, self.onto_contact))

            location_uri, location_class = self._get_random_location_uri()
            triples.append((location_uri, RDF.type, location_class))

            if random.random() < 0.7:
                triples.append((message_uri, self.pred_mentioned_travel_to, location_uri))
                triples.append((message_uri, self.pred_discussed_travel_with, person_uri))
                triples.append((self.user_uri, self.pred_has_calendar_event, message_uri)) # Linking user to the message
            if random.random() < 0.4:
                mode = random.choice(self.modes_of_transport)
                mode_uri = URIRef(f"{KB_BASE_URI}modeoftransport/{mode}")
                triples.append((mode_uri, RDF.type, self.onto_mode_of_transport))
                triples.append((message_uri, self.pred_discussed_mode_for, location_uri))
            if random.random() < 0.3:
                travel_date = datetime.now() + timedelta(days=random.randint(1, 90))
                formatted_date = travel_date.strftime("%Y-%m-%d")
                triples.append((message_uri, self.pred_mentioned_date_for, location_uri))
            if random.random() < 0.2:
                hotel_name = random.choice(self.hotels).replace('-', '_')
                hotel_uri = URIRef(f"{KB_BASE_URI}hotel/{hotel_name}")
                triples.append((hotel_uri, RDF.type, self.onto_hotel))
                triples.append((message_uri, self.pred_asked_about_hotel_in, location_uri))
        return triples

    def _generate_travel_app_triples(self):
        triples = []
        app_name = random.choice(self.travel_apps).replace('.', '_')
        app_uri = URIRef(f"{KB_BASE_URI}travelapp/{app_name}")
        triples.append((app_uri, RDF.type, self.onto_travel_app))

        for i in range(10):
            booking_uri = self._create_instance_uri("Booking", i)
            triples.append((booking_uri, RDF.type, self.onto_booking))
            triples.append((self.user_uri, self.pred_booked_travel_to, booking_uri))
            triples.append((booking_uri, self.pred_booked_via, app_uri))

            location_uri, location_class = self._get_random_location_uri()
            triples.append((booking_uri, self.pred_has_destination, location_uri))
            triples.append((location_uri, RDF.type, location_class))

            travel_date = datetime.now() + timedelta(days=random.randint(1, 120))
            formatted_date = travel_date.strftime("%Y-%m-%d")
            triples.append((booking_uri, self.pred_has_travel_date, Literal(formatted_date, datatype=XSD.date)))

            if random.random() < 0.6:
                mode = random.choice(self.modes_of_transport)
                mode_uri = URIRef(f"{KB_BASE_URI}modeoftransport/{mode}")
                triples.append((mode_uri, RDF.type, self.onto_mode_of_transport))
                triples.append((booking_uri, self.pred_uses, mode_uri))
                if mode == "flight" and random.random() < 0.5:
                    airline_name = random.choice(self.airlines).replace('_', '_')
                    airline_uri = URIRef(f"{KB_BASE_URI}airline/{airline_name}")
                    triples.append((airline_uri, RDF.type, self.onto_airline))
                    triples.append((booking_uri, self.pred_on_airline, airline_uri))
                elif mode in ["train", "bus"] and random.random() < 0.4:
                    company_id = random.randint(1, 20)
                    company_uri = URIRef(f"{KB_BASE_URI}transportcompany/{company_id}")
                    triples.append((company_uri, RDF.type, self.onto_transport_company))
                    triples.append((booking_uri, self.pred_operated_by, company_uri))
            if random.random() < 0.4:
                hotel_name = random.choice(self.hotels).replace('-', '_')
                hotel_uri = URIRef(f"{KB_BASE_URI}hotel/{hotel_name}")
                triples.append((hotel_uri, RDF.type, self.onto_hotel))
                triples.append((booking_uri, self.pred_includes_stay_at, hotel_uri))
                triples.append((hotel_uri, self.pred_located_in, location_uri))
        return triples

    def _generate_browsing_history_triples(self):
        triples = []
        for i in range(10):
            browsing_event_uri = self._create_instance_uri("BrowsingHistory", i)
            # We might not have a specific class for each browsing action,
            # but we can link actions to the user.
            location_uri, location_class = self._get_random_location_uri()
            triples.append((location_uri, RDF.type, location_class))

            if random.random() < 0.8:
                triples.append((self.user_uri, self.pred_browsed_about, location_uri))
            if random.random() < 0.5:
                search_term = random.choice([f"things to do in {location_uri.split('/')[-1].replace('_', ' ')}", f"best hotels {location_uri.split('/')[-1].replace('_', ' ')}", f"flights to {location_uri.split('/')[-1].replace('_', ' ')}", f"train tickets to {location_uri.split('/')[-1].replace('_', ' ')}"])
                search_query_uri = self._create_instance_uri("LocalSearchQuery", f"browse_{i}")
                triples.append((search_query_uri, RDF.type, self.onto_local_search_query))
                triples.append((self.user_uri, self.pred_performed_local_search, search_query_uri))
                triples.append((search_query_uri, self.pred_searched_for, Literal(search_term)))
            if random.random() < 0.3:
                attraction_name = f"{location_uri.split('/')[-1].replace(' ', '_')}_{random.randint(1, 5)}"
                attraction_uri = URIRef(f"{KB_BASE_URI}attraction/{attraction_name}")
                triples.append((attraction_uri, RDF.type, self.onto_attraction))
                triples.append((self.user_uri, self.pred_showed_interest_in, attraction_uri))
                triples.append((attraction_uri, self.pred_located_in, location_uri))
            if random.random() < 0.2:
                region_name = random.choice(self.regions_europe)
                region_uri = URIRef(f"{KB_BASE_URI}region/{region_name}")
                triples.append((region_uri, RDF.type, self.onto_region))
                triples.append((self.user_uri, self.pred_researched_region, region_uri))
        return triples

    def _generate_calendar_event_triples(self):
        triples = []
        for i in range(5):
            calendar_event_uri = self._create_instance_uri("CalendarEvent", i)
            triples.append((calendar_event_uri, RDF.type, self.onto_calendar_event))
            triples.append((self.user_uri, self.pred_has_calendar_event, calendar_event_uri))

            event_date = datetime(2025, 5, random.randint(1, 31)) # Assuming events in May 2025
            formatted_date = event_date.strftime("%Y-%m-%d")
            triples.append((calendar_event_uri, self.pred_on_date, Literal(formatted_date, datatype=XSD.date)))

            if random.random() < 0.7:
                location_uri, location_class = self._get_random_location_uri()
                triples.append((calendar_event_uri, self.pred_located_at, location_uri))
                triples.append((location_uri, RDF.type, location_class))

            if random.random() < 0.4 and location_uri[0] == URIRef(f"{KB_BASE_URI}location/Bengaluru"):
                event_name = random.choice(self.events_bengaluru).replace(' ', '_')
                event_uri = URIRef(f"{KB_BASE_URI}event/{event_name}")
                triples.append((event_uri, RDF.type, self.onto_event))
                triples.append((calendar_event_uri, self.pred_is_related_to, event_uri))
        return triples

    def _generate_social_media_triples(self):
        triples = []
        for i in range(7):
            post_uri = self._create_instance_uri("Post", i)
            triples.append((post_uri, RDF.type, self.onto_post))
            triples.append((self.user_uri, self.pred_shared_post_about, post_uri))

            location_uri, location_class = self._get_random_location_uri()
            triples.append((location_uri, RDF.type, location_class))

            if random.random() < 0.6:
                triples.append((post_uri, self.pred_mentions_location, location_uri))
            if random.random() < 0.4:
                friend_id = random.randint(100, 500)
                friend_uri = URIRef(f"{KB_BASE_URI}friend/{friend_id}")
                triples.append((friend_uri, RDF.type, self.onto_friend))
                triples.append((self.user_uri, self.pred_interacted_with_friend_about, friend_uri))
                if random.random() < 0.5:
                    location_uri_friend, _ = self._get_random_location_uri()
                    triples.append((friend_uri, self.pred_also_interested_in, location_uri_friend))
            if random.random() < 0.3 and location_uri[0] == URIRef(f"{KB_BASE_URI}location/Bengaluru"):
                attraction_name = random.choice(self.local_attractions_bengaluru).replace(' ', '_')
                attraction_uri = URIRef(f"{KB_BASE_URI}attraction/{attraction_name}")
                triples.append((attraction_uri, RDF.type, self.onto_attraction))
                triples.append((self.user_uri, self.pred_checked_in_at, attraction_uri))
                triples.append((attraction_uri, self.pred_located_in, location_uri))
        return triples

    def _generate_local_search_triples(self):
        triples = []
        if datetime.now().month == 4 and datetime.now().year == 2025 and datetime.now().day >= 18: # Context aware
            for i in range(5):
                search_query = random.choice([f"restaurants near me", f"hotels in {random.choice(self.states_india).replace('_', ' ')}", f"tourist places in {random.choice(self.cities).replace('_', ' ')}"])
                search_query_uri = self._create_instance_uri("LocalSearchQuery", i)
                triples.append((search_query_uri, RDF.type, self.onto_local_search_query))
                triples.append((self.user_uri, self.pred_performed_local_search, search_query_uri))
                triples.append((search_query_uri, self.pred_searched_for, Literal(search_query)))

                result_type = random.choice(["restaurant", "hotel", "attraction"])
                result_id = f"{result_type}_{random.randint(1, 300)}"
                result_uri = URIRef(f"{KB_BASE_URI}{result_type}/{result_id}")
                triples.append((search_query_uri, self.pred_has_search_result, result_uri))
                triples.append((result_uri, RDF.type, URIRef(f"{KB_BASE_URI}{result_type.capitalize()}"))) # Inferring class

                if "hotel" in search_query:
                    state_name = random.choice(self.states_india).replace(" ", "_")
                    state_uri = URIRef(f"{KB_BASE_URI}state/{state_name}")
                    triples.append((state_uri, RDF.type, self.onto_location))
                    triples.append((result_uri, self.pred_located_in, state_uri))
                elif "tourist places" in search_query:
                    city_name = random.choice(self.cities).replace(" ", "_")
                    city_uri = URIRef(f"{KB_BASE_URI}location/{city_name}")
                    triples.append((city_uri, RDF.type, self.onto_location))
                    triples.append((result_uri, self.pred_located_in, city_uri))
                elif "restaurants" in search_query:
                    bengaluru_uri = URIRef(f"{KB_BASE_URI}location/Bengaluru")
                    triples.append((bengaluru_uri, RDF.type, self.onto_location))
                    triples.append((result_uri, self.pred_located_in, bengaluru_uri))
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
    
    def get_instances_with_properties(self, graph, class_uri):
        """
        Retrieves all instances of a specific class along with their properties
        from the given RDF graph.

        Args:
            graph (rdflib.Graph): The RDF graph to query.
            class_uri (rdflib.URIRef): The URI of the class to find instances of.

        Returns:
            dict: A dictionary where keys are instance URIs and values are
                  dictionaries of their properties (predicate: list of objects).
        """
        instances_with_properties = {}
        for instance in graph.subjects(RDF.type, class_uri):
            properties = {}
            for predicate, obj in graph.predicate_objects(subject=instance):
                if predicate not in properties:
                    properties[predicate] = []
                properties[predicate].append(obj)
            instances_with_properties[instance] = properties
        return instances_with_properties

    def get_travel_app_instances_with_properties(self, graph):
        """
        Retrieves all instances of the TravelApp class with their properties.

        Args:
            graph (rdflib.Graph): The RDF graph to query.

        Returns:
            dict: A dictionary of TravelApp instances and their properties.
        """
        return self.get_instances_with_properties(graph, self.onto_travel_app)

    def get_location_instances_with_properties(self, graph):
        """
        Retrieves all instances of the Location class with their properties.

        Args:
            graph (rdflib.Graph): The RDF graph to query.

        Returns:
            dict: A dictionary of Location instances and their properties.
        """
        return self.get_instances_with_properties(graph, self.onto_location)

    def get_booking_instances_with_properties(self, graph):
        """
        Retrieves all instances of the Booking class with their properties.

        Args:
            graph (rdflib.Graph): The RDF graph to query.

        Returns:
            dict: A dictionary of Booking instances and their properties.
        """
        return self.get_instances_with_properties(graph, self.onto_booking)

    def get_notification_instances_with_properties(self, graph):
        """
        Retrieves all instances of the Notification class with their properties.

        Args:
            graph (rdflib.Graph): The RDF graph to query.

        Returns:
            dict: A dictionary of Notification instances and their properties.
        """
        return self.get_instances_with_properties(graph, self.onto_notification)

    def get_calendar_event_instances_with_properties(self, graph):
        """
        Retrieves all instances of the CalendarEvent class with their properties.

        Args:
            graph (rdflib.Graph): The RDF graph to query.

        Returns:
            dict: A dictionary of CalendarEvent instances and their properties.
        """
        return self.get_instances_with_properties(graph, self.onto_calendar_event)

    def get_post_instances_with_properties(self, graph):
        """
        Retrieves all instances of the Post class with their properties.

        Args:
            graph (rdflib.Graph): The RDF graph to query.

        Returns:
            dict: A dictionary of Post instances and their properties.
        """
        return self.get_instances_with_properties(graph, self.onto_post)

    def get_local_search_query_instances_with_properties(self, graph):
        """
        Retrieves all instances of the LocalSearchQuery class with their properties.

        Args:
            graph (rdflib.Graph): The RDF graph to query.

        Returns:
            dict: A dictionary of LocalSearchQuery instances and their properties.
        """
        return self.get_instances_with_properties(graph, self.onto_local_search_query)

# Example usage (add this to the end of your if __name__ == '__main__': block)
if __name__ == '__main__':
    generator = TravelGraphGenerator()
    graph = Graph()
    graph.bind("kb", KB_BASE_URI)
    graph.bind("xsd", XSD)
    graph.bind("owl", OWL)

    for category in generator.triples:
        print(f"Adding triples for category: {category}")
        for s, p, o in generator.triples[category]:
            graph.add((s, p, o))

    print(f"\nNumber of triples in the graph: {len(graph)}")

    # Example of getting instances with properties
    notifications_with_props = generator.get_notification_instances_with_properties(graph)
    print(f"\nNotifications with properties:")
    for instance, props in notifications_with_props.items():
        print(f"- {instance}:")
        for prop, values in props.items():
            print(f"  - {prop}: {values}")

    locations_with_props = generator.get_location_instances_with_properties(graph)
    print(f"\nFirst 2 Location instances with properties:")
    for i, (instance, props) in enumerate(locations_with_props.items()):
        if i >= 2:
            break
        print(f"- {instance}:")
        for prop, values in props.items():
            print(f"  - {prop}: {values}")
    
    # Serialize the graph to a file (optional)
    graph.serialize("travel_knowledge_graph_with_classes.ttl", format="turtle")
    print("\nGraph serialized to travel_knowledge_graph_with_classes.ttl")

# if __name__ == '__main__':
#     generator = TravelGraphGenerator()
#     graph = Graph()
#     graph.bind("kb", KB_BASE_URI)
#     graph.bind("onto", KB_BASE_URI)
#     graph.bind("xsd", XSD)
#     graph.bind("owl", OWL)

#     for category in generator.triples:
#         print(f"Adding triples for category: {category}")
#         for s, p, o in generator.triples[category]:
#             graph.add((s, p, o))

#     print(f"\nNumber of triples in the graph: {len(graph)}")

#     # Example query (find all Notifications)
#     print("\nExample query: All Notifications:")
#     for notification in graph.subjects(RDF.type, generator.onto_notification):
#         print(f"- {notification}")

#     # Example query (find things the user received notifications about)
#     print("\nExample query: Things the user received notifications about:")
#     for obj in graph.objects(subject=generator.user_uri, predicate=generator.pred_received_notification):
#         print(f"- {obj} (Type: {list(graph.objects(subject=obj, predicate=RDF.type))})")
            

#     # Serialize the graph to a file (optional)
#     graph.serialize("travel_knowledge_graph_with_classes.ttl", format="turtle")
#     print("\nGraph serialized to travel_knowledge_graph_with_classes.ttl")
