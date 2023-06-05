import copy
import datetime

from HashTable import HashTable
import csv

from vehicle import Vehicle


def load_packages_into_hash(hashtable, filename):
    with open(filename, newline='') as csvfile:
        reader = csv.reader(csvfile)
        next(reader, None)  # skip the headers
        for row in reader:
            package_id, address, city, state, zip_code, deadline, weight, notes = row

            key = package_id

            value = {'Package ID': package_id,
                     'Address': address,
                     'City': city,
                     'State': state,
                     'Zip': zip_code,
                     'Deadline': deadline,
                     'Weight': weight,
                     'Notes': notes}

            hashtable.set(key, value)


def load_distance_data(filename):
    distances = []
    with open(filename, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            distances.append([float(distance) if distance else None for distance in row])
    return distances


def calculate_route(vehicle, distances, packages, hashtable):
    current_location = 0  # assuming 0 is the starting location
    while packages:
        closest_distance = float('inf')
        closest_package = None
        for package in packages:
            current_distance = distances[current_location][int(package)]
            if current_distance is not None and current_distance < closest_distance:
                closest_distance = current_distance
                closest_package = package
        if closest_package is not None:
            vehicle.shipments.append(closest_package)
            packages.remove(closest_package)
            current_location = int(closest_package)
            vehicle.distance_traveled += closest_distance
            vehicle.current_address = hashtable.get(closest_package)['Address']
            vehicle.current_time += datetime.timedelta(hours=closest_distance / 18)
            hashtable.get(closest_package)['Arrival Time'] = str(vehicle.current_time)
        else:
            break


def main():
    # Create a hashtable with 20 buckets
    ht = HashTable(20)
    distances = load_distance_data('Data/Distances.csv')

    # Load the packages from the CSV file into the hashtable
    load_packages_into_hash(ht, 'Data/Packages.csv')

    # Create vehicle objects
    vehicle1 = Vehicle(16, 18, None, [], 0.0, "4001 South 700 East", datetime.timedelta(hours=8))
    vehicle2 = Vehicle(16, 18, None, [], 0.0, "4001 South 700 East", datetime.timedelta(hours=10, minutes=20))

    # All packages
    all_packages = list(map(str, range(1, 41)))  # assuming 40 packages from 1 to 40

    # Calculate routes for vehicles
    packages_for_vehicle1 = copy.deepcopy(all_packages)
    calculate_route(vehicle1, distances, packages_for_vehicle1, ht)

    packages_for_vehicle2 = [p for p in all_packages if p not in vehicle1.shipments]
    calculate_route(vehicle2, distances, packages_for_vehicle2, ht)

    # If there are still packages left undelivered
    while len(vehicle1.shipments) + len(vehicle2.shipments) < len(all_packages):
        # Determine the vehicle that finished their route earlier and assign new packages to that vehicle
        if vehicle1.current_time < vehicle2.current_time:
            undelivered_packages = [p for p in all_packages if p not in vehicle1.shipments]
            calculate_route(vehicle1, distances, undelivered_packages, ht)
        else:
            undelivered_packages = [p for p in all_packages if p not in vehicle2.shipments]
            calculate_route(vehicle2, distances, undelivered_packages, ht)

    # Output the shipments of each vehicle
    print("Vehicle 1 shipments: ", vehicle1.shipments)
    print("Vehicle 2 shipments: ", vehicle2.shipments)
    print("Vehicle 1 current time: ", vehicle1.current_time)
    print("Vehicle 2 current time: ", vehicle2.current_time)


if __name__ == "__main__":
    main()
