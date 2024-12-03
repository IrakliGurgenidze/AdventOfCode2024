import requests
import re


# -- FETCH DATA -- #
url = r"https://adventofcode.com/2024/day/3/input"
session_cookie = r"your cookie here"

response = requests.get(url, cookies={"session": session_cookie})

if response.status_code != 200:
    raise LookupError(f"Failed to fetch data. HTTP Status Code: {response.status_code}")

content = response.text


# -- PARSE CASE 1 -- #
mul_pattern = r"mul\(\d{1,3},\d{1,3}\)"
matches = re.findall(mul_pattern, content)

def evaluate_mul(mul: str) -> int:
    int_pattern = r"\d{1,3}"
    operands = re.findall(int_pattern, mul)

    return int(operands[0]) * int(operands[1])


sum = 0
for mul in matches:
    sum += evaluate_mul(mul)

print(f"Sum of uncorrupted operations: {sum}")


# -- PARSE CASE 2 -- #
do_pattern = r"do\(\)"
dont_pattern = r"don\'t\(\)"
matches = re.findall(do_pattern + "|" + dont_pattern + "|" + mul_pattern, content)

def evaluate_conditional_muls(matches: list[str]):
    sum = 0
    do = True
    for match in matches:
        if match == "do()":
            do = True
        elif match == "don't()":
            do = False
        elif do:
            sum += evaluate_mul(match)

    return sum


print(f"Sum of conditional opeations: {evaluate_conditional_muls(matches)}")
