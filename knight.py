from pico2d import *

animation_names = ['Dash To Idle', 'Dash', 'DownSlash', 'DownSlashEffect', 'Fall','Idle Hurt', 'Idle', 'Slash', 'SlashAlt','SlashEffect','SlashEffectAlt','UpSlash','UpSlashEffect','Walk']
animation_frames = [3,11,14,5,5,11,8,14,14,5,5,14,5,6]
class Knight:
    image = None
    def __init__(self):
        self.load_sprite()
    def load_sprite(self):
        if Knight.image is None:
            Knight.image = {}
            for name, frames in zip(animation_names, animation_frames):
                clean_name = name.strip()
                Knight.image[clean_name] = []
                for i in range(frames):
                    filename = f"./knight_sprite/{clean_name}_{i:03d}.png"
                    try:
                        img = load_image(filename)
                    except Exception:
                        print(f"Missing file: `{filename}`")
                        img = None
                    Knight.image[clean_name].append(img)
    def draw(self):
        self.image['Idle'][0].draw(400, 300)
    def update(self):
        pass


open_canvas(800, 600)

k = Knight()
while True:

    k.draw()
    update_canvas()



