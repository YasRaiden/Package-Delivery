import csv
from hashtable import HashTable


# Space Complexity for Location -> O(1)
# Time Complexity for Location -> O(1)
class Location:
    # Stores address as unique object
    def __init__(self, label):
        self.label = label


class Graph:
    def __init__(self):
        self.adjacency_list = {}
        self.edge_weights = {}
        self.adjacent_packages = {}

    # Creates vertex from unique location objects
    def add_vertex(self, new_vertex):
        self.adjacency_list[new_vertex] = []

    # Adds edge weight between two locations and adds TO location as adjacency to FROM location
    def add_directed_edge(self, from_location, to_location, weight=0.0):
        self.edge_weights[(from_location, to_location)] = weight
        self.adjacency_list[from_location].append(to_location)

    # Calls to directed edge with to populates point A -> B and B -> A with same weight
    def add_undirected_edge(self, location_a, location_b, weight=0.0):
        self.add_directed_edge(location_a, location_b, weight)
        self.add_directed_edge(location_b, location_a, weight)

    # Receives distance between two location objects
    # Time Complexity for distance -> O(1)
    def distance(self, location_a, location_b):
        return self.edge_weights[location_a, location_b]


# Reading distance table CSV and placing data into graph object
# Time Complexity for import distance list -> O(n^2)
# Space Complexity for import distance list -> O(n)
def import_distance_table(filename):
    graph = Graph()
    with open(filename) as csvfile:
        read_csv = csv.reader(csvfile, delimiter=',')
        address_array = []
        # Pull first row in CSV containing addresses
        headers = next(read_csv)
        address_hash = HashTable(len(headers))
        # Creating location objects for each address, adding as vertex to graph, and creating hash table for validating
        for location in headers:
            current_location = Location(location)
            address_hash.add(location, current_location)
            address_array.append(current_location)
            graph.add_vertex(current_location)

        # Iterating through each row in CSV file comparing index value of address array for columns and rows
        # Add each number to adjacency matrix as undirected edge and skipping to next row when encounter blank cell
        for row in read_csv:
            row_num = read_csv.line_num - 1
            col_num = 1
            for column in row[1:len(row)]:
                if column != '':
                    graph.add_undirected_edge(address_array[row_num], address_array[col_num], float(column))
                    col_num += 1
                else:
                    break
        # Removing blank item in address hash was left in to line up distances from table
        address_hash.remove('')
    return graph, address_hash
