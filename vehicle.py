import datetime


class Vehicle:
    def __init__(self, max_load, velocity, cargo, shipments, distance_covered, departure_time, current_address=None,
                 current_time=None):
        self.max_load = max_load
        self.velocity = velocity
        self.cargo = cargo
        self.shipments = shipments
        self.distance_covered = distance_covered
        self.current_address = current_address  # Actual address of the current location
        self.departure_time = departure_time
        if current_time is None:
            self.current_time = datetime.timedelta(hours=0)
        else:
            self.current_time = current_time

    def __str__(self):
        return "%s, %s, %s, %s, %s, %s, %s, %s" % (self.max_load, self.velocity, self.cargo,
                                                   self.shipments, self.distance_covered,
                                                   self.departure_time, self.current_address,
                                                   self.current_time)

    def update_time(self, travel_time):
        self.departure_time += datetime.timedelta(hours=travel_time)
