import random
import pygame

pygame.mixer.pre_init(44100, -16, 2, 512)


class Player():
    def __init__(self, game):
        self.game = game

        # player keys
        self.left_key = False
        self.right_key = False
        self.lshift_key = False

        # player movement
        self.is_jumping = False
        self.on_ground = False
        self.gravity = 0.35
        self.friction =  -0.15
        self.position = pygame.math.Vector2(0, 0)
        self.velocity = pygame.math.Vector2(0, 0)
        self.acceleration = pygame.math.Vector2(0, self.gravity)

        # sfx
        self.kick_sound = pygame.mixer.Sound('assets/sfx/kick.ogg')
        self.punch_sound = pygame.mixer.Sound('assets/sfx/punch.ogg')
        self.jump_sound = pygame.mixer.Sound('assets/sfx/jump.ogg')

        # animation
        self.animation_database = {}
        self.animation_images = {}
        self.load_animations()
        self.current_frame = 0
        self.flip = False
        self.state = 'idle'

        # image
        self.image = self.animation_images['idle_1']
        self.rect = self.image.get_rect()
        self.rect.h -= 4

    def draw_player(self, surface, camera):
        surface.blit(pygame.transform.flip(
            self.image, self.flip, False), (self.rect.x - camera.offset.x, self.rect.y - camera.offset.y))

    def update(self, delta_time, tiles, coins, enemies):
        self.horizontal_movement(delta_time)
        self.check_collisionsx(tiles)
        self.vertical_movement(delta_time)
        self.check_collisionsy(tiles)
        self.check_object_collisions(coins)
        self.check_enemy_collisions(enemies)
        self.animate()

    def horizontal_movement(self, delta_time):
        self.acceleration.x = 0
        acceleration_speed = .2
        if self.lshift_key:
            acceleration_speed = .4
        if self.left_key:
            self.acceleration.x -= acceleration_speed
        elif self.right_key:
            self.acceleration.x += acceleration_speed

        self.acceleration.x += self.velocity.x * self.friction
        self.velocity.x += self.acceleration.x * delta_time
        self.limit_velocity(4)
        self.position.x += self.velocity.x * delta_time + \
            (self.acceleration.x * .5) * (delta_time * delta_time)
        self.rect.x = self.position.x

    def vertical_movement(self, delta_time):
        self.velocity.y += self.acceleration.y * delta_time
        if self.velocity.y > 7:
            self.velocity.y = 7
        self.position.y += self.velocity.y * delta_time + \
            (self.acceleration.y * .5) * (delta_time * delta_time)
        self.rect.bottom = self.position.y

    def limit_velocity(self, max_velocity):
        min(-max_velocity, max(self.velocity.x, max_velocity))
        if abs(self.velocity.x) < .01:
            self.velocity.x = 0

    def jump(self):
        if self.on_ground:
            self.jump_sound.play()
            self.is_jumping = True
            self.velocity.y -= 5.5
            self.on_ground = False

    def get_hits(self, tiles):
        hits = []
        for tile in tiles:
            if self.rect.colliderect(tile):
                hits.append(tile)

        return hits

    def check_collisionsx(self, tiles):
        collisions = self.get_hits(tiles)
        for tile in collisions:
            if self.velocity.x > 0:
                self.position.x = tile.rect.left - self.rect.w
                self.rect.x = self.position.x
                # self.position.x = tile.rect.left
                # self.rect.right = self.position.x
            elif self.velocity.x < 0:
                self.position.x = tile.rect.right
                self.rect.left = self.position.x

    def check_collisionsy(self, tiles):
        self.on_ground = False
        self.rect.bottom += 1

        collisions = self.get_hits(tiles)
        for tile in collisions:
            if self.velocity.y > 0:
                self.on_ground = True
                self.is_jumping = False
                self.velocity.y = 0
                self.position.y = tile.rect.top
                self.rect.bottom = self.position.y
            elif self.velocity.y < 0:
                self.velocity.y = 0
                self.position.y = tile.rect.bottom + self.rect.h
                self.rect.bottom = self.position.y
    
    def check_object_collisions(self, tiles):
        collisions = self.get_hits(tiles)
        
        for tile in collisions:
            if tile.type == 'gold':
                tile.pickup_sound.play()
                self.game.gold += 1
                tiles.remove(tile)
    

    def check_enemy_collisions(self, tiles):
        collisions = self.get_hits(tiles)

        for tile in collisions:
            if tile.type == 'enemy':
                random.choice([self.kick_sound, self.punch_sound]).play()
                tiles.remove(tile)
                # self.game.lives -= 1


    def load_animations(self):
        self.animation_database = {
            'idle': self.create_animation_list_database('assets/player/idle', [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5]),
            'run': self.create_animation_list_database('assets/player/run', [7, 7, 7, 7, 7, 7, 7, 11]),
            'jump': self.create_animation_list_database('assets/player/jump', [5, 5, 5, 45])
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

    def change_state(self, new_state):
        if self.state != new_state:
            self.state = new_state
            self.current_frame = 0

    def animate(self):
        self.current_frame += 1

        if self.velocity.x > 0 or self.velocity.x < 0:
            self.change_state('run')
        if self.velocity.x == 0:
            self.change_state('idle')
        if self.is_jumping:
            self.change_state('jump')

        if self.current_frame >= len(self.animation_database[self.state]):
            self.current_frame = 0
        animation_id = self.animation_database[self.state][self.current_frame]
        self.image = self.animation_images[animation_id]
