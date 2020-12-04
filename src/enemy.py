import pygame


class Skeleton():
    def __init__(self, game, x, y):
        self.game = game

        # animation
        self.flip = False
        self.type = 'enemy'
        self.state = 'walk'
        self.current_frame = 0
        self.animation_database = {}
        self.animation_images = {}
        self.load_animations()

        # image
        self.image = self.animation_images['idle_1']

        # position
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

        # movement
        self.velocity = 1
        self.path = [x, x + 50]

    def draw_skeleton(self):
        self.animate()
        self.move()
        self.game.canvas.blit(
            pygame.transform.scale(pygame.transform.flip(self.image, self.flip, False), (self.rect.w, self.rect.h)), (
                self.rect.x - self.game.camera.offset.x, self.rect.y - self.game.camera.offset.y - self.rect.h / 2)
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

            animation_image = pygame.image.load(image_location).convert()
            animation_image.set_colorkey((0, 0, 0))

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

    def move(self):
        if self.state != 'idle':
            if self.velocity > 0:
                self.flip = False
                if self.rect.x + self.velocity < self.path[1]:
                    self.rect.x += self.velocity
                else:
                    self.velocity *= -1
            else:
                self.flip = True
                if self.rect.x - self.velocity > self.path[0]:
                    self.rect.x += self.velocity
                else:
                    self.velocity *= -1
