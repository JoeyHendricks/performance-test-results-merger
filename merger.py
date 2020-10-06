"""A simple Python Script that merges CSV files

The purpose of this module is to merge together multiple CSV files from the
Neoload load testing tool made by Neotys. This module is therefore writen
to interact with only exports from this tool set.

Usage:
    1. Place the script in any directory containing CSV files.
    2. Run the script you will be prompt to enter which file needs what ID.
    3. An merged version of all your CSV can then be found in the directory.

"""
from os import listdir
from os.path import join, isfile, realpath, dirname
import pandas as pd


class ExportedFile:
    """Represents the exported file

    An object that holds all the information of the exported file.

    Args:
        file_name (str): The full path to the file.

    Attributes:
        file_name (str): The full path to the file.
        data (dataframe): The data that the file contains

    """
    DELIMITER = ";"

    def __init__(self, file_name):

        self.file_name = file_name
        self.data = self.load_csv_file_into_dataframe()

    def load_csv_file_into_dataframe(self):
        """Reads the csv file

        Will read the data to pandas dataframe.

        Returns:
            dataframe: Will hold the contents of the file
        """
        dataframe = pd.read_csv(self.file_name, delimiter=self.DELIMITER, low_memory=False)
        return dataframe

    def add_runid_column_to_dataframe(self, runid):
        """Adds a column to the csv file

        Will add ID column called runid to the dataframe.
        The value of this column just be provided by the user.

        Args:
            runid: The ID that the user has specified.
        """
        self.data["RunID"] = runid


def discover_files_in_directory():
    """Find csv files in the current directory.

    Will scan the current directory and return all file names that are in it.

    Returns:
        list: A list of file paths.
    """
    # Finding current directory
    path_of_current_directory = dirname(realpath(__file__))

    # Listing Contents of current directory
    contents_in_directory = filter(isfile, listdir(path_of_current_directory))
    return [join(path_of_current_directory, f) for f in contents_in_directory]


def merge_csv_files(contents_of_current_directory):
    """Merges all the csv files.

    Will merge all the files into one csv file called GlobalResults.csv.

    Args:
        contents_of_current_directory: List of file paths

    Returns:
        List: That contains the data per csv file
    """

    payload = []  # <-- Data per csv file will be stored in here

    for file in contents_of_current_directory:

        if file[int(len(file) - 4): len(file)] == ".csv":

            # Communicate with the user
            print(f"RunID needed for the following file: {file}")
            runid = input("please provide runid: ")

            # Handle file
            exported_file = ExportedFile(file)
            exported_file.add_runid_column_to_dataframe(runid)
            payload.append(exported_file.data)

        else:
            continue

    return payload


def export_global_results(data_of_each_csv_file):
    """
    Exports the data of all the csv files into a global results csv file.

    Args:
        data_of_each_csv_file: List of data that contains each file.
    """
    global_results = pd.concat(data_of_each_csv_file)
    pd.DataFrame.to_csv(global_results, 'GlobalResults.csv', sep=';', na_rep='.', index=False)


# Read Directory
contents_of_each_csv_file_in_current_directory = merge_csv_files(discover_files_in_directory())

# Export merged csv file as GlobalResults.csv
export_global_results(contents_of_each_csv_file_in_current_directory)
