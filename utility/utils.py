
import json
import os
import re
from concurrent.futures import ThreadPoolExecutor
import base64
import requests

import pandas


def list_files(path: str, extensions: str | tuple = None) -> list[str]:
    filenames = []
    for subdir, _, files in os.walk(path):
        for file in files:
            if not extensions or file.lower().endswith(extensions):
                filename = os.path.join(subdir, file)
                filenames.append(filename)
    return filenames


def flatten(json_obj, prefix=""):
    flattened = {}
    if isinstance(json_obj, dict):
        for key, value in json_obj.items():
            if isinstance(value, (dict, list)):
                flattened.update(flatten(value, prefix + key + "."))
            else:
                flattened[prefix + key] = value
    elif isinstance(json_obj, list):
        for i, item in enumerate(json_obj):
            if isinstance(item, (dict, list)):
                flattened.update(flatten(item, prefix + "[" + str(i) + "]"))
            else:
                flattened[prefix + str(i)] = item
    return flattened


def clean_flat_data(flat_json):
    new_json = {}
    for key, value in flat_json.items():
        k = re.sub(
            r"extracted_data.(?:entity_detail|location_detail|additional_detail|document_detail|charge_details)(.\[\d+\]data\.\[\d+\])?", "", key
        )
        k = k.strip(".")
        if k not in new_json:
            new_json[k] = [value]
        else:
            new_json[k].append(value)
    for key, value in new_json.items():
        if isinstance(value, list) and (len(value) < 2 or not value):
            new_json[key] = str(value[0]) if value else ""
    return new_json


def flatten_json(json):
    flattened = flatten(json)
    return clean_flat_data(flattened)


def dump_json(filename, data: dict | list) -> None:
    with open(filename, "w") as f:
        json.dump(data, f, indent=4)


def run_in_thread(func, iterables, max_workers=10):
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        results = list(executor.map(func, [iterable for iterable in iterables]))
        return results


def rearrange_df(df, cols_to_bring_forth=2):
    columns = df.columns.tolist()
    columns = columns[-cols_to_bring_forth:] + columns[:-cols_to_bring_forth]
    return df[columns]


def json_to_excel(json_data, filename="model_extraction.xlsx"):
    for _json in json_data:
        for k, v in _json.items():
            if isinstance(v, list):
                _json[k] = json.dumps(v, indent=4)
    df = pandas.DataFrame(json_data)
    df = rearrange_df(df)
    df.to_excel(filename, index=False)


def resign(file_name, file_url):
    print(f"Resigning url for {file_name}")
    sign_url = "https://appserver.rippey.ai/analytics/general/signUrl"
    encoded_file_name = file_name.encode("utf-8")
    encoded_file_url = file_url.encode("utf-8")
    base64_encoded_file_name = base64.b64encode(encoded_file_name)
    base64_encoded_file_url = base64.b64encode(encoded_file_url)
    response = requests.get(
        sign_url,
        params={
            "file_name": base64_encoded_file_name,
            "file_url": base64_encoded_file_url,
        },
    )
    if response.ok:
        response = response.json()
        return response.get("data", None)
    print("Couldn't resign!")
    return None