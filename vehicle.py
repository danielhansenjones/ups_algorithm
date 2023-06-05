class Vehicle:
    def __init__(self, max_load, velocity, cargo, shipments, distance_covered, location_index,
                 departure_time, current_address=None):
        self.max_load = max_load
        self.velocity = velocity
        self.cargo = cargo
        self.shipments = shipments
        self.distance_covered = distance_covered
        self.location_index = location_index  # Index of the current location in the addresses list
        self.departure_time = departure_time
        self.current_address = current_address  # Actual address of the current location

    def __str__(self):
        return "%s, %s, %s, %s, %s, %s, %s, %s" % (self.max_load, self.velocity, self.cargo, self.shipments,
                                                   self.distance_covered, self.location_index, self.departure_time,
                                                   self.current_address)
