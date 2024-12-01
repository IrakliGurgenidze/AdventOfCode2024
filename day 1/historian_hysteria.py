import requests
import math
from collections import Counter

# -- FETCH DATA -- #

url = r"https://adventofcode.com/2024/day/1/input"
session_cookie = r"53616c7465645f5f80c8fb65af28afb264ee4334aeb8ed8f369c8f7e13253279284416a4afe3682b4a32b70fa28dfbcca73162e27e6a293e85d6a7cda5776846"

response = requests.get(
    url,
    cookies={"session": session_cookie}
)

if response.status_code != 200:
    raise LookupError(f"Failed to fetch data. HTTP Status Code: {response.status_code}")

content = response.text

# -- SPLIT LISTS -- #

left_values = []
right_values = []

for line in content.strip().split("\n"):
    left, right = map(int, line.split())  # Split and convert to integers
    left_values.append(left)
    right_values.append(right)

# we write quicksort because its fun :)
def quicksort(inlist: list[int]) -> list[int]:
    if inlist == []: 
        return []
    else:
        pivot = inlist[0]
        lesser = quicksort([x for x in inlist[1:] if x < pivot])
        greater = quicksort([x for x in inlist[1:] if x >= pivot])
        return lesser + [pivot] + greater
    
left_values = quicksort(left_values)
right_values = quicksort(right_values)

# -- COMPUTE DIFF -- #

def rowwise_diff(left: list[int], right: list[int]) -> list[int]:
    if len(left) != len(right):
        raise ValueError("Lists have different lengths.")
    return [abs(l - r) for l, r in zip(left, right)]

print(f"Difference between lists: {sum(rowwise_diff(left_values, right_values))}")

# -- COMPUTE SIMILARITY -- #

def fetch_occurrences(input: list[int], target: list[int]) -> list[int]:
    counter = Counter(target)
    return [counter[element] for element in input]

counts = fetch_occurrences(left_values, right_values)

similarity = 0
for i in range(len(left_values)):
    similarity += left_values[i] * counts[i]

print(f"Similarity between lists: {similarity}")






