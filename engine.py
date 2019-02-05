import players
import map

class Engine(object):

    def __init__(self, scene_map):
        self.scene_map = scene_map

    def play(self):
        current_scene = self.scene_map.opening_scene()
        last_scene = self.scene_map.next_scene('finished')

        while current_scene != last_scene:
            next_scene_name = current_scene.enter(self.scene_map.player)
            current_scene = self.scene_map.next_scene(next_scene_name)

map1 = map.Map('slime room')
engine1 = Engine(map1)
engine1.play()