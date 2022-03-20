# Author: Margaret Chrysler, #001224428
# --> package.py file for C950 - Data Structures and Algorithms 2, Practical Assessment
# Submission number 1 on date 05/21/2021

# Defining class for Package
# Big O: O(1) - all methods deal with updating, setting, getting, printing only one package object - no loops
from datetime import *


class Package:
    def __init__(self, package_id, address, city, state, zip_code, delivery_deadline, mass_kilo, special_notes=''):
        self.package_id = package_id
        self.delivery_address = address
        self.delivery_city = city
        self.delivery_state = state
        self.delivery_zip_code = zip_code
        self.delivery_deadline = delivery_deadline
        self.package_weight = mass_kilo
        self.delivery_special_notes = special_notes
        hub_time = time(0, 0)
        self.delivery_status = [['at the hub', hub_time],
                                ['en route', None],
                                ['delivered', None]]

    # Retrieve the package id
    def get_id(self):
        return int(self.package_id)

    # Retrieve the package address
    def get_address(self):
        address = self.delivery_address
        return address

    # Update the package address
    def update_address(self, new_address):
        self.delivery_address = new_address

    # Retrieve the package delivery status
    def get_delivery_status(self):
        return self.delivery_status

    # Retrieve the package special notes
    def get_notes(self):
        return self.delivery_special_notes

    # Retrieve the package delivery deadline
    def get_delivery_deadline(self):
        return self.delivery_deadline

    # Update the time that the package's status is achieved
    def update_package_status(self, status, update_time):
        if status == 'at the hub':
            self.delivery_status[0][1] = update_time
        elif status == 'en route':
            self.delivery_status[1][1] = update_time
        elif status == 'delivered':
            self.delivery_status[2][1] = update_time

    # Print the package information (with no time option)
    def print_package(self):
        print()
        print('Package_ID:', int(self.package_id), '  ', end='')
        print('Delivery Address: ' + self.delivery_address + ', ' + self.delivery_city + ', ' + self.delivery_state +
              ' ' + self.delivery_zip_code)
        print('Delivery Deadline:', self.delivery_deadline, '  ', end='')

        # Format string for delivery status history
        if self.delivery_status[0][1] is not None:
            hub_time_status = 'at ' + str(self.delivery_status[0][1])
        else:
            hub_time_status = 'has not been completed.'
        if self.delivery_status[1][1] is not None:
            route_time_status = 'at ' + str(self.delivery_status[1][1])
        else:
            route_time_status = 'has not been completed.'
        if self.delivery_status[2][1] is not None:
            deliver_time_status = 'at ' + str(self.delivery_status[2][1])
        else:
            deliver_time_status = 'has not been completed.'
        print('Delivery Status Timeline:', self.delivery_status[0][0].capitalize(), hub_time_status + ',',
              self.delivery_status[1][0].capitalize(), route_time_status + ',',
              self.delivery_status[2][0].capitalize(), deliver_time_status)
        print('Package Weight (kg):', int(self.package_weight), '  ', end='')
        if self.delivery_special_notes != '':
            print('Special Notes:', self.delivery_special_notes)
        else:
            print('Special Notes: None')

    # Print the package information at a specified time
    def print_package_at_time(self, check_time):
        print()
        print('Package_ID:', int(self.package_id), '  ', end='')
        print('Delivery Address: ' + self.delivery_address + ', ' + self.delivery_city + ', ' + self.delivery_state +
              ' ' + self.delivery_zip_code)
        print('Delivery Deadline:', self.delivery_deadline, '  ', end='')

        # Format string for delivery status history (ths also finds time range)
        if self.delivery_status[2][1] is not None and check_time > self.delivery_status[2][1]:
            check_delivery_status = self.delivery_status[2]
        elif self.delivery_status[1][1] is not None and\
                check_time > self.delivery_status[1][1]:
            check_delivery_status = self.delivery_status[1]
        elif self.delivery_status[0][1] is not None and\
                check_time >= self.delivery_status[0][1]:
            check_delivery_status = self.delivery_status[0]
        else:
            check_delivery_status = ['invalid results', time(0, 0)]

        print('Delivery Status at', check_time, 'is:',
              check_delivery_status[0].capitalize(), 'at', check_delivery_status[1])

        print('Package Weight (kg):', int(self.package_weight), '  ', end='')
        if self.delivery_special_notes != '':
            print('Special Notes:', self.delivery_special_notes)
        else:
            print('Special Notes: None')
