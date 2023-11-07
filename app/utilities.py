from datetime import datetime
import os
from time import sleep

import openai
import requests
from dotenv import load_dotenv

from app.database import Database


load_dotenv()
openai.api_key = os.getenv("OPENAI_KEY")
hunter_key = os.getenv("HUNTER_KEY")
db = Database("Outreach")


def format_name_email(d: dict) -> str:
    if d["first_name"] and d["last_name"] and d["position"] and d["value"]:
        return f'{d["first_name"]} {d["last_name"]}: {d["position"]}: {d["value"]}'
    elif d["first_name"] and d["last_name"] and d["value"]:
        return f'{d["first_name"]} {d["last_name"]}: {d["value"]}'
    elif d["value"]:
        return d["value"]
    else:
        return ""


def dict_to_str(data) -> str:
    return f"""{{{', '.join(f'"{k}": "{v}"' for k, v in data.items())}}}"""


def try_retry_openai(context, prompt, start):

    def worker():
        return openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": context},
                {"role": "user", "content": prompt},
                {"role": "assistant", "content": start},
            ],
        )

    result = worker()
    while not result:
        sleep(5)
        result = worker()
    return result


def custom_outreach(your_name: str,
                    your_email: str,
                    company: str,
                    job_title: str,
                    job_description: str,
                    key_points_from_resume: str):
    context = "You are a master at cold outreach for tech jobs."
    prompt = f"Write a cold outreach letter to {company} from {your_name} " \
             f"for the {job_title} role. The job description " \
             f"is: {job_description}. Key points from {your_name}'s resume " \
             f"are: {key_points_from_resume}."
    start = "Dear Hiring Manager,\n\n"
    result, *_ = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": context},
            {"role": "user", "content": prompt},
            {"role": "assistant", "content": start},
        ],
    ).choices
    cold_outreach = result.get("message").get("content").replace("\n", "<br>")
    data = requests.get(
        f"https://api.hunter.io/v2/domain-search?company={company}&api_key={hunter_key}"
    ).json()["data"]
    contacts = "<br>".join(format_name_email(d) for d in data["emails"][:3])
    timestamp = datetime.today().isoformat()
    db.write_one({
        "name": your_name,
        "email": your_email,
        "company": company,
        "job_title": job_title,
        "job_description": job_description,
        "key_points_from_resume": key_points_from_resume,
        "outreach": cold_outreach,
        "contacts": contacts,
        "timestamp": timestamp,
    })
    variables = dict_to_str({
        "outreach_message": cold_outreach,
        "contact": contacts,
        "name": your_name,
        "company": company,
        "job_title": job_title,
    })
    requests.post(
        "https://api.mailgun.net/v3/mail.bloomtech.com/messages",
        auth=("api", os.getenv("MAILGUN_API_KEY")),
        data={
            "from": "Outreach Generator <support@bloomtech.com>",
            "to": f"{your_name} <{your_email}>",
            "subject": f"Custom Outreach for {company}",
            "template": "custom_outreach",
            "h:X-Mailgun-Variables": variables,
        }
    )
