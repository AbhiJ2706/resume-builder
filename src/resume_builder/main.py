from fastapi import FastAPI, Response
from pydantic import BaseModel

import io

from resume_builder.pipeline import run_pipeline


APP = FastAPI()


class GenerationRequest(BaseModel):
    user_id: str
    link: str
    theme: str
    desc: str


@APP.get("/")
def ping():
    return {"Hello": "World"}


@APP.get("/generate")
def generate(params: GenerationRequest):
    
    file = run_pipeline(params.user_id, params.link, params.theme, params.desc)

    if file:
        with open(file, "rb") as fh:
            f = io.BytesIO(fh.read())
            return Response(f, media_type="application/pdf")
