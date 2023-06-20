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

    distance = distance_data[address_id_1][address_id_2]  # assuming ids are 1-indexed

    if distance is None:  # If the distance is None, try the reverse
        distance = distance_data[address_id_2][address_id_1]

    return address_1, address_2, distance


def calculate_route(truck, hashtable, addresses, distances):
    print("Addresses:", addresses)
    print("Distances:", distances)
    not_delivered = []
    truck_address_index = None

    for address in addresses:
        if address[2] == truck.current_address:
            truck_address_index = address[0]
            break

    for shipment in truck.shipments:
        package = hashtable.get(shipment)
        not_delivered.append(package)

    truck.shipments.clear()
    total_distance = 0.0

    while len(not_delivered) > 0:
        nearest_distance = float('inf')
        nearest_package = None
        nearest_package_address_index = None

        for package in not_delivered:
            package_address_index = None
            for address in addresses:
                if address[2] == package.address:
                    package_address_index = address[0]
                    break

            if package_address_index is None:
                continue

            _, _, distance = distance_between_addresses(truck_address_index, package_address_index, distances,
                                                        addresses)

            if distance is None:
                distance = float('inf')  # Setting a very high number when distance is None

            if distance < nearest_distance:
                nearest_distance = distance
                nearest_package = package
                nearest_package_address_index = package_address_index

        if nearest_package is None:
            break

        truck.shipments.append(nearest_package.package_id)
        not_delivered.remove(nearest_package)

        if nearest_distance < float('inf'):  # only add to total_distance if it's not inf
            delivery_time = datetime.timedelta(hours=nearest_distance / truck.velocity)
            truck.current_time += delivery_time
            total_distance += nearest_distance

        truck.current_address = nearest_package.address

        print("Truck {} delivered package {} to {} at {}. Distance traveled: {}".format(
            truck.id, nearest_package.package_id, nearest_package.address, truck.current_time, nearest_distance))

    truck.total_distance = total_distance

    return truck, total_distance


def main():
    # Create a hashtable with 20 buckets
    ht = HashTable()
    distances = load_distance_data('Data/Distances.csv')
    # Load the packages from the CSV file into the hashtable
    load_packages_into_hash(ht, 'Data/Packages.csv')

    addresses = load_address_data('Data/Addresses.csv')

    # Create vehicle objects
    vehicle1 = Vehicle(1, 16, 18, None, [15, 13, 20, 37, 14, 34, 30, 16, 31, 40, 7, 6, 32], 0.0,
                       datetime.timedelta(hours=8), "4001 South 700 East")

    vehicle2 = Vehicle(2, 16, 18, None, [3, 18, 36, 38, 23, 27, 35, 24, 19, 17, 21, 22, 26, 2, 33], 0.0,
                       datetime.timedelta(hours=10, minutes=20), "4001 South 700 East")

    vehicle3 = Vehicle(3, 16, 18, None, [5, 8, 11, 28, 25, 12, 4, 9, 1, 29, 10, 39], 0.0,
                       datetime.timedelta(hours=9, minutes=5), "4001 South 700 East")

    vehicle1, distance1 = calculate_route(vehicle1, ht, addresses, distances)
    vehicle2, distance2 = calculate_route(vehicle2, ht, addresses, distances)
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
