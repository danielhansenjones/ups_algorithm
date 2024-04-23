# test_load_packages.py
import unittest
import tempfile
import os

from main import load_packages_into_hash
from package import Package


# A simple dummy hash table implementation for testing purposes.
class DummyHashTable:
    def __init__(self):
        self.data = {}

    def set(self, key: int, package: Package) -> None:
        self.data[key] = package


class TestLoadPackagesIntoHash(unittest.TestCase):

    def setUp(self):
        # Set up a dummy hash table instance for each test.
        self.hashtable = DummyHashTable()

    def create_temp_csv(self, content: str) -> str:
        """Helper function to create a temporary CSV file with the provided content."""
        tmpfile = tempfile.NamedTemporaryFile("w+", delete=False, newline='')
        tmpfile.write(content)
        tmpfile.close()
        return tmpfile.name

    def test_valid_input(self):
        """Test that valid CSV data is correctly loaded into the hash table."""
        csv_content = (
            "Package ID,Address,City,State,Zip,Deadline,Weight,Notes\n"
            "1,195 W Oakland Ave,Salt Lake City,UT,84115,10:30 AM,21,\n"
            "2,2530 S 500 E,Salt Lake City,UT,84106,EOD,44,\n"
        )
        filename = self.create_temp_csv(csv_content)

        try:
            load_packages_into_hash(self.hashtable, filename)
            # Check that both valid entries have been added.
            self.assertIn(1, self.hashtable.data)
            self.assertIn(2, self.hashtable.data)
            # Verify some of the package details (adjust attribute names as needed).
            self.assertEqual(self.hashtable.data[1].address, "195 W Oakland Ave")
            self.assertEqual(self.hashtable.data[1].city, "Salt Lake City")
            # Using 'zip_code' instead of 'Zip' based on common naming conventions in the Package class.
            self.assertEqual(self.hashtable.data[2].zip_code, "84106")
            self.assertEqual(self.hashtable.data[2].deadline, "EOD")
        finally:
            os.remove(filename)

    def test_invalid_package_id(self):
        """Test that a row with an invalid Package ID is skipped."""
        csv_content = (
            "Package ID,Address,City,State,Zip,Deadline,Weight,Notes\n"
            "abc,195 W Oakland Ave,Salt Lake City,UT,84115,10:30 AM,21,\n"
        )
        filename = self.create_temp_csv(csv_content)

        try:
            load_packages_into_hash(self.hashtable, filename)
            # Since the Package ID is invalid (not numeric), no entry should be added.
            self.assertEqual(len(self.hashtable.data), 0)
        finally:
            os.remove(filename)

    def test_missing_fields(self):
        """Test that a row missing expected fields is skipped."""
        # Here the 'Notes' field is missing.
        csv_content = (
            "Package ID,Address,City,State,Zip,Deadline,Weight,Notes\n"
            "1,195 W Oakland Ave,Salt Lake City,UT,84115,10:30 AM,21\n"
        )
        filename = self.create_temp_csv(csv_content)

        try:
            load_packages_into_hash(self.hashtable, filename)
            # Expect no entry to be added since the row is incomplete.
            self.assertEqual(len(self.hashtable.data), 0)
        finally:
            os.remove(filename)

    def test_empty_rows(self):
        """Test that empty rows in the CSV file are ignored."""
        csv_content = (
            "Package ID,Address,City,State,Zip,Deadline,Weight,Notes\n"
            "\n"
            "1,195 W Oakland Ave,Salt Lake City,UT,84115,10:30 AM,21,\n"
            "\n"
        )
        filename = self.create_temp_csv(csv_content)

        try:
            load_packages_into_hash(self.hashtable, filename)
            # Only the valid row should be processed.
            self.assertEqual(len(self.hashtable.data), 1)
            self.assertIn(1, self.hashtable.data)
        finally:
            os.remove(filename)


if __name__ == '__main__':
    unittest.main()
