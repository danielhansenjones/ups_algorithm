import datetime


# The 'Vehicle' class encapsulates all the properties of a vehicle used for package delivery.
# This is an example of Object-Oriented Programming (OOP) where we encapsulate related data
# and methods into objects.

class Vehicle:
    def __init__(self, id, max_load, velocity, cargo, shipments, distance_travelled, departure_time,
                 current_address=None):
        self.id = id  # Add the id attribute
        self.max_load = max_load
        self.velocity = velocity
        self.cargo = cargo
        self.shipments = shipments
        self.distance_travelled = distance_travelled
        self.current_address = current_address
        self.departure_time = departure_time
        self.current_time = departure_time
        self.total_distance = 0.0  # Initialize total distance to zero

    def __str__(self):
        return "%s, %s, %s, %s, %s, %s, %s, %s, %s ,%s" % (self.id, self.max_load, self.velocity, self.cargo,
                                                           self.shipments, self.distance_travelled,
                                                           self.departure_time, self.current_address,
                                                           self.current_time, self.distance_travelled)
