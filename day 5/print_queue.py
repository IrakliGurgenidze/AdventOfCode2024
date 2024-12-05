import requests
import numpy as np


# -- FETCH DATA -- #
url = r"https://adventofcode.com/2024/day/5/input"
session_cookie = r"53616c7465645f5f80c8fb65af28afb264ee4334aeb8ed8f369c8f7e13253279284416a4afe3682b4a32b70fa28dfbcca73162e27e6a293e85d6a7cda5776846"

response = requests.get(url, cookies={"session": session_cookie})

if response.status_code != 200:
    raise LookupError(f"Failed to fetch data. HTTP Status Code: {response.status_code}")

content = response.text


# -- PARSE INSTRUCTIONS FROM PAGES -- #
instructions = []
updates = []
for line in content.strip().split("\n"):
    if "|" in line:
        instructions.append(line)
    elif line != "":
        updates.append(line)

before_lookup = {}
for instruction in instructions:
    before, after = instruction.split("|")
    before, after = int(before), int(after)
    before_lookup.setdefault(before, []).append(after)

# -- VALIDATE UPDATES -- #
def is_valid_update(before_lookup, update):
    pages = list(map(int, update.split(",")))
    for page_idx, page_val in enumerate(pages):
        required_after = before_lookup.get(page_val, [])
        if any(req in pages[:page_idx] for req in required_after):
            return False
    return True

# -- FIND MIDDLE PAGES OF VALID UPDATES -- #
middle_sum = 0
for update in updates:
    if is_valid_update(before_lookup, update):
        pages = list(map(int, update.split(",")))
        middle_page = pages[len(pages) // 2]
        middle_sum += middle_page

print(f"Sum of middle pages: {middle_sum}")


# -- RE-ORDER BAD UPDATES -- #
def reorder_update(before_lookup, update):
    pages = list(map(int, update.split(",")))
    dependency_graph = {page: set(before_lookup.get(page, [])) for page in pages}
    
    sorted_pages = []
    while dependency_graph:
        no_dependencies = [page for page, deps in dependency_graph.items() if not deps]
        
        if not no_dependencies:
            raise ValueError("Cycle detected in dependencies, unable to reorder.")
        
        sorted_pages.extend(no_dependencies)
        for page in no_dependencies:
            del dependency_graph[page]
        for deps in dependency_graph.values():
            deps.difference_update(no_dependencies)
    
    return sorted_pages

# -- PROCESS UPDATES -- #
incorrect_updates = []
middle_sum = 0

for update in updates:
    if not is_valid_update(before_lookup, update):
        reordered = reorder_update(before_lookup, update)
        incorrect_updates.append(reordered)
        
        middle_page = reordered[len(reordered) // 2]
        middle_sum += middle_page

print(f"Sum of middle pages of corrected updates: {middle_sum}")