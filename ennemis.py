import pygame, sys, os, random,time, math

pygame.init()

class Mob(pygame.sprite.Sprite):
    def __init__(self):
        self.image = pygame.image.load("Data/images/ennemis.PNG")
        self.life = 20
        self.movement = [0,0]
        self.collision = {'top':False,'bottom':False,'right':False,'left':False}
        self.range = 80
        self.degats = 10

    def create_mob(self, x, y, game_map):
        self.mob_rect = pygame.Rect(x,y,16,16)
        y = 0
        for layer in game_map:
            x = 0
            for tile in layer:
                if tile == 'e':
                    return (x*16, y*16)
                x += 1
            y += 1

    def move_to_player(self, player_rect):
        if math.sqrt(((player_rect.x-self.mob_rect.x)**2)+((player_rect.y-self.mob_rect.y)**2)) < self.range:
            if player_rect.x < self.mob_rect.x:
                self.movement[0] -= 1
            if player_rect.x > self.mob_rect.x:
                self.movement[0] += 1
            if player_rect.y < self.mob_rect.y:
                self.movement[1] -= 1
            if player_rect.y > self.mob_rect.y:
                self.movement[1] += 1

    def test_hit_player(self, player_rect):
        if self.mob_rect.colliderect(player_rect):
            return True

    def collision_test(self,tiles):
        collisions = []
        for tile in tiles:
            if self.mob_rect.colliderect(tile):
                collisions.append(tile)
        return collisions

    def move(self,movement,tiles):
        self.collision = {'top':False,'bottom':False,'right':False,'left':False}
        self.mob_rect.x += movement[0]
        collisions = self.collision_test(tiles)
        for tile in collisions:
            if movement[0] > 0:
                self.mob_rect.right = tile.left
            if movement[0] < 0:
                self.mob_rect.left = tile.right
        self.mob_rect.y += movement[1]
        collisions = self.collision_test(tiles)
        for tile in collisions:
            if movement[1] > 0:
                self.mob_rect.bottom = tile.top
            if movement[1] < 0:
                self.mob_rect.top = tile.bottom
        return self.mob_rect, self.collision
