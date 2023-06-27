# The 'Package' class encapsulates all the properties of a package that needs to be delivered.
# This is an example of Object-Oriented Programming (OOP) where we encapsulate related data
# and methods into objects.
from datetime import datetime, date


class Package:
    def __init__(self, package_id, address, city, state, zip_code, deadline, weight, notes):
        self.status = None
        self.package_id = package_id
        self.address = address
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.deadline = deadline
        self.weight = weight
        self.notes = notes
        self.departure_time = None
        self.delivery_time = None

    def update_status(self, convert_datetime):
        # Convert datetime to timedelta since midnight
        convert_timedelta = datetime.combine(date.min, convert_datetime.time()) - datetime.min

        if self.delivery_time is not None and self.delivery_time < convert_timedelta:
            self.status = "Delivered"
        elif self.departure_time is not None and self.departure_time > convert_timedelta:
            self.status = "En route"
        else:
            self.status = "At Hub"

