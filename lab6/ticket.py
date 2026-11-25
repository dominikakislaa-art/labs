FACULTIES = {"ИТ": "09", "ЭК": "38", "ЮР": "40", "МЕД": "31"}
CODES = {code: name for name, code in FACULTIES.items()}


def check_digit(body):
    digits = [int(ch) for ch in body if ch.isdigit()]
    return sum(d * (2 if i % 2 == 0 else 1) for i, d in enumerate(digits)) % 10


def make_number(year, faculty, seq):
    if not 2000 <= year <= 2099 or faculty not in FACULTIES or not 1 <= seq <= 9999:
        raise ValueError("bad year, faculty or seq")
    body = "%02d-%s-%04d" % (year % 100, FACULTIES[faculty], seq)
    return "%s-%d" % (body, check_digit(body))


def parse_number(number):
    parts = number.split("-")
    if [len(p) for p in parts] != [2, 2, 4, 1] or not all(p.isdigit() for p in parts):
        raise ValueError("bad format")
    yy, code, seq, check = parts
    if code not in CODES or not 1 <= int(seq) <= 9999:
        raise ValueError("bad faculty or seq")
    return {
        "year": 2000 + int(yy),
        "faculty": CODES[code],
        "seq": int(seq),
        "check": int(check),
    }


def is_valid_number(number):
    try:
        data = parse_number(number)
    except ValueError:
        return False
    body = "%02d-%s-%04d" % (data["year"] % 100, FACULTIES[data["faculty"]], data["seq"])
    return data["check"] == check_digit(body)


def next_number(number):
    data = parse_number(number)
    if data["seq"] == 9999:
        raise ValueError("sequence exhausted")
    return make_number(data["year"], data["faculty"], data["seq"] + 1)
