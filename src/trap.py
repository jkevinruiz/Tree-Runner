import pygame


class Trap():
    def __init__(self, game, vflip, x, y):
        # init
        pygame.mixer.init(44100, -16, 2, 512)

        self.game = game
        self.type = 'trap'
        self.vflip = vflip

        # animation
        self.state = 'active'
        self.current_frame = 0
        self.animation_images = {}
        self.animation_database = {}
        self.load_animations()

        # sfx
        self.touch_sound = pygame.mixer.Sound('assets/sfx/ouch.ogg')

        # image
        self.image = self.animation_images['active_1']

        # hit box
        self.rect = self.image.get_rect()
        self.rect.w = 8
        self.rect.h = 8
        self.rect.x = x + 4
        self.rect.y = y + 10

        # if vertically flip
        if self.vflip:
            self.rect.y -= 12


    def draw(self):
        self.animate()

        if self.vflip:
            self.game.canvas.blit(
                pygame.transform.flip(self.image, False, self.vflip), (self.rect.x - self.game.camera.offset.x - 3, self.rect.y - self.game.camera.offset.y))
        else:
            self.game.canvas.blit(self.image, (self.rect.x - self.game.camera.offset.x - 4, self.rect.y - self.game.camera.offset.y - 5))

    def load_animations(self):
        self.animation_database = {
            'active': self.create_animation_list_database('assets/trap/active', [30, 10, 10, 30, 10, 10])
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
