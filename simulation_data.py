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

        self.triples = {
            "notification": self._generate_notification_triples(),
            "messages": self._generate_message_triples(),
            "travel_app": self._generate_travel_app_triples(),
            "browsing_history": self._generate_browsing_history_triples(),
            "calendar_events": self._generate_calendar_event_triples(),
            "social_media": self._generate_social_media_triples(),
            "local_search": self._generate_local_search_triples(),
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
            triples.append((self.user, "receivedNotificationAbout", trip_id))
            triples.append((trip_id, "hasDestination", location))
            triples.append((trip_id, "hasTravelDate", formatted_date))
            if random.random() < 0.5:
                app = random.choice(self.travel_apps)
                triples.append((trip_id, "notifiedBy", f"app:{app.replace(' ', '_')}"))
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
            # triples.append((booking_id, "hasTravelDate", formatted_date))
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
                # Implicitly, regions are associated with countries
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

# Get some random triples from different categories
print("Random triples from notification:", generator.get_random_triples_by_category("notification", 2))
print("\nRandom triples from messages:", generator.get_random_triples_by_category("messages", 2))
print("\nRandom triples from travel_app:", generator.get_random_triples_by_category("travel_app", 2))
print("\nRandom triples from browsing_history:", generator.get_random_triples_by_category("browsing_history", 2))
print("\nRandom triples from calendar_events:", generator.get_random_triples_by_category("calendar_events", 2))
print("\nRandom triples from social_media:", generator.get_random_triples_by_category("social_media", 2))
print("\nRandom triples from local_search:", generator.get_random_triples_by_category("local_search", 2))

# # Add all generated triples to a single knowledge graph
# all_triples = []
# for category in generator.triples:
#     all_triples.extend(generator.triples[category])

# knowledge_graph = generator.add_triples_to_graph(all_triples)
# print(f"\nTotal number of triples in the generated knowledge graph: {len(knowledge_graph)}")
# # You can further process or store the 'knowledge_graph' list.
