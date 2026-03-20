import random
from circleshape import *
from constants import *
from logger import log_event

class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)
        self.size = self.radius / ASTEROID_MIN_RADIUS
        self.full_health = self.size
        self.health = self.full_health
        self.line_width = int(LINE_WIDTH + (self.size * 2))

    def draw(self, screen):
        pygame.draw.circle(screen, WHITE, self.position, self.radius, self.line_width)
        if self.health < self.full_health:
            self.draw_health_bar(screen)
    
    def draw_health_bar(self, screen):
        health_ratio = self.health / self.full_health
        width = self.radius

        background_rect = pygame.Rect(self.position.x - (width / 2), (self.position.y - (self.size * 2)), width, (HEALTH_BAR_HEIGHT + (self.size * 2)))
        pygame.draw.rect(screen, BLACK, background_rect)
        
        current_width = width * health_ratio
        health_rect = pygame.Rect(self.position.x - (width / 2), (self.position.y - (self.size * 2)), current_width, (HEALTH_BAR_HEIGHT + (self.size * 2)))
        
        pygame.draw.rect(screen, RED, health_rect)

        pygame.draw.rect(screen, WHITE, background_rect, LINE_WIDTH)

    def update(self, dt):
        self.position += self.velocity * dt

    def split(self, damage, HUD):
        self.health -= damage
        if self.health > 0 :
            return
        else:
            HUD.update_score(BASE_SCORE * self.size)
            self.kill()
            if self.size == 1:
                log_event("asteroid_destroyed")
                return
            else:
                log_event("asteroid_split")
                # currently doesn't work but unsure of why
                # it is getting into the for angle in num_angles loop
                # but doesn't like how im trying to assign the range
                # starting at one and stopping after it has appended its own size number to the list
                # num_angles = []
                # angle_num = 1
                # if angle_num <= self.size:
                #   num_angles.append(str(angle_num))
                #   angle_num += 1
                # for angle in num_angles:
                #     range_size = 360 / len(num_angles)
                #     new_angle = random.uniform(1 + (range_size * (int(angle) - 1)), range_size(int(angle)))    
                #     velocity = self.velocity.rotate(new_angle)
                #     radius = self.radius - ASTEROID_MIN_RADIUS
                #     asteroid = Asteroid(self.position.x, self.position.y, radius)
                #     asteroid.velocity = velocity * self.split_factor(angle) * ASTEROID_SPLIT_ACCELERATION
                angle1 = random.uniform(1, 180)
                angle2 = random.uniform(181, 360)
                first = self.velocity.rotate(angle1)
                second = self.velocity.rotate(angle2)
                new_radius = self.radius - ASTEROID_MIN_RADIUS
                asteroid1 = Asteroid(self.position.x, self.position.y, new_radius)
                asteroid1.velocity = first * self.split_factor(angle1) * ASTEROID_SPLIT_ACCELERATION
                asteroid2 = Asteroid(self.position.x, self.position.y, new_radius)
                asteroid2.velocity = second * self.split_factor(angle2) * ASTEROID_SPLIT_ACCELERATION
    
    def split_factor(self, angle):
        factor = 0
        if angle > 270 and angle <= 360:
            angle = angle - 270
            factor = angle / 90   
        elif angle > 180 and angle <= 270:
            angle = angle - 180
            factor = 1 - (angle / 90)
        elif angle > 90 and angle <= 180:
            angle = angle - 90
            factor = angle / 90
        elif angle > 0 and angle <= 90:
            factor = 1 - (angle / 90)
        else:
            raise ValueError
        if factor < MIN_ASTEROID_SPLIT_FACTOR:
            return MIN_ASTEROID_SPLIT_FACTOR
        else:
            return factor