import json
import pyaml
import glob
import collections
import os

os.chdir(os.path.join(os.pardir,'data'))

for filename in glob.glob('*.json'):
    jsonfile = os.path.splitext(filename)[0]
    yamlfile = jsonfile + '.yaml'

    with open(jsonfile+".json", "r") as jfile:
        payload = json.load(jfile, object_pairs_hook=collections.OrderedDict)

    with open(yamlfile, 'w',) as yfile:
        pyaml.dump(payload, yfile, safe=True)
        print(payload)