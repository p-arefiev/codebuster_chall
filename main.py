import sys
import math
import random
import time


# Send your busters out into the fog to trap ghosts and bring them home!

# The amount of busters you control
busters_per_player = int(input())
# The amount of ghosts on the map
ghost_count = int(input())
# if this is 0, your base is on the top left of the map, if it is one, on the bottom right
my_team_id = int(input())


class Entity:
    def __init__(self, entity_id, x, y, entity_type, state, value):
        self.entity_id = entity_id
        self.x = x
        self.y = y
        self.state = state
        self.value = value
        self.entity_type = entity_type


class Buster(Entity):
    def __init__(self, entity_id, x, y, entity_type, state, value):
        super().__init__(
            entity_id,
            x,
            y,
            entity_type,
            state,
            value,
        )
        self.closest_ghost = -1
        self.closest_ghost_dist = 0
        self.closest_ghost_x = 0
        self.closest_ghost_y = 0
        self.closest_op_buster = 0
        self.closest_op_buster_dist = 0
        self.stun_ready = True
        self.stun_reload = 0
        self.status = "IDLE"
        self.target_x = 0
        self.target_y = 0
        self.pos_max = False
        self.pos_min = True


# Busters creation for the current game
my_busters = []
for i in range(busters_per_player):
    if my_team_id == 0:
        # Create obj for all my busters
        my_busters.append(Buster(i, 0, 0, 0, 0, 0))
    else:
        # Create obj for all my busters
        my_busters.append(Buster(i + busters_per_player, 0, 0, 1, 0, 0))

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
    if entity_type == my_team_id:
        # Use entity id to select one of our buster
        n = entity_id if my_team_id == 0 else entity_id - busters_per_player
        my_busters[n].x = x
        my_busters[n].y = y
        my_busters[n].state = state
        my_busters[n].value = value
    else:
        all_entities.append(Entity(entity_id, x, y, entity_type, state, value))


def distance(x1, y1, x2, y2):
    """
    return distance between 2 points
    """
    return int(math.sqrt(math.pow((x1 - x2), 2) + math.pow((y1 - y2), 2)))


def closest_entities(all_entities):
    """
    Look for closest entity per buster when ghost are insight
    """

    # Loop through all created entity for this loop
    for entity in all_entities:
        buster_dist = []

        # For each buster find its distance to a given entity
        for buster in my_busters:
            if entity.entity_type == -1:
                # Update buster params with closest ghost informations
                buster.closest_ghost = entity.entity_id
                buster.closest_ghost_dist = distance(
                    buster.x,
                    buster.y,
                    entity.x,
                    entity.y,
                )
                buster.closest_ghost_x = entity.x
                buster.closest_ghost_y = entity.y
            else:
                buster_dist.append(
                    distance(
                        buster.x,
                        buster.y,
                        entity.x,
                        entity.y,
                    )
                )

        # With all distance calculated choose the smaller one
        # => closest buster to this entity
        if entity.entity_type != -1:
            min_buster = min(buster_dist)
            min_index = buster_dist.index(min_buster)
            # Update buster params with closest buster informations
            my_busters[min_index].closest_op_buster = entity.entity_id
            my_busters[min_index].closest_op_buster_dist = min_buster

        # Debug printing
        # print(f"buster dist : {buster_dist}", file=sys.stderr, flush=True)
        # print(f"min dist : {min_buster}", file=sys.stderr, flush=True)


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
    - BASE => buster is going back to his base while carrying a ghost
    - READY => when a buster is ready to release a ghost in his base
    - STUN => has a buster in sight, go for the kill
    """
    for buster in my_busters:

        # Count reloading time
        if buster.stun_ready == False and buster.stun_reload > 0:
            buster.stun_reload -= 1
        elif buster.stun_ready == False and buster.stun_reload == 0:
            buster.stun_ready = True

        # priority to ghost releasing
        if buster.value != -1 and buster.state == 1 and not in_base(buster.x, buster.y):
            buster.status = "BASE"
            continue
        elif buster.value != -1 and buster.state == 1 and in_base(buster.x, buster.y):
            buster.status = "READY"
            continue

        # then is a buster sees another buster stun him
        if (
            buster.closest_op_buster != 0
            and buster.closest_op_buster_dist < 1760
            and buster.stun_ready
            and buster.stun_reload == 0
        ):

            buster.status = "STUN"
            buster.stun_ready = False
            buster.stun_reload = 20
            continue

        # check if a ghost is in sight
        if buster.closest_ghost >= 0 and buster.closest_ghost_dist > 1700:

            buster.status = "CHASING"
        elif (
            buster.closest_ghost >= 0
            and buster.closest_ghost_dist < 1700
            and buster.closest_ghost_dist > 900
        ):

            buster.status = "BUSTING"
        elif buster.closest_ghost >= 0 and buster.closest_ghost_dist < 900:

            buster.closest_ghost_x = buster.closest_ghost_x - (
                -900 if my_team_id == 0 else 900
            )
            buster.closest_ghost_y = buster.closest_ghost_y - (
                -900 if my_team_id == 0 else 900
            )
            buster.status = "CHASING"
        else:
            buster.status = "IDLE"

            if buster.x >= 16000 or buster.y >= 9000:
                buster.pos_max = True


def direction(buster: Buster, index):

    if buster.pos_max == False:
        if busters_per_player == 2:
            if index == 0:
                x = abs(ori_x - int(math.tan(math.radians(25)) * 9000))
                y = 9000 - ori_y
            elif index == 1:
                x = 16000 - ori_x
                y = abs(ori_y - int(math.tan(math.radians(10)) * 16000))
        elif busters_per_player == 3:
            if index == 0:
                x = 16000 - ori_x
                y = 9000 - ori_y
            elif index == 1:
                x = 16000 - ori_x
                y = abs(ori_y - int(math.tan(math.radians(8)) * 16000))
            elif index == 2:
                x = abs(ori_x - int(math.tan(math.radians(15)) * 9000))
                y = 9000 - ori_y
        elif busters_per_player == 4:
            if index == 0:
                x = abs(ori_x - int(math.tan(math.radians(40)) * 9000))
                y = 9000 - ori_y
            elif index == 1:
                x = 16000 - ori_x
                y = abs(ori_y - int(math.tan(math.radians(25)) * 16000))
            elif index == 2:
                x = abs(ori_x - int(math.tan(math.radians(10)) * 9000))
                y = 9000 - ori_y
            elif index == 3:
                x = 16000 - ori_x
                y = abs(ori_y - int(math.tan(math.radians(5)) * 16000))
    else:
        x = ori_x
        y = ori_y

    if x >= 16000:
        x = 16000

    if y >= 9000:
        y = 9000

    buster.target_x = x
    buster.target_y = y


def print_buster_info(buster: Buster):

    header = [
        "status",
        "X",
        "Y",
        "state",
        "value",
        "closest_ghost",
        "closest_ghost_dist",
        "closest_op_buster",
        "closest_op_buster_dist",
    ]
    row = [
        buster.status,
        buster.x,
        buster.y,
        buster.state,
        buster.value,
        buster.closest_ghost,
        buster.closest_ghost_dist,
        buster.closest_op_buster,
        buster.closest_op_buster_dist,
    ]

    print(
        "{:-^118}".format(f"Buster id = {buster.entity_id}"),
        file=sys.stderr,
        flush=True,
    )
    data = [header, row]
    dash = "-" * 118

    for i in range(len(data)):
        if i == 0:
            print(
                "|{:^10s}{:^6s}{:^6s}{:^7s}{:^7s}|{:^15s}{:^20s}|{:^19s}{:^24s}|".format(
                    data[i][0],
                    data[i][1],
                    data[i][2],
                    data[i][3],
                    data[i][4],
                    data[i][5],
                    data[i][6],
                    data[i][7],
                    data[i][8],
                ),
                file=sys.stderr,
                flush=True,
            )
            print(dash, file=sys.stderr, flush=True)
        else:
            print(
                "|{:^10s}{:^6}{:^6}{:^7}{:^7}|{:^15}{:^20}|{:^19}{:^24}|".format(
                    data[i][0],
                    data[i][1],
                    data[i][2],
                    data[i][3],
                    data[i][4],
                    data[i][5],
                    data[i][6],
                    data[i][7],
                    data[i][8],
                ),
                file=sys.stderr,
                flush=True,
            )
            print(dash, file=sys.stderr, flush=True)


# game loop
while True:

    # list with all ghost visible for this loop
    all_entities = []

    # the number of busters and ghosts visible to you
    entities = int(input())

    start_time = time.time()
    for i in range(entities):
        # entity_id: buster id or ghost id
        # y: position of this buster / ghost
        # entity_type: the team id if it is a buster, -1 if it is a ghost.
        # state: For busters: 0=idle, 1=carrying a ghost.
        # value: For busters: Ghost id being carried. For ghosts: number of busters attempting to trap this ghost.
        entity_id, x, y, entity_type, state, value = [int(j) for j in input().split()]
        info_turn(entity_id, x, y, entity_type, state, value)

    # print(f"visible entities: {len(all_entities)} ", file=sys.stderr, flush=True)

    # Updating flag values:
    closest_entities(all_entities)
    update_status()

    for index, buster in enumerate(my_busters):
        print_buster_info(buster)
        direction(buster, index)

        if buster.status == "CHASING":
            print(f"MOVE {buster.closest_ghost_x} {buster.closest_ghost_y}")

        elif buster.status == "BUSTING":
            print(f"BUST {buster.closest_ghost}")

        elif buster.status == "BASE":
            print(f"MOVE {ori_x} {ori_y}")

        elif buster.status == "READY":
            print(f"RELEASE")

        elif buster.status == "STUN":
            print(f"STUN {buster.closest_op_buster}")

        else:
            print(f"MOVE {buster.target_x} {buster.target_y}")

        buster.closest_ghost = -1
        buster.closest_ghost_dist = 0
        buster.closest_op_buster = 0
        buster.closest_op_buster_dist = 0

    print(
        f"--- {float((time.time() - start_time)) * 1000} ms ---",
        file=sys.stderr,
        flush=True,
    )
