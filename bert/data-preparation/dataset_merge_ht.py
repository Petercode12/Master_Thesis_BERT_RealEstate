import re
import jsonlines

def convert_to_doccano_labels(segmented_content, matched_values, tag_name):
    if matched_values is None:
        return []

    labels = []
    idx = 0
    for txt in matched_values:
        start = segmented_content.find(txt, idx)
        if start < 0:
            continue
        end = start + len(txt)
        labels.append([start, end, tag_name])
        idx = end

    return labels


def reindex_dataset(filename, start_id=1):
  objects = []
  id = start_id
  with jsonlines.open(filename) as reader:
      for obj in reader:
          data = obj['data']
          labels = obj['label']
          labels.sort(key=lambda x: x[0])

          objects.append({'id': id, 'data': data, 'label': labels})
          id += 1

  with jsonlines.open(filename, mode='w') as writer:
    for obj in objects:
        writer.write(obj)

filename = 'labeled-datasets/ner_dataset-1-1000-a.jsonl'
reindex_dataset(filename)


def read_jsonline(filename):
  objects = []
  with jsonlines.open(filename) as reader:
      for obj in reader:
          id = obj['id']
          data = obj['data']
          labels = obj['label']
          labels.sort(key=lambda x: x[0])

          objects.append({'id': id, 'data': data, 'label': labels})

  return objects


def write_jsonline(filename, objects):
  with jsonlines.open(filename, mode='w') as writer:
    for obj in objects:
        writer.write(obj)


major_file = 'labeled-datasets/ner_dataset-1-1000-b/nhibt.jsonl'
minor_file = 'labeled-datasets/ner_dataset-1-1000-b/user1.jsonl'
nonlabel_file = 'labeled-datasets/ner_dataset-1-1000-b/unknown.jsonl'

major_objects = read_jsonline(major_file)
minor_objects = read_jsonline(minor_file)
nonlabel_objects = read_jsonline(nonlabel_file)

objects = major_objects.copy()

exiting_ids = dict()
for obj in objects:
  id = obj['id']
  exiting_ids[id] = True

for obj in minor_objects:
  id = obj['id']
  if not exiting_ids.get(id, None):
    objects.append(obj)

for obj in nonlabel_objects:
  id = obj['id']
  if not exiting_ids.get(id, None):
    objects.append(obj)

print(len(objects))

objects.sort(key=lambda x: x['id'])

id = 1
for obj in objects:
  obj['id'] = id
  id += 1

filename = 'labeled-datasets/ner_dataset-1-1000-b.jsonl'
write_jsonline(filename, objects)

objects_a = read_jsonline('labeled-datasets/ner_dataset-1-1000-a.jsonl')
objects_b = read_jsonline('labeled-datasets/ner_dataset-1-1000-b.jsonl')

for obj_a, obj_b in zip(objects_a, objects_b):
  alabels = obj_a['label']
  blabels = obj_b['label']
  alabels.extend(blabels)
  alabels.sort(key=lambda x: x[0])
  obj_a['label'] = alabels

write_jsonline('labeled-datasets/ner_dataset-1-1000_ab.jsonl', objects_a)
