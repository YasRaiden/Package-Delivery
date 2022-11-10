import itertools
from datetime import timedelta
from packages import str2time


class Truck:
    def __init__(self, label, start_location, package_list):
        self.label = label
        self.capacity = 16
        self.location = start_location
        self.loaded_packages = []
        self.time = None
        self.speed = 18
        self.distance = float(0.0)
        self.package_hash = package_list

    # Getters and setters for modifying truck attributes safely
    # Time Complexity -> O(1)
    def get_location(self):
        return self.location

    # Time Complexity -> O(1)
    # Space Complexity -> O(1)
    def set_location(self, address):
        self.location = address

    # Time Complexity -> O(1)
    def get_distance(self):
        return self.distance

    # Time Complexity -> O(1)
    # Space Complexity -> O(1)
    def add_distance(self, distance):
        self.distance += distance

    # Time Complexity -> O(1)
    def get_time(self):
        return self.time.strftime('%I:%M %p')

    # Time Complexity -> O(1)
    # Space Complexity -> O(1)
    def set_time(self, time):
        if self.time is None:
            self.time = str2time(time)
        else:
            return False

    # Time Complexity -> O(1)
    # Space Complexity -> O(1)
    def wait_time(self, time):
        if self.time < str2time(time):
            self.time = str2time(time)
        else:
            return False

    # Time Complexity -> O(1)
    # Space Complexity -> O(1)
    def add_time(self, time):
        self.time += time

    # Add remaining packages to be delivered
    # Time Complexity for load remaining -> O(n^2)
    # Space Complexity for load remaining -> O(n)
    def load_remaining(self):
        for bucket in self.package_hash.table:
            for package in bucket:
                selected_package = package[1]
                if selected_package.status < 3:
                    self.add_package(selected_package.id)

    # Adds package to truck if allowed
    # Checks against conditions of truck dependency, delays, truck capacity and wrong address.
    # Package dependency is handled by adding packages manually
    # Time Complexity for add package -> O(1)
    # Space Complexity for add package -> O(1)
    def add_package(self, package_id):
        valid_truck = True
        if self.time >= str2time('10:20 AM'):
            package_nine = self.package_hash.search(9)
            package_nine.update_address('410 S State St', 'Salt Lake City', 'UT', '84111')

        if len(self.loaded_packages) < self.capacity:
            selected_package = self.package_hash.search(package_id)
            if selected_package.truck_dependency is not None and selected_package.truck_dependency != self.label:
                valid_truck = False
                print('Invalid Truck for package ID', selected_package.id)
            if selected_package.at_hub_time <= self.time and selected_package.valid is True and valid_truck is True:
                self.loaded_packages.append(selected_package)
                selected_package.status += 1
                selected_package.en_route_time = self.time
            else:
                print("Package Delay: Unable to add package ID ", selected_package.id)
        else:
            print(self.label, "is at capacity.")

    # Takes array of packages, optimizes route, and delivers the packages while updating package status
    # Time Complexity for deliver -> O(n)
    # Space Complexity for deliver -> O(n)
    def deliver(self, graph):
        optimized_route = brute_force_ten(self.loaded_packages, self.location, graph)
        return_location = self.location
        for package in optimized_route[0]:
            package_distance = graph.distance(self.get_location(), package.location)
            package_time = timedelta(hours=(package_distance / self.speed))
            self.add_distance(package_distance)
            self.add_time(package_time)
            self.set_location(package.location)
            package.status = 3
            package.delivered_time = self.time
            self.loaded_packages.remove(package)
        self.add_distance(graph.distance(self.get_location(), return_location))
        self.location = return_location


# Optimization algorithm will run through at most !10 iterations to find best route
# Utilized by grouping packages with same location to deliver at the same time
# No more than 16 packages can be added with no more than 10 unique location
# Time Complexity for brute force ten -> O(n^2)
# Space Complexity for brute force ten -> O(1)
def brute_force_ten(package_set, start_location, graph):
    # Check to see if package set is less than total capacity and consolidate location
    package_locations = []
    if len(package_set) < 17:
        for package in package_set:
            if package.location not in package_locations:
                package_locations.append(package.location)
        # Check to see if consolidate locations is less than 11 for !10 iterations
        if len(package_locations) < 11:
            routes = list(map(list, itertools.permutations(package_locations)))
            travel_costs = []
            for route in routes:
                travel_cost = get_distance_location(route, start_location, graph)
                travel_costs.append(travel_cost)
            # pulls out the smallest travel cost
            smallest_cost = min(travel_costs)
            shortest = [routes[travel_costs.index(smallest_cost)], smallest_cost]
            optimized_route = []
            for location in shortest[0]:
                for package in package_set:
                    if package.location == location:
                        optimized_route.append(package)
            shortest[0] = optimized_route
            # returns tuple of the route and its cost
            return shortest


# Utilized for finding total distance of route with locations
# Time Complexity for get distance location -> O(n)
def get_distance_location(locations, start_end_location, graph):
    current_distance = float(0)
    current_location = start_end_location
    for location in locations:
        current_distance += graph.distance(location, current_location)
        current_location = location
    current_distance += graph.distance(start_end_location, current_location)
    return current_distance
