from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

# Load world
world = World()


# You may uncomment the smaller graphs for development and testing purposes.
map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
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

def get_neigbors(room):
    # get ajacent rooms accessible from given room_id in world
    neighbors = []
    # check all four directions    
    for direction in ['n', 's', 'w', 'e']:
        next_room = room.get_room_in_direction('direction')
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

def dft(curr_room, visited_rooms):
    # Given current room and visited_rooms set, 
    # use DFT to store each step along the path
    s = Stack()
    s.push(curr_room)
    path = []
    while s.size() > 0:
        v = s.pop()
        # visited or not, we want path to record this vertex
        path.append(v)
        if v not in visited_rooms:
            visited_rooms.append(v)
            
            for neighbor in get_neigbors(v):
                s.push(neighbor)

    return path




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
