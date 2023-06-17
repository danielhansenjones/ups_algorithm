import copy
import csv
import datetime
from HashTable import HashTable
from vehicle import Vehicle
from package import Package


def load_packages_into_hash(hashtable, filename):
    with open(filename, newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader, None)  # skip the headers
        for row in reader:
            package_id, address, city, state, zip_code, deadline, weight, notes = row

            key = int(package_id)

            package = Package(package_id, address, city, state, zip_code, deadline, weight, notes)

            hashtable.set(key, package)


def load_distance_data(filename):
    distances = []
    with open(filename, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            distances.append([float(distance) if distance else None for distance in row])
    return distances


def load_address_data(filename):
    addresses = []
    with open(filename, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            id, name, address = row[0], row[1], row[2]
            addresses.append((int(id), name, address))  # convert id to integer
    return addresses


def check_package_status(hashtable, package_id, time):
    package = hashtable.get(package_id)
    if package:
        if time < package.delivery_time:
            return package.status
        else:
            return "Delivered"
    else:
        return "Package not found"


def calculate_route(vehicle, distances, packages, hashtable, address_list):
    current_location = 0
    vehicle.current_address = address_list[current_location][2]
    vehicle.current_time = datetime.datetime.now()

    while packages:
        next_package_id = min(
            packages,
            key=lambda p: distances[current_location][int(p) - 1]
            if distances[current_location][int(p) - 1] is not None
            else float('inf')
        )

        next_package = hashtable.get(int(next_package_id))
        next_location = next((i for i, address in enumerate(address_list) if address[2] == next_package.address), None)

        # Initializing travel_distance and travel_time
        travel_distance = 0
        travel_time = 0

        if distances[current_location][next_location] is not None:
            travel_distance = distances[current_location][next_location]
            travel_time = travel_distance / vehicle.velocity  # in hours

        # Updating status and time of the package
        next_package.status = "In transit"
        vehicle.update_time(travel_time)

        vehicle.shipments.append(next_package)
        packages.remove(next_package_id)

        # Update the current location and address
        current_location = next_location
        vehicle.current_address = address_list[current_location][2]

        # Mark package as delivered and update the delivery time
        next_package.status = "Delivered"
        vehicle.update_time(travel_time)

        # Update the current time and distance covered
        vehicle.current_time += datetime.timedelta(hours=travel_time)
        vehicle.distance_covered += travel_distance

        # Log the delivery information to the console
        delivery_time = vehicle.current_time.strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"Package {next_package_id} delivered to {next_package.address} at {delivery_time}"
        print(log_message)

    return vehicle


def main():
    # Create a hashtable with 20 buckets
    ht = HashTable(20)
    distances = load_distance_data('Data/Distances.csv')

    # Load the packages from the CSV file into the hashtable
    load_packages_into_hash(ht, 'Data/Packages.csv')

    addresses = load_address_data('Data/Addresses.csv')

    # Create vehicle objects
    vehicle1 = Vehicle(16, 18, None, [1, 2, 5, 7, 8, 10, 13, 14, 15, 16, 19, 20, 29, 30, 31], 0.0,
                       datetime.timedelta(hours=8), "4001 South 700 East")

    vehicle2 = Vehicle(16, 18, None, [3, 4, 9, 11, 12, 17, 18, 22, 23, 24, 26, 27, 35, 36, 38, 39], 0.0,
                       datetime.timedelta(hours=10, minutes=20), "4001 South 700 East")

    vehicle3 = Vehicle(16, 18, None, [6, 21, 25, 28, 32, 33, 34, 37, 40], 0.0,
                       datetime.timedelta(hours=9, minutes=5), "4001 South 700 East")

    # All packages
    all_packages = [str(i) for i in range(1, ht.size + 1)]  # assuming packages from 1 to hashtable size

    # Calculate routes for vehicles
    packages_for_vehicle1 = copy.deepcopy(all_packages)
    calculate_route(vehicle1, distances, packages_for_vehicle1, ht, addresses)

    packages_for_vehicle2 = [p for p in all_packages if p not in vehicle1.shipments]
    calculate_route(vehicle2, distances, packages_for_vehicle2, ht, addresses)

    packages_for_vehicle3 = [p for p in all_packages if p not in vehicle1.shipments and p not in vehicle2.shipments]
    calculate_route(vehicle3, distances, packages_for_vehicle3, ht, addresses)

    # If there are still packages left undelivered
    while len(vehicle1.shipments) + len(vehicle2.shipments) + len(vehicle3.shipments) < len(all_packages):
        # Determine the vehicle that finished their route earlier and assign new packages to that vehicle
        if vehicle1.current_time < vehicle2.current_time and vehicle1.current_time < vehicle3.current_time:
            undelivered_packages = [p for p in all_packages if p not in vehicle1.shipments]
            calculate_route(vehicle1, distances, undelivered_packages, ht, addresses)
        elif vehicle2.current_time < vehicle3.current_time:
            undelivered_packages = [p for p in all_packages if p not in vehicle2.shipments]
            calculate_route(vehicle2, distances, undelivered_packages, ht, addresses)
        else:
            undelivered_packages = [p for p in all_packages if p not in vehicle3.shipments]
            calculate_route(vehicle3, distances, undelivered_packages, ht, addresses)

    # Output the shipments of each vehicle
    print("Vehicle 1 shipments: ", vehicle1.shipments)
    print("Vehicle 2 shipments: ", vehicle2.shipments)
    print("Vehicle 3 shipments: ", vehicle3.shipments)
    print("Vehicle 1 current time: ", vehicle1.current_time)
    print("Vehicle 2 current time: ", vehicle2.current_time)
    print("Vehicle 3 current time: ", vehicle3.current_time)


if __name__ == "__main__":
    main()
