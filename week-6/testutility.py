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


def col_header_val(df, table_config):
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
