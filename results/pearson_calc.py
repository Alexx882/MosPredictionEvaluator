from os import listdir
from os.path import basename
import json
from scipy.stats.stats import pearsonr  

filenames = listdir('.')
filenames.remove(basename(__file__))
# filenames.remove('result_04660307.json')
print(filenames)

expected = []
calculated = []

# load all results from files
for filename in filenames:
    with open(filename, 'r') as file:
        content = json.loads(file.read())
        expected += [result['expected'] for result in content]
        calculated += [result['calculated'] for result in content]

assert len(expected) == len(calculated), 'not correct number of calculations'

pearson = pearsonr(expected, calculated)
print(pearson)