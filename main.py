import sys
import math

# Send your busters out into the fog to trap ghosts and bring them home!

busters_per_player = int(input())  # the amount of busters you control
ghost_count = int(input())  # the amount of ghosts on the map
my_team_id = int(input())  # if this is 0, your base is on the top left of the map, if it is one, on the bottom right

class Entity():
    def __init__(self, entity_id, x, y, state, value):
        self.entity_id = 0
        self.x = 0
        self.y = 0
        self.state = 0
        self.value = 0

class Buster(Entity):
    def __init__(self, entity_id, x, y, entity_type, state, value):
        super().__init__(
            entity_id,
            x,
            y,
            state,
            value,
        )

        self.entity_type = 0
        self.closest_ghost = 0
        self.closest_ghost_x = 0
        self.closest_ghost_y = 0
        self.status = 0

class Ghost(Entity):
    def __init__(self, entity_id, x, y, entity_type, state, value):
        super().__init__(
            entity_id,
            x,
            y,
            state,
            value,
        )

        self.entity_type = 0

def info_turn(entity_id, x, y, entity_type, state, value):
    if entity_type == -1:
        ghost = Ghost(entity_id, x, y, entity_type, state, value)
        all_ghost.append( ghost )
    elif entity_type == my_team_id:
        buster = Buster(entity_id, x, y, entity_type, state, value)
        all_buster.append(buster)

def distance(x1, y1, x2, y2):
    return int(math.sqrt(math.pow((x1 - x2), 2) + math.pow((y1 - y2), 2)))

def closest_busters(all_ghost, all_buster):
    min_buster = []

    for ghost_iter in range(len(all_ghost)): 
        buster_dist = []

        for buster_iter in range(busters_per_player):
            buster_dist.append(
                {
                    "buster": all_buster[buster_iter].entity_id,
                    "ghost": all_ghost[ghost_iter].entity_id,
                    "dist": distance(
                        all_buster[buster_iter].x,
                        all_buster[buster_iter].y,
                        all_ghost[ghost_iter].x,
                        all_ghost[ghost_iter].y),
                    "x" : all_ghost[ghost_iter].x,
                    "y" : all_ghost[ghost_iter].y
                }   
            )
        min_buster.append(min(buster_dist, key=lambda x:x['dist']))
        print(f"buster dist : {buster_dist}", file=sys.stderr, flush=True)
    print(f"min dist : {min_buster}", file=sys.stderr, flush=True)

    return min_buster   

# game loop
while True:
    all_buster = []
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

    print(f"ghost count: {len(all_ghost)}", file=sys.stderr, flush=True)
    print(f"buster count: {len(all_ghost)}", file=sys.stderr, flush=True)

    for i in range(busters_per_player):

        # Write an action using print
        # To debug: print("Debug messages...", file=sys.stderr, flush=True)
        # MOVE x y | BUST id | RELEASE
        
        print(f"MOVE {int(math.tan(math.radians((i+1)*(90/(busters_per_player+1))))*9000)} 9000")

            
            
