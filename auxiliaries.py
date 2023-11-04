import math
import csv
import pandas as pd
import numpy as np
import pygame as pg


def import_csv(filename):
    """
    Import data from a CSV file and store it as a list of dictionaries.

    Args:
        filename (str): The path to the CSV file.

    Returns:
        list: A list of dictionaries, where each dictionary represents a row from the CSV file.
    """
    data_list = []
    try:
        with open(filename, newline='', encoding='utf-8-sig') as csv_file:
            reader = csv.DictReader(csv_file, dialect='excel', delimiter=";")
            for row in reader:
                data_list.append(dict(row))
        return data_list
    except FileNotFoundError:
        print(f"Error: File '{filename}' not found.")
        # Handle the error further or exit the program gracefully.
        # You might want to return an empty list or raise an exception depending on your use case.
        return []


def arrow(screen, line_color, triangle_color, start, end, triangle_radius):
    """
    Draw an arrow on a Pygame screen.

    Args:
        screen: Pygame screen object.
        line_color: Color of the arrow line.
        triangle_color: Color of the arrowhead.
        start (tuple): Starting coordinates of the arrow.
        end (tuple): Ending coordinates of the arrow.
        triangle_radius (int): Radius of the arrowhead.
    """
    pg.draw.line(screen, line_color, start, end, 2)
    rotation = math.degrees(math.atan2(start[1] - end[1], end[0] - start[0])) + 90
    pg.draw.polygon(screen, triangle_color, ((end[0] + triangle_radius * math.sin(math.radians(rotation)),
                                              end[1] + triangle_radius * math.cos(math.radians(rotation))),
                                             (end[0] + triangle_radius * math.sin(math.radians(rotation - 120)),
                                              end[1] + triangle_radius * math.cos(math.radians(rotation - 120))),
                                             (end[0] + triangle_radius * math.sin(math.radians(rotation + 120)),
                                              end[1] + triangle_radius * math.cos(math.radians(rotation + 120)))))


def get_trial_input():
    """
    Necessary for a type of study where people see more than one text in a session.
    Gives a prompt to enter which trial (first or second round)

    Returns:
        int: User input, either 1 or 2.
    """
    print("\n \nHello. Please choose whether this ist the first or the second round in your trial.\n")
    user_input = None
    confirmed = False
    while not confirmed:
        user_input = input("Put your cursor behind this text, press \"1\" or \"2\", then press enter.")
        if user_input in ["1", "2"]:
            confirm = input(
                f"You chose {user_input}. If you want to proceed, type \"yes\". Careful with blanks."
                f"If you want to change your input, press any other key and then, press enter.")
            if confirm == "yes":
                confirmed = True
            else:
                pass
        else:
            print("Please choose 1 or 2.")
    return int(user_input)


def compress_data(data, verbose=False):
    """
    Compress data types in a DataFrame to optimize memory usage.

    Args:
        data (list of dict): List of dictionaries containing data.
        verbose (bool, optional): Whether to print verbose output. Defaults to False.

    Returns:
        pd.DataFrame: Compressed DataFrame.
    """
    df = pd.DataFrame.from_dict(data)
    numerics = ['int16', 'int32', 'int64', 'float16', 'float32', 'float64']
    for col in df.columns:
        col_type = df[col].dtypes
        if col_type in numerics:
            c_min = df[col].min()
            c_max = df[col].max()
            if str(col_type)[:3] == 'int':
                if c_min > np.iinfo(np.int8).min and c_max < np.iinfo(np.int8).max:
                    df[col] = df[col].astype(np.int8)
                elif c_min > np.iinfo(np.int16).min and c_max < np.iinfo(np.int16).max:
                    df[col] = df[col].astype(np.int16)
                elif c_min > np.iinfo(np.int32).min and c_max < np.iinfo(np.int32).max:
                    df[col] = df[col].astype(np.int32)
                elif c_min > np.iinfo(np.int64).min and c_max < np.iinfo(np.int64).max:
                    df[col] = df[col].astype(np.int64)
            else:
                if c_min > np.finfo(np.float16).min and c_max < np.finfo(np.float16).max:
                    df[col] = df[col].astype(np.float16)
                elif c_min > np.finfo(np.float32).min and c_max < np.finfo(np.float32).max:
                    df[col] = df[col].astype(np.float32)
                else:
                    df[col] = df[col].astype(np.float64)
    return df

# Example usage:
# data = import_csv("data.csv")
# compressed_data = compress_data(data, verbose=True)
# trial_input = get_trial_input()
# arrow(screen, line_color, triangle_color, start, end, triangle_radius)
