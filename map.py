from sys import exit

map_idea = """
    (0, 0)      (0, 1)      (0, 2)
    _________________________________
    |          |          |          |
    |          |          |          |
    |          |          |          |
    |__________|__________|__________|
    |          |          |          |
    |          |          |          |
    |          |          |          |
    |__________|__________|__________|
    (1, 0)      (1, 1)      (1, 2)
"""


class Map(object):

    scenes = {
        'death' : 'death',
        'floor1' : {
            (0, 0) : None, (0, 1) : None, (0, 2) : None,
            (1, 0) : None, (1, 1) : None, (1, 2) : None
        },
        'floor2' : {

        }
        

    }

    def __init__(self, start_scene):
        self.start_scene = start_scene

    def next_scene(self, scene_name):
        return Map.scenes.get(scene_name)
    
    def opening_scene(self):
        return self.next_scene(self.start_scene)

class Scene(object):

    def __init__(self):
        pass
    
    def enter(self):
        pass

class Death(Scene):

    def __init__(self):
        super(Death, self).__init__()

    def enter(self):
        print("You have died.")
        exit(0)

    