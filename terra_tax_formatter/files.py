import os
import csv

def open_file(fname):
    """
    Opens files safely using realpath and CWD + filename
    """
    return open(os.path.realpath(os.path.join(os.getcwd(), fname)), "r")

def write_csv(fname, data_rows):
    """
    Opens a file safely using realpath and CWD + filename and writes the CSV rows 
    """
    with open(os.path.realpath(os.path.join(os.getcwd(), fname)), "w", newline="\n") as csvfile:
        writer = csv.writer(csvfile, delimiter=',', lineterminator="\n")
        for line in data_rows:
            writer.writerow(line)