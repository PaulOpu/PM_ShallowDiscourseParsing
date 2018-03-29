import json
from os import walk,listdir
from os.path import isfile, join

def read_json(file_path):
    return [json.loads(x) for x in open(file_path)]

def save_json(data,file_path):
    with open(file_path, 'w') as f:
        for date in data:
            f.write(json.dumps(date)+"\n")

def get_parser_paths(path):
	parser_names = list(walk(path))[0][1]
	return [(parser_name,path+parser_name+"/output/output.json") for parser_name in parser_names]

def get_files_in_directory(path):

	return [f for f in listdir(path) if isfile(join(path, f)) and (f != ".DS_Store")]