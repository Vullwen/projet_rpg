import pygame

pygame.init()

class Mob(pygame.sprite.Sprite):
    def __init__(self, x, y):
        self.x = x*16
        self.y = y*16
        self.image = pygame.image.load("Data/images/ennemis.PNG")
        self.rect =  pygame.Rect(self.x,self.y,16,16)

    def move_to_player(self, player_rect,tile):
        if player_rect.x < self.rect.x:
            self.rect = move(movement,tile)
        if player_rect.x > self.rect.x:
            self.rect.x += 1
        if player_rect.y < self.rect.y:
            self.rect.y -= 1
        if player_rect.y > self.rect.y:
            self.rect.y += 1

    def test_hit_player(self, player_rect):
        if self.rect.colliderect(player_rect):
            return True

    def collision_test(self,tiles):
        collisions = []
        for tile in tiles:
            if self.rect.colliderect(tile):
                collisions.append(tile)
        return collisions

    def move(self,movement,tiles):
        rect.x += movement[0]
        collisions = collision_test(self.rect,tiles)
        for tile in collisions:
            if movement[0] > 0:
                self.rect.right = tile.left
            if movement[0] < 0:
                self.rect.left = tile.right
        rect.y += movement[1]
        collisions = collision_test(self.rect,tiles)
        for tile in collisions:
            if movement[1] > 0:
                self.rect.bottom = tile.top
            if movement[1] < 0:
                self.rect.top = tile.bottom
        return self.rect
