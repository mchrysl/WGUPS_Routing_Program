# Author: Margaret Chrysler, #001224428
# --> package_hash_table.py file for C950 - Data Structures and Algorithms 2, Practical Assessment
# Submission number 1 on date 05/21/2021

# The hash table that uses chaining: used to manage package objects

class PackageHashTable:
    # Constructor with optional initial capacity parameter
    # Big-O: every case is worst case of O(N/4)
    # Initializes all buckets with an empty list
    def __init__(self, initial_capacity=10):
        # initialize the hash table with empty bucket list entries
        self.table = []
        for i in range(initial_capacity):
            self.table.append([])

    # Inserts a new package into the hash table
    # Hash value of ID determines which "row" of the table,
    # if the package ID is found, update the package, otherwise append the ID and package to the end
    # Big-O: worst case of O(N)
    def insert(self, pid, pkg):
        # Get the bucket list where this package will go.
        bucket = hash(pid) % len(self.table)
        bucket_list = self.table[bucket]

        # Update package if it is already in the bucket
        for id_pkg in bucket_list:
            # Print (key_value)
            if id_pkg[0] == pid:
                id_pkg[1] = pkg
                return True

        # If not, insert the package to the end of the bucket list.
        id_pkg = [pid, pkg]
        bucket_list.append(id_pkg)
        return True

    # Look up a package with provided package ID in the hash table
    # Returns the package if found, or None if not found.
    # Big-O: O(1)
    def search(self, pid):
        # TROUBLESHOOTING: print('search called successfully')
        # Get the bucket list where this ID would be
        bucket = hash(pid) % len(self.table)
        bucket_list = self.table[bucket]

        # Search bucket_list for the package ID
        for id_pkg in bucket_list:
            # Print (id_pkg)
            if id_pkg[0] == pid:
                # Return the package
                return id_pkg[1]
        # Not found
        return None

    # Removes a package with matching key from the hash table
    # Big-O: worst case of O(N/10)
    def remove(self, pid):
        # Get the bucket list where this package will be removed from.
        bucket = hash(pid) % len(self.table)
        bucket_list = self.table[bucket]

        # Remove the package from the bucket list if it is present
        for id_pkg in bucket_list:
            if id_pkg[0] == pid:
                bucket_list.remove([id_pkg[0], id_pkg[1]])

    # Get and return the complete list of package IDs in the hash table
    # Big-O: the nested for loops cover the full data set so O(N)
    def get_id_list(self):
        package_id_list = []    # declare the list to be returned
        # Retrieve every package ID from the hash table
        for bucket in range(0, len(self.table)):
            bucket_list = self.table[bucket]
            for key_val in bucket_list:
                package_id_list.append(key_val[0])
        package_id_list.sort()  # Sort retrieved IDs from lowest to highest
        return package_id_list

    # Get and return the complete list of packages in the hash table
    # Big-O: the nested for loops cover the full data set so O(N)
    def get_package_list(self):
        package_list = []
        for bucket in range(0, len(self.table)):
            bucket_list = self.table[bucket]
            for key_val in bucket_list:
                package_list.append(key_val[1])
        return package_list
