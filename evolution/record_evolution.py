import csv
import os

def write_to_csv(target, class_name, fitness_records):
    fields = [f"testSuite{i}" for i in range(10)]
    fields.insert(0, "generation")
    if not os.path.isdir(f"record/{target}"):
        os.makedirs(f"record/{target}")
    with open(f"record/{target}/record_{class_name}.csv", 'w', newline='') as csvfile:
        csvwriter = csv.writer(csvfile)

        csvwriter.writerow(fields)
        for i, row in enumerate(fitness_records, start=1):
            csvwriter.writerow([i]+row)

