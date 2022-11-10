class HashTable:
    def __init__(self, capacity):
        self.table = []
        for i in range(capacity):
            self.table.append([])

    # Insertion of an object into Hash table Handling collisions with chaining
    # Space Complexity for HashTable Add -> O(n)
    # Time Complexity for HashTable Add -> O(n)
    def add(self, index, item):
        bucket = hash(index) % len(self.table)
        bucket_list = self.table[bucket]
        for i in bucket_list:
            if i[0] == index:
                i[1] = item
                return True
        index_value = [index, item]
        bucket_list.append(index_value)
        return True

    # Removal of an object from Hash table Handling collisions with chaining
    # Time Complexity for HashTable remove -> O(n)
    def remove(self, key):
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]
        for index_value in bucket_list:
            if index_value[0] == key:
                bucket_list.remove([index_value[0], index_value[1]])
        return False

    # Search for an object in hash table Handling collisions with chaining
    # Packages are being stored based on unique ID and locations are stored by address
    # Time Complexity for HashTable search -> on average O(1) worst O(n)
    def search(self, key):
        bucket = hash(key) % len(self.table)
        bucket_list = self.table[bucket]
        for index_value in bucket_list:

            if index_value[0] == key:
                return index_value[1]
        return False

    # Iterate through all packages listed in hash table and prints status for entered time
    # Time complexity for HashTable full report -> O(n^2)
    def full_report(self, time):
        for bucket in self.table:
            for package in bucket:
                package[1].get_brief_inf(time)
