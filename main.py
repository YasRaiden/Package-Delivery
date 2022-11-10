from packages import import_package_list
from map import import_distance_table
from truck import Truck
import os


# Determine system name to send appropriate clear command to console. 'clear' for posix; 'cls' for nt.
# For function to work modify configuration in PyCharm to emulate terminal in output console or run from console
def clear():
    if os.name == 'posix':
        os.system('clear')
    else:
        os.system('cls')


# Displays main menu when program runs to display information on single package or all packages for given time
def main_menu(distance, packages):
    run_menu = True
    while run_menu:
        print('---------------------------------')
        print('WGUPS PACKAGE DELIVERY')
        print('---------------------------------')
        print('Total Distance: ', distance)
        print()
        print('1) Display report of all packages')
        print('2) Display information of single package')
        print('q) Quit')
        user_select = input('Selection:')

        # Case for when 1 is entered to display information for all packages for entered time
        if user_select == '1':
            selected_time = input("Enter time (ex. 8:00 AM):")
            try:
                packages.full_report(selected_time)
            except TypeError:
                print('Invalid Entry!')
            input('Press enter to continue')
            clear()
        # Case for when 2 is entered to display information for single packages for entered time
        elif user_select == '2':
            select_package = input("Enter valid package ID:")
            try:
                selected_package = packages.search(int(select_package))
                selected_time = input("Enter time (ex. 8:00 AM):")
                try:
                    selected_package.get_full_inf(selected_time)
                except TypeError:
                    print('Invalid Entry!')
                except AttributeError:
                    print('Package ID not found')
            except ValueError:
                print('Invalid package ID!')
            input('Press enter to continue')
            clear()
        # Case for when q is entered to exit program
        elif user_select == 'q':
            run_menu = False

        # Case to handle all other input, screen will clear and display menu again
        else:
            clear()


# Start of main program
if __name__ == '__main__':
    # Importing distance table and package list, address hash is pulled in as a consistency checker
    graph, address_hash = import_distance_table('assets/WGUPSDistanceTable.csv')
    package_hash, package_list = import_package_list('assets/WGUPSPackageFile.csv', address_hash)

    # Storing hub location into variable as location object to utilize as a start and return address for deliveries
    hub_location = address_hash.search("4001 South 700 East")

    # Creating truck objects and importing package hash to provide an interface to package objects
    truck1 = Truck('TRUCK 1', hub_location, package_hash)
    truck2 = Truck('TRUCK 2', hub_location, package_hash)
    truck1.set_time("8:00 am")
    truck2.set_time("9:05 am")

    # Manually adding first batch of packages to Truck 1 delivery starting at set time 8:00 AM
    truck1.add_package(20)
    truck1.add_package(21)
    truck1.add_package(14)
    truck1.add_package(15)
    truck1.add_package(16)
    truck1.add_package(34)
    truck1.add_package(19)
    truck1.add_package(13)
    truck1.add_package(39)
    truck1.add_package(7)
    truck1.add_package(29)
    truck1.add_package(8)
    truck1.add_package(30)
    truck1.add_package(12)
    truck1.add_package(10)
    truck1.deliver(graph)

    # Manually adding second batch of packages to Truck 2 delivery starting at set time 9:05 AM
    truck2.add_package(1)
    truck2.add_package(4)
    truck2.add_package(40)
    truck2.add_package(28)
    truck2.add_package(6)
    truck2.add_package(25)
    truck2.add_package(26)
    truck2.add_package(31)
    truck2.add_package(32)
    truck2.add_package(5)
    truck2.add_package(37)
    truck2.add_package(38)
    truck2.add_package(27)
    truck2.add_package(35)
    truck2.add_package(36)
    truck2.deliver(graph)

    # Truck 2 will load remaining packages and deliver marking EOD
    truck2.load_remaining()
    truck2.deliver(graph)

    # Total distances are capture from truck 1 and truck 2
    total_distance = truck1.get_distance() + truck2.get_distance()

    # Calling menu function with total distance to display below title
    main_menu(total_distance, package_hash)
