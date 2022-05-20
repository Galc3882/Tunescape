import csv
import os


if __name__ == '__main__':
    # Read in the csv file
    with open(os.getcwd()+'\\'+'database.csv', newline='') as f:
        reader = csv.reader(f)
        data = list(reader)

    print(data)
