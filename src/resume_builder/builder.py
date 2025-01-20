import json
import logging

from collections import Counter

from resume_builder.job_posting import JobPosting


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
    sim_points = []

    for i, point in enumerate(resume_points):
        similarity_score = posting.rank_point(point["summary"])

        sim_points.append((similarity_score, point, i))
    
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
