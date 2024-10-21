import json
import re
from sentence_transformers import SentenceTransformer
import logging

def top_k_points(posting, resume_points, single=False, section=None, k=3):
    embedder = SentenceTransformer("multi-qa-mpnet-base-cos-v1")

    posting_embedding = embedder.encode(posting.split("\n"), convert_to_tensor=True)

    logger.error("")

    if single:
        section_string = "\n".join(
            [f"{section['organization']} ({section['location']}) [{', '.join(section['technologies'])}]"] +
            section["description"]
        )
        string_embedding = embedder.encode(section_string, convert_to_tensor=True)

        string_similarity_score = max([
            embedder.similarity(string_embedding, sentence_embedding)[0].cpu().numpy()[0] for sentence_embedding in posting_embedding
        ])

        logger.error(section_string)
        logger.error(string_similarity_score)

    sim_points = []

    logger.error("")

    for i, point in enumerate(resume_points):
        point_embedding = embedder.encode(point, convert_to_tensor=True)

        similarity_score = max([
            embedder.similarity(point_embedding, sentence_embedding)[0].cpu().numpy()[0] for sentence_embedding in posting_embedding
        ])

        sim_points.append((similarity_score, point, i))

        logger.error(point)
        logger.error(similarity_score)
    
    result = list(map(lambda x: x[1], sorted(sorted(sim_points, key=lambda x: x[0], reverse=True)[:k], key=lambda x: x[2])))
    
    if single:
        return result, string_similarity_score, section
    
    return result


def read_resume():
    with open("resume.json", "r+") as f:
        return json.loads(f.read())

def read_posting():
    with open("posting.txt", "r+") as f:
        return f.read()


def get_points(posting, resume):
    for job in resume["experience"]:
        job["description"] = top_k_points(posting, job["description"])
    
    sim_points = []
    
    for i, club in enumerate(resume["extracurriculars"]):
        sim_points.append((*top_k_points(
            posting,
            club["description"],
            single=True,
            section=club,
            k=2
        ), i))

    result = list(map(lambda x: (x[0], x[2]), sorted(sorted(sim_points, key=lambda x: x[1], reverse=True)[:2], key=lambda x: x[3])))

    resume["extracurriculars"] = []

    for (res_points, res) in result:
        res["description"] = res_points
        resume["extracurriculars"].append(res)
    
    with open("resume_result.json", "w+") as f:
        f.write(json.dumps(resume, indent=4))


if __name__ == "__main__":
    logger = logging.getLogger()
    logging.basicConfig(filename='log2.log', level=logging.ERROR)

    get_points(read_posting(), read_resume())
