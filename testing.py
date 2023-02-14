import csv
from fuzzywuzzy import fuzz

# Open the CSV file and read its content into a list
with open('names.csv', 'r') as f:
    reader = csv.reader(f)
    names = list(reader)

# Compare each name with all the others using the fuzz.token_sort_ratio method
for i in range(len(names)):
    for j in range(i+1, len(names)):
        ratio = fuzz.token_sort_ratio(names[i][0], names[j][0])
        print(f"{names[i][0]} and {names[j][0]} are similar with a ratio of {ratio}")
