import sys
from circleshape import *
from constants import *
from shot import *
from logger import log_event

class Player(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, PLAYER_RADIUS)
        self.rotation = 0
        self.shot_cooldown = 0
        self.lives = 3
        self.life = True
        self.invulnerable = False
        
    def draw(self, screen):
        pygame.draw.polygon(screen, "white", self.triangle(), LINE_WIDTH)

    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt

    def move(self, dt):
        unit_vector = pygame.Vector2(0, 1)
        rotated_vector = unit_vector.rotate(self.rotation)
        rotated_with_speed_vector = rotated_vector * PLAYER_SPEED * dt
        self.position += rotated_with_speed_vector

    def shoot(self):
        if self.shot_cooldown > 0:
            return
        else:
            shot = Shot(self.position.x, self.position.y, SHOT_RADIUS)
            shot.velocity = pygame.Vector2(0, 1).rotate(self.rotation) * PLAYER_SHOOT_SPEED
            self.shot_cooldown = PLAYER_SHOOT_COOLDOWN_SECONDS

    def lose_life(self, HUD, respawn_timer, dt):
        log_event("player_hit")
        if self.lives > 0:
            HUD.update_score(LIFE_LOSS_SCORE * self.lives)
            self.respawn(respawn_timer, dt)
            log_event("player_respawned")
            respawn_timer = 0
        else:
            HUD.update_score(GAME_OVER_SCORE)
            log_event("game_over")
            print(f"Score: {HUD.score}")    
            print("Game over!")
            sys.exit()

    def respawn(self, respawn_timer, dt):
        self.lives -= 1
        self.life = False
        self.position.x = SCREEN_WIDTH / 2
        self.position.y = SCREEN_HEIGHT / 2
        self.is_invulnerable()
        if self.invulnerable is True:
            if respawn_timer < PLAYER_RESPAWN_COOLDOWN_SECONDS:
                respawn_timer += dt
                return
            else:
                self.life = True
                self.is_invulnerable()
            
    def collides_with(self, other):
        if self.invulnerable is True:
            return False
        return super().collides_with(other)
    
    def is_invulnerable(self):
        if self.life is not True:
            self.invulnerable = True
        else:
            self.invulnerable = False

    def update(self, dt):
        keys = pygame.key.get_pressed()

        if keys[pygame.K_a]:
            self.rotate(-dt)
        if keys[pygame.K_d]:
            self.rotate(dt)
        if keys[pygame.K_w]:
            self.move(dt)
        if keys[pygame.K_s]:
            self.move(-dt)
        if keys[pygame.K_SPACE]:
            self.shoot()
        
        self.shot_cooldown -= dt

    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]    