import os

import requests
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import openai
from dotenv import load_dotenv

from app.database import Database
from app.utilities import format_name_email

with open("README.md", "r") as file:
    next(file)
    description = file.read()

VERSION = "0.0.26"
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
hunter_key = os.getenv("HUNTER_KEY")
API.db = Database("Outreach")


@API.get("/version", tags=["General"])
async def version():
    """<h3>Version</h3>
    Returns the current version of the API
    <pre><code>
    @return: String </code></pre>"""
    return VERSION


@API.get("/outreach", tags=["Outreach"])
async def outreach(your_name: str,
                   your_email: str,
                   company: str,
                   job_title: str,
                   job_description: str,
                   key_points_from_resume: str):
    """<h3>Outreach</h3>
    Returns an AI Generated Cold Outreach Letter
    <pre><code>
    @param your_name: String
    @param your_email: String
    @param company: String
    @param job_title: String
    @param job_description: String
    @param key_points_from_resume: String
    @return: String </code></pre>"""
    context = "You are a master at cold outreach for tech jobs. Respond to the " \
              "following with only the body of the letter and nothing else. " \
              "Do not address the letter. Do not use the phrase Dear Hiring Manager..."
    prompt = f"Write a cold outreach letter to {company} from {your_name} " \
             f"for the {job_title} role. The job description " \
             f"is: {job_description}. Key points from {your_name}'s resume " \
             f"are: {key_points_from_resume}. Dear Hiring Manager,\n\n"
    result, *_ = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": context},
            {"role": "user", "content": prompt},
        ],
    ).choices
    cold_outreach = result.get("message").get("content").replace("\n", "<br />")
    data = requests.get(
        f"https://api.hunter.io/v2/domain-search?company={company}&api_key={hunter_key}"
    ).json()["data"]
    contacts = ", ".join(format_name_email(d) for d in data["emails"][:3])
    API.db.write_one({
        "name": your_name,
        "email": your_email,
        "company": company,
        "job_title": job_title,
        "job_description": job_description,
        "key_points_from_resume": key_points_from_resume,
        "outreach": cold_outreach,
        "contacts": contacts,
    })
    requests.post(
        "https://api.mailgun.net/v3/mail.bloomtech.com/messages",
        auth=("api", os.getenv("MAILGUN_API_KEY")),
        data={
            "from": "Outreach Generator <support@bloomtech.com>",
            "to": f"{your_name} <{your_email}>",
            "subject": f"Custom Outreach for {company}",
            "template": "custom_outreach",
            "h:X-Mailgun-Variables": f'{{"outreach_message": "{cold_outreach}", "contact": "{contacts}", "name": "{your_name}", "company": "{company}", "job_title": "{job_title}"}}',
        }
    )
    return {
        "outreach": cold_outreach,
        "contacts": contacts,
    }
