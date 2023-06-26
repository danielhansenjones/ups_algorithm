import csv
import datetime
from HashTable import HashTable
from vehicle import Vehicle
from package import Package


# The 'load_packages_into_hash' function reads data from a CSV file and stores it into a hash table.
# The hash table is an optimal data structure in this scenario due to its ability to perform
# lookup, insert and delete operations in O(1) average time complexity. This allows for the
# rapid retrieval of package data using the package ID.
def load_packages_into_hash(hashtable, filename):
    with open(filename, newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader, None)  # skip the headers
        for row in reader:
            package_id, address, city, state, zip_code, deadline, weight, notes = row

            key = int(package_id)

            package = Package(package_id, address, city, state, zip_code, deadline, weight, notes)

            hashtable.set(key, package)


# The 'load_distance_data' function reads the distances from a CSV file and stores it into a list of lists.
# This data structure is chosen because it can represent a 2D matrix well, allowing to store distances
# between any two points in an easily accessible format. The time complexity for accessing an element
# is O(1), which is very efficient.
def load_distance_data(filename):
    distances = []
    with open(filename, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            distances.append([float(distance) if distance else None for distance in row])
    return distances


# The 'load_address_data' function reads data from a CSV file and stores it into a list of tuples.
# This is a suitable data structure because it allows us to store and access related data in a structured format.
# The time complexity for accessing an element is O(1), making it a v
def load_address_data(filename):
    addresses = []
    with open(filename, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            id, name, address = row[0], row[1], row[2]
            addresses.append((int(id), name, address))  # convert id to integer
    return addresses


# The 'check_package_status' function retrieves the package's status from the hashtable using the package_id.
# It then compares the time with the package's delivery_time to determine the package's current status.
# We are using hashtable because of its O(1) average time complexity for lookup operations, which allows
# us to efficiently find the package's status.
def check_package_status(hashtable, package_id, time):
    package = hashtable.get(package_id)
    if package:
        package.update_status(time)
        return package.status
    else:
        return "Package not found"

# The 'distance_between_addresses' function calculates the distance between two addresses given their IDs.
# It uses list of tuples for address data and list of lists for distance data, both providing O(1) time
# complexity for accessing elements. This function first finds the two addresses in the address data and
# then uses their IDs to find the distance between them in the distance data.
def distance_between_addresses(address_id_1, address_id_2, distance_data, address_data):
    address_1 = next((address for address in address_data if address[0] == address_id_1), None)
    address_2 = next((address for address in address_data if address[0] == address_id_2), None)

    if address_1 is None or address_2 is None:
        return None

    distance = distance_data[address_id_1][address_id_2]

    if distance is None:  # If the distance is None, try the reverse
        distance = distance_data[address_id_2][address_id_1]

    if distance is None:  # if the distance is still None, warn and return None
        print(f"Warning: Distance between {address_id_1} and {address_id_2} is not defined.")
        return address_1, address_2, None  # or you can return an error/exception here

    return address_1, address_2, distance


# The 'calculate_return_trip' function calculates the return trip of a vehicle from its last delivery
# address back to the depot. It uses lists for the addresses and distances, which allow for quick and
# easy access to individual elements. This function first finds the indexes of the depot and last delivery
# address, then uses these indexes to calculate the return distance. If a valid distance is found,
# the function calculates the return time and updates the vehicle's current time and total distance.
def calculate_return_trip(vehicle, last_package_address, depot_address, distances, addresses):
    depot_address_index = None
    last_package_address_index = None

    # Find the address indexes
    for address in addresses:
        if address[2] == depot_address:
            depot_address_index = address[0]
        if address[2] == last_package_address:
            last_package_address_index = address[0]
        if depot_address_index is not None and last_package_address_index is not None:
            break

    _, _, return_distance = distance_between_addresses(last_package_address_index, depot_address_index, distances,
                                                       addresses)

    if return_distance is not None:  # if there is a valid distance
        return_time = datetime.timedelta(hours=return_distance / vehicle.velocity)
        vehicle.current_time += return_time
        vehicle.total_distance += return_distance

    return vehicle, vehicle.current_time


# The 'extract_address' function extracts the address index of a given address from a list of addresses.
# This function uses a list for the addresses, which allows for quick and easy access to individual elements.
# The time complexity of this function is O(n) as it needs to traverse through the list to find the desired address.
def extract_address(address, addresses):
    for row in addresses:
        if address in row[2]:
            return int(row[0])


def calculate_route(vehicle, hashtable, addresses, distances):
    # We use two lists to separate the packages with a deadline before EOD and those with a deadline of EOD
    # Time Complexity: O(N) for iterating over each package in vehicle.shipments
    not_delivered = []  # packages with a deadline before EOD
    eod_delivered = []  # packages with a delivery deadline of EOD

    for packageID in vehicle.shipments:
        # Hashtable retrieval: O(1) time complexity
        package = hashtable.get(packageID)
        if package.deadline == 'EOD':
            eod_delivered.append(package)
        else:
            not_delivered.append(package)

    # Clearing list: O(1) time complexity
    vehicle.shipments.clear()
    total_distance = 0.0

    # Define a helper function to deliver packages. It updates the total_distance as a side effect.
    # Time complexity for the function as a whole is O(N^2) due to the nested loop
    def deliver_packages(package_list):
        nonlocal total_distance
        while len(package_list) > 0:  # O(N)
            next_address = float('inf')
            next_package = None

            for parcel in package_list:  # O(N)
                # Assuming both extract_address and distance_between_addresses functions have O(1) time complexity
                vehicle_address = extract_address(vehicle.current_address, addresses)
                package_address = extract_address(parcel.address, addresses)
                distance = distance_between_addresses(vehicle_address, package_address, distances, addresses)[2]

                if next_package:
                    if next_package.departure_time is None:  # This is the first time the package is loaded
                        next_package.departure_time = vehicle.current_time
                    next_package.delivery_time = vehicle.current_time  # Updating the delivery time

                if distance <= next_address:
                    next_address = distance
                    next_package = parcel

            # Update the package status to "Enroute"
            next_package.status = "Enroute"

            # Appending and removing from list: O(1) time complexity
            vehicle.shipments.append(next_package.package_id)
            package_list.remove(next_package)  # Note: Removing an element from a list can be O(N) in worst case

            distance_travelled = next_address if vehicle.current_address != next_package.address else 0

            if distance_travelled > 0:
                # Assuming timedelta operation has O(1) time complexity
                delivery_time = datetime.timedelta(hours=distance_travelled / vehicle.velocity)
                vehicle.current_time += delivery_time
                total_distance += distance_travelled

                # Update the package status to "Delivered"
                next_package.status = "Delivered"
                next_package.delivered = True

            vehicle.current_address = next_package.address

    # Function calls: O(N^2) each due to the time complexity of deliver_packages function
    deliver_packages(not_delivered)
    deliver_packages(eod_delivered)

    # Assignment: O(1) time complexity
    vehicle.total_distance = total_distance
    return vehicle, total_distance


def get_delivery_details(package):
    # Prints out delivery details for a specific package
    return f"Package ID: {package.package_id}\n" \
           f"Address: {package.address}\n" \
           f"City: {package.city}\n" \
           f"State: {package.state}\n" \
           f"Zip Code: {package.zip_code}\n" \
           f"Deadline: {package.deadline}\n" \
           f"Weight: {package.weight}\n" \
           f"Notes: {package.notes}\n" \
           f"Delivered: {'Yes' if package.delivered else 'No'}\n"


# The 'main' function is the entry point of the program. This function orchestrates the whole process
# of loading the package and distance data, initializing the vehicles, calculating the routes,
# and printing out the results. It uses a hashtable for storing package data and lists for storing
# addresses and distances.
def main():
    print("Welcome to the delivery routing system.")
    print("Please select an option:")
    print("1: Check the status of a package at a specific time.")
    print("2: Check delivery details for a specific package.")
    print("3: Show all delivery details.")
    user_input = int(input("Your choice: "))
    # Create a hashtable with 20 buckets
    ht = HashTable()
    distances = load_distance_data('Data/Distances.csv')

    # Load the packages from the CSV file into the hashtable
    load_packages_into_hash(ht, 'Data/Packages.csv')

    # The list structure allows efficient iteration through all addresses when needed.
    addresses = load_address_data('Data/Addresses.csv')

    # Vehicle objects are created with specified properties including maximum capacity, velocity,
    # initial shipments, etc. Object-Oriented Programming (OOP) is used here to encapsulate related data
    # and methods into objects.
    vehicle1 = Vehicle(1, 16, 18, None, [15, 37, 31, 16, 29, 34, 40, 14, 1, 13, 20, 30], 0.0,
                       datetime.timedelta(hours=8), "4001 South 700 East")

    vehicle2 = Vehicle(2, 16, 18, None, [6, 18, 22, 21, 35, 36, 26, 19, 3, 39, 17, 12, 27, 38, 24, 23], 0.0,
                       datetime.timedelta(hours=10, minutes=20), "4001 South 700 East")

    vehicle3 = Vehicle(3, 16, 18, None, [10, 11, 5, 33, 4, 32, 25, 9, 8, 7, 28, 6, 2], 0.0,
                       datetime.timedelta(hours=9, minutes=5), "4001 South 700 East")

    # The `calculate_route` function calculates the delivery route for each vehicle and returns the
    # vehicle object and the total distance traveled.
    vehicle1, distance1 = calculate_route(vehicle1, ht, addresses, distances)
    vehicle2, distance2 = calculate_route(vehicle2, ht, addresses, distances)

    # The `calculate_return_trip` function calculates the return trip of each vehicle from its last
    # delivery address back to the depot.
    depot_address = "4001 South 700 East"

    vehicle1, return_time1 = calculate_return_trip(vehicle1, vehicle1.current_address, depot_address, distances,
                                                   addresses)
    vehicle2, return_time2 = calculate_return_trip(vehicle2, vehicle2.current_address, depot_address, distances,

                                                   addresses)
    # The start time for the third vehicle is determined based on the return times of the first two vehicles.
    # The third vehicle starts after the vehicle that returns earlier.
    if return_time1 <= return_time2:
        vehicle3.start_time = return_time1
        vehicle3.current_time = return_time1
    else:
        vehicle3.start_time = return_time2
        vehicle3.current_time = return_time2

    # Here, start vehicle3's journey after finding the truck that returned first and updated the return time.
    vehicle3, distance3 = calculate_route(vehicle3, ht, addresses, distances)
    # Calculate total distance for all three vehicles
    total_distance = distance1 + distance2 + distance3

    if user_input == 1:
        package_id = int(input("Please enter a package id: "))
        time_str = input("Please enter a time (HH:MM:SS): ")
        time_obj = datetime.datetime.strptime(time_str, '%H:%M:%S')
        # Assuming package_status function is defined, which accepts time_obj and returns package status at that time.
        package = ht.get(package_id)
        print(check_package_status(ht, package_id, time_obj))

    elif user_input == 2:
        package_id = int(input("Please enter a package id: "))
        # Assuming package_delivery_details function is defined, which accepts package_id and returns delivery details.
        package = ht.get(package_id)
        if package:
            print(get_delivery_details(package))
        else:
            print("Package not found.")

    elif user_input == 3:
        print("Total distance traveled for all three vehicles: {}".format(round(total_distance, 1)))

        # Output the shipments of each vehicle
        print("Vehicle 1 shipments: ", vehicle1.shipments)
        print("Vehicle 2 shipments: ", vehicle2.shipments)
        print("Vehicle 3 shipments: ", vehicle3.shipments)
        print("Vehicle 1 current time: ", vehicle1.current_time)
        print("Vehicle 2 current time: ", vehicle2.current_time)
        print("Vehicle 3 current time: ", vehicle3.current_time)
        print("Vehicle 1 total distance: ", vehicle1.total_distance)
        print("Vehicle 2 total distance: ", vehicle2.total_distance)
        print("Vehicle 3 total distance: ", vehicle3.total_distance)

    else:
        print("Invalid option. Please choose a number between 1 and 3.")


if __name__ == "__main__":
    main()
