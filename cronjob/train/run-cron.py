import os
from .utils import DatasetProcessor, PhoBERT

import psycopg2

def extractSentenceApi(text):
    processor = DatasetProcessor()
    processor.load_tags()
    # 
    
    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
      
    bert = PhoBERT(labels=processor.get_tags(), 
    config_file_path=os.path.join(__location__,'PhoBERT_base_transformers','config.json'),
    pretrained_model_path=os.path.join(__location__,'PhoBERT_base_transformers','model.bin'))
    bert.load_model(filename=os.path.join(__location__,'model-training','phobert'))
    contents, labels = bert.predict_sentence(text)
    jsonResult = ''
    start = 0
    for content, label in zip(contents, labels):
        if start > 0 :
            jsonResult += ','
        jsonResult += f'{{"{label}": "{content}"}}'
        start += 1
    return f'[{jsonResult}]'


connection = psycopg2.connect(
    host="129.146.248.20",
    port="5432", #default
    database="ttndung",
    user="tdung",
    password="8M44Ck48wn3J")

cursor = connection.cursor()   

cursor.execute('SELECT house_id, "Description" FROM house_houses where house_id not in (select org_id from house_extractsentence) LIMIT 50 OFFSET 0')
rows = cursor.fetchall()

for row in rows:
    org_id = row[0]
    description = row[1]
    result = extractSentenceApi(description)
    cursor.execute(f"INSERT INTO house_extractsentence (org_id, result_sentence) VALUES ({org_id}, '{result}')")

connection.commit()

connection.close()   