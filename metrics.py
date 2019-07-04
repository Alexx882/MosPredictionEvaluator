from os import listdir
from os.path import basename
import json
from scipy.stats.stats import pearsonr  
import sklearn.metrics as metrics
import math
import csv
import numpy
import re

def calculate_metrics(filenames, output_filename=None):
    expected = []
    calculated = []
    result = {}

    # load all results from files
    for filename in filenames:
        with open(folder_prefix + filename, 'r') as file:
            content = json.loads(file.read())
            expected += [result['expected'] for result in content]
            calculated += [round(result['calculated'], 4) for result in content]

    assert len(expected) == len(calculated), 'not correct number of calculations'

    ### N
    result['N'] = len(calculated)

    ### pearson correlation
    result['Pearson'] = pearsonr(expected, calculated)

    ## https://medium.com/usf-msds/choosing-the-right-metric-for-machine-learning-models-part-1-a99d7d7414e4
    ### absolute error
    result['MAE'] = metrics.mean_absolute_error(expected, calculated)
    result["MEDAE"] = metrics.median_absolute_error(expected, calculated)

    ### deviation
    mse = metrics.mean_squared_error(expected, calculated)
    result['RMSE'] = math.sqrt(mse)

    if output_filename != None:
        with open(f'{output_filename}.txt', 'w') as output:
            output.write(describe_metrics(result))
        create_csv(output_filename, expected, calculated)

    return result

def describe_metrics(metrics):
    sb = []
    sb.append(f"Number of calculations: {metrics['N']}\n")
    sb.append(f"Pearson coefficient: {metrics['Pearson'][0]} (p-val: {metrics['Pearson'][1]})\n")
    sb.append(f"Mean Absolute Error: {metrics['MAE']}\nMedian Absolute Error: {metrics['MEDAE']}\n")
    sb.append(f"Root Mean Square Error (Deviation): {metrics['RMSE']}\n")
    return ''.join(sb)

def create_csv(filename, expected, calculated):
    lines = [['Expected', 'Calculated']]
    lines.extend(numpy.vstack((expected, calculated)).T)
    assert expected[-1] == lines[-1][0] and calculated[-1] == lines[-1][1], "merging arrays did not work"

    with open(f'{filename}.csv', 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerows(lines)


folder_prefix = './results/'
filenames = listdir(folder_prefix)
print(f"Files used: {filenames}")

worst = [1, '']
best = [0, '']

# individual metrics
for filename in filenames:
    met = calculate_metrics([filename], output_filename=f"analysis/{re.sub('.json$', '', filename)}")
    used_metric = met['Pearson'][0]
    if  used_metric < worst[0]:
        worst[0] = used_metric
        worst[1] = filename
    if used_metric > best[0]:
        best[0] = used_metric
        best[1] = filename

print(f"worst: {worst[1]}, best: {best[1]}")

# complete metric
calculate_metrics(filenames, 'analysis/complete')
