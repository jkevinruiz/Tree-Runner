import pygame

class Skeleton():
    def __init__(self, game, x, y):
        self.game = game
        # self.groups = self.game.enemies
        self.animation_database = {}
        self.animation_images = {}
        self.load_animations()
        self.state = 'idle' 
        self.type = 'enemy'
        self.current_frame = 0
        self.image = self.animation_images['idle_1']
        self.rect = self.image.get_rect()
        # self.rect.w = 16
        # self.rect.h = 16
        self.rect.x = x
        self.rect.y = y
    
    def draw_skeleton(self):
        self.animate()
        self.game.canvas.blit(
            pygame.transform.scale(self.image, (self.rect.w, self.rect.h)), (self.rect.x - self.game.camera.offset.x, self.rect.y - self.game.camera.offset.y- self.rect.h / 2)
        )
    
    def load_animations(self):
        self.animation_database = {
            'idle': self.create_animation_list_database('assets/skeleton/idle', [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 10]),
            'walk': self.create_animation_list_database('assets/skeleton/walk', [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 12])
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
