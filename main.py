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


def calculate_return_trip(truck, last_package_address, depot_address, distances, addresses):
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
        return_time = datetime.timedelta(hours=return_distance / truck.velocity)
        truck.current_time += return_time
        truck.total_distance += return_distance

    return truck


def extract_address(address, addresses):
    for row in addresses:
        if address in row[2]:
            return int(row[0])


def calculate_route(truck, hashtable, addresses, distances):
    not_delivered = []
    for packageID in truck.shipments:
        package = hashtable.get(packageID)
        not_delivered.append(package)

    truck.shipments.clear()
    total_distance = 0.0

    while len(not_delivered) > 0:
        next_address = float('inf')
        next_package = None

        for package in not_delivered:
            truck_address = extract_address(truck.current_address, addresses)
            package_address = extract_address(package.address, addresses)
            distance = distance_between_addresses(truck_address, package_address, distances, addresses)[2]

            if distance <= next_address:
                next_address = distance
                next_package = package

        truck.shipments.append(next_package.package_id)
        not_delivered.remove(next_package)

        distance_travelled = next_address if truck.current_address != next_package.address else 0

        if distance_travelled > 0:
            delivery_time = datetime.timedelta(hours=distance_travelled / truck.velocity)
            truck.current_time += delivery_time
            total_distance += distance_travelled

        print("Truck {} delivered package {} to {} at {}. Distance traveled: {}".format(
            truck.id, next_package.package_id, next_package.address, truck.current_time, distance_travelled))

        truck.current_address = next_package.address

    truck.total_distance = total_distance

    return truck, total_distance


def total_distance(route, addresses, distances):
    total = 0
    for i in range(len(route) - 1):
        _, _, distance = distance_between_addresses(route[i], route[i + 1], distances, addresses)
        if distance is not None:
            total += distance
    return total


def main():
    # Create a hashtable with 20 buckets
    ht = HashTable()
    distances = load_distance_data('Data/Distances.csv')

    # Load the packages from the CSV file into the hashtable
    load_packages_into_hash(ht, 'Data/Packages.csv')

    addresses = load_address_data('Data/Addresses.csv')

    # Create vehicle objects
    vehicle1 = Vehicle(1, 16, 18, None, [15, 37, 31, 16, 29, 34, 40, 14, 1, 13, 20, 30], 0.0,
                       datetime.timedelta(hours=8), "4001 South 700 East")

    vehicle2 = Vehicle(2, 16, 18, None, [39, 18, 22, 21, 35, 36, 26, 19, 3, 6, 17, 12, 27, 38, 24, 23], 0.0,
                       datetime.timedelta(hours=10, minutes=20), "4001 South 700 East")

    vehicle3 = Vehicle(3, 16, 18, None, [10, 11, 5, 33, 4, 32, 25, 9, 8, 7, 28, 6, 2], 0.0,
                       datetime.timedelta(hours=9, minutes=5), "4001 South 700 East")

    vehicle1, distance1 = calculate_route(vehicle1, ht, addresses, distances)
    vehicle2, distance2 = calculate_route(vehicle2, ht, addresses, distances)

    depot_address = "4001 South 700 East"  # set this to the correct depot address
    vehicle1 = calculate_return_trip(vehicle1, vehicle1.current_address, depot_address, distances, addresses)
    vehicle2 = calculate_return_trip(vehicle2, vehicle2.current_address, depot_address, distances, addresses)

    if vehicle1.current_time <= vehicle2.current_time:
        vehicle3.start_time = vehicle1.current_time
        distance1 = vehicle1.total_distance  # update distance1 to include return trip
    else:
        vehicle3.start_time = vehicle2.current_time
        distance2 = vehicle2.total_distance  # update distance2 to include return trip

    vehicle3, distance3 = calculate_route(vehicle3, ht, addresses, distances)
    # Calculate total distance for all three trucks
    total_distance = distance1 + distance2 + distance3
    print("Total distance traveled for all three trucks: {}".format(round(total_distance, 1)))

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


if __name__ == "__main__":
    main()
