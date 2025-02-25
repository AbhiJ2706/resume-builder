import nltk.data
import spacy
import torch

from torch.nn.functional import cosine_similarity
from transformers import BertTokenizer, BertModel

import json

from resume_builder.keyword_extractor import get_keywords


NLP = spacy.load("en_core_web_lg")
SENTENCE_TOKENIZER = nltk.data.load('tokenizers/punkt/english.pickle')

EMBEDDING_MODEL_NAME = "jjzha/jobbert-base-cased"

EMBEDDING_TOKENIZER = BertTokenizer.from_pretrained(EMBEDDING_MODEL_NAME)
EMBEDDING_MODEL = BertModel.from_pretrained(EMBEDDING_MODEL_NAME)


class JobPosting:
    def __init__(self, posting):
        self.cache = dict()

        self.raw_posting = posting
        self.sentences = self.__get_posting_sentences()
        self.embedding = self.__get_posting_embedding()
        self.keywords = self.__get_posting_keywords()

    def rank_point(self, point):
        string_embedding = self.__embedding(point)

        # return max([
        #     self.__similarity(string_embedding, sentence_embedding) for sentence_embedding in self.embedding
        # ])

        return self.__similarity(string_embedding, self.embedding)
    
    def rank_keywords(self, keywords, required=set()):
        return sorted([(kw, self.__keyword_score(kw, required)) for kw in keywords], key=lambda x: x[1], reverse=True)

    def __get_posting_sentences(self):
        base_sentences = self.raw_posting.split("\n")
        result = []

        for sent in base_sentences:
            sentences = SENTENCE_TOKENIZER.tokenize(sent)
            result += sentences

        with open("artifacts/sentences.txt", "w+") as f:
            f.write("\n\n".join(result))
        return result
    
    def __calc_embedding(self, text):
        inputs = EMBEDDING_TOKENIZER(text, return_tensors='pt', truncation=True, padding=True)
        with torch.no_grad():
            outputs = EMBEDDING_MODEL(**inputs)
        return outputs.last_hidden_state.mean(dim=1)
    
    def __embedding(self, x):
        if self.cache.get(x) is not None:
            return self.cache[x]
        embedding = self.__calc_embedding(x)
        self.cache[x] = embedding
        return embedding

    def __similarity(self, x, y):
        return cosine_similarity(x, y)

    def __keyword_score(self, kw, required):
        if kw in required:
            return float("inf")
        with open("input/skill_descriptions.json", "r") as f:
            skill_descriptions = json.loads(f.read())
            if skill_descriptions.get(kw.lower()):
                desc = f" ({skill_descriptions.get(kw.lower())})"
            else:
                desc = ""
            kw_embedding = self.__embedding(f"{kw.lower()}{desc}")
            return max([self.__similarity(kw_embedding, self.__embedding(k)) for k in self.keywords])

    def __get_posting_embedding(self):
        # return list(map(self.__embedding, self.sentences))
        return self.__embedding(self.raw_posting)

    def __get_posting_keywords(self):
        return self.__get_keywords(self.raw_posting)
    
    def __get_keywords(self, text):
        return get_keywords(text)
    