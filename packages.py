import csv
from hashtable import HashTable
from datetime import datetime


class Package:
    status_dict = {0: 'DELAYED', 1: 'AT THE HUB', 2: 'EN ROUTE', 3: 'DELIVERED', }

    def __init__(self, id, address, city, state, zip, deadline, mass, special_note):
        self.id = id
        self.address = address
        self.city = city
        self.state = state
        self.zip = zip
        self.deadline = deadline
        self.mass = mass
        self.special_note = special_note

        self.status = 1
        self.valid = True
        self.truck_dependency = None
        self.at_hub_time = str2time("8:00 AM")
        self.en_route_time = str2time("11:59 PM")
        self.delivered_time = str2time("11:59 PM")
        self.location = None
        self.address_hash = None

    # Update address information of package in invalid
    # Time Complexity for update address -> O(1)
    def update_address(self, address, city, state, zip):
        if self.valid is False:
            self.address = address
            self.city = city
            self.state = state
            self.zip = zip
            self.location = self.address_hash.search(address)
            self.valid = True
        else:
            return False

    # Display single line package status information for full report
    # Time Complexity for get brief information -> O(1)
    def get_brief_inf(self, time):
        set_time = str2time(time)

        # Determine if package was delivered at or after given time
        if self.delivered_time < set_time:
            delivery_status = Package.status_dict.get(3) + " at " + self.delivered_time.strftime('%I:%M %p')
        # Determine if package was en route at or after given time
        elif self.en_route_time < set_time:
            delivery_status = Package.status_dict.get(2)
        # Determine if package was at hub at or after given time
        else:
            delivery_status = Package.status_dict.get(1)

        print(
            f'Package ID: {self.id}, '
            f'Status: {delivery_status}'
        )

    # Display full package information and status
    # Time Complexity for get full information -> O(1)
    def get_full_inf(self, time):
        set_time = str2time(time)

        # Determine if package was delivered at or after given time
        if self.delivered_time < set_time:
            delivery_status = Package.status_dict.get(3) + " at " + self.delivered_time.strftime('%I:%M %p')
        # Determine if package was en route at or after given time
        elif self.en_route_time < set_time:
            delivery_status = Package.status_dict.get(2)
        # Determine if package was at hub at or after given time
        else:
            delivery_status = Package.status_dict.get(1)
        print('---------------------------------------------------')
        print('ID:       ', self.id)
        print('Address:  ', self.address)
        print('Deadline: ', self.deadline)
        print('City:     ', self.city)
        print('Zip:      ', self.zip)
        print(f'Weight:    {self.mass}kg')
        print('Status:   ', delivery_status)
        print('---------------------------------------------------')


# Time Complexity for import package list -> O(n)
# Space Complexity for import package list -> O(n)
def import_package_list(filename, address_hash):
    with open(filename) as csvfile:
        read_csv = csv.reader(csvfile, delimiter=',')
        # Skip first header row of CSV file
        next(read_csv)
        # Create variable for HashTable calling out capacity based on package list size
        hash_table = HashTable(41)
        package_list = []
        for row in read_csv:
            id = int(row[0])
            address = row[1]
            city = row[2]
            state = row[3]
            zip = row[4]
            deadline = str2time(row[5])
            mass = row[6]
            special_note = row[7].upper()  # Handles case sensitivity
            package = Package(id, address, city, state, zip, deadline, mass, special_note)
            package.location = address_hash.search(address)
            hash_table.add(id, package)
            # Adding address hash to each package to validate addresses for updates
            package.address_hash = address_hash
            # Check specialty comment for delayed packages update at hub to delay time
            if 'WILL NOT ARRIVE TO DEPOT UNTIL' in special_note:
                split_string = special_note.split('WILL NOT ARRIVE TO DEPOT UNTIL ')
                arrival_time = split_string[len(split_string) - 1]
                package.at_hub_time = str2time(arrival_time)

            # Check specialty comment indicating wrong information listed, set valid status to false
            elif 'WRONG ADDRESS LISTED' in special_note:
                package.valid = False
            # Check specialty comment for truck dependency and add truck as attribute
            elif 'CAN ONLY BE ON' in special_note:
                split_string = special_note.split('CAN ONLY BE ON ')
                truck_dependency = split_string[len(split_string) - 1]
                package.truck_dependency = str2time(truck_dependency)
            package_list.append(package)
    return hash_table, package_list


# Converts string to time variable
# Time Complexity for string to time -> O(1)
def str2time(string):
    try:
        return datetime.strptime(string, '%I:%M %p')
    except ValueError:
        return string
