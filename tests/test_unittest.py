import unittest
import os
from libs.utils import Utils


class TestZinobe(unittest.TestCase):

    def test_encrypt(self):
        self.assertIsInstance(Utils.encrypt("spanish"), str)

    def test_external_request(self):
        self.assertTrue(len(Utils.external_request(os.environ.get('REGIONS_URL'))) > 0)

    def test_sql_connection(self):
        self.assertTrue(Utils.sql_connection())

    def test_create_table_time(self):
        self.assertIsNone(Utils.create_table_times(Utils.sql_connection()))

    def test_create_table_countries(self):
        self.assertIsNone(Utils.create_table_countries(Utils.sql_connection()))

    def test_time_save(self):
        self.assertIsNone(Utils.time_save(0.5, 0.25, 0.25, 0.25))

    def test_data_frame(self):
        data = {
            'region': ['Africa', 'Americas'],
            'country': ['Angola', 'Colombia'],
            'language': [Utils.encrypt("english"), Utils.encrypt("spanish")],
            'time': [0.3, 0.28]
        }
        self.assertTrue(Utils.data_frame(data))


if __name__ == '__main__':
    unittest.main()
