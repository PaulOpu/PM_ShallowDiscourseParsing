import json


def read_json(file_path):
    return [json.loads(x) for x in open(file_path)]

def save_json(data,file_path):
    with open(file_path, 'w') as f:
        for date in data:
            f.write(json.dumps(date)+"\n")

def save_model_json