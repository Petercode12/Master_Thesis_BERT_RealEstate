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

objects = []

filename = 'dataset_1-1000_220314.jsonl'

with jsonlines.open(filename) as reader:
    for obj in reader:
        # print(obj)
        text = obj['data']
        labels = obj['label']

        # create new labels
        new_labels = []
        for idx, label in enumerate(labels):
            # remove surrounding label
            if label[2] == 'surrounding':
                continue

            # remove usage label
            if label[2] == 'usage':
                continue

            # modify label room
            if label[2] == 'room':
                spos = label[0]
                epos = label[1]
                content = text[spos:epos]
                if 'phòng ngủ' in content or 'Phòng ngủ' in content or 'Phòng Ngủ' in content or 'PN' in content or 'pn' in content or 'Pn' in content:
                    label[2] = 'bed_room'
                elif 'ngủ' in content:
                    label[2] = 'bed_room'
                elif 'phòng khách' in content or 'Phòng khách' in content or 'Phòng Khách' in content or 'PK' in content or 'pk' in content:
                    label[2] = 'living_room'
                elif 'phòng tắm' in content or 'Phòng tắm' in content or 'Phòng Tắm' in content or 'PT' in content or 'pt' in content:
                    label[2] = 'bath_room'
                elif 'toilet' in content or 'Toilet' in content or 'tolet' in content or 'toile' in content:
                    label[2] = 'bath_room'
                elif 'WC' in content or 'wc' in content:
                    label[2] = 'bath_room'
                elif 'nhà_vệ_sinh' in content or 'Nhà_vệ_sinh' in content:
                    label[2] = 'bath_room'
                elif 'vệ_sinh' in content or 'Vệ_sinh' in content:
                    label[2] = 'bath_room'
                elif 'vệ_sinh' in content or 'Vệ_sinh' in content:
                    label[2] = 'bath_room'
                elif 'phòng_vệ sinh' in content or 'phòng_vệ_sinh' in content:
                    label[2] = 'bath_room'
                else:
                    continue

            if label[2] == "real_estate_type":
                spos = label[0]
                epos = label[1]
                content = text[spos:epos]
                real_estate_sub_types = ["chung_cư", "Chung_cư"]
                if content in real_estate_sub_types:
                    label[2] = 'real_estate_sub_type'

            new_labels.append(label)

        # add new real_estate_type
        pattern = r'(?:nhà biệt_thự|biệt_thự|Biệt_thự|BT)'
        real_estate_type_list = [
            r.strip() if r is not None else None for r in re.findall(pattern, text)]
        new_labels.extend(convert_to_doccano_labels(
            text, real_estate_type_list, 'real_estate_type'))

        # add new real_estate_sub_types
        pattern = r'(?:CHUNG_CƯ|lofthouse|Lofthouse|penthouse|Penthouse|Shophouse|shophouse|Penhouse|Officetel|officetel|Duplex_Feliz_En_Vista|Duplex|Căn_Duplex|sky villas|Đơn_lập|đơn_lập|Song lập|song lập|tứ lập|Tứ lập)'
        real_estate_sub_type_list = [
            r.strip() if r is not None else None for r in re.findall(pattern, text)]
        new_labels.extend(convert_to_doccano_labels(
            text, real_estate_sub_type_list, 'real_estate_sub_type'))

        objects.append({'text': text, 'label': new_labels})


new_filename = 'ner_dataset-1-1000_updated.jsonl'


with jsonlines.open(new_filename, mode='a') as writer:
    for obj in objects:
        writer.write(obj)
