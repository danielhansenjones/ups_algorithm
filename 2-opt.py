def calculate_route(truck, hashtable, addresses, distances):
    not_delivered = []
    truck_address_index = None

    for address in addresses:
        if address[2] == truck.current_address:
            truck_address_index = address[0]
            break

    for shipment in truck.shipments:
        package = hashtable.get(shipment)
        not_delivered.append((package.address, package))

    truck.shipments.clear()

    while len(not_delivered) > 0:
        nearest_distance = float('inf')
        nearest_package = None

        for address, package in not_delivered:
            package_address_index = None
            for address_info in addresses:
                if address_info[2] == address:
                    package_address_index = address_info[0]
                    break

            distance = distances[truck_address_index - 1][package_address_index - 1]

            if distance < nearest_distance:
                nearest_distance = distance
                nearest_package = package

        truck.shipments.append(nearest_package.package_id)
        not_delivered.remove((nearest_package.address, nearest_package))
        truck.current_address = nearest_package.address
        delivery_time = datetime.timedelta(hours=nearest_distance / 18)
        truck.current_time += delivery_time
        truck.total_distance += nearest_distance

    improved = True
    while improved:
        improved = False
        for i in range(1, len(truck.shipments) - 2):
            for j in range(i + 1, len(truck.shipments)):
                if j - i == 1: continue
                new_shipments = truck.shipments[:]
                new_shipments[i:j] = truck.shipments[j - 1:i - 1:-1]
                if total_distances(new_shipments, hashtable, addresses, distances) < total_distances(truck.shipments,
                                                                                                   hashtable, addresses,
                                                                                                   distances):
                    truck.shipments = new_shipments
                    improved = True

    return truck
