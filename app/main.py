from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.background import BackgroundTasks

from app.utilities import custom_outreach

with open("README.md", "r") as file:
    next(file)
    description = file.read()

VERSION = "0.0.33"
API = FastAPI(
    title='Outreach API',
    description=description,
    version=VERSION,
    docs_url='/',
)
API.add_middleware(
    CORSMiddleware,
    allow_origins=['https://custom-outreach-generator.vercel.app'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


@API.get("/version", tags=["General"])
async def version():
    """<h3>Version</h3>
    Returns the current version of the API
    <pre><code>
    @return: String </code></pre>"""
    return VERSION


@API.get("/outreach", tags=["Outreach"])
async def outreach(queue: BackgroundTasks,
                   your_name: str,
                   your_email: str,
                   company: str,
                   job_title: str,
                   job_description: str,
                   key_points_from_resume: str):
    """<h3>Outreach</h3>
    Sends an AI Generated Cold Outreach Email
    <pre><code>
    @param queue: Automatic FastAPI BackgroundTasks.
    @param your_name: String.
    @param your_email: String.
    @param company: String.
    @param job_title: String.
    @param job_description: String.
    @param key_points_from_resume: String.
    @return: String.</code></pre>"""
    queue.add_task(custom_outreach,
                   your_name,
                   your_email,
                   company,
                   job_title,
                   job_description,
                   key_points_from_resume)
    return {"status": 200, "message": "job started"}
