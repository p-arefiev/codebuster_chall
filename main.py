import sys
import math

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


def info_turn(entity_id, x, y, entity_type, state, value):
    if entity_type == -1:
        ghost = Ghost(entity_id, x, y, entity_type, state, value)
        all_ghost.append(ghost)

    elif entity_type == my_team_id:
        buster = Buster(entity_id, x, y, entity_type, state, value)
        all_buster.append(buster)


def distance(x1, y1, x2, y2):
    return int(math.sqrt(math.pow((x1 - x2), 2) + math.pow((y1 - y2), 2)))


def closest_busters(all_ghost, all_buster):

    for ghost_iter in range(len(all_ghost)):
        buster_dist = []
    
        for buster_iter in range(busters_per_player):
            buster_dist.append(distance(
                all_buster[buster_iter].x,
                all_buster[buster_iter].y,
                all_ghost[ghost_iter].x,
                all_ghost[ghost_iter].y,
            ))

        #print(f"min dist : {min_buster}", file=sys.stderr, flush=True)
        #print(f"buster dist : {buster_dist}", file=sys.stderr, flush=True)
        min_buster = min(buster_dist)
        min_index = buster_dist.index(min_buster)
        if all_buster[min_index].status == "IDLE":
            all_buster[min_index].closest_ghost = all_ghost[ghost_iter].entity_id
            all_buster[min_index].closest_ghost_x = all_ghost[ghost_iter].x
            all_buster[min_index].closest_ghost_y = all_ghost[ghost_iter].y
            all_buster[min_index].closest_ghost_dist = min_buster

def update_status(all_buster):
    for buster_iter in all_buster:

        if buster_iter.value != -1 and (buster.x > 1600 or buster_iter.y > 1600) :
            buster_iter.status = "GB"
            continue
        elif buster_iter.value != -1 and (buster_iter.x <= 1600 or buster.y <= 1600):
            buster_iter.status = "READY"
            continue
        else:
            pass

        if buster_iter.closest_ghost > 0 and buster_iter.closest_ghost_dist > 1700:
            buster_iter.status = "CHASING"
        elif buster_iter.closest_ghost > 0 and buster_iter.closest_ghost_dist < 1700 and buster_iter.closest_ghost_dist > 900:
            buster_iter.status = "BUSTING"
        elif buster_iter.closest_ghost > 0 and buster_iter.closest_ghost_dist < 900:
            buster_iter.closest_ghost_x = 0
            buster_iter.closest_ghost_y = 0
            buster_iter.status = "CHASING"
        else:
            buster_iter.status = "IDLE"


# game loop
while True:
    all_buster = []
    all_ghost = []
    min_buster = []

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
    #print(f"buster count: {len(all_buster)}", file=sys.stderr, flush=True)
    closest_busters(all_ghost, all_buster)
    update_status(all_buster)

    #for i in range(busters_per_player):
    for buster in all_buster:
        # Write an action using print
        # To debug: print("Debug messages...", file=sys.stderr, flush=True)
        # MOVE x y | BUST id | RELEASE
        print(f"buster {buster.entity_id} closes ghost: {buster.closest_ghost} | status: {buster.status}", file=sys.stderr, flush=True)
        if buster.status == "CHASING":
            print(f"MOVE {buster.closest_ghost_x} {buster.closest_ghost_y}")
        elif buster.status == "BUSTING":
            print(f"BUST {buster.closest_ghost}")
        elif buster.status == "GB": 
            print(f"MOVE {0} {0}")
        elif buster.status == "READY":
            print(f"RELEASE")
        else:
            print(
                f"MOVE {int(math.tan(math.radians((buster.entity_id+1)*(90/(busters_per_player+1))))*9000)} 9000"
            )
