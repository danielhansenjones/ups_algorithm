from HashTable import HashTable
import csv


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


def load_address_data(filename):
    addresses = []
    with open(filename, newline='') as csvfile:
        reader = csv.reader(csvfile)
        for row in reader:
            address_id, name, address = row[0], row[1], row[2]
            addresses.append((int(address_id), name, address))  # convert id to integer
    return addresses


def main():
    # Create a hashtable with 20 buckets
    ht = HashTable(20)
    distances = load_distance_data('Data/Distances.csv')

    # Load the packages from the CSV file into the hashtable
    load_packages_into_hash(ht, 'Data/Packages.csv')

    # Load the addresses from the CSV file into a list
    addresses = load_address_data('Data/Addresses.csv')

    print(addresses)


if __name__ == "__main__":
    main()
