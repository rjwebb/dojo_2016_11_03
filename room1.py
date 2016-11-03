from adventurelib import *
import random
import time

Room.items = Bag()


Room.start_time = None
Room.time_until = None
Room.name = ''


hallway = Room("""
You are in the hallway. The Headmaster's office is to the north. The Science room is to the East. The Maths room is to the West. The school exit is South
""")


maths = Room("""
You are in the Maths room. There is a blackboard on the West wall. Exit to the East.
""")
maths.name = 'Maths'

science = Room("""
You are in the science room. There is a strange smell of burning and a smouldering hole in the ceiling. Exit to the West.
""")
science.name = 'Science'

headteachers_room = Room("""
You are in the headmaster's office. You see books lining the walls. There is a smell of old leather and adolescent fear. Exit to the South
""")

yard = Room("""
You are in the yard. The school entrance is to the North.
""")

hallway.west = maths
hallway.east = science
hallway.north = headteachers_room
hallway.south = yard

science.west = hallway
maths.east = hallway
headteachers_room.south = hallway
yard.north = hallway

current_room = hallway
starting_room = hallway

def missed_class():
    current_room = headteachers_room

classrooms = [maths, science]

@when('look')
def look():
    say(current_room)
    if current_room == hallway:
        for room in classrooms:
            if room.start_time is None:
                room.start_time = time.time()
                room.time_until = random.randint(5, 25)

            t = how_long_until(room)
            if t > 0:
                say('It is {} seconds until {} class!'
                    .format(int(t), room.name))
            else:
                say('You are {} seconds late to {} class!'
                    .format(int(-t), room.name))

def how_long_until(room):
    timediff = time.time() - room.start_time
    return room.time_until - timediff
            

@when('north', direction='north')
@when('south', direction='south')
@when('east', direction='east')
@when('west', direction='west')
def go(direction):
    global current_room
    room = current_room.exit(direction)
    if room:
        if room in classrooms:
            t = how_long_until(room)
            if t > 0:
                say('You have arrived on time to {} class!'
                    .format(room.name))
                say('You go %s.' % direction)
                current_room = room
            else:
                say('You are {} seconds late to {} class!'
                    .format(int(-t), room.name))
                missed_class()
        else:
            current_room = room
        look()


look()
start()
