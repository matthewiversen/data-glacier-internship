import logging
import os
import subprocess
import yaml
import pandas as pd
import datetime 
import gc
import re
import difflib


# summary of a data file
def summary(df: pd.DataFrame, file_path: str) -> None:
    # filesize in mb
    file_size_bytes = os.path.getsize(file_path)
    file_size_mb = file_size_bytes / (1024 * 1024)

    # get dimensions
    total_rows = len(df)
    total_columns = len(df.columns)

    print(f"Total number of rows: {total_rows}")
    print(f"Total number of columns: {total_columns}")
    print(f"File size: {file_size_mb:.2f} MB")


# prints the number of nans in each column
def show_nan_all_columns(df: pd.DataFrame) -> None:
    nan_counts = df.isnull().sum().sort_values(ascending=False)
    print(f"NaN Counts:\n{nan_counts}")
    

# prints the number of nans in columns with nans
def show_nan_columns(df: pd.DataFrame) -> None:
    nan_counts = df.isnull().sum().sort_values(ascending=False)
    nan_counts = nan_counts[nan_counts > 0]
    print(f"NaN Counts:\n{nan_counts}")
    

# returns what features have nans
def find_nan_columns(df: pd.DataFrame) -> pd.Index:
    nan_features = df.isnull().sum()
    non_zero_nans = nan_features[nan_features > 0]
    return non_zero_nans.index


# changes the number of columns seen on output
def set_pd_max_columns(max_columns: int | None) -> None:
    pd.set_option("display.max_columns", max_columns)


# changes the number of rows seen on output
def set_pd_max_rows(max_rows: int | None) -> None:
    pd.set_option("display.max_rows", max_rows)


def detect_outliers_iqr(data: pd.DataFrame) -> pd.DataFrame:
    """
    Detects and returns any outliers for a given dataframe.
    """
    Q1 = data.quantile(0.25)
    Q3 = data.quantile(0.75)
    IQR = Q3 - Q1
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR

    # filter for outliers
    outliers = data[(data < lower_bound) | (data > upper_bound)]
    return outliers


def show_spelling_errors(
    df: pd.DataFrame, similarity_threshold: float, exclude_columns: list[str]
) -> None:
    """This prints all of the observations in a column that are similar above a threshold

    Args:
        df (pd.DataFrame): Pandas DataFrame
        similarity_threshold (float): Decimal of how similar of results we want to see (0.0-1.0)
        exclude_columns (list[str]): List of columns you want to exclude from spelling check
    """

    spelling_errors = {}

    if exclude_columns is None:
        exclude_columns = []

    # find potential spelling errors for object columns
    for column in df.select_dtypes(include="object"):
        if column not in exclude_columns:
            unique_values = df[column].dropna().unique()
            potential_errors = []

            for i, value1 in enumerate(unique_values):
                for value2 in unique_values[i + 1 :]:
                    similarity = difflib.SequenceMatcher(None, value1, value2).ratio()
                    if similarity > similarity_threshold:
                        potential_errors.append((value1, value2))

            if potential_errors:
                spelling_errors[column] = potential_errors

    # print the errors
    for column, errors in spelling_errors.items():
        print(f"Potential spelling errors in column '{column}':")
        for error in errors:
            print(f"- '{error[0]}' might be similar to '{error[1]}'")
