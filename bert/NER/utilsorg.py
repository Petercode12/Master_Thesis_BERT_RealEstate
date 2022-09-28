import enum
from operator import index
import jsonlines
import numpy as np
from tqdm import trange

from sklearn.metrics import classification_report
from sklearn.metrics import f1_score, accuracy_score

from tensorflow.keras.preprocessing.sequence import pad_sequences

import torch

from transformers import RobertaForTokenClassification, RobertaConfig, AdamW
from transformers import get_linear_schedule_with_warmup
from transformers import AutoTokenizer

from vncorenlp import VnCoreNLP

from constants import *

PADDING_TAG = "PAD"

class DatasetProcessor(object):
    def __init__(self, model_name='MODEL_PHOBERT_BASE') -> None:
        self.__raw_sentences = None
        self.__sentences = None

        self.__tags = None
        self.__tag2idx = None
        self.__idx2tag = None

        self.__tokenizer = None

        self.__load_tokenizer(model_name)

    def load_sentences(self, filename='dataset.jsonl', max_sentence_len=200):
        # provision for bos_token and eos_token
        max_sentence_len = max_sentence_len-2
        self.__raw_sentences, self.__sentences = self.__read_jsonline_file(filename, max_sentence_len)    # 

        tags = [t for sentence in self.__sentences for _, t in sentence]
        tags = list(set(tags))
        tags.sort()
        tags.append(PADDING_TAG)
        self.__tags = tags

        self.__tag2idx = {t: i for i, t in enumerate(tags)}
        self.__idx2tag = {i: t for i, t in enumerate(tags)}    
    
    def __generate_sentence(self, id, text, labels):
        encoded_words = self.__tokenizer.tokenize(text)
        current_pos = 0
        tags = []
        for label in labels:
            #if len(tags) < len(encoded_words) :
            #    break
            spos = label[0]
            epos = label[1]
            label_name = label[2]
            
            normal_text = text[current_pos:spos]
            if normal_text:
                subwords = self.__tokenizer.tokenize(normal_text)
                tags.extend(['O'] * len(subwords))
            
            labeled_text = text[spos:epos]
            subwords = self.__tokenizer.tokenize(labeled_text)
            tags.append('B-'+label_name)
            if len(subwords) > 1:
                for i in range(1, len(subwords)):
                    tags.append('I-'+label_name)
            
            current_pos = epos
        
        if current_pos < len(text):
            normal_text = text[current_pos:len(text)]
            subwords = self.__tokenizer.tokenize(normal_text)
            tags.extend(['O'] * len(subwords))
        
        if len(encoded_words) != len(tags):
            print("raw text id:", id)
            # print("raw text:", text)
            # print("length of encoded_words:", len(encoded_words))
            # print("length of tags:", len(tags))
            # print("encoded_words:", encoded_words)
            # print("tags:", tags)
            return None
        assert len(encoded_words) == len(tags)
        
        sentence = []
        for idx, w in enumerate(encoded_words):
            sentence.append((w, tags[idx]))
        return sentence

    def __append_sentence(self, sentences, sentence, max_sentence_len):
        if len(sentence) <= max_sentence_len:
            sentences.append(sentence)
            return

        idx = max_sentence_len-1
        while sentence[idx][0] != "." and sentence[idx][0] != "," and idx > 0:
            idx -= 1
        if idx == 0:
            idx = max_sentence_len-1
        s = sentence[:idx+1].copy()
        sentences.append(s)
        remaining_s = sentence[idx+1:].copy()
        self.__append_sentence(sentences, remaining_s, max_sentence_len)

    def __read_jsonline_file(self, filename, max_sentence_len):
        sentences = []
        intdex = 1
        with jsonlines.open(filename) as reader:
            for obj in reader:                
                id = obj['id']
                text = obj['data']
                labels = obj['label']
                labels.sort(key=lambda x: x[0])

                sentence = self.__generate_sentence(id, text, labels)
                if sentence != None:
                    self.__append_sentence(sentences, sentence, max_sentence_len)
                #else:
                    #intdex +=1
                    #print("number lost: ", intdex)

        raw_sentences = []
        for sentence in sentences:
            words = []
            for word, _ in sentence:
                words.append(word)
            raw_sentence = ' '.join(words)
            raw_sentences.append(raw_sentence.replace("@@ ", ""))
        return raw_sentences, sentences

    def get_raw_sentences(self):
        return self.__raw_sentences

    def get_sentences(self):
        return self.__sentences

    def __load_tokenizer(self, model_name):
        if model_name == 'MODEL_PHOBERT_BASE':
            self.__tokenizer = AutoTokenizer.from_pretrained("vinai/phobert-base", use_fast=False)
        elif model_name == 'MODEL_PHOBERT_LARGE':
            self.__tokenizer = AutoTokenizer.from_pretrained("vinai/phobert-large", use_fast=False)
        else:
            self.__tokenizer = AutoTokenizer.from_pretrained("vinai/phobert-base", use_fast=False)

    def get_tokenizer(self):
        return self.__tokenizer

    def encode_sentence(self, sentence: str, add_special_tokens=False):
        result = self.__tokenizer.encode(sentence, add_special_tokens=add_special_tokens)
        #if None in result:
        #print ("result: ==========", result)
        return result

    def get_tags(self):
        return self.__tags

    def get_tag2idx(self):
        return self.__tag2idx

    def get_idx2tag(self):
        return self.__idx2tag

    def save_tags(self):
        with open('NER/tags.txt', 'w') as f:
            for tag in self.__tags:
                f.write(tag + '\n')

    def load_tags(self):
        with open('NER/tags.txt', 'r') as f:
            self.__tags = [line.rstrip('\n') for line in f]
            
        self.__tag2idx = {t: i for i, t in enumerate(self.__tags)}
        self.__idx2tag = {i: t for i, t in enumerate(self.__tags)}

    def generate_dataset(self, max_len=None):
        # bos_token = <s>   --> 0
        # eos_token = </s>  --> 2
        # pad_token = <pad> --> 1
        print("max_len=None------", max_len)
        if max_len is None:
            max_len = max([len(s) for s in self.__sentences])
        
        input_ids = [self.encode_sentence(txt, True) for txt in self.__raw_sentences]
        
        tags = [[self.__tag2idx.get(t) for _, t in sentence] for sentence in self.__sentences]
        for idx, ts in enumerate(tags):
            ts.insert(0, self.__tag2idx['O'])
            ts.append(self.__tag2idx['O'])

            res = []
            for val in ts:
                if val != None :
                    res.append(val)
            if len(ts) != len (res):
                print ("The original list is : " + str(ts))
                print ("List after removal of None values : " + str(res))
            
            tags[idx] = res
        
        attention_masks = [[1.0]*len(ii) for ii in input_ids]
        print("value=self.__tokenizer.pad_token_id-----", self.__tokenizer.pad_token_id)
        print("value=self.__tag2idx[PADDING_TAG]-----", self.__tag2idx[PADDING_TAG])
        input_ids = pad_sequences( input_ids, maxlen=max_len, dtype="long", truncating="post", padding="post", value=self.__tokenizer.pad_token_id )
        tags = pad_sequences( tags, maxlen=max_len, dtype="long", truncating="post", padding="post", value=self.__tag2idx[PADDING_TAG] )
        attention_masks = pad_sequences( attention_masks, maxlen=max_len, dtype="long", truncating="post", padding="post", value=0.0)

        return input_ids, tags, attention_masks

class PhoBERT(object):
    def __init__(self, labels, config_file_path, pretrained_model_path, model_name='MODEL_PHOBERT_BASE') -> None:
        
        self.__device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        self.__labels = labels

        config = RobertaConfig.from_pretrained(
            config_file_path, from_tf=False, num_labels = len(labels),
            output_hidden_states=False, output_attentions = False,
        )

        self.__model = RobertaForTokenClassification.from_pretrained(
            pretrained_model_path,
            config=config
        )
        self.__model.to(self.__device)

        self.__optimizer = None
        self.__scheduler = None

        self.__annotator = VnCoreNLP('NER/VnCoreNLP/VnCoreNLP-1.1.1.jar',
                                     annotators="wseg,pos,parse")
        if model_name == 'MODEL_PHOBERT_BASE':
            self.__tokenizer = AutoTokenizer.from_pretrained("vinai/phobert-base", use_fast=False)
        elif model_name == 'MODEL_PHOBERT_LARGE':
            self.__tokenizer = AutoTokenizer.from_pretrained("vinai/phobert-large", use_fast=False)
        else:
            self.__tokenizer = AutoTokenizer.from_pretrained("vinai/phobert-base", use_fast=False)

    def get_device(self):
        return self.__device

    def get_annotator(self):
        return self.__annotator

    def get_tokenizer(self):
        return self.__tokenizer

    def get_model(self):
        return self.__model

    def save_model(self, filename="phobert"):
        torch.save(self.__model, filename)

    def load_model(self, filename="phobert"):
        model = torch.load(filename, map_location=torch.device("cuda" if torch.cuda.is_available() else "cpu"))
        self.__model = model

    def __set_optimizer(self, learning_rate, eps):
        param_optimizer = list(self.__model.named_parameters())
        no_decay = ['bias', 'gamma', 'beta']
        optimizer_grouped_parameters = [
            {'params': [p for n, p in param_optimizer if not any(nd in n for nd in no_decay)],
            'weight_decay_rate': 0.01},
            {'params': [p for n, p in param_optimizer if any(nd in n for nd in no_decay)],
            'weight_decay_rate': 0.0}
        ]
        self.__optimizer = AdamW(
            optimizer_grouped_parameters,
            lr=learning_rate,
            eps=eps
        )
    
    def __set_scheduler(self, num_batches, epochs):
        # Total number of training steps is number of batches * number of epochs.
        total_steps = num_batches * epochs

        # Create the learning rate scheduler.
        self.__scheduler = get_linear_schedule_with_warmup(
            self.__optimizer,
            num_warmup_steps=0,
            num_training_steps=total_steps
        )

    def train(self, train_dataloader, valid_dataloader, learning_rate=3e-5, eps=1e-8, max_grad_norm=1.0, epochs=10, saved_model_name="phobert"):
        print('Training by: ', self.__device)
        self.__set_optimizer(learning_rate, eps)
        self.__set_scheduler(len(train_dataloader), epochs)

        ## Store the average loss after each epoch so we can plot them.
        loss_values, validation_loss_values = [], []
        accuracy_values, validation_accuracy_values = [], []
        f1_score_values, validation_f1_score_values = [], []
        max_accuracy, max_f1_score, min_loss = 0.0, 0.0, 1E9

        for _ in trange(epochs, desc="Epoch"):
            saved = False

            # ========================================
            #               Training
            # ========================================
            # Perform one full pass over the training set.

            # Put the model into training mode.
            self.__model.train()
            # Reset the total loss for this epoch.
            total_loss = 0
            predictions , true_labels = [], []
            # Training loop
            for step, batch in enumerate(train_dataloader):
                # add batch to gpu
                batch = tuple(t.to(self.__device) for t in batch)
                b_input_ids, b_input_mask, b_labels = batch
                b_labels = b_labels.to(torch.int64)
                # Always clear any previously calculated gradients before performing a backward pass.
                self.__model.zero_grad()
                # forward pass
                # This will return the loss (rather than the model output)
                # because we have provided the `labels`.
                outputs = self.__model(b_input_ids, token_type_ids=None,
                                attention_mask=b_input_mask, labels=b_labels)
                # get the loss
                loss = outputs[0]
                # track train loss
                total_loss += loss.item()
                # Perform a backward pass to calculate the gradients.
                loss.backward()

                # Move logits and labels to CPU
                logits = outputs[1].detach().to('cpu').numpy()
                label_ids = b_labels.to('cpu').numpy()

                predictions.extend([list(p) for p in np.argmax(logits, axis=2)])
                true_labels.extend(label_ids)

                # Clip the norm of the gradient
                # This is to help prevent the "exploding gradients" problem.
                torch.nn.utils.clip_grad_norm_(parameters=self.__model.parameters(), max_norm=max_grad_norm)
                # update parameters
                self.__optimizer.step()
                # Update the learning rate.
                self.__scheduler.step()

            # Calculate the average loss over the training data.
            avg_train_loss = total_loss / len(train_dataloader)
            # Store the loss value for plotting the learning curve.
            loss_values.append(avg_train_loss)
            print("Average train loss: {}".format(avg_train_loss))

            pred_tags = [self.__labels[p_i] for p, l in zip(predictions, true_labels)
                                        for p_i, l_i in zip(p, l) if self.__labels[l_i] != PADDING_TAG]
            valid_tags = [self.__labels[l_i] for l in true_labels
                                        for l_i in l if self.__labels[l_i] != PADDING_TAG]
            
            accuracy = accuracy_score(pred_tags, valid_tags)
            accuracy_values.append(accuracy)
            print("Average Train Accuracy: {}".format(accuracy))

            f1score = f1_score(pred_tags, valid_tags, average='weighted')
            f1_score_values.append(f1score)
            print("Average Train F1-Score: {}".format(f1score))

            # check to save model if current model is the best
            if max_accuracy < accuracy and max_f1_score < f1score and min_loss > avg_train_loss:
                max_accuracy = accuracy
                max_f1_score = f1score
                min_loss = avg_train_loss
                print("saving the best performance model ...")
                self.save_model("{}".format(saved_model_name))
                saved = True
            else:
                print("saving model ...")
                self.save_model("{}1".format(saved_model_name))

            print()

            # ========================================
            #               Validation
            # ========================================
            # After the completion of each training epoch, measure our performance on
            # our validation set.

            if valid_dataloader is not None:
                _, _, eval_loss, accuracy, f1score = self.evaluate(valid_dataloader)
                validation_loss_values.append(eval_loss)
                validation_accuracy_values.append(accuracy)
                validation_f1_score_values.append(f1score)

                print()
            
            with open("{}_logs.csv".format(saved_model_name), 'a') as file:
                if valid_dataloader is not None:
                    file.write(f"{loss_values[len(loss_values)-1]},{accuracy_values[len(accuracy_values)-1]},{f1_score_values[len(f1_score_values)-1]},\
                        {validation_loss_values[len(validation_loss_values)-1]},{validation_accuracy_values[len(validation_accuracy_values)-1]},\
                        {validation_f1_score_values[len(validation_f1_score_values)-1]},{saved}\n")
                else:
                    file.write(f"{loss_values[len(loss_values)-1]},{accuracy_values[len(accuracy_values)-1]},{f1_score_values[len(f1_score_values)-1]},0,0,0,{saved}\n")
                    
        return loss_values, validation_loss_values,  accuracy_values, validation_accuracy_values, f1_score_values, validation_f1_score_values

    def evaluate(self, valid_dataloader):
        # Put the model into evaluation mode
        self.__model.eval()
        # Reset the validation loss for this epoch.
        eval_loss = 0
        predictions , true_labels = [], []
        for batch in valid_dataloader:
            batch = tuple(t.to(self.__device) for t in batch)
            b_input_ids, b_input_mask, b_labels = batch
            b_labels = b_labels.to(torch.int64)

            # Telling the model not to compute or store gradients,
            # saving memory and speeding up validation
            with torch.no_grad():
                # Forward pass, calculate logit predictions.
                # This will return the logits rather than the loss because we have not provided labels.
                outputs = self.__model(b_input_ids, token_type_ids=None,
                                attention_mask=b_input_mask, labels=b_labels)
            # Move logits and labels to CPU
            logits = outputs[1].detach().to('cpu').numpy()
            label_ids = b_labels.to('cpu').numpy()

            # Calculate the accuracy for this batch of test sentences.
            eval_loss += outputs[0].mean().item()
            predictions.extend([list(p) for p in np.argmax(logits, axis=2)])
            true_labels.extend(label_ids)

        eval_loss = eval_loss / len(valid_dataloader)
        
        print("Validation loss: {}".format(eval_loss))
        
        pred_tags = [self.__labels[p_i] for p, l in zip(predictions, true_labels)
                                    for p_i, l_i in zip(p, l) if self.__labels[l_i] != PADDING_TAG]
        valid_tags = [self.__labels[l_i] for l in true_labels
                                    for l_i in l if self.__labels[l_i] != PADDING_TAG]
        
        accuracy = accuracy_score(pred_tags, valid_tags)
        print("Validation Accuracy: {}".format(accuracy))

        f1score = f1_score(pred_tags, valid_tags, average='weighted')
        print("Validation F1-Score: {}".format(f1score))

        return pred_tags, valid_tags, eval_loss, accuracy, f1score

    def predict_sentence(self, sentence, max_len=200):
        segmented_words = self.__annotator.tokenize(sentence)
        segmented_words = [word for sublist in segmented_words for word in sublist]
        segmented_sentence = " ".join(segmented_words)
        return self.predict_segmented_sentence(segmented_sentence, max_len, True)

    def __split_array(self, arr, max_len):
        if len(arr) <= max_len:
            return [arr.copy()]
        idx = max_len
        # 4 = . ; 5 = ,
        while arr[idx] != 4 and arr[idx] != 5 and idx > 0:
            idx -= 1
        if idx == 0:
            idx = max_len
        results = [arr[:idx].copy()]
        results.extend(self.__split_array(arr[idx:].copy(), max_len))
        return results

    def predict_segmented_sentence(self, segmented_sentence, max_len=200, unsegmented=False):
        # Put the model into evaluation mode
        self.__model.eval()
        x_raw = self.__tokenizer.encode(segmented_sentence, add_special_tokens=True)
        xs = self.__split_array(x_raw, max_len)
        new_tokens, new_tags = [], []
        for x in xs:
            input_ids = torch.tensor([x])
            with torch.no_grad():
                y = self.__model(input_ids) if self.__device == 'cpu' else self.__model(input_ids)
            label_indices = np.argmax(y[0].to('cpu').numpy(), axis=2)
            label_indices = label_indices[0]
            tokens = self.__tokenizer.convert_ids_to_tokens(input_ids.to('cpu').numpy()[0])

            for token, label_idx in zip(tokens, label_indices):
                if token == "<s>" or token == "</s>" or token == "<pad>":
                    continue
                tag = self.__labels[label_idx]
                if tag == PADDING_TAG:
                    tag = "O"
                new_tags.append(tag)
                new_tokens.append(token)

        new_tokens, new_tags = self.__convert_subwords_to_text(new_tokens, new_tags)
        new_tokens = self.__fix_unknown_tokens(new_tokens, segmented_sentence)
        return self.__generate_content_label(new_tokens, new_tags, unsegmented)

    def __convert_subwords_to_text(self, tokens, tags):
        idx = 0
        tks, ts = [], []
        while idx < len(tags):
            current_tag = tags[idx]
            current_token = tokens[idx]
            updated = True
            while current_token.endswith("@@"):
                idx += 1
                if idx < len(tags):
                    if tokens[idx] != "," and tokens[idx] != ".":
                        current_token += " " + tokens[idx]
                        current_token = current_token.replace("@@ ", "")
                        if current_tag == "O":
                            current_tag = tags[idx]
                    else:
                        updated = False
                        current_token = current_token.replace("@@", "")
                        break
                else:
                    updated = False
                    current_token = current_token.replace("@@", "")
                    break
            tks.append(current_token)
            ts.append(current_tag)
            if updated:
                idx += 1

        return tks, ts

    def __generate_content_label(self, tokens, tags, unsegmented):
        contents, labels = [], []
        idx = 0
        while idx < len(tags):
            ts = []
            current_tag = tags[idx]
            current_token = tokens[idx]
            
            if current_tag == "O":
                current_label = current_tag
                ts.append(current_token)
                labels.append(current_label)

                idx += 1
                while idx < len(tags):
                    next_tag = tags[idx]
                    if next_tag != "O":
                        break
                    next_token = tokens[idx]
                    ts.append(next_token)
                    idx += 1
                
                content = ' '.join(ts)
                if unsegmented:
                    content = content.replace(" _ ", " ")
                    content = content.replace("_", " ")
                contents.append(content)
                continue

            if current_tag.startswith('B-') or current_tag.startswith('I-'):
                current_label = current_tag[2:]
                ts.append(current_token)
                labels.append(current_label)

                idx += 1
                while idx < len(tags):
                    next_tag = tags[idx]
                    next_label = next_tag[2:]
                    if next_label != current_label:
                        break
                    next_token = tokens[idx]
                    ts.append(next_token)
                    idx += 1
                
                content = ' '.join(ts)
                if unsegmented:
                    content = content.replace(" _ ", " ")
                    content = content.replace("_", " ")
                contents.append(content)
                continue

        return contents, labels

    def __fix_unknown_tokens(self, tokens, segmented_text):
        current_pos = 0
        for idx, token in enumerate(tokens):
            if token == "<unk>" and idx < len(tokens)-1:
                next_token = tokens[idx+1]
                pos = segmented_text.find(next_token, current_pos)
                if pos >= 0:
                    tokens[idx] = segmented_text[current_pos:pos-1]
            current_pos += len(tokens[idx]) + 1
        return tokens

def plot_classification_report(preds, truths, idx2tag):
    preds = np.argmax(preds, axis=-1)
    truths = np.argmax(np.array(truths), axis=-1)

    preds = preds.flatten()
    truths = truths.flatten()

    pred_tag = [idx2tag[i] for i in preds]
    true_tag = [idx2tag[i] for i in truths]

    report = classification_report(true_tag, pred_tag)
    print(report)