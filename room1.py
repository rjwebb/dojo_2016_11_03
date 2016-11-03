from adventurelib import *
import random
import time


Room.start_time = None
Room.time_until = None



hallway = starting_room = Room("""
You are in the hallway.
""")

maths = starting_room.west = Room("""
You are in the maths room.
""")

headteachers_room = Room("""
You are in detention! This is the headteacher's room.
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

        timediff = time.time() - maths.start_time
        if timediff < maths.time_until:
            say('It is {} seconds until maths class!'
                .format(maths.time_until - timediff))
        else:
            say('You are {} seconds late to maths class!'
                .format(timediff - maths.time_until))


@when('north', direction='north')
@when('south', direction='south')
@when('east', direction='east')
@when('west', direction='west')
def go(direction):
    global current_room
    room = current_room.exit(direction)
    if room:
        if room == maths:
            timediff = time.time() - maths.start_time
            if timediff < maths.time_until:
                say('You have arrived on time to maths class!')
                say('You go %s.' % direction)
                current_room = room
            else:
                say('You are {} seconds late to maths class!'
                    .format(timediff - maths.time_until))
                missed_class()
            look()
        
    
look()
start()
