import pygame
from circleshape import CircleShape
from constants import *

class Explosion(CircleShape):
    def __init__(
        self,
        x,
        y,
        radius=EXPLOSION_RADIUS,
        color=EXPLOSION_COLOR,
        duration=EXPLOSION_DURATION,
        max_alpha=EXPLOSION_MAX_ALPHA,
        line_width=0
    ):
        super().__init__(x, y, radius)
        self.color = color
        self.duration = duration
        self.timer = duration
        self.max_alpha = max_alpha
        self.line_width = line_width

    def update(self, dt):
        self.timer -= dt
        if self.timer <= 0:
            self.kill()

    def draw(self, screen):
        if self.duration <= 0:
            return

        alpha_ratio = max(0, self.timer / self.duration)
        alpha = int(self.max_alpha * alpha_ratio)

        surface_size = self.radius * 2
        effect_surface = pygame.Surface((surface_size, surface_size), pygame.SRCALPHA)

        pygame.draw.circle(
            effect_surface,
            (*self.color, alpha),
            (self.radius, self.radius),
            self.radius,
            self.line_width
        )

        rect = effect_surface.get_rect(center=(self.position.x, self.position.y))
        screen.blit(effect_surface, rect)