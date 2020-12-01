import pygame
class Coin():
    def __init__(self, game, x, y):
        self.animation_database = {}
        self.animation_images = {}
        self.load_animations()
        self.state = 'spin'
        self.type = 'gold'
        self.current_frame = 0
        self.game = game
        self.image = self.animation_images['gold_1']
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def draw_coin(self):
        self.animate()
        self.game.canvas.blit(
            self.image, (self.rect.x - self.game.camera.offset.x, self.rect.y - self.game.camera.offset.y))
        # self.game.canvas.blit(self.image, (self.rect.x , self.rect.y))


    def load_animations(self):
        self.animation_database = {
            'spin': self.create_animation_list_database('assets/coin/gold', [10, 10, 10, 10])
        }


    def create_animation_list_database(self, path, frame_durations):
        name = path.split('/')[-1]
        animation_frame_data = []
        n = 1
        for frame in frame_durations:
            animation_frame_id = f'{name}_{str(n)}'
            image_location = f'{path}/{animation_frame_id}.png'
            animation_image = pygame.image.load(image_location)
            # animation_image.set_colorkey((0, 0, 0))
            self.animation_images[animation_frame_id] = animation_image.copy()
            for i in range(frame):
                animation_frame_data.append(animation_frame_id)
            n += 1

        return animation_frame_data

    
    def animate(self):
        self.current_frame += 1

        if self.current_frame >= len(self.animation_database[self.state]):
            self.current_frame = 0
        animation_id = self.animation_database[self.state][self.current_frame]
        self.image = self.animation_images[animation_id]


    def collect(self):
        #TODO: update gold coin count
        #TODO: remove from sprite list
        pass

