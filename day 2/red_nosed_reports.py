import requests
import math
from collections import Counter

# -- FETCH DATA -- #
url = r"https://adventofcode.com/2024/day/2/input"
session_cookie = r"your cookie here"

response = requests.get(url, cookies={"session": session_cookie})

if response.status_code != 200:
    raise LookupError(f"Failed to fetch data. HTTP Status Code: {response.status_code}")

content = response.text


# -- ANALYZE REPORTS -- #
def is_monotonic_and_safe(report):
    if len(report) <= 1:
        return True

    safe_intervals = [1, 2, 3]
    for i in range(len(report) - 1):
        diff = abs(report[i] - report[i + 1])
        if diff not in safe_intervals:
            return False

    is_increasing = all(report[i] <= report[i + 1] for i in range(len(report) - 1))
    is_decreasing = all(report[i] >= report[i + 1] for i in range(len(report) - 1))

    return is_increasing or is_decreasing


num_safe_reports = 0
for line in content.strip().split("\n"):
    report = list(map(int, line.split()))  # Split and convert to integers
    if is_monotonic_and_safe(report):
        num_safe_reports += 1

print(f"Num safe reports: {num_safe_reports}")


# -- ANALYZE WITH DAMPER -- #
def is_monotonic_and_safe_with_damper(report):
    if is_monotonic_and_safe(report):
        return True

    for i in range(len(report)):
        modified_report = report[:i] + report[i + 1 :]
        if is_monotonic_and_safe(modified_report):
            return True

    return False


num_safe_reports = 0
for line in content.strip().split("\n"):
    report = list(map(int, line.split()))  # Split and convert to integers
    if is_monotonic_and_safe_with_damper(report):
        num_safe_reports += 1

print(f"Num safe reports with damper: {num_safe_reports}")
