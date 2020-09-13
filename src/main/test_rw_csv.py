import csv
import pandas as pd


# initial content
with open("mycsvfile.csv", "w") as f:
    f.write("a,b,c\n1,1,1\n")

with open("mycsvfile.csv", "a", newline="") as f:
    writer = csv.writer(f)
    writer.writerow([0, 0, 0])
    writer.writerow([0, 0, 0])
    writer.writerow([0, 0, 0])

with open("mycsvfile.csv") as f:
    print(f.read())


with open("names.csv", "a", newline="") as f:
    fieldnames = ["This", "aNew"]
    writer = csv.DictWriter(f, fieldnames=fieldnames)

    writer.writerow({"This": "is", "aNew": "Row"})

with open("names.csv") as f:
    print(f.read())


# pandasing:
mydf = pd.read_csv("mycsvfile.csv")
print("Mydf:\n", mydf.head())


names = pd.read_csv("names.csv")
print("names:\n", names.head())
