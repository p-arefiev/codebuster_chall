import sys
import math
import random

# Send your busters out into the fog to trap ghosts and bring them home!

# The amount of busters you control
busters_per_player = int(input())  
# The amount of ghosts on the map
ghost_count = int(input())  
# if this is 0, your base is on the top left of the map, if it is one, on the bottom right
my_team_id = int(input())  

class Entity:
    def __init__(self, entity_id, x, y, state, value):
        self.entity_id = entity_id
        self.x = x
        self.y = y
        self.state = state
        self.value = value

class Buster(Entity):
    def __init__(self, entity_id, x, y, entity_type, state, value):
        super().__init__(
            entity_id,
            x,
            y,
            state,
            value,
        )
        self.entity_type = entity_type
        self.closest_ghost = 0
        self.closest_ghost_dist = 0
        self.closest_ghost_x = 0
        self.closest_ghost_y = 0
        self.closest_op_buster = 0
        self.closest_op_buster_dist = 0
        self.status = "IDLE"

class Ghost(Entity):
    def __init__(self, entity_id, x, y, entity_type, state, value):
        super().__init__(
            entity_id,
            x,
            y,
            state,
            value,
        )
        self.entity_type = entity_type

his_busters = []
my_busters = []

# Busters creation for the current game
for i in range(busters_per_player):
    if my_team_id == 0:
        # Create obj for all my busters
        my_busters.append(Buster(i, 0, 0, 0, 0, 0))
        # Create obj for all my opponent busters
        his_busters.append(Buster(i + busters_per_player, 0, 0, 1, 0, 0))
    else:
        # Create obj for all my busters
        my_busters.append(Buster(i + busters_per_player, 0, 0, 1, 0, 0))
        # Create obj for all my opponent busters
        his_busters.append(Buster(i, 0, 0, 0, 0, 0))

# Set base position depending on which team we are
ori_x = 0
ori_y = 0
if my_team_id == 1:
    ori_x = 16000
    ori_y = 9000

def info_turn(entity_id, x, y, entity_type, state, value):
    """
    Each loop create all insight ghosts.
    Update our buster positions state & value
    Same for opponent busters.
    """

    # Check entity type to choose what action to do :  create a ghost / update our
    # Busters infos / update opponent buster info
    if entity_type == -1:
        ghost = Ghost(entity_id, x, y, entity_type, state, value)
        all_ghost.append(ghost)
    elif entity_type == my_team_id :
            # Use entity id to select one of our buster
            n = entity_id if my_team_id == 0 else entity_id - busters_per_player
            my_busters[n].x = x
            my_busters[n].y = y
            my_busters[n].state = state
            my_busters[n].value = value
    else :
            # Use entity id to select one of his buster
            n = entity_id - busters_per_player if my_team_id == 0 else entity_id
            his_busters[n].x = x
            his_busters[n].y = y
            his_busters[n].state = state
            his_busters[n].value = value

def distance(x1, y1, x2, y2):
    """
    return distance between 2 points
    """
    return int(math.sqrt(math.pow((x1 - x2), 2) + math.pow((y1 - y2), 2)))

def closest_busters(all_ghost):
    """
    Look for closest ghost per buster when ghost are insight
    """

    # Loop through all created ghost for this loop
    for ghost_iter in range(len(all_ghost)):
        buster_dist = []

        # For each buster find its distance for a given ghost
        for buster_iter in range(busters_per_player):
            buster_dist.append(distance(
                my_busters[buster_iter].x,
                my_busters[buster_iter].y,
                all_ghost[ghost_iter].x,
                all_ghost[ghost_iter].y,
            ))
        
        # With all distance calculated choose the smaller one 
        # => closest buster for this ghost
        min_buster = min(buster_dist)
        min_index = buster_dist.index(min_buster)

        # Update buster params with closest ghost informations
        my_busters[min_index].closest_ghost = all_ghost[ghost_iter].entity_id
        my_busters[min_index].closest_ghost_x = all_ghost[ghost_iter].x
        my_busters[min_index].closest_ghost_y = all_ghost[ghost_iter].y
        my_busters[min_index].closest_ghost_dist = min_buster

        # Debug printing
        print(f"min dist : {min_buster}", file=sys.stderr, flush=True)
        print(f"buster dist : {buster_dist}", file=sys.stderr, flush=True)

def in_base(x, y):
    """
    Find out if a buster is within the range of his base.
    Used to tell if a buster needs to release a ghost.
    """
    if distance(x, y, ori_x, ori_y) > 1600:
        return False
    else:
        return True

def update_status():
    """
    Main buster loop here its overall status is updated.
    A buster can have one of the 5 status.
    - IDLE => looking for an entity
    - CHASING => ghost in sight, getting closer to a ghost to bust him
    - BUSTING => a buster is ready to bust
    - GB => buster is going back to his base while carrying a ghost
    - READY => when a buster is ready to release a ghost in his base
    """
    for buster_iter in my_busters:
        if buster_iter.value != -1 and not in_base(buster_iter.x, buster_iter.y) :
            buster_iter.status = "GB"
            continue
        elif buster_iter.value != -1 and in_base(buster_iter.x, buster_iter.y):
            buster_iter.status = "READY"
            buster_iter.closest_ghost = 0
            buster_iter.closest_ghost_dist = 0
            continue
        else:
            pass
        if buster_iter.closest_ghost > 0 and buster_iter.closest_ghost_dist > 1700:
            buster_iter.status = "CHASING"
        elif buster_iter.closest_ghost > 0 and buster_iter.closest_ghost_dist < 1700 and buster_iter.closest_ghost_dist > 900:
            buster_iter.status = "BUSTING"
        elif buster_iter.closest_ghost > 0 and buster_iter.closest_ghost_dist < 900:
            buster_iter.closest_ghost_x = buster_iter.closest_ghost_x - ( -900 if my_team_id == 0 else 900)
            buster_iter.closest_ghost_y = buster_iter.closest_ghost_y - ( -900 if my_team_id == 0 else 900)
            buster_iter.status = "CHASING"
        else:
            buster_iter.status = "IDLE"

def direction( busters_per_player, my_team_id, i):
    rand_x = random.randint(0, 100 )
    rand_y = random.randint(0, 100 )
    if my_team_id == 0:
        if busters_per_player == 1:
            print(f"MOVE 16000 9000")
        else:
            print(f"MOVE {rand_x + int(math.tan(math.radians((i+1)*(90/(busters_per_player +1))))*9000)} 9000")
    else: 
        if busters_per_player == 1:
            print(f"MOVE 0 0")
        else:
            print(f"MOVE {rand_x + int(math.tan(math.radians((i+1)*(90/(busters_per_player+1))))*9000)} 0")

def print_buster_info(buster: Buster):

    header = [
        'status', 'X', 'Y', 'state', 'value', 
        'closest_ghost', 'closest_ghost_dist', 
        'closest_op_buster', 'closest_op_buster_dist'
        ]
    row = [
        buster.status, buster.x, buster.y, buster.state, buster.value,
        buster.closest_ghost, buster.closest_ghost_dist,
        buster.closest_op_buster, buster.closest_op_buster_dist
    ]

    print('{:-^110}'.format(f"Buster id = {buster.entity_id}"), file=sys.stderr, flush=True)
    data = [header, row]
    dash = '-' * 110

    for i in range(len(data)):
        if i == 0:
            print('|{:^10s}{:^6s}{:^7s}{:^7s}{:^15s}{:^20s}{:^19s}{:^24s}|'.format(data[i][0], data[i][1], data[i][2], data[i][3], data[i][4], data[i][5], data[i][6], data[i][7], data[i][8]), file=sys.stderr, flush=True)
            print(dash, file=sys.stderr, flush=True)
        else:
            print('|{:^10s}{:^6}{:^7}{:^7}{:^15}{:^20}{:^19}{:^24}|'.format(data[i][0], data[i][1], data[i][2], data[i][3], data[i][4], data[i][5], data[i][6], data[i][7], data[i][8]), file=sys.stderr, flush=True)
            print(dash, file=sys.stderr, flush=True)


# game loop
while True:

    # list with all ghost visible for this loop
    all_ghost = []

    # the number of busters and ghosts visible to you
    entities = int(input())  

    for i in range(entities):
        # entity_id: buster id or ghost id
        # y: position of this buster / ghost
        # entity_type: the team id if it is a buster, -1 if it is a ghost.
        # state: For busters: 0=idle, 1=carrying a ghost.
        # value: For busters: Ghost id being carried. For ghosts: number of busters attempting to trap this ghost.
        entity_id, x, y, entity_type, state, value = [int(j) for j in input().split()]
        info_turn(entity_id, x, y, entity_type, state, value)

    print(f"ghost count: {len(all_ghost)} ", file=sys.stderr, flush=True)
    #print(f"buster count: {len(my_busters)}", file=sys.stderr, flush=True)
    closest_busters(all_ghost)
    update_status()

    for index, buster in enumerate(my_busters):
        print_buster_info(buster)
        
        if buster.status == "CHASING":
            print(f"MOVE {buster.closest_ghost_x} {buster.closest_ghost_y}")

        elif buster.status == "BUSTING":
            print(f"BUST {buster.closest_ghost}")

        elif buster.status == "GB":
            print(f"MOVE {ori_x} {ori_y}")

        elif buster.status == "READY":
            print(f"RELEASE")

        else:
            direction(busters_per_player,my_team_id, index)
