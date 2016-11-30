import sys
import math

# Grab Snaffles and try to throw them through the opponent's goal!
# Move towards a Snaffle and use your team id to determine where you need to throw it.

my_team_id = int(input())  # if 0 you need to score on the right of the map, if 1 you need to score on the left

LEFT_GOAL_CENTER = (0, 3750)
RIGHT_GOAL_CENTER = (16000, 3750)
OPPONENT_GOAL_CENTER = RIGHT_GOAL_CENTER if my_team_id == 0 else LEFT_GOAL_CENTER
MY_GOAL_CENTER = RIGHT_GOAL_CENTER if my_team_id == 1 else LEFT_GOAL_CENTER

class GameObject():
    def __init__(self, id, object_type, x, y, vx, vy):
        self.id = id
        self.object_type = object_type
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.distances = {}

    def calculate_distance(self, game_object):
        return math.sqrt((self.x - game_object.x)**2 + (self.y - game_object.y)**2)

    def discover(self, game_objects):
        for game_object in game_objects:
            if game_object.id != self.id:
                if not game_object.object_type in self.distances:
                    self.distances[game_object.object_type] = []
                self.distances[game_object.object_type].append({'id': game_object.id, 'distance': self.calculate_distance(game_object)})

        for object_type in self.distances:
            self.distances[object_type] = sorted(self.distances[object_type], key=lambda x: x['distance'])

    def get_nearest_object(self, object_type):
        return self.distances[object_type][0]
            

class Wizard(GameObject):
    def __init__(self, id, x, y, vx, vy, state):
        super().__init__(id, 'WIZARD', x, y, vx, vy)
        self.state = state

    def move(self, x, y, thrust):
        print('MOVE {} {} {}'.format(x, y, thrust))

    def rush(self, x, y):
        self.move(x, y, 150)

    def throw(self, x, y, power):
        print('THROW {} {} {}'.format(x, y, power))

    def full_power_throw(self, x, y):
        self.throw(x, y, 500)

    def get_nearest_untargetted_snaffle(self):
        return get_object_by_params(snaffles, {'id': wizard.get_nearest_object('SNAFFLE')['id'], 'targetted': False})



class OppWizard(GameObject):
    def __init__(self, id, x, y, vx, vy, state):
        super().__init__(id, 'OPPONENT_WIZARD', x, y, vx, vy)
        self.state = state


class Snaffle(GameObject):
    def __init__(self, id, x, y, vx, vy):
        super().__init__(id, 'SNAFFLE', x, y, vx, vy)
        self.targetted = False

def get_object_by_params(collection, params):
    results = []
    for item in collection:
        for param in params.items():
            if item.__getattribute__(param[0]) != param[1]:
                break
            results.append(item)
    return results

def log(string):
    print(string, file=sys.stderr)

# game loop
while True:
    entities = int(input())  # number of entities still in game
    wizards = []
    opp_wizards = []
    snaffles = []
    for i in range(entities):
        # entity_id: entity identifier
        # entity_type: "WIZARD", "OPPONENT_WIZARD" or "SNAFFLE" (or "BLUDGER" after first league)
        # x: position
        # y: position
        # vx: velocity
        # vy: velocity
        # state: 1 if the wizard is holding a Snaffle, 0 otherwise
        entity_id, entity_type, x, y, vx, vy, state = input().split()
        if entity_type == 'WIZARD':
            wizard = Wizard(int(entity_id), int(x), int(y), int(vx), int(vy), int(state))
            wizards.append(wizard)
        elif entity_type == 'OPPONENT_WIZARD':
            opp_wizard = OppWizard(int(entity_id), int(x), int(y), int(vx), int(vy), int(state))
            opp_wizards.append(opp_wizard)
        elif entity_type == 'SNAFFLE':
            snaffle = Snaffle(int(entity_id), int(x), int(y), int(vx), int(vy))
            snaffles.append(snaffle)

    for game_object in (wizards + opp_wizards + snaffles):
        game_object.discover(wizards + opp_wizards + snaffles)
        
    for wizard in wizards:

        # Write an action using print
        # To debug: print("Debug messages...", file=sys.stderr)
        
        # Edit this line to indicate the action for each wizard (0 <= thrust <= 150, 0 <= power <= 500)
        # i.e.: "MOVE x y thrust" or "THROW x y power"
        if wizard.state == 0:
            nearest_snaffle = wizard.get_nearest_untargetted_snaffle()
            nearest_snaffle.targetted = True
            wizard.rush(nearest_snaffle.x, nearest_snaffle.y)
        else:
            wizard.full_power_throw(OPPONENT_GOAL_CENTER)


        
