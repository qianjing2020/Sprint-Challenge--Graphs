from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
#map_file = "maps/test_line.txt"
map_file = "maps/test_cross.txt"
# map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
#map_file = "maps/main_maze.txt"

# Loads the map into a dictionary
room_graph=literal_eval(open(map_file, "r").read())
world.load_graph(room_graph)

# Print an ASCII map
world.print_rooms()

player = Player(world.starting_room)

# Fill this out with directions to walk
# traversal_path = ['n', 'n']
""" move player around to traverse all graph
All rooms need to be covered.
Record total moves len(traversal_path) """
traversal_path = []


def get_room_graph(world):
    """ 
    Construct room graphs from the world object. 
    vertices are: 
    {
        0: {'n': '?', 's': 5, 'w': '?', 'e': '?'},
        5: {'n': 0, 's': '?', 'e': '?'}
    }
    """      
    room_graph = {}
    rooms = world.rooms
    for n in rooms:
        r = rooms[n]
        key = r.id
        # initiate a dictionary with direction as key, room in direction as value
        value = {'n': '?', 's': '?', 'w': '?', 'e': '?'}
        
        for D in r.get_exits():
            value[D] = r.get_room_in_direction(D).id
        
        room_graph[key] = value
    return room_graph
    

def get_neigbors(room):
    # get ajacent rooms accessible from given room_id in world
    neighbors = []
    # check all four directions    
    for direction in ['n', 's', 'w', 'e']:
        next_room = room.get_room_in_direction(direction)
        if next_room is not None:
            neighbors.append(next_room)    
    return neighbors

class Stack():
    def __init__(self):
        self.stack = []
    def push(self, value):
        self.stack.append(value)
    def pop(self):
        if self.size() > 0:
            return self.stack.pop()
        else:
            return None
    def size(self):
        return len(self.stack)

def dft(curr_room, visited_rooms=None, path=None):
    # Given current room and visited_rooms set, 
    # use DFT to store each step along the path
    
    if visited_rooms  == None:
        visited_rooms = set()
    if path == None:
        path = []
    
    visited_rooms.add(curr_room)
    path += [curr_room]
    
    for r in get_neigbors(curr_room):
        if r not in visited_rooms:
            dft(r, visited_rooms, path)
    
    return path


def get_direction_from_path(path):
    # get the id of the room in path
    ids = [item.id for item in path]
    # initialize edges
    edges =  ['?' for item in range(len(ids)-1)]
    # loop through ids
    for n, id in enumerate(ids):
        for D in ['n', 's', 'e', 'w']:
            if path[id].get_room_in_direction(D) == path[ids[n+1]]:
                edges[n] = D
    return edges


current_room = world.starting_room
path = dft(current_room)
path_id = [item.id for item in path]
print('LLLLLLLLLL')

print(get_room_graph(world))
breakpoint()
# TRAVERSAL TEST - DO NOT MODIFY
visited_rooms = set()
player.current_room = world.starting_room
visited_rooms.add(player.current_room)

for move in traversal_path:
    player.travel(move)
    visited_rooms.add(player.current_room)

if len(visited_rooms) == len(room_graph):
    print(f"TESTS PASSED: {len(traversal_path)} moves, {len(visited_rooms)} rooms visited")

else:
    print("TESTS FAILED: INCOMPLETE TRAVERSAL")
    print(f"{len(room_graph) - len(visited_rooms)} unvisited rooms")


#######
# UNCOMMENT TO WALK AROUND
#######
player.current_room.print_room_description(player)
while True:
    cmds = input("-> ").lower().split(" ")
    if cmds[0] in ["n", "s", "e", "w"]:
        player.travel(cmds[0], True)
    elif cmds[0] == "q":
        break
    else:
        print("I did not understand that command.")
