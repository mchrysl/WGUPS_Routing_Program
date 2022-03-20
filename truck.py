# Author: Margaret Chrysler, #001224428
# --> truck.py file for C950 - Data Structures and Algorithms 2, Practical Assessment
# Submission number 1 on date 05/21/2021

# a class for the delivery trucks and their specific information
from main import *
import main as m
from import_data import *

# Declare as global variables for sorting
global packages_with_notes_list
global packages_no_notes_list
global pkg_notes_2_trucks
global pkg_no_notes_2_trucks
global truck1_list
global truck2_list
global truck3_list


class Truck:

    def __init__(self, package_ids):
        self.package_queue = package_ids.copy()
        self.current_package_id = -1
        self.max_load = len(package_ids)       # Later define to be 16
        # Initial hub_departure_time and date_time set to today midnight for instantiation purposes only
        self.hub_departure_time = time(0, 0, 0)
        self.mileage = 0
        self.date_time = self.hub_departure_time

    # Deliver the packages of a truck once the truck's package list has been sorted
    # Big-O: O(N)
    def deliver_packages(self, pkgs_table, distance_table, hub_depart_time):
        # First, set the start time for the route and begin the tracking variable date_time
        self.hub_departure_time = hub_depart_time
        self.date_time = self.hub_departure_time
        # Next, update delivery_status of the packages to "en route" with the departure time
        for pid in self.package_queue:
            pkgs_table.search(pid).update_package_status('en route', self.hub_departure_time.time())

        # List the packages to be delivered
        print('Number of packages to deliver:', len(self.package_queue))
        print()

        # Deliver the packages
        while len(self.package_queue) > 0:       # While there is at least one entry in the truck's package_list
            # If it's the first delivery (current_package = -1)
            if self.current_package_id < 0:
                # Assign WGU HUB as start_address5
                start_address = '4001 South 700 East'       # WGU Hub address
            else:
                # Assign current_package's address as the start address
                start_address = pkgs_table.search(self.current_package_id).get_address()

            # Pull a new current_package from the package_list
            temp_current_id = self.package_queue.pop(0)
            print('Current delivery, package ID:', temp_current_id)
            self.current_package_id = temp_current_id
            # Get next ("current") delivery address using current_package
            temp_pack = pkgs_table.search(temp_current_id)
            # FOR TROUBLESHOOTING: print('the associated package:', temp_pack)
            end_address = temp_pack.get_address()
            print('Start_address:', start_address, end='')
            print(' End_address:', end_address, end='')

            # Find current_distance to next delivery (use start & end addresses in the distance table)
            delivery_distance = float(m.get_distance(distance_table, start_address, end_address))
            print('  Delivery Distance:', delivery_distance, '  ', end='')

            # Add current_distance to truck's mileage
            self.mileage = round(self.mileage + delivery_distance, 1)
            print('Truck mileage:', self.mileage)

            # Update truck's time (specified miles/hour = 18 ==> 18miles/60minutes)
            # FOR TROUBLESHOOTING: print('Add to time:', delivery_distance/(18/60))
            minutes = int(delivery_distance/(18/60))
            # FOR TROUBLESHOOTING: print('minutes:', minutes)
            seconds = int(((delivery_distance/(18/60)) - minutes) * 60)
            print('Time to deliver, in seconds:', seconds, end='')
            print(' Start time:', self.date_time.time(), end='')
            self.date_time = self.date_time + timedelta(minutes=minutes, seconds=seconds)
            print(' Time of delivery:', self.date_time.time(), end='')
            print(' Delivery deadline:', temp_pack.get_delivery_deadline())

            # Update the package's status
            # FOR TROUBLESHOOTING: print('Status timeline before delivery:', end='')
            temp_pack.update_package_status('delivered', self.date_time.time())     # The actual update
            # FOR TROUBLESHOOTING: print('Status timeline after delivery:', end='')
            d_status_list = temp_pack.get_delivery_status()
            print('Delivery Status Timeline: ', end='')
            for s in d_status_list:
                print(s[0].capitalize() + ' at ' + str(s[1]) + ', ', end='')
            print()

            print('Packages left to deliver:', len(self.package_queue))
            print()
            # Pause between each package delivery - FOR TESTING
            # pause_input = input('press enter to continue delivery run')
            # if pause_input == '':
            #     pass

        return [self.date_time, self.mileage]

    def organize_truck_route(self, pkgs_table, dist_list):
        # Get the package objects so program doesn't always have to "search" --> this is something to do better later
        # For this method, a tuple is created so the list can be sorted into delivery deadline groups
        # Big-O: O(N)
        list_of_packages = []
        for pid in self.package_queue:
            pkg = pkgs_table.search(pid)
            # print('package_id:', pid, 'deadline:', pkg.get_delivery_deadline(), ' package:', pkg)
            list_of_packages.append(pkg)

        # Sort so all package ids with time specific deadlines are in the queue/list first
        truck_packages_sort_list = []
        for pkg in list_of_packages:
            # Extract delivery time from the input type string
            input_time = pkg.get_delivery_deadline()
            time_list = input_time.split()
            # FOR TROUBLESHOOTING: print('time_list', time_list)

            if time_list[0] != 'EOD':
                # Strip out just the time as a time object
                delivery_time = datetime.strptime(time_list[0], '%H:%M').time()
                # Update time for 24 hour clock
                if time_list[1] == 'PM':
                    delivery_time = (datetime.strptime(time_list[0], '%H:%M') + timedelta(hours=12, minutes=0)).time()
                    # FOR TROUBLESHOOTING: print('delivery time plus 12 hours:', delivery_time)
                # Back to a string object
                delivery_time_string = time.strftime(delivery_time, '%H:%M')
                # FOR TROUBLESHOOTING: print('delivery_time:', delivery_time_string)

                # Append to remaining_delivery_list the processed tuple of (pkg, delivery_time_string)
                truck_packages_sort_list.append((pkg.get_id(), delivery_time_string))
            else:
                # Append to remaining_delivery_list the tuple of (pkg, 'EOD')
                truck_packages_sort_list.append((pkg.get_id(), 'EOD'))

        # Sort by the second entry in the tuple (delivery deadline)
        truck_packages_sort_list.sort(key=lambda x: x[1])
        # print('packages list in delivery order')
        # print(truck_packages_sort_list)

        # Refresh the truck's package queue to the sorted list
        self.package_queue.clear()
        for pid, d in truck_packages_sort_list:
            self.package_queue.append(pid)

        # Next Section: Find the shortest route within each delivery deadline group
        # Show the list before sorting
        # print('Sorting the following list')
        # for pid in self.package_queue:
        #     print(pid, ' ', end='')
        # print()

        # Build a queue to deliver the packages in order:
        delivery_queue = []
        # Create a copy of the truck's package queue to send to nearest neighbor sort to find same addresses
        # This will be manipulated to prevent duplicate package numbers in final delivery queue
        # Remove any id appended to delivery_sublist or in nearest neighbor sorted_package_id_list
        truck_package_id_list = self.package_queue.copy()

        # Split lists: one for each unique early delivery deadline and one for End Of Day deadline
        last_delivery_deadline = ''
        last_address = '4001 South 700 East'  # initialize to the hub address - starting point
        delivery_sublist = []  # To create a list of package ids that have the same deadline

        # Split out the sub-lists of the table
        for pid in self.package_queue:
            # print('last_delivery_deadline:', last_delivery_deadline)
            # print('current delivery deadline:', pkgs_table.search(pid).get_delivery_deadline())
            if last_delivery_deadline == pkgs_table.search(pid).get_delivery_deadline() and pid not in delivery_queue:
                # If the delivery deadline is the same as the previous and is not already in delivery queue,
                # add the id to the sub-list
                delivery_sublist.append(pid)
                # remove from the truck_package_id_list
                truck_package_id_list.remove(pid)
                # print('delivery_sublist:', delivery_sublist)
            elif last_delivery_deadline != pkgs_table.search(pid).get_delivery_deadline():
                if len(delivery_sublist) == 0:
                    # The first entry in the sublist
                    # print('[if] Sublist should be empty:', delivery_sublist)
                    # Append the package id to start the subset
                    delivery_sublist.append(pid)
                    # remove from the truck_package_id_list
                    truck_package_id_list.remove(pid)
                    # Update the last_delivery_deadline to the value for this new sublist
                    last_delivery_deadline = pkgs_table.search(pid).get_delivery_deadline()
                    # print('[if] Begin new sublist', delivery_sublist)

                elif len(delivery_sublist) > 0:     # Condition: found the start of the next sublist
                    # Sort and finish the current sublist
                    # print('[elif] sublist of delivery deadlines:', delivery_sublist)

                    # Send the list to return a time constrained (sub)-list sorted by nearest neighbor
                    sorted_delivery_sublist = nearest_neighbor_sort(pkgs_table, dist_list, truck_package_id_list,
                                                                    delivery_sublist, last_address)
                    # print('[elif] sorted delivery addresses:', sorted_delivery_sublist)

                    # Add the returned list to the end of delivery_queue
                    delivery_queue.extend(sorted_delivery_sublist)
                    # print('[elif] delivery_queue:', delivery_queue)
                    # print('length delivery_queue:', len(delivery_queue))
                    # print('[elif] last_id:', pkgs_table.search(delivery_queue[len(delivery_queue) - 1]).get_id(),
                    #      'last_address:', pkgs_table.search(delivery_queue[len(delivery_queue) - 1]).get_address())
                    last_address = pkgs_table.search(delivery_queue[len(delivery_queue) - 1]).get_address()

                    # Clear the list to start on the next delivery deadline sublist
                    delivery_sublist.clear()

                    # Begin the next sublist
                    # print('[elif] Sublist should be empty:', delivery_sublist)
                    # Append the package id to start the subset
                    if pid not in delivery_queue:
                        delivery_sublist.append(pid)
                        # remove from the truck_package_id_list
                        truck_package_id_list.remove(pid)
                    # Update the last_delivery_deadline to the value for this new sublist
                    last_delivery_deadline = pkgs_table.search(pid).get_delivery_deadline()
                    # print('[elif] Begin new sublist', delivery_sublist)

        # Sort final sublist and finish truck's delivery_queue
        if len(delivery_sublist) > 0:  # Condition: found the start of the next sublist
            # Sort and finish the current sublist
            # print('[elif] sublist of delivery deadlines:', delivery_sublist)
            # Send the list to return a (sub)-list sorted by nearest neighbor
            sorted_delivery_sublist = nearest_neighbor_sort(pkgs_table, dist_list, truck_package_id_list,
                                                            delivery_sublist, last_address)
            # print('[elif] sorted delivery addresses:', sorted_delivery_sublist)
            # Add the returned list to the end of delivery_queue
            delivery_queue.extend(sorted_delivery_sublist)
            # FOR TROUBLESHOOTING:
            # print('delivery_queue:', delivery_queue)
            # print('length delivery_queue:', len(delivery_queue))

        self.package_queue = delivery_queue.copy()


def nearest_neighbor_sort(pkgs_table, dist_list, truck_package_id_list, delivery_sublist, last_address):
    # Sort the sublist parameter using nearest neighbor algorithm
    # This is a self-adjusting part of the program -- Big O complexity: O(N**2)

    # Declare needed variables for the sorted list and first package id in delivery_sublist
    sorted_package_id_list = []  # The sorted list that will be returned
    compare_list = delivery_sublist.copy()

    # If the delivery_sublist is only one entry, it is the first (and only) entry in sorted_package_id_list
    if len(delivery_sublist) == 1:
        sorted_package_id_list.append(delivery_sublist[0])
        # Remove the first item from the compare_list (it is in the sorted list)
        compare_list.remove(delivery_sublist[0])

    elif len(delivery_sublist) > 1:
        # If there is more than one entry in delivery_sublist, sort finding nearest neighbors

        # Shortest distance for comparison in loop which finds the nearest neighbor from the remaining list
        shortest_distance = [999, 999.9]  # Start lowest distance search with an unreasonably large entry

        # Find the nearest neighbor of what is left in the list until there are no list entries left
        while len(compare_list) > 0:
            # The for loop determines a list containing the package id with the shortest delivery distance
            for c_pid in compare_list:
                c_pid_address = pkgs_table.search(c_pid).get_address()
                c_pid_distance = get_distance(dist_list, last_address, c_pid_address)
                if c_pid_distance < shortest_distance[1]:
                    shortest_distance = [c_pid, c_pid_distance]

            sorted_package_id_list.append(shortest_distance[0])     # Append nearest neighbor id to sorted list
            # Note: Removing id from full package list was done when the delivery_sublist was made

            # If any addresses in the (full) delivery list match the address associated with the shortest distance,
            # add that ID to the list.
            for pid in truck_package_id_list:
                if pid != shortest_distance[0] and \
                        pkgs_table.search(pid).get_address() == pkgs_table.search(shortest_distance[0]).get_address():
                    # Add package id with same address to the sorted list
                    sorted_package_id_list.append(pid)
                    # remove from the truck_package_id_list
                    truck_package_id_list.remove(pid)
            # print('shortest_distance values: ', shortest_distance[0], shortest_distance[1])
            # print('compare_list:', compare_list)
            last_address = pkgs_table.search(shortest_distance[0]).get_address()  # Update latest address
            compare_list.remove(shortest_distance[0])      # Update compare list - remove n.n. package id
            # print('compare list length:', len(compare_list))
            # print('sorted_package_id_list:', sorted_package_id_list)
            # print('compare_list:', compare_list)
            shortest_distance = [999, 999.9]  # Reset lowest distance search with an unreasonably large entry

    return sorted_package_id_list


# Sorts the initial package list into trucks - called from main
# Big-O: O(N**2)
# Could be better optimized - later
def packages_to_trucks(all_packages_list):

    # This method needs all global variables (?)
    global packages_with_notes_list
    global packages_no_notes_list
    global pkg_notes_2_trucks
    global pkg_no_notes_2_trucks
    global truck1_list
    global truck2_list
    global truck3_list

    # Split the packages with special notes from the full packages list to handle first
    packages_with_notes_list = []
    packages_no_notes_list = []
    # print('packages_to_trucks', all_packages_list)
    # print('packages_to_trucks length:', len(all_packages_list))

    # See if each package has a special note,
    # if so, add that package to the packages_with_notes_list
    # and remove it from the all_packages_list
    for pk in all_packages_list:
        # print('package id:', pk.get_id(), 'package notes*', pk.get_notes(), '*')
        if pk.get_notes():
            # Print('put in the with notes list', pk.get_id)
            packages_with_notes_list.append(pk)
        else:
            packages_no_notes_list.append(pk)

    # Output to track results
    # print('packages_no_notes_list count:', len(packages_no_notes_list))
    # for pnnl in packages_no_notes_list:
    #     print('package #:', pnnl.get_id(), 'note:', pnnl.get_notes())
    #     print('packages_with_notes_list count:', len(packages_with_notes_list))
    # for pwnl in packages_with_notes_list:
    #     print('package #:', pwnl.get_id(), 'note:', pwnl.get_notes())

    # Pull out of packages_with_notes_list each Truck 2 package and put it in a list for truck 2
    pkg_notes_2_trucks = []    # Packages with notes sent to trucks lists
    pkg_no_notes_2_trucks = []  # Packages with no notes sent to trucks lists
    truck2_list = []
    # print()
    # print('truck2 list length @ start:', len(truck2_list))      # Should be zero (0)
    # print('packages_with_notes_list length @ start:', len(packages_with_notes_list))
    # print('Special Note --> Can only be on truck2')

    for pkg in packages_with_notes_list:
        if pkg.get_notes() == 'Can only be on truck 2':
            truck2_list.append(pkg)     # Add package to truck2 list
            pkg_notes_2_trucks.append(pkg.get_id())     # Add package to pkg_notes_2_trucks

            # Build a list (both_lists) that combines packages_with_notes_list and packages_no_notes_list
            both_lists = packages_no_notes_list.copy()  # Create updated combined list
            both_lists.extend(packages_with_notes_list)   # Add to updated combined list
            # Search for packages with the same address
            for dup_addr_pkg in both_lists:
                # Conditions: same address, not on truck2 list, and is not the same package (by id number)
                if dup_addr_pkg.get_address() == pkg.get_address() and \
                        dup_addr_pkg not in truck2_list and dup_addr_pkg.get_id() != pkg.get_id():
                    truck2_list.append(dup_addr_pkg)        # Add to truck2 list

                    # Also add to pkg_notes_2_trucks or pkg_no_notes_2_trucks for later processing
                    if dup_addr_pkg in packages_with_notes_list and dup_addr_pkg.get_id() not in pkg_notes_2_trucks:
                        pkg_notes_2_trucks.append(dup_addr_pkg.get_id())  # Add package id to pkg_notes_2_trucks
                    elif dup_addr_pkg in packages_no_notes_list and dup_addr_pkg.get_id() not in pkg_no_notes_2_trucks:
                        pkg_no_notes_2_trucks.append(dup_addr_pkg.get_id())    # Add package id to pkg_no_notes_2_trucks

    # Remove packages from packages_with_notes_list and packages_no_notes_list (refresh/update list)
    # print('Remove packages from main lists:')
    packages_with_notes_list = [pkg for pkg in packages_with_notes_list if pkg.get_id() not in pkg_notes_2_trucks]
    packages_no_notes_list = [pkg for pkg in packages_no_notes_list if pkg.get_id() not in pkg_no_notes_2_trucks]
    # print('Done')

    # FOR TROUBLESHOOTING: Show truck2_list
    # show_truck_state(truck2_list)

    # Pull out of packages_with_notes packages that much be loaded together and start truck1_list
    # print()
    # print('Truck1 stuff --> Must be delivered...')
    truck1_list = []
    # Get the list of package IDs that must be delivered from the same truck
    # (i.e., parse information from each "Must be delivered..." special note)
    final_package_group = []    # Declare the final list of packages to add to truck1
    for pkg in packages_with_notes_list:
        # Pull out the "Must be delivered" statements from which to get the package ids
        if pkg.get_notes().find('Must be delivered with') != -1:
            # Start the individual package group with the package's id
            package_group = [pkg.get_id()]
            # Pull out just the numbers at the end of the notes string
            package_numbers = pkg.get_notes().lstrip('Must be delivered with ')
            # FOR TROUBLESHOOTING: print('package_numbers string:', package_numbers)

            # Split the numbers - they are still in string format
            package_numbers_string_list = package_numbers.split(", ")
            for pid in package_numbers_string_list:
                package_group.append(int(pid))
            # FOR TROUBLESHOOTING: print('package_group:', package_group)

            # Append each package_group entry to the final package group if it is not already there
            for pid in package_group:
                if pid not in final_package_group:
                    final_package_group.append(pid)
            # print('final_package_group:', final_package_group)

    # Add the packages to the truck1 list --> need to use a "both_lists" structure because
    # not all items in final_package_group have special notes associated with them
    both_lists = packages_no_notes_list.copy()
    both_lists.extend(packages_with_notes_list)
    for pkg in both_lists:
        if pkg.get_id() in final_package_group and pkg not in truck1_list:
            truck1_list.append(pkg)     # Add package to truck1_list
            # Also add to either pkg_notes_2_trucks or pkg_no_notes_2_trucks for later processing
            # Must accommodate both since both lists are used
            if pkg in packages_with_notes_list and pkg.get_id() not in pkg_notes_2_trucks:
                pkg_notes_2_trucks.append(pkg.get_id())  # Add package id to pkg_notes_2_trucks
                # print('after add, pkg_notes_2_trucks:', pkg_notes_2_trucks)
            if pkg in packages_no_notes_list and pkg.get_id() not in pkg_no_notes_2_trucks:
                pkg_no_notes_2_trucks.append(pkg.get_id())  # Add package id to pkg_no_notes_2_trucks
                # print('after add, pkg_not_notes_2_trucks:', pkg_no_notes_2_trucks)

            # Check for an item with the same address (duplicate addresses)
            for dup_addr_pkg in both_lists:
                # Condition: addresses are the same, duplicate package is not on truck, & is not the same package
                if dup_addr_pkg.get_address() == pkg.get_address() and \
                        dup_addr_pkg not in truck1_list and dup_addr_pkg.get_id() != pkg.get_id():
                    truck1_list.append(dup_addr_pkg)    # add to truck1_list
                    # print('Add duplicate package:', dup_addr_pkg, ' to truck1_list')

                    # Put duplicate's id in either "with_notes" or "no_notes" list for later processing
                    # Must accommodate both since both lists are used
                    if dup_addr_pkg in packages_with_notes_list and dup_addr_pkg.get_id() not in pkg_notes_2_trucks:
                        # print('Add duplicate - id:', dup_addr_pkg.get_id(), ' to pkg_notes_2_trucks')
                        pkg_notes_2_trucks.append(dup_addr_pkg.get_id())  # Add package id to pkg_notes_2_trucks
                    elif dup_addr_pkg in packages_no_notes_list and dup_addr_pkg.get_id() not in pkg_no_notes_2_trucks:
                        # print('Add duplicate - id:', dup_addr_pkg.get_id(), 'to pkg_no_notes_2_trucks')
                        pkg_no_notes_2_trucks.append(dup_addr_pkg.get_id())  # Add package id to pkg_no_notes_2_trucks

    # Remove packages from packages_with_notes_list and packages_no_notes_list (refresh/update list)
    # print('Remove packages from main lists:')
    packages_with_notes_list = [pkg for pkg in packages_with_notes_list if pkg.get_id() not in pkg_notes_2_trucks]
    packages_no_notes_list = [pkg for pkg in packages_no_notes_list if pkg.get_id() not in pkg_no_notes_2_trucks]
    # print('Done')

    # Show truck1_list
    # show_truck_state(truck1_list)

    # Pull out of packages_with_notes_list package(s) with "Wrong address" and start truck3_list
    # print()
    # print('Truck3 Stuff --> Wrong Address')
    truck3_list = []

    for pkg in packages_with_notes_list:
        if pkg.get_notes().find('Wrong address') != -1:
            truck3_list.append(pkg)
            pkg_notes_2_trucks.append(pkg.get_id())
            # Not going to look for duplicates ... yet

    # Remove packages from packages_with_notes_list and packages_no_notes_list (refresh/update list)
    # print('Remove packages from main lists:')
    packages_with_notes_list = [pkg for pkg in packages_with_notes_list if pkg.get_id() not in pkg_notes_2_trucks]
    packages_no_notes_list = [pkg for pkg in packages_no_notes_list if pkg.get_id() not in pkg_no_notes_2_trucks]
    # print('Done')

    # FOR TROUBLESHOOTING: Show truck3_list
    # show_truck_state(truck3_list)

    # Pull out of packages_with_notes_list packages with "Delayed on flight" and load onto truck 2
    # print()
    # print('Last group of notes --> Delayed on flight...')
    for pkg in packages_with_notes_list:
        # FOR TROUBLESHOOTING: print('ID:', pkg.get_id(), 'Note:', pkg.get_notes())
        if pkg.get_notes().find('Delayed on flight') != -1:
            # FOR TROUBLESHOOTING: print('Add delayed package:', pkg.get_id(), ' to truck2')

            # All delayed packages go on truck2 which will depart around 9:05/9:10
            truck2_list.append(pkg)
            # Update when package arrived at the hub
            pkg.update_package_status("at the hub", time(9, 5))
            # Add package id to pkg_notes_2_trucks for later processing - only used "with_notes" list
            if pkg in packages_with_notes_list and pkg.get_id() not in pkg_notes_2_trucks:
                pkg_notes_2_trucks.append(pkg.get_id())  # Add package id to pkg_notes_2_trucks
                # FOR TROUBLESHOOTING: print('Add delayed package to pkg_notes_2_trucks', pkg_notes_2_trucks)

            both_lists = packages_no_notes_list.copy()
            both_lists.extend(packages_with_notes_list)
            for dup_addr_pkg in both_lists:
                # FOR TROUBLESHOOTING: print('delayed - potential duplicate:', dup_addr_pkg.get_id())

                # Condition: same address, is not on truck2_list, and does not have the same id
                if dup_addr_pkg.get_address() == pkg.get_address() and \
                        dup_addr_pkg not in truck2_list and dup_addr_pkg.get_id() != pkg.get_id():
                    # print(dup_addr_pkg.get_address(), ' is a duplicate address')
                    truck2_list.append(dup_addr_pkg)
                    # print('truck2 list:')
                    # for i in truck2_list:
                    #    print(i.get_id(), ' ', end='')
                    # print()

                    # Put duplicate's id in either "with_notes" or "no_notes" list for later processing
                    # Must accommodate both since both lists are used
                    if dup_addr_pkg in packages_with_notes_list and dup_addr_pkg.get_id() not in pkg_notes_2_trucks:
                        # print('duplicate added to pkg_notes_2_trucks:', pkg_notes_2_trucks)
                        pkg_notes_2_trucks.append(dup_addr_pkg.get_id())  # Add package id to pkg_notes_2_trucks
                    elif dup_addr_pkg in packages_no_notes_list and dup_addr_pkg.get_id() not in pkg_no_notes_2_trucks:
                        # print('duplicate added to pkg_no_notes_2_trucks:', pkg_no_notes_2_trucks)
                        pkg_no_notes_2_trucks.append(dup_addr_pkg.get_id())  # Add package id to pkg_no_notes_2_trucks

    # Remove packages from packages_with_notes_list and packages_no_notes_list (refresh/update list)
    # print('Remove packages from main lists:')
    packages_with_notes_list = [pkg for pkg in packages_with_notes_list if pkg.get_id() not in pkg_notes_2_trucks]
    packages_no_notes_list = [pkg for pkg in packages_no_notes_list if pkg.get_id() not in pkg_no_notes_2_trucks]
    # print('Done')

    # FOR TROUBLE SHOOTING: Show truck list
    # show_truck_state(truck2_list)

    # Show information after special notes processing
    # FOR TROUBLESHOOTING
    # post_special_notes_processing_info()

    # Process the remaining "no notes" list entries into a remaining_delivery_list
    remaining_delivery_list = []
    for pkg in packages_no_notes_list:
        # Extract delivery time from the input type string
        input_time = pkg.get_delivery_deadline()
        time_list = input_time.split()
        # FOR TROUBLESHOOTING: print('time_list', time_list)

        if time_list[0] != 'EOD':
            # Strip out just the time as a time object
            delivery_time = datetime.strptime(time_list[0], '%H:%M').time()
            # Update time for 24 hour clock
            if time_list[1] == 'PM':
                delivery_time = (datetime.strptime(time_list[0], '%H:%M') + timedelta(hours=12, minutes=0)).time()
                # FOR TROUBLESHOOTING: print('delivery time plus 12 hours:', delivery_time)
            # Back to a string object
            delivery_time_string = time.strftime(delivery_time, '%H:%M')
            # FOR TROUBLESHOOTING: print('delivery_time:', delivery_time_string)

            # Append to remaining_delivery_list the processed tuple of (pkg, delivery_time_string)
            remaining_delivery_list.append((pkg, delivery_time_string))
        else:
            # Append to remaining_delivery_list the tuple of (pkg, 'EOD')
            remaining_delivery_list.append((pkg, 'EOD'))

    # Sort by the second entry in the tuple (which is delivery_deadline)
    remaining_delivery_list.sort(key=lambda x: x[1])

    # Output the sorted list
    # print('The remaining package list - sorted:')
    # for pkg, d in remaining_delivery_list:
    #    print(pkg.get_id(), ' ', d)

    # Load the remaining_delivery_list's packages onto trucks
    # For packages with time constraints, load on trucks 1 & 2 (these are at the top of the list)
    # For packages with End Of Day delivery deadlines, fill truck1 then move to truck2 until full, then truck3.
    truck_bool = True  # A boolean flag to indicate which truck to load
    truck_list = {True: truck1_list, False: truck2_list}  # Start by flipping between truck1 and truck2

    while len(remaining_delivery_list) != 0:        # While the remaining delivery list/stack is not empty
        # print('remaining delivery list')
        # for pkg, d in remaining_delivery_list:
        #    print(pkg.get_id(), ' ', d)

        # Pop the top package_group tuple from the list
        package_group = remaining_delivery_list.pop(0)
        new_package = package_group[0]  # Extract just the package from the tuple
        # print('new_package', new_package.get_id(), ' ', new_package)

        # For items that have a deadline other than End Of Day
        if new_package.get_delivery_deadline() != 'EOD':
            if len(truck_list[truck_bool]) < 16:    # Make sure the truck is not full
                # print(truck_list[truck_bool], ' still has space for', new_package)
                # Load the package
                truck_list[truck_bool].append(new_package)
                # print(new_package, 'loaded')

                # Refresh duplicate_remaining_delivery_list by copying the remaining_delivery_list
                duplicate_remaining_delivery_list = remaining_delivery_list.copy()

                # Look for duplicates to load
                for dup_addr_pkg in duplicate_remaining_delivery_list:
                    if dup_addr_pkg[0].get_address() == new_package.get_address() and \
                            dup_addr_pkg[0] not in truck_list[truck_bool] and \
                            dup_addr_pkg[0].get_id() != new_package.get_id() and len(truck_list[truck_bool]) < 16:
                        # FOR TROUBLESHOOTING:print(dup_addr_pkg[0].get_address(), ' is a duplicate address')
                        if len(truck_list[truck_bool]) < 16:
                            # Load package with same address on the same truck
                            truck_list[truck_bool].append(dup_addr_pkg[0])
                            # Remove package from remaining delivery list
                            remaining_delivery_list.remove(dup_addr_pkg)
                        else:
                            # If there's not room on the truck, do nothing
                            # (leave the package in the remaining_delivery_list to be loaded on another truck)
                            pass

                # Switch the truck
                truck_bool = not truck_bool
            else:
                # When the originally requested truck is full, put the package on the other truck
                # Note: for original data, one trucks 1 & 2 will have enough slots for all packages with early deadlines
                # print('Append to', truck_list[not truck_bool], ': ', new_package)
                truck_list[not truck_bool].append(new_package)
        else:       # Delivery deadline is  End Of Day ('EOD')
            # Determine which truck to begin loading first
            if len(truck_list[True]) < 16:
                load_truck = truck1_list
            elif len(truck_list[False]) < 16:
                load_truck = truck2_list
            else:           # Original data set has 40 packages so three trucks at 16 packages each is enough.
                load_truck = truck3_list

            # Put the package in the truck's list
            load_truck.append(new_package)

    # FOR TROUBLESHOOTING:
    # Output package ids on respective truck:
    # to watch progress place inside the while loop
    # to see final listing remove indent so it runs after while loop is finished
    # print('packages (ids) on trucks:')
    # print('Truck 1:')
    # for pid in truck1_list:
    #     print(pid.get_id(), ' ', end='')
    # print()
    # print('Truck2:')
    # for pid in truck2_list:
    #     print(pid.get_id(), ' ', end='')
    # print()
    # print('Truck3:')
    # for pid in truck3_list:
    #     print(pid.get_id(), ' ', end='')
    # print()
    # print('packages with notes on trucks:', pkg_notes_2_trucks)
    # print('packages with no notes on trucks:', pkg_no_notes_2_trucks)
    # print()
    # print('Truck1:', len(truck1_list))
    # print('Truck2:', len(truck2_list))
    # print('Truck3:', len(truck3_list))
    # print('Total loaded on trucks:', len(truck1_list) + len(truck2_list) + len(truck3_list))
    # print()

    # Return a tuple of the trucks' package id lists
    r_truck1_list = []
    for i in truck1_list:
        r_truck1_list.append(i.get_id())
    r_truck2_list = []
    for i in truck2_list:
        r_truck2_list.append(i.get_id())
    r_truck3_list = []
    for i in truck3_list:
        r_truck3_list.append(i.get_id())

    return_tuple = (r_truck1_list, r_truck2_list, r_truck3_list)
    return return_tuple


def show_truck_state(load_truck):
    # This method is useful for troubleshooting and updating code
    # The method shows information about the state of the truck_list passed to it as a parameter (load_truck)
    # Big-O: O(N)

    # Global variables that are needed in this method:
    global packages_with_notes_list
    global packages_no_notes_list
    global pkg_notes_2_trucks
    global pkg_no_notes_2_trucks

    # Show truck list
    print()
    if load_truck == truck2_list:
        print('Truck2 List:')
    elif load_truck == truck1_list:
        print('Truck1 List:')
    elif load_truck == truck3_list:
        print('Truck3 List:')

    for i in load_truck:
        print('package ID:', i.get_id(), ' Address:', i.get_address())
    print('length:', len(load_truck))
    print('packages with notes on trucks:', pkg_notes_2_trucks)
    print()

    # Output remaining lists
    print('packages_with_notes_list')
    for i in packages_with_notes_list:
        print(i.get_id(), ', ', end='')
    print()
    print('pkg_notes_2_trucks:', pkg_notes_2_trucks)
    print('packages_no_notes_list')
    for i in packages_no_notes_list:
        print(i.get_id(), ', ', end='')
    print()
    print('pkg_no_notes_2_trucks:', pkg_no_notes_2_trucks)


def post_special_notes_processing_info():
    # This method is useful for troubleshooting and updating code
    # The method shows information about the following global variables:
    # Big-O: O(N)

    # This method needs these global variables
    global packages_with_notes_list
    global packages_no_notes_list
    global pkg_notes_2_trucks
    global pkg_no_notes_2_trucks
    global truck1_list
    global truck2_list
    global truck3_list

    print()
    print('Packages Stats once special notes packages are loaded:')
    print('packages_with_notes_list length:', len(packages_with_notes_list))
    for pkg in packages_with_notes_list:
        print(pkg.get_id(), ' ', end='')  # Should be empty at this point
    print()
    print('packages_no_notes_list length:', len(packages_no_notes_list))
    for pkg in packages_no_notes_list:
        print(pkg.get_id(), ' ', end='')  # Should be what's left to place at this point
    print()
    print('packages (ids) on trucks:')
    print('Truck1:')
    for pid in truck1_list:
        print(pid.get_id(), ' ', end='')
    print()
    print('Truck2:')
    for pid in truck2_list:
        print(pid.get_id(), ' ', end='')
    print()
    print('Truck3:')
    for pid in truck3_list:
        print(pid.get_id(), ' ', end='')
    print()
    print('packages with notes on trucks:', pkg_notes_2_trucks)
    print('Truck1:', len(truck1_list))
    print('Truck2:', len(truck2_list))
    print('Truck3:', len(truck3_list))
    print('Total loaded on trucks:', len(truck1_list) + len(truck2_list) + len(truck3_list))
    print()
    print()
