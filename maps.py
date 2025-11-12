from pico2d import load_image

class Map:
    image = None
    def __init__(self):
        if Map.image == None:
            Map.image = load_image('./map_sprite/final_boss_room_0027_boss_floor_core.png')
        self.x1, self.x2,self.x3,self.x4,self.x5, self.y = 0,400,800,1200,1600,100
    def draw(self):

        Map.image.clip_composite_draw(0,0,632,86,0, '', self.x1, self.y, 400, 100)
        Map.image.clip_composite_draw(0, 0, 632, 86, 0, '', self.x2, self.y, 400, 100)
        Map.image.clip_composite_draw(0, 0, 632, 86, 0, '', self.x3, self.y, 400, 100)
        Map.image.clip_composite_draw(0, 0, 632, 86, 0, '', self.x4, self.y, 400, 100)
        Map.image.clip_composite_draw(0, 0, 632, 86, 0, '', self.x5, self.y, 400, 100)
    def update(self):
        pass
    def get_bb(self):
        return 0, 0, 1600, 186
    def handle_collision(self, group, other):
        pass
