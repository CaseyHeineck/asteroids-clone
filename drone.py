import pygame
from circleshape import *
from constants import *
from player import *
from shot import *

class Drone(CircleShape):
    def __init__(self, player, asteroids):
        super().__init__(player.position.x, player.position.y, DRONE_RADIUS)
        self.asteroids = asteroids
        self.player = player
        self.orbit_angle = DRONE_ORBIT_ANGLE_OFFSET
        self.orbit_radius = DRONE_ORBIT_RADIUS
        self.orbit_speed = DRONE_ORBIT_SPEED
        self.rotation = 0
        self.shot_cooldown = 0
        self.target = None
        self.range = 600

    def acquire_target(self):
        closest_so_far = float("inf")
        self.target = None

        for asteroid in self.asteroids:
            player_distance = self.player.position.distance_to(asteroid.position)
            drone_distance = self.position.distance_to(asteroid.position)

            if drone_distance <= self.range and player_distance < closest_so_far:
                closest_so_far = player_distance
                self.target = asteroid
    
    def aim_at_target(self):
        if self.target is None:
            return
        direction = self.target.position - self.position
        if direction.length_squared() > 0:
            self.rotation = pygame.Vector2(0, -1).angle_to(direction)

    def shoot(self):
        if self.shot_cooldown > 0 or self.target is None:
            return
        forward = pygame.Vector2(0, -1).rotate(-self.rotation)
        turret_length = self.radius - 2
        spawn_position = self.position + forward * turret_length
        shot = Shot(spawn_position.x, spawn_position.y, SHOT_RADIUS)
        shot.velocity = forward * DRONE_SHOT_SPEED
        self.shot_cooldown = DRONE_SHOOT_COOLDOWN_SECONDS

    def draw(self, screen):
        pygame.draw.circle(screen, GRAY, self.position, self.radius, LINE_WIDTH)
        turret_width = 6
        turret_length = self.radius - 2
        surface_size = turret_length * 2
        turret_surface = pygame.Surface((surface_size, surface_size), pygame.SRCALPHA)
        center_x = surface_size // 2
        center_y = surface_size // 2
        turret_rect = pygame.Rect(
            center_x - turret_width // 2,
            center_y - turret_length,
            turret_width,
            turret_length
        )
        pygame.draw.rect(turret_surface, MAGENTA, turret_rect)
        rotated_turret = pygame.transform.rotate(turret_surface, self.rotation)
        rotated_rect = rotated_turret.get_rect(center=(self.position.x, self.position.y))
        screen.blit(rotated_turret, rotated_rect)

    def update(self, dt):
        self.orbit_player(dt)
        self.shot_cooldown -= dt
        self.acquire_target()
        self.aim_at_target()
        self.shoot()        

    def orbit_player(self, dt):
        self.orbit_angle += self.orbit_speed * dt
        offset = pygame.Vector2(self.orbit_radius, 0).rotate(self.orbit_angle)
        self.position = self.player.position + offset

    def collides_with(self, other):
        return False
