import os
import csv

def open_file(fname):
    """
    Opens files safely using realpath and CWD + filename
    """
    return open(get_file_realpath(fname), "r")

def write_csv(fname, data_rows):
    """
    Opens a file safely using realpath and CWD + filename and writes the CSV rows 
    """
    with open(get_file_realpath(fname), "w", newline="\n") as csvfile:
        writer = csv.writer(csvfile, delimiter=',', lineterminator="\n")
        for line in data_rows:
            writer.writerow(line)

def write_csv_dict(fname, fieldnames, data, restval=""):
    with open(get_file_realpath(fname), "w", newline="\n") as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames, restval=restval)
        writer.writeheader()
        for line in data:
            writer.writerow(line)

def get_file_realpath(fname):
    return os.path.realpath(os.path.join(os.getcwd(), fname))