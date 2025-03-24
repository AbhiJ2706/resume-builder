from datetime import datetime
from urllib.parse import urlparse
from botocore.exceptions import ClientError
from dotenv import load_dotenv
from validator_collection import validators

import boto3

from importlib import import_module

import json
import os
import subprocess

from resume_builder.data_builder import build_resume
from resume_builder.job_posting import JobPosting
from resume_builder.templates.template import LatexTemplate


load_dotenv()


def domain_to_template(domain, default):
    if "workday" in domain:
        return "workday_default"
    return default


def to_camel_case(snake_str):
    return "".join(x.capitalize() for x in snake_str.lower().split("_"))


def date_to_string(date: datetime.date):
    return [
        "January",
        "February",
        "March",
        "April",
        "May",
        "June",
        "July",
        "August",
        "September",
        "October",
        "November",
        "December"
    ][date.month - 1] + f" {str(date.year)}"


def to_valid_format(data):
    def sort_section(sect):
        for i in range(len(data[sect])):
            data[sect][i]["start"] = datetime.strptime(data[sect][i]["start"], "%Y-%m-%dT%H:%M:%S.%fZ").date()
            data[sect][i]["end"] = datetime.strptime(data[sect][i]["end"], "%Y-%m-%dT%H:%M:%S.%fZ").date()
        data[sect] = sorted(data[sect], key=lambda x: x["end"], reverse=True)
        for i in range(len(data[sect])):
            data[sect][i]["start"] = date_to_string(data[sect][i]["start"])
            data[sect][i]["end"] = date_to_string(data[sect][i]["end"])
        
    sort_section("education")
    sort_section("extracurriculars")
    sort_section("experience")
    sort_section("projects")
    sort_section("research")

    data["info"] = data["user_resume_information"]
    data["info"]["education"] = data["education"]
    new_sections = []
    for k, v in data["sections"].items():
        data["sections"][k]["items"] = data[data["sections"][k]["name"]]
        new_sections.append(data["sections"][k])
    data["sections"] = new_sections
    
    return data


def run_pipeline(user_id, link, posting):
    print(user_id)
    print(link)
    print(posting)

    domain = urlparse(link).netloc

    print(domain)

    with open("../resume-builder-frontend/tailor-frontend/src/1_intermediate.json") as f:
        resume_data = to_valid_format(json.loads(f.read()))
    
    with open("artifacts/1_intermediate.json", "w+") as f:
        f.write(json.dumps(resume_data, indent=4))
    
    template = domain_to_template(domain, resume_data['info']['default_template'])

    posting = JobPosting(posting)

    build_resume(posting, resume_data)

    builder_class = getattr(import_module("resume_builder.templates." + template), to_camel_case(template))

    builder: LatexTemplate = builder_class("artifacts/resume_result.json", "artifacts/final_doc.tex")
    builder.build_doc()

    proc = subprocess.Popen(['./render.sh'], cwd="artifacts")
    proc.communicate()
    os.rename('artifacts/final_doc.pdf', f"output/{resume_data['info']['firstname']}_{resume_data['info']['lastname']}_resume.pdf")

    return f"output/{resume_data['info']['firstname']}_{resume_data['info']['lastname']}_resume.pdf"
