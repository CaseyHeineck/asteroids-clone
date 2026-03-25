from circleshape import *
from constants import *
from logger import log_event

class Shot(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)

    def hits(self, asteroid, HUD):
        log_event("asteroid_shot")                    
        asteroid.split(SHOT_DAMAGE, HUD)
        self.kill()

    def draw(self, screen):
        pygame.draw.circle(screen, MAGENTA, self.position, self.radius)

    def update(self, dt):
        self.position += self.velocity * dt