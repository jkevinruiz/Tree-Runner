import pygame


class Coin():
    def __init__(self, game, x, y):
        # init
        pygame.mixer.pre_init(44100, -16, 2, 512)

        self.game = game
        self.type = 'gold'

        # animation
        self.state = 'spin'
        self.current_frame = 0
        self.animation_images = {}
        self.animation_database = {}
        self.load_animations()

        # sfx
        self.loot_sound = pygame.mixer.Sound('assets/sfx/loot_coin.ogg')
        self.loot_sound.set_volume(0.2)

        self.image = self.animation_images['gold_1']
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

    def draw(self):
        self.animate()
        self.game.canvas.blit(
            self.image, (self.rect.x - self.game.camera.offset.x, self.rect.y - self.game.camera.offset.y))

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
