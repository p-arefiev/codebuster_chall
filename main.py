import sys
import math
import random

# Send your busters out into the fog to trap ghosts and bring them home!

busters_per_player = int(input())  # the amount of busters you control
ghost_count = int(input())  # the amount of ghosts on the map
my_team_id = int(
    input()
)  # if this is 0, your base is on the top left of the map, if it is one, on the bottom right

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

for i in range(busters_per_player):
    if my_team_id == 0:
        # Create obj for all my busters
        buster = Buster(i, 0, 0, 0, 0, 0)
        my_busters.append(buster)
        # Create obj for all my opponent busters
        buster_opp = Buster(i + busters_per_player, 0, 0, 1, 0, 0)
        his_busters.append(buster)
    else:
        # Create obj for all my busters
        buster = Buster(i + busters_per_player, 0, 0, 1, 0, 0)
        my_busters.append(buster)
        # Create obj for all my opponent busters
        buster_opp = Buster(i, 0, 0, 0, 0, 0)
        his_busters.append(buster)

ori_x = 0
ori_y = 0
if my_team_id == 1:
    ori_x = 16000
    ori_y = 9000

def info_turn(entity_id, x, y, entity_type, state, value):
    if entity_type == -1:
        ghost = Ghost(entity_id, x, y, entity_type, state, value)
        all_ghost.append(ghost)
    elif entity_type == my_team_id :
            n = entity_id if my_team_id == 0 else entity_id - busters_per_player
            my_busters[n].x = x
            my_busters[n].y = y
            my_busters[n].state = state
            my_busters[n].value = value

def distance(x1, y1, x2, y2):
    return int(math.sqrt(math.pow((x1 - x2), 2) + math.pow((y1 - y2), 2)))

def closest_busters(all_ghost):

    for ghost_iter in range(len(all_ghost)):
        buster_dist = []
    
        for buster_iter in range(busters_per_player):
            buster_dist.append(distance(
                my_busters[buster_iter].x,
                my_busters[buster_iter].y,
                all_ghost[ghost_iter].x,
                all_ghost[ghost_iter].y,
            ))
        #print(f"min dist : {min_buster}", file=sys.stderr, flush=True)
        #print(f"buster dist : {buster_dist}", file=sys.stderr, flush=True)
        min_buster = min(buster_dist)
        min_index = buster_dist.index(min_buster)
        my_busters[min_index].closest_ghost = all_ghost[ghost_iter].entity_id
        my_busters[min_index].closest_ghost_x = all_ghost[ghost_iter].x
        my_busters[min_index].closest_ghost_y = all_ghost[ghost_iter].y
        my_busters[min_index].closest_ghost_dist = min_buster

def in_base(x, y):
    if distance(x, y, ori_x, ori_y) > 1600:
        return False
    else:
        return True

def update_status():
    for buster_iter in my_busters:
        if buster_iter.value != -1 and not in_base(buster_iter.x, buster_iter.y) :
            buster_iter.status = "GB"
            continue
        elif buster_iter.value != -1 and in_base(buster_iter.x, buster_iter.y):
            buster_iter.status = "READY"
            buster_iter.closest_ghost = 0
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

# game loop
while True:
    all_ghost = []

    entities = int(input())  # the number of busters and ghosts visible to you

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

    #for i in range(busters_per_player):
    for index, buster in enumerate(my_busters):
        # Write an action using print
        # To debug: print("Debug messages...", file=sys.stderr, flush=True)
        # MOVE x y | BUST id | RELEASE
        print(f"buster {buster.entity_id} closes ghost: {buster.closest_ghost} | status: {buster.status}", file=sys.stderr, flush=True)
        
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
