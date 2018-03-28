import json


def read_json(file_path):
    return [json.loads(x) for x in open(file_path)]

def save_json(alignments,file_path):
    with open(file_path, 'w') as f:
        for alignment in alignments:
            f.write(json.dumps(alignment)+"\n")
