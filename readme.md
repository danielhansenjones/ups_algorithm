# WGU UPS Algorithm Project

A routing application that simulates a UPS-style delivery system. This project calculates optimal delivery routes for a fleet of vehicles using various data structures and algorithms, and it provides real-time package status updates.

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Project Structure](#project-structure)
- [Requirements](#requirements)
- [Setup and Running the Application](#setup-and-running-the-application)
- [Running Tests](#running-tests)
- [Code Improvements](#code-improvements)
- [Conclusion](#conclusion)

## Overview

The WGU UPS Algorithm Project is a Python-based application designed to:
- Load package, distance, and address data from CSV files.
- Optimize delivery routes for multiple vehicles.
- Allow users to query individual package statuses in real time.

The project was originally developed on 2023/07/01 using Python 3.9.6 and requires Python 3.9 or higher.

## Features

- **Efficient Data Retrieval:**  
  Uses a hash table for quick package data lookup with an average time complexity of O(1).

- **Optimized Routing:**  
  Employs lists to construct distance matrices and address mappings, ensuring quick access and efficient calculations for determining the shortest distances.

- **Dynamic Status Updates:**  
  Supports real-time query of package statuses based on current operational time.

- **Vehicle Routing:**  
  Calculates optimal routes that accommodate delivery deadlines, minimizing total travel distance.

## Project Structure

Below is a brief description of the core modules and their purposes:

- **main.py:**  
  Entry point of the application. Handles data loading, vehicle initialization, route calculation, and user interaction.

- **vehicle.py:**  
  Contains the `Vehicle` class, which encapsulates properties and behaviors of delivery vehicles.

- **package.py:**  
  Defines the `Package` class, which includes methods for updating the package status based on delivery and departure times.

- **HashTable.py:**  
  Implements a custom hash table for package data management, including methods for setting, retrieving, and deleting entries.

## Requirements

- **Python Version:**  
  Python 3.9 or higher

- **Required Packages:**  
  - datetime (standard library)
  - csv (standard library)

Ensure these libraries are installed as part of your Python distribution.

## Setup and Running the Application

1. **Clone the Repository:**  
   Clone or download the project files to your local environment.

2. **Navigate to the Project Directory:**  
   Open a terminal and change to the project’s root directory:
   
   ```shell
   cd /path/to/project
   ```

3. **Run the Application:**  
   Execute the main script:

   ```shell
   python main.py
   ```

## Running Tests

The project includes a suite of unit tests to ensure the integrity of key functionalities. To run the tests, use the following command from the project’s root directory:

```shell
python tests.py
```

This command will automatically discover and run all tests located in the `tests` folder.


## Conclusion

The WGU UPS Algorithm Project combines efficient data structures with real-time routing calculations to manage a complex package delivery system. With continued refinements, this project can serve as a versatile tool for delivery system simulations and logistics management.

Feel free to suggest further improvements or tailor the structure based on your specific requirements. Happy coding!