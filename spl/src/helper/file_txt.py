import csv
import os


def file_load_lines(pathfile: str) -> list[str]:
    direktori = os.getcwd()
    with open(direktori + pathfile) as fp:
        data_read = fp.readlines()
    data_read = list(filter(None, data_read))
    return data_read


def save_data(data: list[str], pathfile: str) -> None:
    with open(pathfile, "a", newline="") as file:
        w = csv.writer(file)
        w.writerow(data)