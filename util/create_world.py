from django.contrib.auth.models import User
from adventure.models import Player, Room
from random import choice
from collections import deque
Room.objects.all().delete()
class World:
    def __init__(self, nx, ny):
        self.width = nx
        self.height = ny
        self.grid = [[None for y in range(ny)] for x in range(nx)]
    def __str__(self):
        '''
        Print the rooms in room_grid in ascii characters.
        '''
        # Add top border
        str = "# " * ((3 + self.width * 5) // 2) + "\n"
        # The console prints top to bottom but our array is arranged
        # bottom to top.
        #
        # We reverse it so it draws in the right direction.
        reverse_grid = list(self.grid)  # make a copy of the list
        reverse_grid.reverse()
        for row in reverse_grid:
            # PRINT NORTH CONNECTION ROW
            str += "#"
            for room in row:
                if room is not None and room.n_to is not None:
                    str += "  |  "
                else:
                    str += "     "
            str += "#\n"
            # PRINT ROOM ROW
            str += "#"
            for room in row:
                if room is not None and room.w_to is not None:
                    str += "-"
                else:
                    str += " "
                if room is not None:
                    str += f"{room.id}".zfill(3)
                else:
                    str += "   "
                if room is not None and room.e_to is not None:
                    str += "-"
                else:
                    str += " "
            str += "#\n"
            # PRINT SOUTH CONNECTION ROW
            str += "#"
            for room in row:
                if room is not None and room.s_to is not None:
                    str += "  |  "
                else:
                    str += "     "
            str += "#\n"
        # Add bottom border
        str += "# " * ((3 + self.width * 5) // 2) + "\n"
        return str
    def room_at(self, x, y):
        return self.grid[x][y]
    def find_valid_neighbours(self, room):
        """Returns a list of unvisited neighbours"""
        delta = [('n', (0, -1)), ('s', (0, 1)), ('w', (-1, 0)), ('e', (1, 0))]
        neighbours = []
        for direction, (dx, dy) in delta:
            x2, y2 = room.x + dx, room.y + dy
            if (0 <= x2 < self.width) and (0 <= y2 < self.height):
                neighbour = self.room_at(x2, y2)
                if neighbour.is_disconnected():
                    neighbours.append((direction, neighbour))
        return neighbours
    def make_world(self):
        """ Creates a world based on initial parameters using dfs algorithm """
        # Total num of rooms
        for xi in range(self.width):
            for yj in range(self.height):
                newRoom = Room(x=xi, y=yj)
                newRoom.save()
                self.grid[xi][yj] = newRoom
        # Stack for depth first search
        current_room = self.room_at(self.width//2, self.height//2)
        room_stack = deque([current_room])
        while len(room_stack):
            print(len(room_stack))
            neighbours = self.find_valid_neighbours(current_room)
            if len(neighbours):
                print(neighbours)
              # if there are valid neighbours, choose a random one, connect them, 
                direction, next_room = choice(neighbours)
                current_room.connectRooms(next_room, direction)
                room_stack.append(current_room)
                current_room = next_room
            else:
                # Reached a dead end, go back
                current_room = room_stack.pop()

w = World(25, 25)
w.make_world()
players = Player.objects.all()
for p in players:
    p.currentRoom = w.room_at(0, 0).id
    p.save()
