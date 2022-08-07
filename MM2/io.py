#!/usr/bin/env python3

"""
HELPERS

"""

import os
from csv import DictReader, DictWriter
import pickle

# import json


def read_typed_csv(rel_path, field_types):
    """
    Read a CSV with DictReader
    Patterned after: https://stackoverflow.com/questions/8748398/python-csv-dictreader-type
    """

    abs_path = FileSpec(rel_path).abs_path

    try:
        rows = []
        with open(abs_path, "r", encoding="utf-8-sig") as file:
            reader = DictReader(
                file, fieldnames=None, restkey=None, restval=None, dialect="excel"
            )

            for row_in in reader:
                if len(field_types) >= len(reader.fieldnames):
                    # Extract the values in the same order as the csv header
                    ivalues = map(row_in.get, reader.fieldnames)

                    # Apply type conversions
                    iconverted = [cast(x, y) for (x, y) in zip(field_types, ivalues)]

                    # Pass the field names and the converted values to the dict constructor
                    row_out = dict(zip(reader.fieldnames, iconverted))

                rows.append(row_out)

        return rows

    except:
        raise Exception("Exception reading CSV with explicit types.")


def write_csv(rel_path, rows, cols):
    try:
        abs_path = FileSpec(rel_path).abs_path

        with open(abs_path, "w") as f:
            writer = DictWriter(f, fieldnames=cols)
            writer.writeheader()

            for row in rows:
                mod = {}
                for (k, v) in row.items():
                    if isinstance(v, float):
                        mod[k] = "{:.6f}".format(v)
                    else:
                        mod[k] = v
                writer.writerow(mod)

    except:
        raise Exception("Exception writing CSV.")


def cast(t, v_str):
    return t(v_str)


class FileSpec:
    def __init__(self, path, name=None):
        file_name, file_extension = os.path.splitext(path)

        self.rel_path = path
        self.abs_path = os.path.abspath(path)
        self.name = name.lower() if (name) else os.path.basename(file_name).lower()
        self.extension = file_extension


### PICKLING ###


def write_pickle(rel_path, obj):
    abs_path = FileSpec(rel_path).abs_path

    try:
        with open(abs_path, "wb") as handle:
            pickle.dump(obj, handle, protocol=pickle.HIGHEST_PROTOCOL)
        return True
    except Exception as e:
        print("Exception pickling: ", e)
        return False


def read_pickle(rel_path):
    abs_path = FileSpec(rel_path).abs_path

    try:
        with open(abs_path, "rb") as handle:
            return pickle.load(handle)
    except Exception as e:
        print("Exception unpickling: ", e)
        return False
