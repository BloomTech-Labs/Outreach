def dict_to_json_str(data) -> str:
    return f"""{{{', '.join(f'"{k}": "{v}"' for k, v in data.items())}}}""".replace("\n", "<br>")


print(repr(dict_to_json_str({
        "name": "Robert Sharp",
        "company": "Google",
        "job_title": "Data Science Instructor",
        "outreach": "cold_outreach\n\nsome more text...",
        "contacts": "contacts",
    })))
