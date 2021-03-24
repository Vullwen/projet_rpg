import pygame, sys, os, random, time
pygame.init()
pygame.mixer.set_num_channels(64) #je choisi le nombre de channels audio, le nombre de sons qui peuvent etres jouée en meme temps
pygame.mixer.pre_init(44100, -16, 2, 512) #j'initialyse tous les sons sinon il y a un décalage audio

music_playing = True #me sert à savoir  si la music est en train d'etre jouée
grass_sounds = [pygame.mixer.Sound('Data/Sound/grass_0.wav'),pygame.mixer.Sound('Data/Sound/grass_1.wav')] #j'ai deux sons d'herbes donc je met le tous dans la variable
grass_sounds[0].set_volume(0.2) #je réduis leur volume (1 = normal; <1 = plus fort; >1 = moins fort)
grass_sounds[1].set_volume(0.2)
pygame.mixer.music.load('Data/Sound/music.wav') #"j'initialise" la musique de fond
pygame.mixer.music.play(-1) #je la joue
grass_sound_timer = 0 #un timer pour savoir au bout de combien de ticks un son d'herbe se jouera
