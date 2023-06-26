# The 'HashTable' class is a data structure that stores key-value pairs.
# It uses a hash function to compute an index into an array in which an element will be inserted or searched.
# This allows for constant time average complexity for search, insert, and delete operations.

class HashTable:
    # The __init__ method initializes a new instance of the HashTable class.
    # The time complexity of the init method is O(n), where n is the number of items in the list
    # that the hashtable is initialized with.
    def __init__(self, items=None, load_factor=0.75):
        if items is None:
            self.size = 0
            self.capacity = 10
        else:
            self.size = len(items)
            self.capacity = self._calculate_capacity(len(items), load_factor)

        self.load_factor = load_factor
        self.table = [[] for _ in range(self.capacity)]

        if items is not None:
            for key, value in items:
                self.set(key, value)

    # The _hash method returns a hash value for a given key. The time complexity is O(1).
    def _hash(self, key):
        return hash(key) % self.capacity

    # The _calculate_capacity method calculates the capacity for the hashtable based on load factor.
    # It finds the power of 2 which is greater than or equal to num_items/load_factor.
    # The time complexity of this method is O(log n), where n is num_items/load_factor.
    def _calculate_capacity(self, num_items, load_factor):
        min_capacity = num_items / load_factor
        capacity = 1
        while capacity < min_capacity:
            capacity *= 2
        return capacity

    # The _resize method resizes the hash table when the size exceeds capacity*load_factor.
    # It doubles the capacity of the table and re-hashes all the key-value pairs in the table.
    # The time complexity of this method is O(n), where n is the number of elements in the hash table.
    def _resize(self):
        new_capacity = self.capacity * 2
        new_table = [[] for _ in range(new_capacity)]

        for bucket in self.table:
            for key, value in bucket:
                hash_index = hash(key) % new_capacity
                new_table[hash_index].append([key, value])

        self.table = new_table
        self.capacity = new_capacity

    # The set method adds a key-value pair to the hashtable. If the key already exists in the hashtable,
    # it updates the value. The average time complexity of this method is O(1).
    def set(self, key, value):
        hash_index = self._hash(key)
        bucket = self.table[hash_index]

        for index, key_value_pair in enumerate(bucket):
            current_key, current_value = key_value_pair
            if key == current_key:
                bucket[index] = [key, value]
                return

        bucket.append([key, value])
        self.size += 1

        if self.size > self.capacity * self.load_factor:
            self._resize()

    # The get method retrieves a value from the hashtable based on the provided key.
    # The average time complexity is O(1).
    def get(self, key):
        hash_index = self._hash(key)
        bucket = self.table[hash_index]

        for index, key_value_pair in enumerate(bucket):
            current_key, current_value = key_value_pair
            if key == current_key:
                return current_value

        return None

    # The delete method removes the key-value pair from the hashtable based on the provided key.
    # The average time complexity is O(1).
    def delete(self, key):
        hash_index = self._hash(key)
        bucket = self.table[hash_index]

        for index, key_value_pair in enumerate(bucket):
            current_key, current_value = key_value_pair
            if key == current_key:
                del bucket[index]
                self.size -= 1
                return True

        return False

    # The __str__ method provides a string representation of the hashtable.
    # It's helpful for debugging and understanding the distribution of key-value pairs across the buckets.
    # The time complexity of this method is O(n), where n is the number of elements in the hashtable.
    def __str__(self):
        result = ""
        for index, bucket in enumerate(self.table):
            for key_value_pair in bucket:
                key, value = key_value_pair
                result += f"Bucket {index}: {key} => {value}\n"
        return result
