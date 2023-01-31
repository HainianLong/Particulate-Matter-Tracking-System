import unittest


import purple_air_system


class Test(unittest.TestCase):
    def test_load_data(self):
        dataset = purple_air_system.DataSet()
        dataset.load_file()
        self.assertEqual(6147, len(dataset._data))


if __name__ == "__main__":
    unittest.main()