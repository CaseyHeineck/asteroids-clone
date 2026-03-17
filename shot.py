from circleshape import *
from constants import *
from logger import log_event

class Shot(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)

    def hits(self, asteroid, HUD):
        log_event("asteroid_shot")
        HUD.update_score(BASE_SCORE * (asteroid.radius / ASTEROID_MIN_RADIUS))                    
        asteroid.split()
        self.kill()

    def draw(self, screen):
        pygame.draw.circle(screen, "white", self.position, self.radius, LINE_WIDTH)

    def update(self, dt):
        self.position += self.velocity * dt