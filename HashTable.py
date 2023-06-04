

class HashTable:
    def __init__(self, size):
        self.size = size
        self.table = [[] for _ in range(self.size)]

    def _hash(self, key):
        return hash(key) % self.size

    def set(self, key, value):
        hash_index = self._hash(key)
        bucket = self.table[hash_index]

        for index, key_value_pair in enumerate(bucket):
            current_key, current_value = key_value_pair
            if key == current_key:
                bucket[index] = [key, value]
                return

        bucket.append([key, value])

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
                return True
        return False

    def __str__(self):
        result = ""
        for index, bucket in enumerate(self.table):
            for key_value_pair in bucket:
                key, value = key_value_pair
                result += f"Bucket {index}: {key} => {value}\n"
        return result

