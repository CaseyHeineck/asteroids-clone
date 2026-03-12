import pygame
from main import *
from constants import *
from logger import *

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
score = 0

def update_score(amount):
    global score
    score += amount

def show_score(x, y):
    font = pygame.font.SysFont("comicsans", 30, True)
    score_text = font.render("Score: " + str(score), True, "white")
    screen.blit(score_text, (x, y))


    