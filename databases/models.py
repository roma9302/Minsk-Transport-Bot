from databases.methods import *

class Vehicle:
    def __init__(self, number, link):
        self.number = number
        self.link = link

        

class Routes:
    def __init__(self, number, route1, route2, stops1, stops2):
        self.number = number
        self.route1 = route1
        self.route2 = route2
        self.stops1 = stops1 
        self.stops2 = stops2

