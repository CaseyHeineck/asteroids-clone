import pygame
from circleshape import CircleShape
from constants import *
from projectile import Kinetic, Plasma, Rocket

class Drone(CircleShape):
    def __init__(self, player, asteroids):
        super().__init__(player.position.x, player.position.y, DRONE_RADIUS)
        self.asteroids = asteroids
        self.player = player
        
        self.orbit_angle = DRONE_ORBIT_ANGLE_OFFSET
        self.orbit_radius = DRONE_ORBIT_RADIUS
        self.orbit_speed = DRONE_ORBIT_SPEED

        self.rotation = 0
        self.target = None

        self.range = float("inf")
        self.weapons_free_timer = 0
        self.weapons_free_timer_max = DRONE_WEAPONS_FREE_TIMER
        self.body_color = WHITE
        self.body_line_width = DRONE_LINE_WIDTH

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

    def get_forward_vector(self):
        return pygame.Vector2(0, -1).rotate(-self.rotation)
    
    def get_projectile_spawn_position(self):
        forward = self.get_forward_vector()
        return self.position + forward * self.radius

    def create_projectile(self):
        raise NotImplementedError("Drone subclass not instantiated")

    def shoot(self):
        if self.weapons_free_timer > 0 or self.target is None:
            return
        
        self.create_projectile()
        self.weapons_free_timer = self.weapons_free_timer_max

    def draw_body(self, screen):
        pygame.draw.circle(screen, self.body_color, self.position, self.radius, self.body_line_width)

    def draw_weapons_platform(self, screen):
        raise NotImplementedError("Drone subclass not instantiated")

    def draw(self, screen):    
        self.draw_body(screen)
        self.draw_weapons_platform(screen)

    def update(self, dt):
        self.orbit_player(dt)
        self.weapons_free_timer -= dt
        self.acquire_target()
        self.aim_at_target()
        self.shoot()        

    def orbit_player(self, dt):
        self.orbit_angle += self.orbit_speed * dt
        offset = pygame.Vector2(self.orbit_radius, 0).rotate(self.orbit_angle)
        self.position = self.player.position + offset

    def collides_with(self, other):
        return False
    
class ExplosiveDrone(Drone):
    def __init__(self, player, asteroids):
        super().__init__(player, asteroids)

        self.body_color = EXPLOSIVE_DRONE_BODY_COLOR
        self.range = EXPLOSIVE_DRONE_WEAPONS_RANGE
        self.weapons_free_timer_max = EXPLOSIVE_DRONE_WEAPONS_FREE_TIMER
        self.projectile_speed = EXPLOSIVE_DRONE_PROJECTILE_SPEED

        self.launcher_color = EXPLOSIVE_DRONE_WEAPONS_PLATFORM_COLOR
        self.launcher_radius = EXPLOSIVE_DRONE_LAUNCHER_RADIUS

        self.door_offset = EXPLOSIVE_DRONE_DOOR_OFFSET
        self.door_width = EXPLOSIVE_DRONE_DOOR_WIDTH
        self.door_length = EXPLOSIVE_DRONE_DOOR_LENGTH

        self.launch_animation_timer = 0
        self.launch_animation_duration = EXPLOSIVE_DRONE_DOOR_ANIMATION_TIME

    def get_projectile_spawn_position(self):
        forward = self.get_forward_vector()
        return self.position + forward * (self.radius + 4)

    def create_projectile(self):
        spawn_position = self.get_projectile_spawn_position()
        forward = self.get_forward_vector()

        projectile = Rocket(spawn_position.x, spawn_position.y, self.asteroids)
        projectile.velocity = forward * self.projectile_speed

        self.launch_animation_timer = self.launch_animation_duration

    def update(self, dt):
        super().update(dt)
        self.launch_animation_timer = max(0, self.launch_animation_timer - dt)

    def draw_weapons_platform(self, screen):
        surface_size = self.radius * 3
        platform_surface = pygame.Surface((surface_size, surface_size), pygame.SRCALPHA)

        center_x = surface_size // 2
        center_y = surface_size // 2

        # main circular launcher
        pygame.draw.circle(
            platform_surface,
            self.launcher_color,
            (center_x, center_y),
            self.launcher_radius,
            2
        )

        # amount the doors are opened
        open_ratio = 0
        if self.launch_animation_duration > 0:
            open_ratio = self.launch_animation_timer / self.launch_animation_duration

        door_slide = int(6 * open_ratio)

        # doors split horizontally relative to the launcher face
        left_door = pygame.Rect(
            center_x - self.door_offset - self.door_width - door_slide,
            center_y - self.door_length // 2,
            self.door_width,
            self.door_length
        )

        right_door = pygame.Rect(
            center_x + self.door_offset + door_slide,
            center_y - self.door_length // 2,
            self.door_width,
            self.door_length
        )

        pygame.draw.rect(platform_surface, self.launcher_color, left_door)
        pygame.draw.rect(platform_surface, self.launcher_color, right_door)

        rotated_platform = pygame.transform.rotate(platform_surface, self.rotation)
        rotated_rect = rotated_platform.get_rect(center=(self.position.x, self.position.y))
        screen.blit(rotated_platform, rotated_rect)

class KineticDrone(Drone):
    def __init__(self, player, asteroids):
        super().__init__(player, asteroids)

        self.body_color = KINETIC_DRONE_BODY_COLOR
        self.body_line_width = 0
        self.range = KINETIC_DRONE_WEAPONS_RANGE
        self.weapons_free_timer_max = KINETIC_DRONE_WEAPONS_FREE_TIMER

        self.projectile_speed = KINETIC_DRONE_PROJECTILE_SPEED
        self.weapons_platform_color = KINETIC_DRONE_WEAPONS_PLATFORM_COLOR
        self.weapons_platform_length = KINETIC_DRONE_WEAPONS_PLATFORM_LENGTH
        self.weapons_platform_front_width = KINETIC_DRONE_WEAPONS_PLATFORM_FRONT_WIDTH
        self.weapons_platform_back_width = KINETIC_DRONE_WEAPONS_PLATFORM_BACK_WIDTH

    def get_projectile_spawn_position(self):
        forward = self.get_forward_vector()
        return self.position + forward * self.weapons_platform_length

    def create_projectile(self):
        spawn_position = self.get_projectile_spawn_position()
        forward = self.get_forward_vector()

        projectile = Kinetic(spawn_position.x, spawn_position.y)
        projectile.velocity = forward * self.projectile_speed

    def draw_weapons_platform(self, screen):
        surface_size = self.weapons_platform_length * 2
        platform_surface = pygame.Surface((surface_size, surface_size), pygame.SRCALPHA)

        center_x = surface_size // 2
        center_y = surface_size // 2

        front_half = self.weapons_platform_front_width / 2
        back_half = self.weapons_platform_back_width / 2
        length = self.weapons_platform_length

        points = [
            (center_x - front_half, center_y - length),  
            (center_x + front_half, center_y - length),  
            (center_x + back_half, center_y),
            (center_x - back_half, center_y),                ]

        pygame.draw.polygon(platform_surface, self.weapons_platform_color, points)

        rotated_platform = pygame.transform.rotate(platform_surface, self.rotation)
        rotated_rect = rotated_platform.get_rect(center=(self.position.x, self.position.y))
        screen.blit(rotated_platform, rotated_rect)

class PlasmaDrone(Drone):
    def __init__(self, player, asteroids):
        super().__init__(player, asteroids)
        self.body_color = PLASMA_DRONE_BODY_COLOR
        self.range = PLASMA_DRONE_WEAPONS_RANGE
        self.weapons_free_timer_max = PLASMA_DRONE_WEAPONS_FREE_TIMER
        
        self.projectile_speed = PLASMA_DRONE_PROJECTILE_SPEED
        self.weapons_platform_color = PLASMA_DRONE_WEAPONS_PLATFORM_COLOR
        self.weapons_platform_length = self.radius + PLASMA_DRONE_WEAPONS_PLATFORM_LENGTH_OFFSET
        self.weapons_platform_width = PLASMA_DRONE_WEAPONS_PLATFORM_WIDTH 
    
    def get_projectile_spawn_position(self):
        forward = self.get_forward_vector()
        return self.position + forward * self.weapons_platform_length

    def create_projectile(self):
        spawn_position = self.get_projectile_spawn_position()
        forward = self.get_forward_vector()

        projectile = Plasma(spawn_position.x, spawn_position.y)
        projectile.velocity = forward * self.projectile_speed

    def draw_weapons_platform(self, screen):
        surface_size = self.weapons_platform_length * 2
        platform_surface = pygame.Surface((surface_size, surface_size), pygame.SRCALPHA)

        center_x = surface_size // 2
        center_y = surface_size // 2

        platform_rect = pygame.Rect(
            center_x - self.weapons_platform_width // 2,
            center_y - self.weapons_platform_length,
            self.weapons_platform_width,
            self.weapons_platform_length
        )

        pygame.draw.rect(platform_surface, self.weapons_platform_color, platform_rect)

        rotated_platform = pygame.transform.rotate(platform_surface, self.rotation)
        rotated_rect = rotated_platform.get_rect(center=(self.position.x, self.position.y))
        screen.blit(rotated_platform, rotated_rect)
