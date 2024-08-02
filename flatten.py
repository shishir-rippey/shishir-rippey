import json
from utility.utils import dump_json
from settings import settings


def flatten_json(obj):
    ret = {}
    def flatten(x, flattened_key=""):
        if type(x) is list:
            i = 0
            for elem in x:
                flatten(elem, flattened_key + str(i) + '_')
        elif type(x) is dict:
            for current_key in x:
                flatten(x[current_key], flattened_key + current_key + '_')

        else:
            # if x is string or int not nested
            ret[flattened_key[:-1]] = x
    flatten(obj)
    return ret 

if __name__=="__main__":
    with open("tmp/azure_extraction.json", "r") as nested_obj:
        json_objs=json.load(nested_obj)
        # print(json_objs)
        flatten_data=[]
        for data in json_objs:
            data_flatten=flatten_json(data)
            flatten_data.append(data_flatten)
        dump_json(settings.FLAT_AZURE_EXTRACTION, flatten_data)

