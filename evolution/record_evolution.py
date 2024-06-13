import csv
import os
from datetime import datetime
from evolution.settings import *

def write_to_csv(target, class_name, fitness_records):
    fields = [f"testSuite{i}" for i in range(1, POP_PER_GEN+1)]
    fields.insert(0, "generation")
    if not os.path.isdir(f"record/{target}"):
        os.makedirs(f"record/{target}")
    curr_time = datetime.now().strftime('%Y%m%d_%H%M%S')
    with open(f"record/{target}/record_{class_name}_{curr_time}.csv", 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)

        csvwriter.writerow(fields)
        for i, row in enumerate(fitness_records, start=1):
            csvwriter.writerow([i]+row)

