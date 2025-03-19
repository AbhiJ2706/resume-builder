from fastapi import FastAPI, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel

import io

from resume_builder.pipeline import run_pipeline


APP = FastAPI()


APP.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"], 
    allow_headers=["*"],
)


class GenerationRequest(BaseModel):
    user_id: str
    link: str
    desc: str


@APP.get("/")
def ping():
    return {"Hello": "World"}


@APP.post("/generate")
def generate(params: GenerationRequest):
    
    file = run_pipeline(params.user_id, params.link, params.desc)

    if file:
        with open(file, "rb") as fh:
            return FileResponse(file, media_type="application/pdf", filename=file)
