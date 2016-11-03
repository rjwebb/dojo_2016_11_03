from adventurelib import *
import random
import time

Room.items = Bag()


Room.start_time = None
Room.time_until = None


hallway = starting_room = Room("""
You are in the hallway. The Headmaster's office is to the north. The Science room is to the East. The Maths room is to the West. The school exit is South
""")


maths = starting_room.west = Room("""
You are in the Maths room. There is a blackboard on the West wall. Exit to the East.
""")

science = starting_room.east = Room("""
You are in the science room. There is a strange smell of burning and a smouldering hole in the ceiling. Exit to the West.
""")

headteachers_room = starting_room.north = Room("""
You are in the headmaster's office. You see books lining the walls. There is a smell of old leather and adolescent fear. Exit to the South
""")

yard = starting_room.south = Room("""
You are in the yard. The school entrance is in to the North
""")

current_room = hallway

def missed_class():
    current_room = headteachers_room


@when('look')
def look():
    say(current_room)
    if current_room == hallway:
        if maths.start_time is None:
            maths.start_time = time.time()
            maths.time_until = random.randint(5, 25)

        t = how_long_until(maths)
        if t > 0:
            say('It is {} seconds until maths class!'
                .format(int(t)))
        else:
            say('You are {} seconds late to maths class!'
                .format(int(-t)))

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
        if room == maths:
            t = how_long_until(maths)
            if t > 0:
                say('You have arrived on time to maths class!')
                say('You go %s.' % direction)
                current_room = room
            else:
                say('You are {} seconds late to maths class!'
                    .format(int(-t)))
                missed_class()
            look()


look()
start()
