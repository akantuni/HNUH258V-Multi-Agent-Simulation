# Example file showing a circle moving on screen


import pygame

from agent import Agent
from options import AGENT_COUNT, REGENERATE_TICKS, STOP_QUANTITY, TURN_EVIL_TICKS

# pygame setup
pygame.init()
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
clock = pygame.time.Clock()
running = True
dt = 0
evil_start_time = pygame.time.get_ticks()
health_start_time = pygame.time.get_ticks()
game_over_font = pygame.font.Font("assets/fonts/game_over.ttf", 160)
agent_quantity_font = pygame.font.Font("assets/fonts/game_over.ttf", 80)


agents = [Agent(screen) for _ in range(AGENT_COUNT)]

while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")

    agent_quantity_text = agent_quantity_font.render(
        f"Agents: {len(agents)}", True, "white"
    )
    screen.blit(agent_quantity_text, (10, 10))

    good_left = any(not agent.evil for agent in agents)
    evil_left = any(agent.evil for agent in agents)
    if not good_left or len(agents) <= STOP_QUANTITY:
        if evil_left:
            text = game_over_font.render("Simulation Over: Evil Wins", True, "white")
        else:
            text = game_over_font.render("Simulation Over: Good Wins", True, "white")
        screen.blit(
            text,
            (
                screen.get_width() // 2 - text.get_width() // 2,
                screen.get_height() // 2 - text.get_height() // 2,
            ),
        )
        pygame.display.flip()
    else:
        agent_positions = {}

        for agent in agents:
            agent_positions[agent.uid] = {
                "pos": agent.pos,
                "evil": agent.evil,
                "radius": agent.radius,
            }

        for agent in agents:
            agent.draw()
            agent.move(agent_positions, dt)

        for agent1 in agents:
            for agent2 in agents:
                if (
                    agent1 != agent2
                    and agent1.pos.distance_to(agent2.pos)
                    <= agent1.radius + agent2.radius
                ):
                    if agent1.evil != agent2.evil:
                        agent1.attack(agent2, agents)
                        agent2.attack(agent1, agents)

            if pygame.time.get_ticks() - evil_start_time > TURN_EVIL_TICKS:
                for agent in agents:
                    agent.life_happens()
                evil_start_time = pygame.time.get_ticks()

        if pygame.time.get_ticks() - health_start_time > REGENERATE_TICKS:
            for agent in agents:
                agent.regenerate()
            health_start_time = pygame.time.get_ticks()

        pygame.display.flip()

        # limits FPS to 60
        # dt is delta time in seconds since last frame, used for framerate-
        # independent physics.
        dt = clock.tick(60) / 1000

pygame.quit()
