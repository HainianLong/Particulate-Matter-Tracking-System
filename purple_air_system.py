""" PurpleAir system provide users with air quality data in an
interactive experience.
"""
from enum import Enum

import csv

filename = './purple_air.csv'


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
        self._header = header
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

    def get_zips(self):
        """Return copy of zipcode data"""
        return self._zips.copy()

    def toggle_zip(self, target_zip: str):
        """Allow user to deactivate some zipcode"""
        if target_zip not in self._zips:
            raise LookupError
        else:
            self._zips[target_zip] = not self._zips[target_zip]

    def _initialize_labels(self):
        """Initialize label for dataset"""
        self._zips = {}
        zip_code = [item[0] for item in self._data]
        zip_code_dict = {item: True for item in zip_code}
        self._zips = zip_code_dict
        times_set = set([item[1] for item in self._data])
        time_of_day = list(times_set)
        self._times = time_of_day

    def load_file(self):
        """File I/O
        DictReader key = ['Approximate Zip Code', 'Reading Time String',
        'Concentration']
        """
        with open(filename) as csvfile:
            file = csv.DictReader(csvfile)
            data_list = []
            for row in file:
                concentrations = float(row['Concentration'])
                tuple_file = (row['Approximate Zip Code'],
                              row['Reading Time String'], concentrations)
                data_list.append(tuple_file)
        self._data = data_list
        print(f"{len(self._data)} lines loaded")
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
        value_con = min(concentration), sum(concentration) \
            / len(concentration), max(concentration)
        return value_con

    def display_cross_table(self, stat: Stats):
        """Set up the interface of PurpleAir system"""
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
                    print(f"{concentrations[stat.value] : >10.2f}", end='')
                except NoMatchingItems:
                    print(f"{'N/A' : >10}", end='')
            print()


def manage_filters(my_dataset: DataSet):
    """Set up filter for user to select their choice of zipcode"""
    if not my_dataset.get_zips():
        print("Please load a dataset first")
    else:
        print("The following labels are in the dataset:")
        while True:
            zips_list = list(my_dataset.get_zips().items())
            for zips_number, zips in enumerate(zips_list, 1):
                print(f"{zips_number}: {zips[0]}", end="")
                mode = "ACTIVE" if zips[1] is True else "INACTIVE"
                print(f"{mode: >10}")
            user_input = input("Please select an item to toggle or press "
                               "enter return when you are finished ")
            if user_input == "":
                break
            try:
                user_int = int(user_input)
                select = user_int - 1
                zipcode = zips_list[select][0]
                my_dataset.toggle_zip(zipcode)
            except ValueError:
                print("Please enter a number or enter/return to exit")
                continue
            except IndexError:
                print("Please enter a number from the list")
                continue


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
            manage_filters(my_dataset)
        elif int_choice == 1:
            my_dataset.display_cross_table(Stats.AVG)
        elif int_choice == 2:
            my_dataset.display_cross_table(Stats.MIN)
        elif int_choice == 3:
            my_dataset.display_cross_table(Stats.MAX)
        elif int_choice == 5:
            my_dataset.load_file()
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
    main()


"""
---sample run #1 ---
/Users/peng/PycharmProjects/CS3Aassignment/venv/bin/python /Users/peng/PycharmProjects/CS3Aassignment/venv/purple_air_system.py 
Please enter your name: Audrey
Hi Audrey, Hope you have a wonderful day!
Enter a header for the menu: CLEAN AIR 2022


CLEAN AIR 2022
Main Menu
1 - Print Average Particulate Concentration by Zip Code and Time
2 - Print Minimum Particulate Concentration by Zip Code and Time
3 - Print Maximum Particulate Concentration by Zip Code and Time
4 - Adjust Zip Code Filters
5 - Load Data
9 - Quit
What is your choice? 1
Please load a dataset first

CLEAN AIR 2022
Main Menu
1 - Print Average Particulate Concentration by Zip Code and Time
2 - Print Minimum Particulate Concentration by Zip Code and Time
3 - Print Maximum Particulate Concentration by Zip Code and Time
4 - Adjust Zip Code Filters
5 - Load Data
9 - Quit
What is your choice? 5
6147 lines loaded

CLEAN AIR 2022
Main Menu
1 - Print Average Particulate Concentration by Zip Code and Time
2 - Print Minimum Particulate Concentration by Zip Code and Time
3 - Print Maximum Particulate Concentration by Zip Code and Time
4 - Adjust Zip Code Filters
5 - Load Data
9 - Quit
What is your choice? 1
        Evening   Morning    Midday     Night
94028      2.26      1.54      2.92      1.58
94304      1.17      1.36      2.89      1.23
94022      1.22      1.50      2.92      1.32
94024      3.42      1.71      3.27      1.69
94040      4.57      1.86      3.28      2.47
94087      4.77      2.24      3.92      2.31
94041      4.53      2.41      3.52      3.43
95014      2.38      1.06      3.29      2.19

CLEAN AIR 2022
Main Menu
1 - Print Average Particulate Concentration by Zip Code and Time
2 - Print Minimum Particulate Concentration by Zip Code and Time
3 - Print Maximum Particulate Concentration by Zip Code and Time
4 - Adjust Zip Code Filters
5 - Load Data
9 - Quit
What is your choice? 2
        Evening   Morning    Midday     Night
94028      0.00      0.00      0.00      0.00
94304      0.00      0.00      0.00      0.00
94022      0.00      0.00      0.00      0.00
94024      0.00      0.00      0.00      0.00
94040      0.00      0.00      0.00      0.00
94087      0.00      0.00      0.00      0.00
94041      0.00      0.00      0.00      0.00
95014      0.00      0.00      0.00      0.00

CLEAN AIR 2022
Main Menu
1 - Print Average Particulate Concentration by Zip Code and Time
2 - Print Minimum Particulate Concentration by Zip Code and Time
3 - Print Maximum Particulate Concentration by Zip Code and Time
4 - Adjust Zip Code Filters
5 - Load Data
9 - Quit
What is your choice? 3
        Evening   Morning    Midday     Night
94028     79.88     25.72     24.21     25.00
94304      9.73      9.66     20.93      9.92
94022     11.53     12.90     26.59     14.38
94024     37.57     15.12     29.17      9.67
94040     44.05     10.49     25.95     20.34
94087     38.11      9.39     26.48     13.14
94041     31.82      8.02     25.89     19.67
95014     69.05      9.95     25.00     37.82

CLEAN AIR 2022
Main Menu
1 - Print Average Particulate Concentration by Zip Code and Time
2 - Print Minimum Particulate Concentration by Zip Code and Time
3 - Print Maximum Particulate Concentration by Zip Code and Time
4 - Adjust Zip Code Filters
5 - Load Data
9 - Quit
What is your choice? 4
The following labels are in the dataset:
1: 94028    ACTIVE
2: 94304    ACTIVE
3: 94022    ACTIVE
4: 94024    ACTIVE
5: 94040    ACTIVE
6: 94087    ACTIVE
7: 94041    ACTIVE
8: 95014    ACTIVE
Please select an item to toggle or press enter return when you are finished 8
1: 94028    ACTIVE
2: 94304    ACTIVE
3: 94022    ACTIVE
4: 94024    ACTIVE
5: 94040    ACTIVE
6: 94087    ACTIVE
7: 94041    ACTIVE
8: 95014  INACTIVE
Please select an item to toggle or press enter return when you are finished 

CLEAN AIR 2022
Main Menu
1 - Print Average Particulate Concentration by Zip Code and Time
2 - Print Minimum Particulate Concentration by Zip Code and Time
3 - Print Maximum Particulate Concentration by Zip Code and Time
4 - Adjust Zip Code Filters
5 - Load Data
9 - Quit
What is your choice? 3
        Evening   Morning    Midday     Night
94028     79.88     25.72     24.21     25.00
94304      9.73      9.66     20.93      9.92
94022     11.53     12.90     26.59     14.38
94024     37.57     15.12     29.17      9.67
94040     44.05     10.49     25.95     20.34
94087     38.11      9.39     26.48     13.14
94041     31.82      8.02     25.89     19.67

CLEAN AIR 2022
Main Menu
1 - Print Average Particulate Concentration by Zip Code and Time
2 - Print Minimum Particulate Concentration by Zip Code and Time
3 - Print Maximum Particulate Concentration by Zip Code and Time
4 - Adjust Zip Code Filters
5 - Load Data
9 - Quit
What is your choice? 9
Goodbye! Thank you for using the database. 

Process finished with exit code 0

"""
