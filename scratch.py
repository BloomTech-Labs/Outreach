def dict_to_str(data) -> str:
    return f"""{{{', '.join(f'"{k}": "{v}"' for k, v in data.items())}}}"""


print(repr(dict_to_str({
        "name": "Robert Sharp",
        "company": "Google",
        "job_title": "Data Science Instructor",
        "outreach": "cold_outreach\n\nsome more text...",
        "contacts": "contacts",
    })))


# d = dict_to_str({
#     "outreach_message": cold_outreach,
#     "contact": contacts,
#     "name": your_name,
#     "company": company,
#     "job_title": job_title,
# })

"""
"h:X-Mailgun-Variables": f'{{"outreach_message": "{cold_outreach}", "contact": "{contacts}", "name": "{your_name}", "company": "{company}", "job_title": "{job_title}"}}',
"""
