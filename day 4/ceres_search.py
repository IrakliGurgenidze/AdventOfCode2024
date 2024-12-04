import requests
import numpy as np


# -- FETCH DATA -- #
url = r"https://adventofcode.com/2024/day/4/input"
session_cookie = r"53616c7465645f5f80c8fb65af28afb264ee4334aeb8ed8f369c8f7e13253279284416a4afe3682b4a32b70fa28dfbcca73162e27e6a293e85d6a7cda5776846your cookie here"

response = requests.get(url, cookies={"session": session_cookie})

if response.status_code != 200:
    raise LookupError(f"Failed to fetch data. HTTP Status Code: {response.status_code}")

content = response.text


# -- FIND XMAS STRINGS -- #
content_lines = []
for line in content.strip().split("\n"):
    content_lines.append(line)

content_array = np.array(content_lines)


def search_from_index(content_array, row, col) -> int:
    matches = 0
    matching_string = "XMAS"
    string_length = len(matching_string)

    if content_array[row][col] != "X":
        return matches

    rows = len(content_array)
    cols = len(content_array[0])

    # Helper to check bounds and extract string
    def extract_string(start_row, start_col, delta_row, delta_col):
        result = ""
        for i in range(string_length):
            r, c = start_row + i * delta_row, start_col + i * delta_col
            if 0 <= r < rows and 0 <= c < cols:
                result += content_array[r][c]
            else:
                return None
        return result

    # Define directions (row_delta, col_delta)
    directions = [
        (-1, 0),  # Up
        (-1, 1),  # Up-right
        (0, 1),  # Right
        (1, 1),  # Down-right
        (1, 0),  # Down
        (1, -1),  # Down-left
        (0, -1),  # Left
        (-1, -1),  # Up-left
    ]

    # Check all directions
    for delta_row, delta_col in directions:
        extracted = extract_string(row, col, delta_row, delta_col)
        if extracted == matching_string:
            matches += 1

    return matches


matched_strings = 0
for row in range(len(content_array)):
    for col in range(len(content_array[0])):
        if content_array[row][col] == "X":
            matched_strings += search_from_index(content_array, row, col)

print(f"Detected {matched_strings} matching strings.")


# -- FIND X-MAS CLUSTERS -- #
def is_valid_x(content_array, row, col):
    # Assuming pos passed for center of the x
    matches = 0
    matching_string = "MAS"
    string_length = len(matching_string)

    if content_array[row][col] != "A":
        return matches

    rows = len(content_array)
    cols = len(content_array[0])

    def extract_string(start_row, start_col, delta_row, delta_col):
        result = ""
        for i in range(string_length):
            r, c = start_row + i * delta_row, start_col + i * delta_col
            if 0 <= r < rows and 0 <= c < cols:
                result += content_array[r][c]
            else:
                return None
        return result

    directions = [(-1, 1), (1, 1), (1, -1), (-1, -1)]

    for delta_row, delta_col in directions:
        extracted = extract_string(
            row + delta_row, col + delta_col, -delta_row, -delta_col
        )
        if extracted == matching_string:
            matches += 1

    if matches < 2:
        return 0
    else:
        return 1


matched_clusters = 0
for row in range(len(content_array)):
    for col in range(len(content_array[0])):
        if content_array[row][col] == "A":
            matched_clusters += is_valid_x(content_array, row, col)

print(f"Detected {matched_clusters} matching x-mas clusters.")
