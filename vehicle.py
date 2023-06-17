
class Vehicle:
    def __init__(self, id, max_capacity, location, shipments, velocity, current_time, distance_covered):
        self.id = id
        self.max_capacity = max_capacity
        self.location = location  # starting location
        self.shipments = shipments  # initial assigned packages for delivery
        self.delivered_packages = []  # list to hold packages that have been delivered
        self.velocity = velocity
        self.current_time = current_time
        self.distance_covered = distance_covered

    def deliver_package(self, package_id):
        self.delivered_packages.append(package_id)
