import csv
import traceback

def save_results(data: list[str]):
    with open("./report_spl.csv", "a", newline="") as file:
        w = csv.writer(file)
        w.writerow(data)


def save_error(err: Exception):
    with open("./log_error.txt", "w+") as f:
        f.write(traceback.format_exc())