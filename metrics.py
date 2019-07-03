from os import listdir
from os.path import basename
import json
from scipy.stats.stats import pearsonr  
import sklearn.metrics as metrics
import math
import csv
import numpy

folder_prefix = './results/'
filenames = listdir(folder_prefix)
print(f"Files used: {filenames}")

# filenames = ['FULLTEXT01.json']

expected = []
calculated = []

# load all results from files
for filename in filenames:
    with open(folder_prefix + filename, 'r') as file:
        content = json.loads(file.read())
        expected += [result['expected'] for result in content]
        calculated += [round(result['calculated'], 4) for result in content]

assert len(expected) == len(calculated), 'not correct number of calculations'

### N
print(f"Number of calculations: {len(calculated)}")

### pearson correlation
pearson = pearsonr(expected, calculated)
print(f"Pearson coefficient: {pearson[0]} (p-val: {pearson[1]})")

## https://medium.com/usf-msds/choosing-the-right-metric-for-machine-learning-models-part-1-a99d7d7414e4
### absolute error
mae = metrics.mean_absolute_error(expected, calculated)
medae = metrics.median_absolute_error(expected, calculated)
print(f"Mean Absolute Error: {mae}\nMedian Absolute Error: {medae}")

### deviation
mse = metrics.mean_squared_error(expected, calculated)
rmse = math.sqrt(mse)
print(f"Root Mean Squared Error (Deviation): {rmse}")

### write csv file
lines = [['Expected', 'Calculated']]
lines.extend(numpy.vstack((expected, calculated)).T)
assert expected[-1] == lines[-1][0] and calculated[-1] == lines[-1][1], "merging arrays did not work"
with open('results.csv', 'w', newline='') as csv_file:
    writer = csv.writer(csv_file)
    writer.writerows(lines)