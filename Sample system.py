""" PurpleAir system provide users with air quality data in an
interactive experience.
"""

from enum import Enum


class EmptyDatasetError(Exception):
    """Error raised when dataset is empty"""
    pass


class NoMatchingItems(Exception):
    """Error raised when there is no matching item in the dataset"""
    pass


class Stats(Enum):
    """Variable set to a constant"""
    MIN = 0
    AVG = 1
    MAX = 2


class DataSet:
    """Build a dataset storing air quality measure."""
    def __init__(self, header=''):
        self._data = None
        self.header = header
        self._zips = {}
        self._times = set()

    @property
    def header(self):
        """Access the value of self._header"""
        return self._header

    @header.setter
    def header(self, header: str):
        """Set the value of self._header"""
        max_header_length = 30
        if len(header) <= max_header_length:
            self._header = header
        else:
            raise ValueError

    def _initialize_labels(self):
        """Initialize label for dataset"""
        self._zips = {}
        zip_code = [item[0] for item in self._data]
        zip_code_dict = {item: True for item in zip_code}
        self._zips = zip_code_dict
        times_set = set([item[1] for item in self._data])
        time_of_day = list(times_set)
        self._times = time_of_day

    def load_default_data(self):
        """Load air quality data"""
        self._data = [("12345", "Morning", 1.1), ("94022", "Morning", 2.2),
                      ("94040", "Morning", 3.0), ("94022", "Midday", 1.0),
                      ("94040", "Morning", 1.0), ("94022", "Evening", 3.2)]
        self._initialize_labels()

    def _cross_table_statistics(self, descriptor_one: str,
                                descriptor_two: str):
        """Return concentration with valid zipcode and time entries"""
        if self._data is None:
            raise EmptyDatasetError
        concentration = [thing[2] for thing in self._data
                         if thing[0] == descriptor_one
                         and thing[1] == descriptor_two]
        if len(concentration) == 0:
            raise NoMatchingItems
        to_load_data = min(concentration), sum(concentration) \
            / len(concentration), max(concentration)
        return to_load_data

    def display_cross_table(self, stat: Stats):
        if not self._data:
            print("Please load a dataset first")
            return
        print("     ", end='')
        for time_of_day in self._times:
            print(f"{time_of_day : >10}", end='')
        print()
        filtered_zips = {key: value for (key, value) in self._zips.items()
                         if value is True}
        for zip_code in filtered_zips:
            print(f"{zip_code:5}", end='')
            for item in self._times:
                try:
                    concentrations = self._cross_table_statistics(zip_code,
                                                                  item)
                    print(f"{concentrations[stat.value] : >10}", end='')
                except NoMatchingItems:
                    print(f"{'N/A' : >10}", end='')
            print()


def print_menu():
    """Set up a menu. """
    print("Main Menu")
    print("1 - Print Average Particulate Concentration by Zip Code and "
          "Time")
    print("2 - Print Minimum Particulate Concentration by Zip Code and "
          "Time")
    print("3 - Print Maximum Particulate Concentration by Zip Code and "
          "Time")
    print("4 - Adjust Zip Code Filters")
    print("5 - Load Data")
    print("9 - Quit")


def menu(my_dataset: DataSet):
    """ Obtain the user's input from the menu. """
    keep_running = True
    while keep_running:
        print()
        print(my_dataset.header)
        print_menu()
        user_choice = input("What is your choice? ")
        try:
            int_choice = int(user_choice)
        except ValueError:
            print("Please enter a number only. ")
            continue
        if int_choice == 4:
            print("Option", int_choice, "is not available yet. ")
        elif int_choice == 1:
            my_dataset.display_cross_table(Stats.AVG)
        elif int_choice == 2:
            my_dataset.display_cross_table(Stats.MIN)
        elif int_choice == 3:
            my_dataset.display_cross_table(Stats.MAX)
        elif int_choice == 5:
            my_dataset.load_default_data()
        elif int_choice == 9:
            keep_running = False
        else:
            print("That's not a valid selection. ")
    print("Goodbye! Thank you for using the database. ")


def main():
    """ Run the PurpleAir system. """
    name = input("Please enter your name: ")
    print("Hi ", name, ", Hope you have a wonderful day!", sep="")
    purple_air = DataSet()
    while True:
        try:
            header = input("Enter a header for the menu: ")
            purple_air.header = header
            break
        except ValueError:
            print("Header must be a string less or equal to than thirty "
                  "characters long")
            continue
    print()
    menu(purple_air)


if __name__ == "__main__":
    def unit_test():
        my_dataset = DataSet()
        my_dataset.load_default_data()
        my_dataset.display_cross_table(Stats.MIN)
        my_dataset._zips["94022"] = False
        my_dataset.display_cross_table(Stats.MIN)
        my_dataset._zips["12345"] = False
        my_dataset._zips["94040"] = False
        my_dataset.display_cross_table(Stats.MIN)
    unit_test()
    main()


"""
---sample run #1 ---
Evening    Midday   Morning
12345       N/A       N/A       1.1
94022       3.2       1.0       2.2
94040       N/A       N/A       1.0
        Evening    Midday   Morning
12345       N/A       N/A       1.1
94040       N/A       N/A       1.0
        Evening    Midday   Morning
Please enter your name: 

"""
