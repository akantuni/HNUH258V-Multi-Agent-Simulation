import random
import uuid

import pygame

from options import (
    EVIL_COLOR,
    EVIL_HEALTH_MULTIPLIER,
    EVIL_POWER_MULTIPLIER,
    EVIL_RADIUS_MULTIPLIER,
    EVIL_SPEED_MULTIPLIER,
    GOOD_COLOR,
    GOOD_HEALTH,
    GOOD_POWER,
    GOOD_RADIUS,
    GOOD_SPEED,
    POWER_INCREASE_AFTER_WIN,
    RADIUS_INCREASE_AFTER_WIN,
    TURN_EVIL_PROBABILITY,
)


class Agent:
    color = GOOD_COLOR
    radius = GOOD_RADIUS
    speed = GOOD_SPEED
    power = GOOD_POWER
    health = GOOD_HEALTH
    evil = False
    attacking = None

    def __init__(self, screen):
        self.screen = screen
        self.uid = uuid.uuid4()
        self.pos = pygame.Vector2(
            random.randint(0, screen.get_width() - 2 * self.radius),
            random.randint(0, screen.get_height() - 2 * self.radius),
        )

    def draw(self):
        pygame.draw.circle(self.screen, self.color, self.pos, self.radius)

    def turn_evil(self):
        self.evil = True
        self.color = EVIL_COLOR
        self.health *= EVIL_HEALTH_MULTIPLIER
        self.radius *= EVIL_RADIUS_MULTIPLIER
        self.power *= EVIL_POWER_MULTIPLIER
        self.speed *= EVIL_SPEED_MULTIPLIER
        self.draw()

    def life_happens(self):
        if not self.evil and random.random() < TURN_EVIL_PROBABILITY:
            self.turn_evil()

    def move(self, agent_positions, dt):
        closest_agent = None
        closest_distance = float("inf")
        for uid, agent in agent_positions.items():
            if uid == self.uid:
                continue
            distance = self.pos.distance_to(agent["pos"]) - (
                self.radius + agent["radius"]
            )
            if distance <= 0:
                continue
            if distance < closest_distance:
                closest_distance = distance
                closest_agent = agent

        if closest_agent:
            direction = closest_agent["pos"] - self.pos
            direction.normalize_ip()
            self.pos += direction * self.speed * dt

    def attack(self, agent, agents):
        if not self.attacking:
            self.attacking = agent.uid

        if self.attacking != agent.uid:
            return

        agent.health -= self.power
        self.power += POWER_INCREASE_AFTER_WIN
        self.radius += RADIUS_INCREASE_AFTER_WIN
        if agent.health <= 0:
            self.attacking = None
            if agent in agents:
                agents.remove(agent)

    def regenerate(self):
        if self.health < 100:
            self.health += 10
