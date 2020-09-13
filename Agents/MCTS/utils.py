import numpy as np

def Match_goal_box(previous_state, new_state):
    box_loc = get_box_loc(previous_state) == get_box_loc(new_state)
    goal_loc = get_goals_loc(previous_state) == get_box_loc(new_state)
    if box_loc.all() and goal_loc.all():
        return True
    else:
        return False



def get_box_loc(state):
    prev_box = np.where(state == 4)
    prev_box = np.append(prev_box, np.where(state == 3), axis= 1)
    return prev_box

def get_goals_loc(state):
    prev_goal = np.where(state == 2)
    return prev_goal
