import logging
import os
import subprocess
import yaml
import pandas as pd
import datetime 
import gc
import re

# Supplied by Data Glacier
def read_config_file(filepath):
    with open(filepath, 'r') as stream:
        try:
            return yaml.safe_load(stream)
        except yaml.YAMLError as exc:
            logging.error(exc)


def num_col_validation(df, table_config) -> bool:
    if len(df.columns)== len(table_config['columns']):
        return True
    else:
        return False


def col_header_val(df, table_config) -> bool:
    # sort, strip leading and trailing spaces, and replace space with _
    df_columns = sorted([col.strip().lower().replace(' ', '_') for col in df.columns])
    yaml_columns = sorted([col.strip().lower().replace(' ', '_') for col in table_config['columns']])

    if df_columns == yaml_columns:
        return True
    else:
        # Find the mismatched columns
        mismatched_columns = set(df_columns) ^ set(yaml_columns)
        print(f"Mismatched columns: {list(mismatched_columns)}")
        return False

def summary(df, file_path) -> None:
    # filesize in mb
    file_size_bytes = os.path.getsize(file_path)
    file_size_mb = file_size_bytes / (1024 * 1024)

    # get dimensions
    total_rows = len(df)
    total_columns = len(df.columns)

    print(f"Total number of rows: {total_rows}")
    print(f"Total number of columns: {total_columns}")
    print(f"File size: {file_size_mb:.2f} MB")
