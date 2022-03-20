# Author: Margaret Chrysler, #001224428
# --> import_data.py file for C950 - Data Structures and Algorithms 2, Practical Assessment
# Submission number 1 on date 05/21/2021

import csv
from package_hash_table import *
from package import *


# Create and fill a distance table from the .csv file data
# Big-O: O(N**2)
def fill_distance_table():
    with open('distance.csv', newline='') as distance_input:

        row_count = 0
        distances_list = []    # List of entries --> [[start_address, end_address, distance], [s_a, e_a, d],...]

        csv_reader = csv.reader(distance_input, dialect='excel', delimiter=',')

        for row in csv_reader:
            cell_count = 0
            while cell_count != len(row):
                # Clean up distance file input - remove ", CR, and LF
                # Things learned: .replace is a string manipulator: string.replace("old_char_str", "new_char_str"[,max])
                if row[cell_count].count('\n') > 0:         # Ef there are line breaks
                    # print('pre-processing:', row[cell_count])
                    temp_row_list = row[cell_count].rsplit("\n")        # Split the input
                    row[cell_count] = temp_row_list[1]                  # Assign only the address to row[cell_count]
                    # print('temp_row_list:', temp_row_list)
                    # print('row[cell_count]:', row[cell_count])
                    # Strip out quotes, carriage returns and commas
                    row[cell_count] = row[cell_count].replace("\"", "").replace("\r", " ").replace(",", "")
                # Trim spaces from ends
                row[cell_count] = row[cell_count].strip(" ")
                # print('post-processing row[cell_count]:', row[cell_count])
                cell_count += 1         # Increment for next cell in row
                # print('NEXT CELL')

            if row_count == 0:
                # First row of input - all are destinations and addresses
                # Save them as a list of starting addresses to match up with distance values
                # print('\nRow 0 entries are:')
                # print(','.join(row))       # Things learned: .join is a string manipulator: string.join(iterable)
                start_list = row.copy()
                # print('\nStart List:')
                # print(','.join(start_list))
                row_count += 1
            else:
                # Rows that start with destination & address followed by distances to other destinations/addresses
                # print('Row', row_count, ':')
                # print(','.join(row))

                # Print each entry [start_address, end_address, distance)
                end_address_index = 0
                end_distance_index = end_address_index + 2
                while end_distance_index < len(row) and row[end_distance_index] != '':
                    start_address = start_list[end_distance_index]
                    end_address = row[end_address_index]
                    distance = float(row[end_distance_index])
                    new_distance = [start_address, end_address, distance]
                    distances_list.append(new_distance)

                    # print('start_address:', start_address)
                    # print('end_address:', end_address)
                    # print('distance:', distance)
                    # print('Entry:')
                    # print(new_distance)
                    # print(distances_list)

                    end_distance_index += 1

                row_count += 1  # Next row

        # print('Total Number of Entries:', row_count - 1)
        return distances_list


# Create and fill a package hash table from the package.csv file
# Big-O: O(N)
def fill_package_table():
    packages_table = PackageHashTable()

    with open('package.csv') as package_import:
        csv_reader = csv.reader(package_import, dialect='excel', delimiter=',')
        package_count = 0
        for row in csv_reader:
            if package_count == 0:
                # First row is a header row - skip it
                package_count += 1
            elif package_count > 0:
                package_id = int(row[0])
                address = row[1]
                city = row[2]
                state = row[3]
                zip_code = row[4]
                deadline = row[5]
                mass_kilo = row[6]
                special_notes = row[7].replace("\"", "")
                new_package = Package(package_id, address, city, state, zip_code, deadline, mass_kilo, special_notes)
                # Put package ID in hash table
                packages_table.insert(new_package.get_id(), new_package)
                # print('New package ID:', new_package.get_id())
                # New_package.print_package()
                # TEST: print package using the hash table lookup
                # print('package', pkgs_table.search(package_id))
                # print('pkgs_table:', pkgs_table.table)

    return packages_table


# Retrieve the distance from an entry in the distance list/table
# Big-O:O(N) - loops through each entry in the distance list
def get_distance(dist_list, start_address, end_address):
    distance = -1.0
    for entry in dist_list:
        # FOR TESTING: does start address match either key1 or key2
        # print('get_distance --> entry:', entry)
        # print('start address', start_address)
        # print('end address', end_address)
        # print('key1:', entry[0])
        # print('key2:', entry[1])
        # print('values:', entry[2])
        # if start_address == entry[0]:
        #     print('start_address:', start_address, ' matches key1', entry[0])
        # elif start_address == entry[1]:
        #     print('start_address:', start_address, ' matches key2', entry[1])
        # else:
        #     print('NO start address match')
        # if end_address == entry[0]:
        #     print('start_address:', start_address, ' matches key1', entry[0])
        # elif end_address == entry[1]:
        #     print('start_address:', start_address, ' matches key2', entry[1])
        # else:
        #     print('NO end address found')
        # END TESTING

        # match up start/end addresses as either way
        if entry[0] == start_address and entry[1] == end_address:
            # print('start/end addresses found')
            # print('start address', start_address, ' ', entry[0])
            # print('end address', end_address, ' ', entry[1])
            distance = entry[2]
            # print('distance:', distance, ' ', entry[2])
            return distance
        elif entry[0] == end_address and entry[1] == start_address:
            # print('end/start addresses found')
            # print('end address:', end_address, ' ', entry[0])
            # print('start address:', start_address, ' ', entry[1])
            distance = entry[2]
            # print('distance:', distance, ' ', entry[2])
            return distance
    # Return from table distance list[2], if found
    print('Distance not Found!')
    return distance     # Or could return distance which is -1.0 ?
