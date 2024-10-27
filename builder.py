from collections import Counter
import json
import re
from sentence_transformers import SentenceTransformer
import logging
import spacy
import string
import yake
import nltk.data


NLP = spacy.load("en_core_web_sm")
SENTENCE_TOKENIZER = nltk.data.load('tokenizers/punkt/english.pickle')


class JobPosting:
    def __init__(self, posting):
        self.embedder = SentenceTransformer("multi-qa-mpnet-base-cos-v1")
        self.cache = dict()

        self.raw_posting = posting
        self.sentences = self.__get_sentences()
        self.embedding = self.__get_embedding()
        self.keywords = self.__get_keywords()

    def rank_point(self, point):
        string_embedding = self.__embedding(point)

        return max([
            self.__similarity(string_embedding, sentence_embedding) for sentence_embedding in self.embedding
        ])
    
    def rank_keywords(self, keywords, required=set()):
        return sorted([(kw, self.__keyword_score(kw, required)) for kw in keywords], key=lambda x: x[1], reverse=True)

    def __get_sentences(self):
        sentences = SENTENCE_TOKENIZER.tokenize(self.raw_posting)
        result = []
        for sent in sentences:
            nl_split = sent.split("\n")
            if type(nl_split) == str:
                result += [sent]
            else:
                result += nl_split
        with open("sentences.txt", "w+") as f:
            f.write("\n\n".join(result))
        return result
    
    def __embedding(self, x):
        if self.cache.get(x) is not None:
            return self.cache[x]
        embedding = self.embedder.encode(x, convert_to_tensor=True)
        self.cache[x] = embedding
        return embedding

    def __similarity(self, x, y):
        return self.embedder.similarity(x, y)[0].cpu().numpy()[0]

    def __keyword_score(self, kw, required):
        if kw in required:
            return float("inf")
        kw_embedding = self.__embedding(kw.lower())
        return max([self.__similarity(kw_embedding, self.__embedding(k)) for k in self.keywords])

    def __get_embedding(self):
        return list(map(self.__embedding, self.sentences))

    def __get_keywords(self):
        topics = set()

        doc = NLP(string.capwords(self.raw_posting))
        for token in doc:
            if token.pos_ == 'PROPN':
                topics.add(str(token).lower())
        
        extractor = yake.KeywordExtractor(lan="en", n=2, dedupLim=0.5, top=20, features=None)

        keywords = extractor.extract_keywords(self.raw_posting)

        for kw in keywords:
            topics.add(kw[0].lower())
        
        with open("sentences.txt", "a+") as f:
            f.write(", ".join(topics))
        
        return list(topics)


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
    logger.error("")

    sim_points = []

    for i, point in enumerate(resume_points):
        similarity_score = posting.rank_point(point["summary"])

        sim_points.append((similarity_score, point, i))

        logger.error(point)
        logger.error(similarity_score)
    
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


def get_skills(posting, languages, frameworks, n=5, required=set()):
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
    with open("resume.json", "r+") as f:
        return json.loads(f.read())

def read_posting():
    with open("posting.txt", "r+") as f:
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
    
    with open("resume_result.json", "w+") as f:
        f.write(json.dumps(resume, indent=4))


if __name__ == "__main__":
    logger = logging.getLogger()
    logging.basicConfig(filename='log2.log', level=logging.ERROR)

    posting = JobPosting(read_posting())
    get_points(posting, read_resume())
