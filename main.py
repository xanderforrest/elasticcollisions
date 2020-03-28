import pygame
import random
import numpy as np
import pygame.gfxdraw
from pygame.locals import (
    RLEACCEL,
    K_ESCAPE,
    KEYDOWN,
    K_LEFT,
    QUIT
)

pygame.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600

BALL= pygame.Surface((30, 30), pygame.SRCALPHA)
pygame.gfxdraw.aacircle(BALL, 15, 15, 14, (0, 255, 0))
pygame.gfxdraw.filled_circle(BALL, 15, 15, 14, (0, 255, 0))

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
screen.fill((255, 255, 255))

def apply_collision(ball_a, ball_b):
    normal_vector = ball_b.get_position() - ball_a.get_position()
    try:
        nu_vector = normal_vector / np.linalg.norm(normal_vector)
    except:
        print("Division by 0 Error, cancelling collision")
        return False
    tan_vector = np.array([nu_vector[1]*-1, nu_vector[0]])

    v1n = np.dot(nu_vector, ball_a.get_velocity())
    v1t = np.dot(tan_vector, ball_a.get_velocity())

    v2n = np.dot(nu_vector, ball_b.get_velocity())
    v2t = np.dot(tan_vector, ball_b.get_velocity())

    NEW_v1t = v1t
    NEW_v2t = v2t

    NEW_v1n = (v1n * (ball_a.mass - ball_b.mass) + (2 * ball_b.mass * v2n)) / (ball_a.mass + ball_b.mass)
    NEW_v2n = (v2n * (ball_b.mass - ball_a.mass) + (2 * ball_a.mass * v1n)) / (ball_a.mass + ball_b.mass)

    ball_a_velocity = (np.dot(NEW_v1n, nu_vector) + np.dot(NEW_v1t, tan_vector))
    ball_b_velocity = (np.dot(NEW_v2n, nu_vector) + np.dot(NEW_v2t, tan_vector))
    #print(f"OLD VELOCITY A: {ball_a.v}")
    #print(f"OLD VELOCITY B: {ball_b.v}")
    ball_a.update_velocity(ball_a_velocity)
    #print(f"NEW VELOCITY A: {ball_a.v}")
    ball_b.update_velocity(ball_b_velocity)
    #print(f"NEW VELOCITYB : {ball_b.v}")

class Ball(pygame.sprite.Sprite):
    def __init__(self):
        super(Ball, self).__init__()
        self.surf = BALL
        self.surf.set_colorkey((0, 0, 0), RLEACCEL)
        self.rect = self.surf.get_rect(
            center = (
                random.randint(0, SCREEN_WIDTH),
                random.randint(0, SCREEN_HEIGHT)
                ))
        self.v = np.array([random.randint(-6, 6), random.randint(-6, 6)])
        self.mass = random.randint(20, 100)

    def update_velocity(self, velocity):
        print(f"MY OLD VELOCITY WAS {self.v}")
        self.v = velocity
        print(f"MY NEW VELOCITY IS {self.v}")
        print(f"MY MASS IS {self.mass}")
        self.rect.move_ip(1.5*self.v[0], 1.5*self.v[1])

    def update(self):
        self.rect.move_ip(self.v[0], self.v[1])
        #print(f"CHANGING VELOCITY BY {self.v}")

        if self.rect.left < 0: # LEFT BORDER
            self.v[0] = self.v[0] * -1
        if self.rect.right > SCREEN_WIDTH: # RIGHT BORDER
            self.v[0] = self.v[0] * -1
        if self.rect.top <= 0: # TOP BORDER
            self.v[1] = self.v[1] * -1
        if self.rect.bottom >= SCREEN_HEIGHT: # BOTTOM BORDER
            self.v[1] = self.v[1] * -1

    def get_velocity(self):
        return np.array(self.v)

    def get_position(self):
        return np.array([self.rect.center[0], self.rect.center[1]])


all_balls = pygame.sprite.Group()

ball = Ball()
all_balls.add(ball)

ALLOWCOLLISION = pygame.USEREVENT + 1
pygame.time.set_timer(ALLOWCOLLISION, 1000)
clock = pygame.time.Clock()
collided = []
running = True
while running:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                running = False
            elif event.key == K_LEFT:
                new_ball = Ball()
                all_balls.add(new_ball)
        elif event.type == QUIT:
            running = False
        elif event.type == ALLOWCOLLISION:
            collided = []

    all_balls.update()
    screen.fill((255, 255, 255))


    for entity in all_balls:
        screen.blit(entity.surf, entity.rect)
        #nballs = all_balls
        #nballs = nballs.remove(entity)
        #if nballs:
        #    ball_b = pygame.sprite.spritecollideany(entity, nballs)
        #    if ball_b:
        #        print("There was a collision")
        #        apply_collision(entity, ball_b)
    pygame.display.flip()

    for entity in all_balls:
        all_balls.remove(entity)
        for ball in collided:
            try:
                all_balls.remove(ball)
            except:
                pass
        ball_b = pygame.sprite.spritecollideany(entity, all_balls)
        if ball_b and ball_b not in collided:
            #print("There was a collision")
            apply_collision(entity, ball_b)
            collided.append(ball_b)
        if entity not in all_balls:
            all_balls.add(entity)
        for ball in collided:
            if ball not in all_balls:
                all_balls.add(ball)
