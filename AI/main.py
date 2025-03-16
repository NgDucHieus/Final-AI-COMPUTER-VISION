import itertools
from collections import deque

# Define the 8-Puzzle
GOAL_STATE = (1, 2, 3, 4, 5, 6, 7, 8, 0)

# Define possible moves
MOVES = {
    'up': -3,
    'down': 3,
    'left': -1,
    'right': 1
}

# Function to get the possible actions from a state
def get_possible_actions(state):
    actions = []
    blank = state.index(0)
    row, col = divmod(blank, 3)
    if row > 0:
        actions.append('up')
    if row < 2:
        actions.append('down')
    if col > 0:
        actions.append('left')
    if col < 2:
        actions.append('right')
    return actions

# Function to perform an action and return the new state
def perform_action(state, action):
    blank = state.index(0)
    move = MOVES[action]
    new_blank = blank + move
    state = list(state)
    state[blank], state[new_blank] = state[new_blank], state[blank]
    return tuple(state)

# Function to generate all possible states (not feasible for large puzzles)
def generate_all_states():
    return set(itertools.permutations(range(9)))

# Value Iteration for 8-Puzzle
def value_iteration_8_puzzle(gamma=0.9, threshold=1e-4):
    V = {GOAL_STATE: 0}
    policy = {GOAL_STATE: None}
    states_to_process = deque([GOAL_STATE])
    
    while states_to_process:
        state = states_to_process.popleft()
        for action in get_possible_actions(state):
            next_state = perform_action(state, action)
            # Since we're working backwards, the reward is -1 for each move
            value = -1 + gamma * V[state]
            if next_state not in V or value > V[next_state]:
                V[next_state] = value
                policy[next_state] = action
                states_to_process.append(next_state)
    
    return V, policy

# Function to reconstruct the path from a state to the goal
def reconstruct_path(policy, start_state):
    path = []
    state = start_state
    while state != GOAL_STATE:
        action = policy.get(state)
        if action is None:
            return None  # No solution
        path.append(action)
        state = perform_action(state, action)
    return path

# Example Usage
if __name__ == "__main__":
    # Example scrambled state
    start_state = (1, 2, 3, 4, 5, 6, 0, 7, 8)
    
    print("Running Value Iteration for 8-Puzzle...")
    V, policy = value_iteration_8_puzzle()
    
    path = reconstruct_path(policy, start_state)
    if path:
        print(f"Solution found in {len(path)} moves: {path}")
    else:
        print("No solution found.")
