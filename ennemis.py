import pygame

pygame.init()

class Mob(pygame.sprite.Sprite):
    def __init__(self, x, y):
        self.x = x*16
        self.y = y*16
        self.image = pygame.image.load("Data/images/ennemis.PNG")
        self.rect =  pygame.Rect(self.x,self.y,16,16)

    def move_to_player(self, player_rect):
        if player_rect.x < self.rect.x:
            self.rect.x -= 1
        if player_rect.x > self.rect.x:
            self.rect.x += 1
        if player_rect.y < self.rect.y:
            self.rect.y -= 1
        if player_rect.y > self.rect.y:
            self.rect.y += 1

    def test_hit_player(self, player_rect):
        if self.rect.colliderect(player_rect):
            return True
