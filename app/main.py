import os

from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
import openai
from dotenv import load_dotenv

with open("README.md", "r") as file:
    next(file)
    description = file.read()

VERSION = "0.0.4"
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
    """<h3>Version</h3>
    Returns the current version of the API
    <pre><code>
    @return: String </code></pre>"""
    return VERSION


@API.post("/outreach", tags=["Outreach"])
async def outreach(your_name: str = Form(),
                   company: str = Form(),
                   job_title: str = Form(),
                   job_description: str = Form(),
                   key_points_from_resume: str = Form()):
    """<h3>Outreach</h3>
    Returns an AI Generated Cold Outreach Letter
    <pre><code>
    @param your_name: String
    @param company: String
    @param job_title: String
    @param job_description: String
    @param key_points_from_resume: String
    @return: String </code></pre>"""
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
