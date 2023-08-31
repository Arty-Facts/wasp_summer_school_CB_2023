# Stations
# CHARGE1, CHARGE2, CONVEYOR_HEAVY, CONVEYOR_LIGHT, DELIVERY.

change_station1 = "CHARGE1"
change_station2 = "CHARGE2"
conveyor_station_heavy = "CONVEYOR_HEAVY"
conveyor_station_light = "CONVEYOR_LIGHT"
delivery_station = "DELIVERY"

carry_type_light = "light"
carry_type_heavy = "heavy"

# Action nodes
# ‘idle!’
# Does nothing. Always returns RUNNING.

# ‘charge!’
# If the robot is at any of the charging stations it will charge, adding 10 to the current battery level and returning RUNNING. If it’s not at a charging station it will return FAILURE. IF battery is fully charged it returns SUCCESS.

# ‘pick!’
# If the robot is at any of the conveyors, and there is an object there that the robot can carry without exceeding the weight limit it will pick it up and return RUNNING, otherwise returns FAILURE. Only picks one object per time step.

# ‘place!’
# If the robot is at the delivery table it will place all objects on the delivery table and return RUNNING, otherwise returns FAILURE. Places all currently held objects in one time step. Returns RUNNING regardless of whether any objects are actually carried and then placed.

# ‘move to <STATION>!’
# Move towards the given station with a maximum speed of 5. Only moves in either x or y direction any given time step. A movement of 1 in x and 1 in y will therefore take 2 timesteps even if total distance is less than 5. <STATION> can be any of the following five: CHARGE1, CHARGE2, CONVEYOR_HEAVY, CONVEYOR_LIGHT, DELIVERY. If the robot is already at the station it will return SUCCESS, otherwise it will return RUNNING.

pick = "pick!"
place = "place!"
charge = "charge!"
idle = "idle!"

def move_to(target):
    return f"move to {target}!",


# Condition nodes
# ‘at station <STATION>?’
# Checks if robot is currently at <STATION>. <STATION> can be any of the following five: CHARGE1, CHARGE2, CONVEYOR_HEAVY, CONVEYOR_LIGHT, DELIVERY.

# Returns SUCCESS if robot is at the station, FAILURE otherwise.

# ‘battery level <value>?’
# Checks if battery level is currently above or below the given value. Example ‘battery level > 4’ returns SUCCESS if battery level is above 4, FAILURE otherwise while ‘battery level < 4’ returns SUCCESS if battery level is below 4, FAILURE otherwise.

# ‘carried weight <value>?’
# Checks if the robots currently carried weight is above or below the given value. Works like the battery level behavior.

# ‘carried light <value>?’
# Checks if the number of currently carried light objects is above or below the given value. Works like the battery level behavior.

# ‘carried heavy <value>?’
# Checks if the number currently carried heavy objects is above or below the given value. Works like the battery level behavior.

# ‘conveyor light <value>?’
# Checks if the number of objects currently on the light conveyor is above or below the given value. Works like the battery level behavior.

# ‘conveyor heavy <value>?’
# Checks if the number of objects currently on the heavy conveyor is above or below the given value. Works like the battery level behavior.

def at_station(station):
    return f"at station {station}?",

def battery_level(condition, value):
    return f"battery level {condition} {value}?",

def battery_level_above(value):
    return f"battery level > {value}?",

def battery_level_below(value):
    return f"battery level < {value}?",



def carried_weight(condition, value):
    return f"carried weight {condition} {value}?",

def carried_weight_above(value):
    return f"carried weight > {value}?",

def carried_weight_below(value):
    return f"carried weight < {value}?",



def carried_light(condition, value):
    return f"carried light {condition} {value}?",

def carried_heavy(condition, value):
    return f"carried heavy {condition} {value}?",

def carried_above(carry_type, value):
    if carry_type == carry_type_light:
        return f"carried light > {value}?",
    elif carry_type == carry_type_heavy:
        return f"carried heavy > {value}?",
    else:
        raise ValueError(f"Unknown carry type: {carry_type}")

def carried_below(carry_type, value):
    if carry_type == carry_type_light:
        return f"carried light < {value}?",
    elif carry_type == carry_type_heavy:
        return f"carried heavy < {value}?",
    else:
        raise ValueError(f"Unknown carry type: {carry_type}")


def conveyor_light(condition, value):
    return f"conveyor light {condition} {value}?",

def conveyor_heavy(condition, value):
    return f"conveyor heavy {condition} {value}?",

def conveyor_above(conveyor_station, value):
    if conveyor_station == conveyor_station_light:
        return f"conveyor light > {value}?",
    elif conveyor_station == conveyor_station_heavy:
        return f"conveyor heavy > {value}?",
    else:
        raise ValueError(f"Unknown conveyor station: {conveyor_station}")

def conveyor_below(conveyer_station, value):
    if conveyer_station == conveyor_station_light:
        return f"conveyor light < {value}?",
    elif conveyer_station == conveyor_station_heavy:
        return f"conveyor heavy < {value}?",
    else:
        raise ValueError(f"Unknown conveyor station: {conveyer_station}")
    


# Available behaviors
# Only a specified set of behaviors can be used as listed below.

# Control nodes
# ‘f(’
# Fallback node without memory. All subsequent nodes up to an ending ‘)’ are part of the subtree.

# ‘fm(’
# Fallback node with memory. All subsequent nodes up to an ending ‘)’ are part of the subtree.

# ‘s(’
# Sequence node without memory. All subsequent nodes up to an ending ‘)’ are part of the subtree.

# ‘sm(’
# Sequence node with memory. All subsequent nodes up to an ending ‘)’ are part of the subtree.


def f(*args):
    return ["f(", *args, ")"]

def fm(*args):
    return ["fm(", *args, ")"]

def s(*args):
    return ["s(", *args, ")"]

def sm(*args):
    return ["sm(", *args, ")"]

def p(*args):
    return ["p(", *args, ")"]



# modules nodes

def other_station(station):
    if station == conveyor_station_heavy:
        return conveyor_station_light
    elif station == conveyor_station_light:
        return conveyor_station_heavy
    else:
        raise ValueError(f"Unknown station: {station}")


def deliver_box(carrying_above=3):
    return f(
        *carried_weight_below(carrying_above),
        # *s(
            # *at_station(delivery_station),
            place,
        # ),
        # *at_station(delivery_station),
        *move_to(delivery_station),

    )

def pick_best_conveyor(items_h=1, items_l=1):
    return f(
        *s(

            *conveyor_above(conveyor_station_heavy, items_h),
            *move_to(conveyor_station_heavy),
            pick,
        ),
        *s(
            *conveyor_above(conveyor_station_light, items_l),
            *move_to(conveyor_station_light),
            pick,
        ),

    )

def get_box(conveyor_station, items=1):
    return s( 
        *conveyor_above(conveyor_station, items),
        *move_to(conveyor_station),
        pick,

    )

def battery_level(min_bat=10, max_bat=90, charge_station=change_station2):
    return f(
        # *s(
        #     *at_station(charge_station),
        #     *battery_level_below(max_bat),
        #     charge,
        # ),
        charge,
        *battery_level_above(min_bat),
        # *at_station(delivery_station),
        *move_to(charge_station),       

    )
