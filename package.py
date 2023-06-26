# The 'Package' class encapsulates all the properties of a package that needs to be delivered.
# This is an example of Object-Oriented Programming (OOP) where we encapsulate related data
# and methods into objects.

class Package:
    def __init__(self, package_id, address, city, state, zip_code, deadline, weight, notes):
        self.package_id = package_id
        self.address = address
        self.city = city
        self.state = state
        self.zip_code = zip_code
        self.deadline = deadline
        self.weight = weight
        self.notes = notes
        self.status = "At hub"
        self.delivered = False
