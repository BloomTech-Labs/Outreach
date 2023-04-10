import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import openai
from dotenv import load_dotenv

with open("README.md", "r") as file:
    next(file)
    description = file.read()

VERSION = "0.0.1"
API = FastAPI(
    title='Outreach API',
    description=description,
    version=VERSION,
    docs_url='/',
)
API.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)
load_dotenv()
openai.api_key = os.getenv("OPENAI_KEY")


@API.get("/version", tags=["General"])
async def version():
    """<h3>Returns API Version</h3>"""
    return VERSION


@API.post("/outreach", tags=["Outreach"])
async def outreach(your_name,
                   company,
                   job_title,
                   job_description,
                   key_points_from_resume):
    context = "You are a master at cold outreach for tech jobs."
    prompt = f"Write a cold outreach letter to {company} from {your_name} " \
             f"for the {job_title} role. The job description " \
             f"is: {job_description}. Key points from {your_name}'s resume " \
             f"are: {key_points_from_resume}."
    result, *_ = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": context},
            {"role": "user", "content": prompt},
        ],
    ).choices
    return result.get("message").get("content")
