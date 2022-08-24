import os
import jsonlines
import json

def read_doccano_files(input_directory):
    objects = []

    for name in os.listdir(input_directory):
        filename = os.path.join(input_directory, name)
        with jsonlines.open(filename) as reader:
            for obj in reader:
                objects.append(obj)
    objects.sort(key=lambda obj: obj["id"])

    return objects


input_directory = "D:/Documents/Master/Thesis/Documents/Phuong Hoai/label-studio/doccano-jsonl-files"
doccano_objects = read_doccano_files(input_directory)

objects = []
for obj in doccano_objects:
    id = obj["id"]
    data = obj["data"]
    labels = obj["label"]

    result = []
    for label in labels:
        spos = label[0]
        epos = label[1]
        label_name = label[2]
        text = data[spos:epos]
        res = {
            "value": {
                "start": spos,
                "end": epos,
                "text": text,
                "labels": [label_name]
            },
            "from_name": "label",
            "to_name": "text",
            "type": "labels",
            "origin": "manual"
        }
        result.append(res)

    new_obj = {
        "data": {
            "text": data
        },
        "annotations": [
            {
                "result": result
            }
        ]
    }
    objects.append(new_obj)

json_object = json.dumps(objects, indent=4)
with open("D:/Documents/Master/Thesis/Documents/Phuong Hoai/label-studio/label-studio-files/final.json", "w") as outfile:
    outfile.write(json_object)
