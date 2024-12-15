import requests
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt


# -- FETCH DATA -- #
url = r"https://adventofcode.com/2024/day/5/input"
session_cookie = r"your cookie here"

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

def create_dependency_graph(before_lookup: dict):
    G = nx.DiGraph()
    
    for key, values in before_lookup.items():
        for value in values: 
            G.add_edge(key, value)

    return G

def reorder_update(before_lookup, update):
    pages = list(map(int, update.split(",")))

    G = nx.DiGraph()
    for page in pages:
        if page in before_lookup:
            for dependent in before_lookup[page]:
                if dependent in pages:
                    G.add_edge(page, dependent)

    sorted_pages = list(nx.topological_sort(G))
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