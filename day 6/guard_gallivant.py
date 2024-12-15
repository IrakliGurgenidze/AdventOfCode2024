import requests
import numpy as np
import tqdm


# -- FETCH DATA -- #
url = r"https://adventofcode.com/2024/day/6/input"
session_cookie = r"your cookie here"

response = requests.get(url, cookies={"session": session_cookie})

if response.status_code != 200:
    raise LookupError(f"Failed to fetch data. HTTP Status Code: {response.status_code}")

content = response.text


# -- PARSE MAP -- #
content_lines = []
for line in content.strip().split("\n"):
    content_lines.append(list(line))

og_grid = np.array(content_lines)

# -- SIMULATE GUARD -- #
def simulate_guard_patrol(og_grid, obstruction=None):
    grid = og_grid.copy()  # Create a copy of the grid to simulate changes
    if obstruction:
        grid[obstruction] = "#"  # Place an obstruction if provided

    directions = {'^': (-1, 0), '>': (0, 1), 'v': (1, 0), '<': (0, -1)}
    turn_order = ['^', '>', 'v', '<']  # Define the turn order for 90-degree right turns

    # Find the guard's initial position and direction
    guard_pos = None
    guard_dir = None
    
    for r, row in enumerate(grid):
        for c, char in enumerate(row):
            if char in directions:
                guard_pos = (r, c)
                guard_dir = char
                break
        if guard_pos:
            break

    visited_positions = set()
    visited_states = set()  # For Part Two: Track guard's position and direction
    visited_positions.add(guard_pos)
    
    rows, cols = grid.shape
    
    while True:
        # Save the current state for loop detection
        state = (guard_pos, guard_dir)
        if state in visited_states:
            return visited_positions, True  # Loop detected
        visited_states.add(state)
        
        # Calculate next position
        dr, dc = directions[guard_dir]
        next_pos = (guard_pos[0] + dr, guard_pos[1] + dc)
        
        # Check if the guard is out of bounds
        if not (0 <= next_pos[0] < rows and 0 <= next_pos[1] < cols):
            break
        
        # Check if there's an obstacle
        if grid[next_pos] == '#':
            guard_dir = turn_order[(turn_order.index(guard_dir) + 1) % 4]  # Turn right
        else:
            # Move forward
            guard_pos = next_pos
            visited_positions.add(guard_pos)

    return visited_positions, False  # No loop detected


# Part One: Simulate without obstruction
visited_positions, _ = simulate_guard_patrol(og_grid)
print(f"Distinct positions visited: {len(visited_positions)}")

# -- DETERMINE OBSTRUCTION PATH -- #
def determine_valid_obstructions(og_grid):
    visited_positions, _ = simulate_guard_patrol(og_grid)
    valid_obstacles = []
    
    for visited_row, visited_col in tqdm.tqdm(visited_positions, desc="Searching for obstacles"):
        if og_grid[(visited_row, visited_col)] == ".":
            visited_set, loop = simulate_guard_patrol(og_grid, obstruction=(visited_row, visited_col))
            if loop:
                valid_obstacles.append((visited_row, visited_col))

    return valid_obstacles

print(f"Num valid obstacles: {len(determine_valid_obstructions(og_grid))}")


