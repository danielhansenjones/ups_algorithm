class Vehicle:
    def __init__(self, max_load, velocity, cargo, shipments, distance_covered, location, departure_time):
        self.max_load = max_load
        self.velocity = velocity
        self.cargo = cargo
        self.shipments = shipments
        self.distance_covered = distance_covered
        self.location = location
        self.departure_time = departure_time

    def __str__(self):
        return "%s, %s, %s, %s, %s, %s, %s" % (self.max_load, self.velocity, self.cargo, self.shipments,
                                               self.distance_covered, self.location, self.departure_time)
