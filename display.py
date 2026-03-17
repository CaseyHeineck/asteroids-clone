import pygame

class Display:
    def __init__(self, x, y, font_size=30, color=(255, 255, 255)):
        if hasattr(self, "containers"):
            super().__init__(self.containers)
        else:
            super().__init__()
        self.score = 0
        self.font = pygame.font.Font(None, font_size)
        self.color = color
        self.x, self.y = x, y
        self.update_image()

    def update_image(self):
        self.image = self.font.render(f"Score: {int(self.score)}", True, self.color)
        self.rect = self.image.get_rect(topleft=(self.x, self.y))

    def update_score(self, points):
        self.score += points
        if self.score <= 0:
            self.score = 0
        self.update_image()

    def update(self, dt):
        pass        

    def draw(self, screen):
        screen.blit(self.image, self.rect)