import os
from .utils import DatasetProcessor, PhoBERT

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