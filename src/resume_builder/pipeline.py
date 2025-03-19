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


def run_pipeline(user_id, link, posting):
    print(user_id)
    print(link)
    print(posting)

    domain = urlparse(link).netloc

    print(domain)

    with open("../resume-builder-frontend/1_final.json") as f:
        resume_data = json.loads(f.read())
    
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
