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


if os.environ.get("ENVIRONMENT"):
    ENVIRONMENT = "local"
    AWS_ACCESS_KEY_ID = os.environ["AWS_ACCESS_KEY_ID"]
    AWS_SECRET_KEY_ID = os.environ["AWS_SECRET_KEY_ID"]
    REDIRECT_URI = os.environ["REDIRECT_URI"]
    GOOGLE_CLOUD_CREDENTIALS = json.loads(os.environ["GOOGLE_CLOUD_CREDENTIALS"])
    with open("credentials.json", "w+") as f:
        f.write(json.dumps(GOOGLE_CLOUD_CREDENTIALS))
else:
    ENVIRONMENT = "production"

AWS_S3_BUCKET = "user-resume-info-resume-builder-tailor"

if ENVIRONMENT == "local":
    S3_CLIENT = boto3.client(
        's3', 
        aws_access_key_id=AWS_ACCESS_KEY_ID, 
        aws_secret_access_key=AWS_SECRET_KEY_ID
    )
else:
    S3_CLIENT = boto3.client('s3')


DOMAIN_TO_TEMPLATE = {
    "workday": "workday_default"
}


def to_camel_case(snake_str):
    return "".join(x.capitalize() for x in snake_str.lower().split("_"))


def run_pipeline(user_id, link, theme, posting):
    domain = validators.domain(link)

    template = DOMAIN_TO_TEMPLATE.get(domain, theme)

    user_file = f"{user_id}_final.json"

    try:
        response = S3_CLIENT.get_object(
            Bucket=AWS_S3_BUCKET, 
            Key=user_file
        )

        resume_data = json.loads(response["Body"].read().decode())
    except ClientError as e:
        response = None
        resume_data = None
        return ""

    posting = JobPosting(posting)

    build_resume(posting, resume_data)

    builder_class = getattr(import_module("templates." + template), to_camel_case(template))

    builder: LatexTemplate = builder_class("artifacts/resume_result.json", "artifacts/final_doc.tex")
    builder.build_doc()

    proc = subprocess.Popen(['./render.sh'], cwd="artifacts")
    proc.communicate()
    os.rename('artifacts/final_doc.pdf', f"output/{resume_data['info']['firstname']}_{resume_data['info']['lastname']}_resume.pdf")

    return f"output/{resume_data['info']['firstname']}_{resume_data['info']['lastname']}_resume.pdf"
