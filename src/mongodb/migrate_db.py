import json

with open('data.json', 'r') as data_file:
    data = json.load(data_file)

for element in data:
    element.pop('hours', None)

with open('data.json', 'w') as data_file:
    data = json.dump(data, data_file)