import copy
import json
import logging

from collections import Counter

from resume_builder.backend.job_posting import JobPosting


def rank_whole_point(posting: JobPosting, section):
    section_string = "\n".join(
        [f"{section['organization']} ({section['location']}) [{', '.join(section['core_skills'] + section['extra_skills'])}]"] +
        list(map(
            lambda x: f"{x['summary']} ({', '.join(x['required_skills'])})", 
            section["description"]
        ))
    )
    
    return posting.rank_point(section_string)


def top_k_points(posting: JobPosting, resume_points, k=3):
    sim_points = []

    for point in resume_points:
        similarity_score = posting.rank_point(point["summary"])
        sim_points.append((similarity_score, point))
    
    return list(map(
        lambda x: x[1],
        sorted(
            sim_points, 
            key=lambda x: x[0], 
            reverse=True
        )[:k]
    ))


def get_skills(posting: JobPosting, core_skills, extra_skills, n=5, required=set()):
    sorted_core = posting.rank_keywords(core_skills, required=required)
    sorted_extra = posting.rank_keywords(extra_skills, required=required)

    used_payload = dict(
        core_skills=Counter(),
        extra_skills=Counter()
    )

    def used(x):
        nonlocal used_payload
        key = -1 if x[0] in core_skills else 1
        if key == -1: 
            used_payload["core_skills"].update([x[0]])
        else:
            used_payload["extra_skills"].update([x[0]])
        return key
    
    sorted_overall = sorted(sorted_core + sorted_extra, key=lambda x: x[1], reverse=True)

    num_languages_in_top_n = len(list(filter(lambda x: x in sorted_core, sorted_overall[:n])))
    if num_languages_in_top_n > 3:
        sorted_overall = sorted_core[:3] + sorted_extra[:(n-3)]

    sorted_overall = sorted(
        sorted_overall[:n],
        key=lambda x: used(x)
    )

    return list(map(lambda x: x[0], sorted_overall)), used_payload
    

def build_section(posting, items, include=None, k=3):
    section_ranking = []
    
    for i, item in enumerate(items):
        section_ranking.append((
            list(map(lambda x: x["summary"], top_k_points(posting, item["description"], k))), 
            rank_whole_point(posting, item), 
            item, i
        ))
        required_skills = set(sum(map(lambda x: x["required_skills"], item["description"]), start=[]))
        item["skills"], item["used_payload"] = get_skills(posting, item["core_skills"], item["extra_skills"], required=required_skills)
        
    if include is not None:
        result = list(map(
            lambda x: (x[0], x[2]), 
            sorted(
                sorted(section_ranking, 
                    key=lambda x: x[1], 
                    reverse=True)[:include], 
                key=lambda x: x[3]
            )
        ))
    else:
        result = list(map(lambda x: (x[0], x[2]), section_ranking))
    
    core_skills = Counter()
    extra_skills = Counter()
    for item in result:
        core_skills.update(item[1]["used_payload"]["core_skills"])
        extra_skills.update(item[1]["used_payload"]["extra_skills"])
        del item[1]["used_payload"], item[1]["core_skills"], item[1]["extra_skills"]

    for (res_points, res) in result:
        res["description"] = res_points

    return list(map(lambda x: x[1], result)), core_skills, extra_skills
    

def build_resume(posting, resume):
    core_skills = Counter()
    extra_skills = Counter()

    new_resume = dict(info=copy.deepcopy(resume["info"]))
    new_resume["sections"] = []

    for section in resume["sections"]:
        new_section, temp_core_skills, temp_extra_skills = \
            build_section(posting, section["items"], include=section["include"], k=section["num_top_points"])
        new_resume["sections"].append({
            "name": section["name"],
            "items": new_section
        })
    
        core_skills.update(temp_core_skills)
        extra_skills.update(temp_extra_skills)

    new_resume["core_skills"] = list(map(lambda x: x[0], core_skills.most_common()))
    new_resume["extra_skills"] = list(map(lambda x: x[0], extra_skills.most_common()))
    
    with open("artifacts/resume_result.json", "w+") as f:
        f.write(json.dumps(new_resume, indent=4))


def read_resume():
    with open("input/resume.json", "r+") as f:
        return json.loads(f.read())


def read_posting():
    with open("input/posting.txt", "r+") as f:
        return f.read()


if __name__ == "__main__":
    logger = logging.getLogger()
    logging.basicConfig(filename='artifacts/log.log', level=logging.ERROR)

    posting = JobPosting(read_posting())
    build_resume(posting, read_resume())
