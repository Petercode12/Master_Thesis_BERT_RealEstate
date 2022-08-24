import re
import pandas as pd
import jsonlines

df = pd.read_csv("hungthinh.csv")
df.info()

print(df.head())

df.loc[df["area"].isna(), "area"] = None
df.loc[df["price"].isna(), "price"] = None
df.loc[df["direction"].isna(), "direction"] = None
df.loc[df["email"].isna(), "email"] = None
df.loc[df["phone"].isna(), "phone"] = None
df.loc[df["real_estate_type"].isna(), "real_estate_type"] = None
df.loc[df["transaction"].isna(), "transaction"] = None
df.loc[df["street"].isna(), "street"] = None
df.loc[df["ward"].isna(), "ward"] = None
df.loc[df["district"].isna(), "district"] = None
df.loc[df["city"].isna(), "city"] = None
df.loc[df["position"].isna(), "position"] = None
df.loc[df["usage"].isna(), "usage"] = None
df.loc[df["room"].isna(), "room"] = None
df.loc[df["floor"].isna(), "floor"] = None
df.loc[df["surrounding"].isna(), "surrounding"] = None
df.loc[df["legal"].isna(), "legal"] = None


def get_values_from_series(series, name):
    values = series[name]
    if values:
        values = values.split(";")
    return values


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

def update_tags(segmented_content, tags, matched_values, tag_name):
    idx = 0
    if not matched_values:
        return
    for txt in matched_values:
        s = txt.split(" ")
        # to do fix     update_tags(segmented_content, tags, price, 'price')
        # File "d:\Documents\Master\Thesis\Documents\Phuong Hoai\data-preparation\dataset_preparation_ht.py", line 59, in update_tags
        # pos = segmented_content.index(s[0], idx)
        # ValueError: '3.8' is not in list
        try:
          pos = segmented_content.index(s[0], idx)
          tags[pos] = 'B-'+tag_name
          for i in range(1, len(s)):
              tags[pos+i] = 'I-'+tag_name
          idx += len(s)
        except:
          print('')

for index, row in df.iterrows():
    segmented_content = row["segmented_content"]
    segmented_content = segmented_content.split()

    area = get_values_from_series(row, 'area')
    direction = get_values_from_series(row, 'direction')
    price = get_values_from_series(row, 'price')
    phone = get_values_from_series(row, 'phone')
    email = get_values_from_series(row, 'email')
    real_estate_type = get_values_from_series(row, 'real_estate_type')
    transaction = get_values_from_series(row, 'transaction')
    street = get_values_from_series(row, 'street')
    ward = get_values_from_series(row, 'ward')
    district = get_values_from_series(row, 'district')
    city = get_values_from_series(row, 'city')
    position = get_values_from_series(row, 'position')
    usage = get_values_from_series(row, 'usage')
    room = get_values_from_series(row, 'room')
    floor = get_values_from_series(row, 'floor')

    tags = ['O'] * len(segmented_content)
    update_tags(segmented_content, tags, area, 'area')
    update_tags(segmented_content, tags, direction, 'direction')
    update_tags(segmented_content, tags, price, 'price')
    update_tags(segmented_content, tags, phone, 'phone')
    update_tags(segmented_content, tags, email, 'email')
    update_tags(segmented_content, tags, real_estate_type, 'real_estate_type')
    update_tags(segmented_content, tags, transaction, 'transaction')
    update_tags(segmented_content, tags, street, 'street')
    update_tags(segmented_content, tags, ward, 'ward')
    update_tags(segmented_content, tags, district, 'district')
    update_tags(segmented_content, tags, city, 'city')
    update_tags(segmented_content, tags, position, 'position')
    update_tags(segmented_content, tags, position, 'usage')
    update_tags(segmented_content, tags, position, 'room')
    update_tags(segmented_content, tags, position, 'floor')

    df.loc[index, "tags"] = ";".join(tags)

objects = []

for index, row in df.iterrows():
    labels = []
    text = row["segmented_content"]

    area = get_values_from_series(row, 'area')
    direction = get_values_from_series(row, 'direction')
    price = get_values_from_series(row, 'price')
    phone = get_values_from_series(row, 'phone')
    email = get_values_from_series(row, 'email')
    real_estate_type = get_values_from_series(row, 'real_estate_type')
    transaction = get_values_from_series(row, 'transaction')
    street = get_values_from_series(row, 'street')
    ward = get_values_from_series(row, 'ward')
    district = get_values_from_series(row, 'district')
    city = get_values_from_series(row, 'city')
    position = get_values_from_series(row, 'position')
    usage = get_values_from_series(row, 'usage')
    room = get_values_from_series(row, 'room')
    floor = get_values_from_series(row, 'floor')
    surrounding = get_values_from_series(row, 'surrounding')
    legal = get_values_from_series(row, 'legal')

    labels.extend(convert_to_doccano_labels(text, area, 'area'))
    labels.extend(convert_to_doccano_labels(text, direction, 'direction'))
    labels.extend(convert_to_doccano_labels(text, price, 'price'))
    labels.extend(convert_to_doccano_labels(text, phone, 'phone'))
    labels.extend(convert_to_doccano_labels(text, email, 'email'))
    labels.extend(convert_to_doccano_labels(
        text, real_estate_type, 'real_estate_type'))
    labels.extend(convert_to_doccano_labels(text, transaction, 'transaction'))
    labels.extend(convert_to_doccano_labels(text, street, 'street'))
    labels.extend(convert_to_doccano_labels(text, ward, 'ward'))
    labels.extend(convert_to_doccano_labels(text, district, 'district'))
    labels.extend(convert_to_doccano_labels(text, city, 'city'))
    labels.extend(convert_to_doccano_labels(text, position, 'position'))
    labels.extend(convert_to_doccano_labels(text, usage, 'usage'))
    labels.extend(convert_to_doccano_labels(text, room, 'room'))
    labels.extend(convert_to_doccano_labels(text, floor, 'floor'))
    labels.extend(convert_to_doccano_labels(text, surrounding, 'surrounding'))
    labels.extend(convert_to_doccano_labels(text, legal, 'legal'))

    labels.sort(key=lambda x: x[0])

    objects.append({'text': text, 'label': labels})

    # if index == 5:
    #     break

with jsonlines.open('ner_dataset.jsonl', mode='a') as writer:
    for obj in objects:
        writer.write(obj)
