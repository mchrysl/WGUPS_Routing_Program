# Author: Margaret Chrysler, #001224428
# --> main.py file for C950 - Data Structures and Algorithms 2, Practical Assessment
# Submission number 1 on date 05/21/2021

import package_hash_table
import package
from datetime import *
from import_data import *
from truck import *

global packages_table
global distance_list
global total_trucks_mileage
global trucks_lists_tuple
global truck1
global truck2
global truck3


def print_menu():
    # Print the menu/user interface for the program
    print()
    print('1. Look Up a Package (optional: specified time)')
    print('2. Look Up all Packages Statuses at a User Specified Time')
    print('3. Total Distance Traveled by Trucks')
    print('99. Exit program')


# Actions to take when certain menu inputs are selected
# Big O: O(N) - from menu_input 2 looping through the hash table to print all packages
def menu_feedback(menu_input):
    # Needed global variables:
    global total_trucks_mileage
    global trucks_lists_tuple
    global truck1
    global truck2
    global truck3

    if menu_input == 1:
        # Output information for a single package
        # Big-O: worst case is O(1) - just runs once, no runs through the package hash table
        print()
        print('Look Up a Package')
        try:
            input_package = int(input('Look Up which Package Number? '))
            if 1 <= input_package <= len(packages_table.get_id_list()):
                include_time = input('Would you like to check the packages at a specific time (Yes or No)? ')
                if include_time[0].upper() == 'Y':
                    time_input = input('Enter the time in military time (i.e., 13:00 is 1:00 PM): ')
                    try:
                        time_to_check = datetime.strptime(time_input, "%H:%M").time()
                        call_package = packages_table.search(input_package)
                        call_package.print_package_at_time(time_to_check)
                    except ValueError:
                        print('Not a valid time. Leaving section to main menu.')
                elif include_time[0].upper() == 'N':
                    call_package = packages_table.search(input_package)
                    call_package.print_package()
                else:
                    print('Not a valid answer. Leaving section to main menu.')
            else:
                print('Not a valid package ID. Leaving section to main menu.')
        except ValueError:
            print('Not a valid package ID. Leaving section to main menu.')

    if menu_input == 2:
        # Output all packages statuses at a given point in time
        # Big-O: worst case is O(N) to print each package's information
        # Learning: try-except in Python instead of try-catch
        try:
            print()
            print('Please choose within our loading and delivery times of 6:00 AM (06:00) and 6:00pm (18:00)')
            input_string = input('Enter the time to show packages statuses ("HH:MM" from 06:00 - 17:59): ')
            print('input_string:', input_string)
            time_to_check = datetime.strptime(input_string, "%H:%M").time()
            print('time_to_check', time_to_check)
            min_time = time(6, 0)
            max_time = time(18, 0)
            if min_time <= time_to_check <= max_time:
                for pid in packages_table.get_id_list():
                    packages_table.search(pid).print_package_at_time(time_to_check)
        except ValueError:
            print('Not a valid time. Leaving selection to main menu.')

    if menu_input == 3:
        # Output the total mileage for all the deliveries
        # Big-O: worst cases is O(1)
        print()
        print('Total Distance Traveled by all trucks:', total_trucks_mileage)


# This is where it starts -- the main method
# Note: it does not have a specific definition like C++
if __name__ == '__main__':
    # Import data from .csv files
    print('Reading in .csv data files...', end='')
    distance_list = fill_distance_table()
    packages_table = fill_package_table()
    total_trucks_mileage = 0
    print('done. \n')

    # Sort the packages into queues for the trucks
    print('Sorting packages into trucks...', end='')
    full_package_list = packages_table.get_package_list()
    # print('full_package_list in main:', full_package_list)
    # print('full_package_list in main - length:', len(full_package_list))
    trucks_lists_tuple = packages_to_trucks(full_package_list)
    print('done. \n')

    # Find the shortest route for each truck
    print('Find shortest route for each truck...')
    # Truck1
    print('Truck1...', end='')
    truck1 = Truck(trucks_lists_tuple[0])
    truck1.organize_truck_route(packages_table, distance_list)
    print('done.')
    # Truck2
    print('Truck2...', end='')
    truck2 = Truck(trucks_lists_tuple[1])
    truck2.organize_truck_route(packages_table, distance_list)
    print('done.')
    # Truck3 --> has to update address for package 9 to 410 S State St
    print('Truck3...', end='')
    truck3 = Truck(trucks_lists_tuple[2])
    packages_table.search(9).update_address("410 S State St")
    truck3.organize_truck_route(packages_table, distance_list)
    print('done.\n')

    # Deliver Packages
    print('Deliver Packages')
    # Set up departure date_time for each truck
    truck_date = date.today()
    t1_depart_date_time = datetime(truck_date.year, truck_date.month, truck_date.day, 8, 0, 0)
    t2_depart_date_time = datetime(truck_date.year, truck_date.month, truck_date.day, 9, 6, 0)
    # Note: Departure time for truck3 is determined after either truck1 or truck2 return
    # Run deliveries for truck1
    print('Truck1...depart time:', t1_depart_date_time)
    t1_endtime_mileage = truck1.deliver_packages(packages_table, distance_list, t1_depart_date_time)
    # Run deliveries for truck2
    print('Truck2...depart time:', t2_depart_date_time)
    t2_endtime_mileage = truck2.deliver_packages(packages_table, distance_list, t2_depart_date_time)
    # Truck 3 depart time cannot be established until either truck1 or truck2 is back
    # However, the depart time must wait until at least 10:20 AM for package #9's address change
    pkg9_readdress_hour = 10
    pkg9_readdress_minute = 20
    truck_date = date.today()
    pkg9_readdress_date_time = datetime(truck_date.year, truck_date.month, truck_date.day,
                                        pkg9_readdress_hour, pkg9_readdress_minute, 0)
    t3_depart_hour = 0
    t3_depart_minute = 0
    # Determine if truck1 or truck2 came back first or if the truck has to wait for readdressing of package 9
    if truck2.date_time > truck1.date_time > pkg9_readdress_date_time:
        t3_depart_hour = truck1.date_time.hour
        t3_depart_minute = truck1.date_time.minute + 1  # Go to the next minute just in case there are seconds
    elif truck1.date_time > truck2.date_time > pkg9_readdress_date_time:
        t3_depart_hour = truck2.date_time.hour
        t3_depart_minute = truck2.date_time.minute + 1  # Go to the next minute just in case there are seconds
    else:
        t3_depart_hour = pkg9_readdress_hour
        t3_depart_minute = pkg9_readdress_minute

    t3_depart_date_time = datetime(truck_date.year, truck_date.month, truck_date.day,
                                   t3_depart_hour, t3_depart_minute, 0)
    print('Truck3...depart time:', t3_depart_date_time)
    # Run deliveries for truck3
    t3_endtime_mileage = truck3.deliver_packages(packages_table, distance_list, t3_depart_date_time)
    # Output end times for all the trucks
    print('Truck1 deliveries completed at:', t1_endtime_mileage[0].time())
    print('Truck1 mileage:', t1_endtime_mileage[1])
    print('Truck2 deliveries completed at:', t2_endtime_mileage[0].time())
    print('Truck2 mileage:', t2_endtime_mileage[1])
    print('Truck3 deliveries completed at:', t3_endtime_mileage[0].time())
    print('Truck3 mileage:', t3_endtime_mileage[1])
    # Find value of the global variable for mileage
    total_trucks_mileage = t1_endtime_mileage[1] + t2_endtime_mileage[1] + t3_endtime_mileage[1]
    print('Trucks\' total mileage:', total_trucks_mileage)

    # Done initializing/processing data
    print('Done processing data.\n\n')

    # A basic command line user interface
    print_menu()

    # Get input on what to do from user
    action_input = input('Type number 1, 2, 3, or 99 and press enter: ')
    # Decide what menu action to take
    while action_input != '99':
        invalid_flag = False
        if action_input.isdigit():
            action_input = int(action_input)
            if action_input in {1, 2, 3}:
                menu_feedback(action_input)
                print_menu()
            else:
                invalid_flag = True
        else:
            invalid_flag = True

        if invalid_flag:
            action_input = None
            print()
            print('Invalid Input. Please select a number from the menu:')
            print_menu()
        action_input = input('Type number 1, 2, 3, or 99 and press enter: ')

    print('End of Program. Good Bye')
