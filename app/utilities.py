def format_name_email(d: dict) -> str:
    if d["first_name"] and d["last_name"] and d["position"] and d["value"]:
        return f'{d["first_name"]} {d["last_name"]}: {d["position"]}: {d["value"]}'
    elif d["first_name"] and d["last_name"] and d["value"]:
        return f'{d["first_name"]} {d["last_name"]}: {d["value"]}'
    elif d["value"]:
        return d["value"]
    else:
        return ""
