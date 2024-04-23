import datetime


# The 'Vehicle' class encapsulates all the properties of a vehicle used for package delivery.
# This is an example of Object-Oriented Programming (OOP) where we encapsulate related data
# and methods into objects.

class Vehicle:
    def __init__(self, id, max_load, velocity, cargo, shipments, distance_travelled, departure_time,
                 current_address=None):
        self.id = id
        self.max_load = max_load
        self.velocity = velocity
        self.cargo = cargo
        self.shipments = shipments
        self.distance_travelled = distance_travelled
        self.current_address = current_address
        self.departure_time = departure_time
        self.current_time = departure_time
        self.total_distance = 0.0

    def __str__(self):
        return (f"ID: {self.id}, Max Load: {self.max_load}, Velocity: {self.velocity}, "
                f"Cargo: {self.cargo}, Shipments: {self.shipments}, Distance Travelled: {self.distance_travelled}, "
                f"Departure Time: {self.departure_time}, Current Address: {self.current_address}, "
                f"Current Time: {self.current_time}, Total Distance: {self.total_distance}")

