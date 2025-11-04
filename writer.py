import random
import csv
import re
import os

def csv_save(path: str):
    path = os.path.join(path, 'Dane.csv')
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file, delimiter=';')
        writer.writerow(['Model', 'Wynik', 'Czas'])
        writer.writerow([
            random.choice(['A', 'B', 'C']),
            random.randint(0, 1000),
            f"{random.randint(0, 1000)}s"
        ])


def validate_header(header: list):
    correct_header = ['Model', 'Wynik', 'Czas']
    if not header:
        print('No header in a file!')
        return 0
    elif len(header) < 3:
        print('Header has less then 3 columns!')
        return 0
    else:
        for i, name in enumerate(header):
            if name != correct_header[i]:
                print('Header is incorrect! Must be in order: Model;Wynik;Czas')
                return 0
    return 1


def validate_time(value: str):
    return bool(re.fullmatch(r'\d+s', value.strip()))


def extract_time(value: str):
    return int(value.rstrip('s'))


def validate_model(model):
    correct_model = {'A', 'B', 'C'}
    if model in correct_model:
        return 1
    return 0


def validate_result(result):
    if 0 <= int(result) <= 1000:
        return 1
    return 0


def validate_line(line):
    if validate_model(line[0]) and validate_result(line[1]) and validate_time(line[2]):
        return 1
    return 0


def check_csv_exists(path: str):
    file_path = os.path.join(path, 'Dane.csv')
    return os.path.isfile(file_path), os.path.join(path, 'Dane.csv')


def csv_read(path: str):
    if_file_exists, path = check_csv_exists(path)
    if not if_file_exists:
        print(f'File in this {path} does not exist. Could not read csv')
        return 0

    with open(path, 'r', newline='') as file:
        csvFile = csv.reader(file, delimiter=';')
        header = next(csvFile)
        print(header)

        if not validate_header(header):
            print(f'No header in file {path}')
            return 0
        
        time = 0
        for line in csvFile:
            if not validate_line(line):
                print(f'Incorrect line format in file - {path}')
                return 0
            print(line)
            if line[0] == 'A':
                time += extract_time(line[2])
    
    return time