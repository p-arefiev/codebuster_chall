import sys
import math

# Send your busters out into the fog to trap ghosts and bring them home!

busters_per_player = int(input())  # the amount of busters you control
ghost_count = int(input())  # the amount of ghosts on the map
my_team_id = int(input())  # if this is 0, your base is on the top left of the map, if it is one, on the bottom right

def info_round(entity_id, x, y, entity_type, state, value):
    if entity_type == -1:
        all_ghost.append({
            "entity_id" : entity_id,
            "x": x,
            "y": y,
            "entity_type": entity_type,
            "state": state,
            "value": value
            }
        )
    elif entity_type == my_team_id:
        all_buster.append({
            "entity_id" : entity_id,
            "x": x,
            "y": y,
            "entity_type": entity_type,
            "state": state,
            "value": value
            } 
        )

def distance(x1, y1, x2, y2):
    return int(math.sqrt(math.pow((x1 - x2), 2) + math.pow((y1 - y2), 2)))

def closest_busters(all_ghost, all_buster):
    min_buster = []
    if len(all_ghost) > 0:
        for ghost_iter in range(len(all_ghost)): 
            buster_dist = []

            for buster_iter in range(busters_per_player):
                buster_dist.append(
                    {
                        "buster": all_buster[buster_iter]["entity_id"],
                        "ghost": all_ghost[ghost_iter]["entity_id"],
                        "dist": distance(
                            all_buster[buster_iter]['x'],
                            all_buster[buster_iter]['y'],
                            all_ghost[ghost_iter]['x'],
                            all_ghost[ghost_iter]['y']),
                        "x" : all_ghost[ghost_iter]['x'],
                        "y" : all_ghost[ghost_iter]['y'] 
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
        info_round(entity_id, x, y, entity_type, state, value)

    print(f"all ghost : {len(all_ghost)}", file=sys.stderr, flush=True)
    min_buster = closest_busters(all_ghost, all_buster)

    for i in range(busters_per_player):

        # Write an action using print
        # To debug: print("Debug messages...", file=sys.stderr, flush=True)
        # MOVE x y | BUST id | RELEASE
        if all_buster[i]['x'] <= 1000 and all_buster[i]['y'] <= 1000:
            print("RELEASE")
        
        elif all_buster[i]['state'] == 1:
            print("MOVE 0 0")

        elif all_buster[i]['state'] == 0 and i in [x["buster"] for x in min_buster]:
            x_cible = [x for x in min_buster if x['buster'] == i][0]['x']
            y_cible = [x for x in min_buster if x['buster'] == i][0]['y']

            dist_to_ghost = distance(x_cible, y_cible, x, y)

            if dist_to_ghost >= 900 and dist_to_ghost < 1700:
                print(f"BUST {[x for x in min_buster if x['buster'] == i][0]['ghost']}")
            
            elif dist_to_ghost > 1700 or dist_to_ghost < 900:
                print(f"MOVE {x_cible - 500 } {y_cible - 500}")

        else:
            print(f"MOVE {int(math.tan(math.radians((i+1)*(90/(busters_per_player+1))))*9000)} 9000")

            
            
