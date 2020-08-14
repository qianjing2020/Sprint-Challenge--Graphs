from room import Room
from player import Player
from world import World

import random
from ast import literal_eval

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

# Load world
world = World()

# You may uncomment the smaller graphs for development and testing purposes.
#map_file = "maps/test_line.txt"
# map_file = "maps/test_cross.txt"
#map_file = "maps/test_loop.txt"
# map_file = "maps/test_loop_fork.txt"
map_file = "maps/main_maze.txt"

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

class RoomGraph():
    def __init__(self, world):        
        """ 
        Construct room graphs from the world object. 
        vertices are: 
        {   0: {'n': '?', 's': 5, 'w': '?', 'e': '?'},
            5: {'n': 0, 's': '?', 'e': '?'}
        }
        """ 
        rooms = world.rooms
        self.size = len(rooms)
        self.graph = {}
        for n in rooms:
            r = rooms[n]            
            # initiate key, value for each item in graph
            key = r.id
            value = {'n': None, 's': None, 'w': None, 'e': None}
            # updated wherever there is a valid exit 
            for D in r.get_exits():
                value[D] = r.get_room_in_direction(D).id
            
            self.graph[key] = value           
    
    def get_neigbors(self, room_id):
        # get ajacent rooms accessible to room
        about = self.graph[room_id]
        neighbors = {key: value for key, value in about.items() if value is not None}    
        return neighbors

    def dft(self, curr_room_id, visited_rooms=None, path=None):
        # Given current room and visited_rooms set, 
        # use DFT to store each step along the path        
        if visited_rooms  == None:
            visited_rooms = set()
        if path == None:
            path = []        
        visited_rooms.add(curr_room_id)
        # path += [curr_room_id] 

        # Get (Direction, Room id) for each neigbor            
        for D, R in self.get_neigbors(curr_room_id).items():
            if R not in visited_rooms:
                path.append(D)
                self.dft(R, visited_rooms, path)
        
        return path
   
    def player_wonder_about(self, starting_room):
        # create a player
        player = Player(starting_room)
        # visited nodes storage
        visited = set()
        # upfront nodes storage
        s = Stack()
        # a map for back track once reach a node whose neighbors have been exhausted
        backtrack = {'s':'n','n':'s','w':'e','e':'w'}

        # as long as there are room not visited in the graph, do this:
        while len(visited) < len(self.graph):
            # find valid exit 
            exits = player.current_room.get_exits()
            # creat a branches list for current valid directions to go
            branches = []
            # go through each direction
            for D in exits:
                if (D != None) and (player.current_room.get_room_in_direction(D) not in visited):
                    branches.append(D)
            # add curr to visited 
            visited.add(player.current_room)
            
            # if there are more than 1 direction to go 
            if len(branches) > 0 :
                # generate a random number for direction to go
                rand = random.randint(0, len(branches)-1)
                direction = branches[rand]
                # push direction to stack and go there
                s.push(direction)
                player.travel(direction)
                traversal_path.append(direction)
            else:
                previous_D = s.pop() 
                # new direction for player to go back to previous room
                reverse_D = backtrack[previous_D]
                # player goes back
                player.travel(reverse_D)
                traversal_path.append(reverse_D)
        return traversal_path

x = world.starting_room
g = RoomGraph(world)
print(f"neighbors:{g.get_neigbors(x.id)}")
traversal_path = g.player_wonder_about(x)

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
# player.current_room.print_room_description(player)
# while True:
#     cmds = input("-> ").lower().split(" ")
#     if cmds[0] in ["n", "s", "e", "w"]:
#         player.travel(cmds[0], True)
#     elif cmds[0] == "q":
#         break
#     else:
#         print("I did not understand that command.")
