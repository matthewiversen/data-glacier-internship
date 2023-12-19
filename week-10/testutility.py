import logging
import os
import subprocess
import yaml
import pandas as pd
import datetime 
import gc
import re
import difflib

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

def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """Prints info about and removes duplicate columns and rows

    Args:
        df (pd.DataFrame): Incoming Pandas DataFrame

    Returns:
        pd.DataFrame: Pandas DataFrame with no duplicate rows/columns
    """

    # count and remove duplicate rows
    duplicate_rows = df[df.duplicated()]
    num_duplicate_rows = len(duplicate_rows)
    df = df.drop_duplicates()

    # count and remove duplicate columns
    duplicate_columns = df.columns[df.columns.duplicated()]
    num_duplicate_columns = len(duplicate_columns)
    df = df.loc[:, ~df.columns.duplicated()]

    print(f"Number of duplicate rows removed: {num_duplicate_rows}")
    print(f"Number of duplicate columns removed: {num_duplicate_columns}")

    return df


def get_object_cols(df: pd.DataFrame) -> list:
    """
    Get a list of column names that have 'object' or categorical data type in a DataFrame.

    Args:
        df (pd.DataFrame): The DataFrame to analyze.

    Returns:
        list: A list of column names containing 'object' or categorical data type.
    """
    
    object_columns = []

    for col in df.columns:
        if df[col].dtype == 'object' or pd.api.types.is_categorical_dtype(df[col]):
            object_columns.append(col)

    return object_columns


def get_numerical_cols(df: pd.DataFrame) -> list:
    """
    Get a list of column names that have numerical data type in a DataFrame.

    Args:
        df (pd.DataFrame): The DataFrame to analyze.

    Returns:
        list: A list of column names containing numerical data type.
    """

    numerical_columns = []

    for col in df.columns:
        if pd.api.types.is_numeric_dtype(df[col]):
            numerical_columns.append(col)

    return numerical_columns


def object_cols_distribution(
    df: pd.DataFrame, object_cols: list[str], exclude_cols: list[str] = []
):
    """
    Print the percentage distribution of values in categorical columns.

    Args:
        df (pd.DataFrame): The DataFrame to analyze.
        object_cols (list): A list of column names with categorical data.
        exclude_cols (list, optional): A list of columns to exclude from analysis.

    Returns:
        None
    """
    
    for col in object_cols:
        if col not in exclude_cols:
            category_percentage = (df[col].value_counts() / len(df)) * 100
            print(category_percentage)
            print("=" * 50)  # Separator for readability
