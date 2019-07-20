import itertools
import json
import operator
import random

map_height = 50
map_width = 50
min_path = 10
max_path = 15
max_path_iterations = 50


road = 1
grass = 89
road_v_barrier = 10
road_h_barrier = 3
road_blc_barrier = 18
road_brc_barrier = 19
road_tlc_barrier = 2
road_trc_barrier = 4


ops = {
    "+": operator.add,
    "-": operator.sub
}


def create_rand_path(map, startx, starty, direction, iterations=0):
    xopfunc = None
    yopfunc = None
    current_x = startx
    current_y = starty

    iterations += 1

    if iterations > max_path_iterations:
        return

    path_length = random.randint(min_path, max_path)

    print("Create path called. X: {} Y: {} Iter: {} Dir: {}".format(startx, starty, iterations, direction))
    if direction == "UP":
        yopfunc = ops["-"]
        xopfunc = None
    if direction == "DOWN":
        yopfunc = ops["+"]
        xopfunc = None
    if direction == "LEFT":
        xopfunc = ops["-"]
        yopfunc = None
    if direction == "RIGHT":
        xopfunc = ops["+"]
        yopfunc = None

    for i in range(0, path_length):
        current_x = xopfunc(startx, i) if xopfunc else startx
        current_y = yopfunc(starty, i) if yopfunc else starty

        try:
            if map[current_y][current_x] == grass:
                # Add path
                map[yopfunc(starty, i) if yopfunc else starty][xopfunc(startx, i) if xopfunc else startx] = road

                # Add path lines
                if direction in ["LEFT", "RIGHT"]:
                    if map[current_y+1][current_x] == grass:
                        map[current_y+1][current_x] = road
                    if map[current_y-1][current_x] == grass:
                        map[current_y-1][current_x] = road
                if direction in ["UP", "DOWN"]:
                    if map[current_y][current_x+1] == grass:
                        map[current_y][current_x+1] = road
                    if map[current_y][current_x-1] == grass:
                         map[current_y][current_x-1] = road

        except IndexError:
            print("Index error yo - get out!")
            return

    if direction in ["UP", "DOWN"]:
        new_dir = get_random_direction(exclude=["UP", "DOWN"])
    else:
        new_dir = get_random_direction(exclude=["LEFT", "RIGHT"])

    return create_rand_path(map, current_x, current_y, new_dir, iterations)


def cleanup_patchy_grass(level):
    added_road_count = 0
    for y in range(map_height):
        for x in range(map_width):
            if level[y][x] == grass:
                count = 0
                try:
                    for dx in [-1, 1]:
                        for dy in [-1, 1]:
                            a = y + dx
                            b = x + dy
                            if level[a][b] == road:
                                count += 1
                except IndexError:
                    pass

                if count >= 5:
                    added_road_count +=1
                    level[y][x] = road

    print("Added road: {}".format(added_road_count))


def cleanup(level):

    for y in range(map_height):
        for x in range(map_width):
            if level[y][x] == road:
                count = 0
                try:
                    if level[y][x + 1] == grass:
                        count += 1
                    if level[y][x - 1] == grass:
                        count += 1
                    if level[y + 1][x] == grass:
                        count += 1
                    if level[y - 1][x] == grass:
                        count += 1
                except IndexError:
                    pass
                if count >= 2:
                    print("Removing road")
                    level[y][x] = grass


def get_map_file():
    output_json = json.load(open('base-map-file.json'))
    return output_json


def output_array(map_array):
    with open("outfile", 'w') as f:
        for i in map_array:
            f.write(str(i))
            f.write("\n")


def get_random_direction(exclude):
    dir_list = ['UP', 'DOWN', 'LEFT', 'RIGHT']
    if exclude is not None:
        for x in exclude:
            dir_list.remove(x)

    return random.choice(['UP', 'DOWN', 'LEFT', 'RIGHT'])


"""
Pick centre point
Create 1-4 directions outwards
continue forward for 5-15 tiles
choice left/right/forward/down

"""



def main():
    tilemap = get_map_file()

    # Populate 2d array of given height and width with - values
    level1 = [[grass for x in range(0, map_width)] for y in range(0, map_height)]

    cy, cx = int(map_height/2), int(map_width/2)
    print("centerX: {} \ncenterY: {}".format(cx, cy))

    # Generate central plaza
    level1[cy][cx] = road
    for i in range(-2, +2):
        for j in range(-2, 2):
            level1[cy+i][cx+j] = road
            level1[cy-i][cx+j] = road
            level1[cy-i][cx-j] = road
            level1[cy+i][cx-j] = road

    level1[cy + 2][cx +2] = road_brc_barrier
    level1[cy - 2][cx +2 ] = road_trc_barrier
    level1[cy + 2][cx - 2 ] = road_blc_barrier
    level1[cy - 2][cx - 2 ] = road_tlc_barrier
    level1[cy - 2][cx-1] = road_brc_barrier
    level1[cy + 2][cx-1] = road_trc_barrier
    level1[cy-1][cx - 2] = road_brc_barrier
    level1[cy-1][cx + 2] = road_blc_barrier
    level1[cy-2][cx + 1] = road_blc_barrier
    level1[cy+1][cx - 2] = road_trc_barrier
    level1[cy+1][cx + 2] = road_tlc_barrier
    level1[cy+2][cx + 1] = road_tlc_barrier


    # Between 2 and 4 paths
    directions =  random.sample(['UP', 'DOWN', 'LEFT', 'RIGHT'], k=random.randint(2,4))
    # directions = ['UP', 'DOWN', 'LEFT', 'RIGHT']
    # for dir in directions:
    create_rand_path(level1, cx, cy-3, "UP")
    create_rand_path(level1, cx, cy+3, "DOWN")
    create_rand_path(level1, cx+3, cy, "RIGHT")
    create_rand_path(level1, cx-3, cy, "LEFT")

    cleanup_patchy_grass(level1)
    # cleanup_road_tiles(level1)

    tilemap['layers'][0]["data"] = list(itertools.chain(*level1))
    with open('/Users/adamprobert/Documents/Projects/twin-stick-shooter/twin-stick-frontend/src/assets/tilesets/horrormap.json', 'w') as fp:
        json.dump(tilemap, fp)

    output_array(level1)


if __name__ == '__main__':
    main()
