import nltk.data
import spacy
import torch

from keybert import KeyBERT
from torch.nn.functional import cosine_similarity
from transformers import BertTokenizer, BertModel, AutoTokenizer, AutoModelForTokenClassification

import json
import logging

from collections import Counter


NLP = spacy.load("en_core_web_lg")
SENTENCE_TOKENIZER = nltk.data.load('tokenizers/punkt/english.pickle')

TRANSFORMER_MODEL = "jjzha/jobbert_knowledge_extraction"
EMBEDDING_MODEL_NAME = "jjzha/jobbert-base-cased"

TRANSFORMER_TOKENIZER = AutoTokenizer.from_pretrained(TRANSFORMER_MODEL)
TRANSFORMER_LLM = AutoModelForTokenClassification.from_pretrained(TRANSFORMER_MODEL)
EMBEDDING_TOKENIZER = BertTokenizer.from_pretrained(EMBEDDING_MODEL_NAME)
EMBEDDING_MODEL = BertModel.from_pretrained(EMBEDDING_MODEL_NAME)


class KeywordExtractor:
    def __get_relevant_tokens(self, tokens, logits):
        zipped = [(x, y) for x, y in zip(logits, tokens)]

        results = []
        adding = False
        current = []

        for (label, token) in zipped:
            if label == 2:
                if not adding:
                    continue
                else:
                    results.append(current)
                    current = []
                    adding = False
            else:
                if label == 1:
                    current.append(token)
                elif label == 0:
                    if not adding:
                        adding = True
                        current.append(token)
                    else:
                        if token != 1116:
                            results.append(current)
                            current = []
                        current.append(token)
        
        return results
    
    def __reconstruct_keywords(self, tokens):
        decoded = [TRANSFORMER_TOKENIZER.decode(result) for result in tokens]

        true_results = []
        in_list = False

        for token in decoded:
            if in_list:
                if token.startswith("##") and len(token) >= 3 and len(true_results):
                    true_results[-1] += token[2:]
                else:
                    true_results[-1] += token
                if token.endswith(")"):
                    in_list = False
                continue
            if token.startswith("##") and len(token) >= 3 and len(true_results):
                true_results[-1] += token[2:]
            elif token.startswith("+"):
                true_results[-1] += token
            elif len(true_results) and true_results[-1].endswith("("):
                in_list = True
                true_results[-1] += token
            else:
                true_results.append(token)
        
        return true_results


    def get_keywords(self, text, lowercase=True):
        inputs = TRANSFORMER_TOKENIZER.encode(text, return_tensors="pt")
        outputs = TRANSFORMER_LLM(inputs)
        
        relevant_tokens = self.__get_relevant_tokens(inputs[0], outputs.logits.argmax(-1)[0])
        reconstructed_tokens = self.__reconstruct_keywords(relevant_tokens)
        
        keywords = set(list(filter(lambda x: len(x) > 1 or x.lower() == "c", reconstructed_tokens)))
        if lowercase:
            keywords = set(list(map(lambda x: x.lower(), keywords)))
        
        if not keywords:
            kw_model = KeyBERT()
            keywords = list(map(lambda x: x[0].lower(), kw_model.extract_keywords(text, top_n=20, keyphrase_ngram_range=(1, 2))))

        with open("artifacts/topics.txt", "w+") as f:
            f.write("\n".join(keywords))
        return keywords


class JobPosting:
    def __init__(self, posting):
        self.cache = dict()

        self.raw_posting = posting
        self.sentences = self.__get_posting_sentences()
        self.embedding = self.__get_posting_embedding()
        self.keywords = self.__get_posting_keywords()

    def rank_point(self, point):
        string_embedding = self.__embedding(point)

        return max([
            self.__similarity(string_embedding, sentence_embedding) for sentence_embedding in self.embedding
        ])
    
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
        return list(map(self.__embedding, self.sentences))

    def __get_posting_keywords(self):
        return self.__get_keywords(self.raw_posting)
    
    def __get_keywords(self, text):
        return KeywordExtractor().get_keywords(text)


def rank_whole_point(posting, section):
    section_string = "\n".join(
        [f"{section['organization']} ({section['location']}) [{', '.join(section['technologies'])}]"] +
        list(map(
            lambda x: f"{x['summary']} ({', '.join(x['required_skills'])})", 
            section["description"]
        ))
    )
    
    string_similarity_score = posting.rank_point(section_string)

    logger.error(section_string)
    logger.error(string_similarity_score)

    return string_similarity_score


def top_k_points(posting, resume_points, k=3):
    # logger.error("")

    sim_points = []

    for i, point in enumerate(resume_points):
        similarity_score = posting.rank_point(point["summary"])

        sim_points.append((similarity_score, point, i))

        # logger.error(point)
        # logger.error(similarity_score)
    
    result = list(map(
        lambda x: x[1], 
        sorted(
            sorted(
                sim_points, 
                key=lambda x: x[0], 
                reverse=True
            )[:k], 
            key=lambda x: x[2]
        )
    ))
    
    return result


def get_skills(posting: JobPosting, languages, frameworks, n=5, required=set()):
    sorted_languages = posting.rank_keywords(languages, required=required)
    sorted_frameworks = posting.rank_keywords(frameworks, required=required)

    used_payload = dict(
        languages=Counter(),
        frameworks=Counter()
    )

    def used(x):
        nonlocal used_payload
        key = -1 if x[0] in languages else 1
        if key == -1: 
            used_payload["languages"].update([x[0]])
        else:
            used_payload["frameworks"].update([x[0]])
        return key
    
    sorted_overall = sorted(sorted_languages + sorted_frameworks, key=lambda x: x[1], reverse=True)

    num_languages_in_top_n = len(list(filter(lambda x: x in sorted_languages, sorted_overall[:n])))
    if num_languages_in_top_n > 3:
        sorted_overall = sorted_languages[:3] + sorted_frameworks[:(n-3)]

    sorted_overall = sorted(
        sorted_overall[:n],
        key=lambda x: used(x)
    )

    return list(map(lambda x: x[0], sorted_overall)), used_payload


def read_resume():
    with open("input/resume.json", "r+") as f:
        return json.loads(f.read())

def read_posting():
    with open("input/posting.txt", "r+") as f:
        return f.read()


def get_points(posting, resume):
    languages = Counter()
    frameworks = Counter()
    for job in resume["experience"]:
        job["description"] = top_k_points(posting, job["description"])
        required_skills = set(sum(map(lambda x: x["required_skills"], job["description"]), start=[]))
        job["description"] = list(map(lambda x: x["summary"], job["description"]))
        job["technologies"], used_payload = get_skills(posting, job["languages"], job["frameworks"], required=required_skills)
        del job["languages"]
        del job["frameworks"]

        languages.update(used_payload["languages"])
        frameworks.update(used_payload["frameworks"])
    
    resume["languages"] = list(map(lambda x: x[0], languages.most_common()))
    resume["frameworks"] = list(map(lambda x: x[0], frameworks.most_common()))
    
    extracurriculars_ranking = []
    
    for i, club in enumerate(resume["extracurriculars"]):
        extracurriculars_ranking.append((
            list(map(lambda x: x["summary"], top_k_points(posting, club["description"], k=2))), 
            rank_whole_point(posting, club), 
            club, i
        ))

    result = list(map(
        lambda x: (x[0], x[2]), 
        sorted(
            sorted(extracurriculars_ranking, 
                   key=lambda x: x[1], 
                   reverse=True)[:2], 
            key=lambda x: x[3]
        )
    ))

    resume["extracurriculars"] = []

    for (res_points, res) in result:
        res["description"] = res_points
        resume["extracurriculars"].append(res)
    
    with open("artifacts/resume_result.json", "w+") as f:
        f.write(json.dumps(resume, indent=4))


if __name__ == "__main__":
    logger = logging.getLogger()
    logging.basicConfig(filename='artifacts/log.log', level=logging.ERROR)

    posting = JobPosting(read_posting())
    get_points(posting, read_resume())
