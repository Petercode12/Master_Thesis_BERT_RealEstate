from sklearn.metrics import classification_report
from transformers import AutoTokenizer
import numpy as np

import torch
from torch.utils.data import TensorDataset, DataLoader, RandomSampler, SequentialSampler

from sklearn.model_selection import train_test_split

from utils import DatasetProcessor, PhoBERT

import matplotlib.pyplot as plt
plt.style.use("ggplot")

from vncorenlp import VnCoreNLP
# git clone --depth=1 https://github.com/vncorenlp/VnCoreNLP
annotator = VnCoreNLP('NER/VnCoreNLP/VnCoreNLP-1.1.1.jar',
                      annotators="wseg,pos,parse")
print('annotator', annotator)
# https://github.com/VinAIResearch/PhoBERT
tokenizer = AutoTokenizer.from_pretrained("vinai/phobert-base", use_fast=False)

print(tokenizer.bos_token)
print(tokenizer.eos_token)
print(tokenizer.sep_token)
print(tokenizer.pad_token)

tokenizer.encode("{} {} {}".format(tokenizer.bos_token,
                 tokenizer.eos_token, tokenizer.pad_token), add_special_tokens=False)

print(tokenizer.cls_token_id)
print(tokenizer.sep_token_id)
print(tokenizer.pad_token_id)

# text = "Nhà 1 trệt 1 lầu. Diện tích đất 175m2 (Rộng 4.5 x dài 40m). Thổ cư 100m2. Vị trí căn nhà tọa lạc tại khu phố 4, phường Chánh Nghĩa, Thủ Dầu Một, Bình Dương. Cách ngã 3 Lò Chén giao nhau với Cách Mạng Tháng tám khoảng 100m. Nhà có 3 phòng ngủ, 1 phòng thờ, 2 nhà vệ sinh. Diện tích sân trước rộng 100m2 (để được 4 chiếc xe hơi). Nhà có camera an ninh gắn xung quanh nhà. Nước máy năng lượng nóng lạnh. Nhà hướng Tây Bắc. Phong cách thiết kế hiện đại, thoáng mát. Phòng ngủ lót sàn gỗ và ốp gỗ xung quanh nhà. Cần nhượng giá 3,5 tỷ. (Thương lượng trực tiếp). Hoa hồng môi giới 2%. Nhà chính chủ. ĐT: 0947.465.999 Mr Minh."
text = "đường Nguyễn Hậu"
word_segmented_text = annotator.tokenize(text)
word_segmented_text = [w for sentence in word_segmented_text for w in sentence]
segmented_text = ' '.join(word_segmented_text)
segmented_text = segmented_text.replace("\u200b", '')
print(segmented_text)

tokenized_text = tokenizer.tokenize(segmented_text)
# print(tokenized_text)

input_ids = tokenizer.encode(tokenized_text)
# print(input_ids)

tokens = tokenizer.convert_ids_to_tokens(input_ids)
# print(tokens)

max_len = 200

filename = 'NER/labeled_dataset.jsonl'
processor = DatasetProcessor()
processor.load_sentences(filename, max_len)
sentences = processor.get_sentences()
raw_sentences = processor.get_raw_sentences()

print(sentences[3])

processor.load_tags()

tags = processor.get_tags()
n_tags = len(tags)
print(n_tags)
print('tags', tags)
plt.hist([len(s) for s in sentences], bins=5)
# plt.show()
maxlen = max([len(s) for s in sentences])
print('Maximum sentence length:', maxlen)

i = 3
ids = processor.encode_sentence(raw_sentences[i])
print(ids)
print(len(ids))
print(len(sentences[i]))
print(torch.max(torch.tensor(ids)))

# batch size
bs = 32  # changed from 32 to 4
tag_values = processor.get_tags()
tag_values

input_ids, tags, attention_masks = processor.generate_dataset(max_len)

print(len(input_ids[0]))
print(len(tags[0]))
print(len(attention_masks[0]))

for i, ids in enumerate(input_ids):
  m = np.max(ids, axis=-1)
  if m > 64000:
    print(f"sentence #{i+1}, max index = {m}")

idx = 0
tokens = tokenizer.convert_ids_to_tokens(input_ids[idx])
for token, tag in zip(tokens, tags[idx]):
    print("{} : {}".format(token, tag))

tr_inputs, val_inputs, tr_tags, val_tags = train_test_split(input_ids, tags,
                                                            random_state=2022, test_size=0.1)
tr_masks, val_masks, _, _ = train_test_split(attention_masks, input_ids,
                                             random_state=2022, test_size=0.1)

tr_inputs = torch.tensor(tr_inputs)
val_inputs = torch.tensor(val_inputs)
tr_tags = torch.tensor(tr_tags)
val_tags = torch.tensor(val_tags)
tr_masks = torch.tensor(tr_masks)
val_masks = torch.tensor(val_masks)

train_data = TensorDataset(tr_inputs, tr_masks, tr_tags)
train_sampler = RandomSampler(train_data)
train_dataloader = DataLoader(train_data, sampler=train_sampler, batch_size=bs)

valid_data = TensorDataset(val_inputs, val_masks, val_tags)
valid_sampler = SequentialSampler(valid_data)
valid_dataloader = DataLoader(valid_data, sampler=valid_sampler, batch_size=bs)

# download from https://public.vinai.io/PhoBERT_base_transformers.tar.gz
bert = PhoBERT(labels=processor.get_tags(), 
  config_file_path='NER/PhoBERT_base_transformers/config.json',
  pretrained_model_path='NER/PhoBERT_base_transformers/model.bin')

loss_values, validation_loss_values,  accuracy_values, validation_accuracy_values, f1_score_values, validation_f1_score_values = bert.train(
    train_dataloader, valid_dataloader, learning_rate=3e-5, eps=1e-8, max_grad_norm=1.0, epochs=1)

# Plot the learning curve.
plt.plot(loss_values, 'b-o', label="training loss")
plt.plot(validation_loss_values, 'r-o', label="validation loss")

# Label the plot.
plt.title("Learning curve")
plt.xlabel("Epoch")
plt.ylabel("Loss")
plt.legend()

plt.show()
# Plot the accuracy curve.
plt.plot(accuracy_values, 'b-o', label="training accuracy")
plt.plot(validation_accuracy_values, 'r-o', label="validation accuracy")

# Label the plot.
plt.title("Accuracy curve")
plt.xlabel("Epoch")
plt.ylabel("Accuracy")
plt.legend()

plt.show()

# Plot the accuracy curve.
plt.plot(accuracy_values, 'b-o', label="training accuracy")
plt.plot(validation_accuracy_values, 'r-o', label="validation accuracy")

# Label the plot.
plt.title("Accuracy curve")
plt.xlabel("Epoch")
plt.ylabel("Accuracy")
plt.legend()

plt.show()

# Plot the f1-score curve.
plt.plot(f1_score_values, 'b-o', label="training f1-score")
plt.plot(validation_f1_score_values, 'r-o', label="validation f1-score")

# Label the plot.
plt.title("F1-Score curve")
plt.xlabel("Epoch")
plt.ylabel("f1-score")
plt.legend()

plt.show()

bert.save_model(filename="NER/data/phobert")

valid_tags, pred_tags, _, _, _ = bert.evaluate(valid_dataloader)


report = classification_report(valid_tags, pred_tags)
print(report)

bert.load_model()

test_sentence = "Chính chủ cần bán nhà mặt tiền đường Lý Thái Tổ, P1, Quận 10. Đoạn đường lớn gần vòng xoay Lê Hông Phong, Ngô Gia Tự. Diện tích 4.2 x 18m, kết cấu 1 trệt 4 lầu mới, hiện cho thuê thẩm mỹ quốc tế  75tr/tháng. Sản phẩm duy nhất trong tầm giá trên mặt tiền đường chính, lớn, có hợp đồng thuê tốt. Phù hợp cho nhu cầu đầu tư lâu dài giữ tài sản. Giá bán 22.8 tỷ thương lượng. Liên hệ Tấn Phát 0918 92 4949."

contents, labels = bert.predict_sentence(test_sentence)

print('prediction result')
for content, label in zip(contents, labels):
  print("{}\t{}".format(content, label))
