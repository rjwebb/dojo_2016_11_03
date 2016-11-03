from adventurelib import *
import random
import time

inventory = Bag()


Room.start_time = None
Room.time_until = None
Room.name = ''


hallway = Room("""
You are in the hallway. The Headmaster's office is to the north. The Science room is to the East. The Maths room is to the West. The school exit is South
""")


math = Room("""
You are in the Maths room with Mr Tangent. There is a blackboard on the West wall. Exit to the East.
""")
math.name = 'Maths'

science = Room("""
You are in the science room with Miss Chaganti. There is a strange smell of burning and a smouldering hole in the ceiling. Exit to the West.
""")
science.name = 'Science'

headteachers_room = Room("""
You are in the headmaster's office. You see books lining the walls. There is a smell of old leather and adolescent fear. Exit to the South
""")

yard = Room("""
You are in the yard. The school entrance is to the North.
""")

hallway.west = math
hallway.east = science
hallway.north = headteachers_room
hallway.south = yard

science.west = hallway
math.east = hallway
headteachers_room.south = hallway
yard.north = hallway

current_room = hallway
starting_room = hallway

def missed_class():
    current_room = headteachers_room

classrooms = [math, science]

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

def reset_times():
    for room in classrooms:
        room.start_time = None
        room.time_until = None


@when('read WHAT')
def read(what):
    if current_room == math:
        if what == 'blackboard':
            say('What is 7 times 6?')
    elif current_room == science:
        if what == 'whiteboard':
            say('What came first, the chicken or the egg?')

@when('write SOMETHING')
def write(something):
    say('You wrote %s' % something)
    if current_room == math:
        if something == '42':
            say('Something sparkly drops into your schoolbag.')
            inventory.add(Item('Gold star'))
        else:
            say('Anguish fills your bag and you bring shame upon yourself and your family.')
            inventory.add(Item('Lines'))
    elif current_room == science:
        if something.lower() == 'egg':
            say('Something sparkly drops into your schoolbag.')
            inventory.add(Item('Gold star'))
        else:
            say('Anguish fills your bag and you bring shame upon yourself and your family.')
            inventory.add(Item('Lines'))

@when('inventory')
def look_inventory():
    say('These things are in your inventory')
    for thing in inventory:
        say(thing)
        
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
            reset_times()
        else:
            current_room = room
        look()


look()
start()
