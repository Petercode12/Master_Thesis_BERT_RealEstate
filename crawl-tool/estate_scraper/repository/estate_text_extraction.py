from ner_tag import NER
import os

ner = NER()

# Query data
query = 'SELECT id , CONCAT(title, " " , IFNULL(price, ""), " ", IFNULL(sqm, ""), " ", description) AS descriptions FROM batdongsancom'
cursor.execute(query)
data = cursor.fetchall()

for row in data:
    insert_data = []
    postId = row[0]
    text = row[1]
    result = ner.predict([text])
    for tag in result[0]['tags']:
        if(tag['type'] != 'normal'):
            insert_data.append(
                (tag['type'].strip(), tag['content'].strip(), postId))
    cursor.executemany(insert_script, list(set(insert_data)))
    db.commit()
