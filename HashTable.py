class HashTable:
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

    def _hash(self, key):
        return hash(key) % self.capacity

    def _calculate_capacity(self, num_items, load_factor):
        min_capacity = num_items / load_factor
        capacity = 1
        while capacity < min_capacity:
            capacity *= 2
        return capacity

    def _resize(self):
        new_capacity = self.capacity * 2
        new_table = [[] for _ in range(new_capacity)]

        for bucket in self.table:
            for key, value in bucket:
                hash_index = hash(key) % new_capacity
                new_table[hash_index].append([key, value])

        self.table = new_table
        self.capacity = new_capacity

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

    def get(self, key):
        hash_index = self._hash(key)
        bucket = self.table[hash_index]

        for index, key_value_pair in enumerate(bucket):
            current_key, current_value = key_value_pair
            if key == current_key:
                return current_value

        return None

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

    def __str__(self):
        result = ""
        for index, bucket in enumerate(self.table):
            for key_value_pair in bucket:
                key, value = key_value_pair
                result += f"Bucket {index}: {key} => {value}\n"
        return result
