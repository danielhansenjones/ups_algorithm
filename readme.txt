WGU UPS Algorithm Project
This project is developed by Daniel Hansen-Jones (Student ID: 004636371). It involves creating a routing algorithm for a delivery system similar to UPS, and it was created on 2023/07/01.


Developed in Python 3.9.6
This project was developed in Python 3.9.6, and it requires Python 3.9 or higher to run. It also requires the following Python packages:
datetime
csv

Running the Application
To run the application, open a terminal window and navigate to the project directory. Then run the following command:
python main.py


Description
The application loads data from CSV files into a variety of data structures, including hash tables and lists. It uses these structures to quickly calculate optimal delivery routes for a fleet of vehicles, while also allowing users to query the status of individual packages.

Features
Rapid retrieval of package data using a hash table (average time complexity O(1))
Use of lists to represent distance matrices and address details, allowing efficient data access
Calculations of distance between two points using their IDs
Determination of package delivery status at any given time
Calculation of vehicle routing considering package delivery deadlines and the shortest distance
Core Functions
load_packages_into_hash(hashtable, filename): Reads package data from a CSV file and stores it in a hash table.
load_distance_data(filename): Reads distance data from a CSV file and stores it in a list of lists.
load_address_data(filename): Reads address data from a CSV file and stores it in a list of tuples.
check_package_status(hashtable, package_id, time): Checks the status of a package at a given time.
distance_between_addresses(address_id_1, address_id_2, distance_data, address_data): Calculates the distance between two addresses given their IDs.
calculate_return_trip(vehicle, last_package_address, depot_address, distances, addresses): Calculates the return trip of a vehicle from its last delivery address back to the depot.
calculate_route(vehicle, hashtable, addresses, distances): Determines the route for a vehicle to deliver packages while considering delivery deadlines and the shortest distance.
get_delivery_details(package): Provides delivery details for a specific package.
main(): The entry point of the program, it loads data, initiates calculations and interactions with the user.
Getting Started
The entry point of the application is the main() function, which first loads package and distance data from CSV files. It then initializes three vehicles with their respective shipments, and uses the calculate_route() function to calculate their delivery routes.

Once the data has been loaded and the routes calculated, the application prompts the user with options to check the status of a package(s) at a specific time, show delivery details including mileage, or close the program.

Conclusion
This project uses a combination of data structures and algorithms to implement a complex package delivery system. It is capable of determining the optimal route for package delivery while also providing the ability to query individual package statuses. This functionality makes it a versatile tool for managing a delivery system.