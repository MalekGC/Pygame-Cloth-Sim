import random
import time

import pygame
import sys

from pygame.locals import *
from objs import *
from data import *
camera = Camera(Vector2(0, 0), zoom=12.3473479)
nodes = []
lines = []
mouse_left_down = False
mouse_right_down = False
mouse_middle_down = False
last_mouse_pos = Vector2(0, 0)
drag_start = 0
drag_end = 0
external_forces = 0
cutting_tool = True


def main():
    global lines, drag_start, drag_end, nodes, mouse_left_down, mouse_right_down, last_mouse_pos, camera
    global mouse_middle_down, external_forces
    # Initialise screen
    pygame.init()
    screen = pygame.display.set_mode((800, 800))
    pygame.display.set_caption('Rope sim')
    for y in range(0, 20):
        y *= 5
        for x in range(0, 20):
            x *= 5
            locked = True if y == 0 else False
            nodes.append(Node(Vector2(x, y), locked=locked))

    for y in range(0, 20):
        for x in range(0, 19):
            lines.append(Line((nodes[x + y * 20], nodes[1 + x + y * 20])))

    for y in range(0, 19):
        for x in range(0, 20):
            lines.append(Line((nodes[x + y * 20], nodes[20 + x + y * 20])))

    clock = pygame.time.Clock()
    while 1:
        dt = clock.tick(framerate)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 4:
                    zoom = camera.zoom
                    zoom = 1 / zoom
                    zoom *= 0.9
                    camera = Camera(camera.position, zoom=zoom)
                if event.button == 5:
                    zoom = camera.zoom
                    zoom = 1 / zoom
                    zoom *= 1.1
                    camera = Camera(camera.position, zoom=zoom)
        mouse_buttons = pygame.mouse.get_pressed(num_buttons=5)
        mouse_pos = pygame.mouse.get_pos()
        mouse_pos_vector = Vector2(mouse_pos[0], mouse_pos[1])
        mouse_pos_world = camera.screen_to_world_pos(mouse_pos)

        # Left mouse button
        if mouse_buttons[0]:
            if not mouse_left_down:
                drag_start = mouse_pos_world
                mouse_left_down = True
        else:
            if mouse_left_down:
                drag_end = mouse_pos_world
                if Vector2.distance_between(drag_start, drag_end) < 1:
                    too_close_to_node = False
                    for node in nodes:
                        if Vector2.distance_between(node.position, mouse_pos_world) < node.radius * 2:
                            too_close_to_node = True
                            close_node = node
                    if not too_close_to_node:
                        node = Node(drag_start)
                        if mouse_buttons[2]:
                            node.locked = True
                        nodes.append(node)

                    else:
                        close_node.locked = not close_node.locked

                else:
                    found = 0
                    for node in nodes:
                        if Vector2.distance_between(node.position, drag_start) < node.radius * 2:
                            start_node = node
                            found += 1
                        if Vector2.distance_between(node.position, drag_end) < node.radius * 2:
                            end_node = node
                            found += 1
                    if found == 2:
                        lines.append(Line((start_node, end_node)))
                mouse_left_down = False

        if mouse_buttons[1]:
            if mouse_middle_down:
                midde_drag_end = mouse_pos_world
                external_forces = (midde_drag_end - midde_drag_start) / 4
            else:
                midde_drag_start = mouse_pos_world
                mouse_middle_down = True
        else:
            mouse_middle_down = False
            external_forces = Vector2(0, 0)

        if mouse_buttons[2]:
            offset = last_mouse_pos - mouse_pos_vector
            if offset.distance() > 0.1:
                camera.position += camera.screen_to_world_unit(offset)
        last_mouse_pos = mouse_pos_vector
        simulate(dt)
        draw(screen)
        if mouse_buttons[4]:
            for line in lines:
                line_center = (line.parents[0].position + line.parents[1].position) / 2
                if Vector2.distance_between(mouse_pos_world, line_center) < 2:
                    lines.remove(line)


def simulate(dt):
    for node in nodes:
        node.move(dt, external_forces)
    for i in range(0, line_passes):
        random.shuffle(lines)
        for line in lines:
            line.work(dt)


def draw(screen):
    global camera
    screen.fill((0, 0, 0))
    for line in lines:
        line_start = camera.world_to_screen_pos(line.parents[0].position)
        line_end = camera.world_to_screen_pos(line.parents[1].position)
        line_start.tuple()
        pygame.draw.aaline(screen, line_color, line_start.tuple(), line_end.tuple())

    for node in nodes:
        center = camera.world_to_screen_pos(node.position).tuple()
        radius = camera.world_to_screen_unit(node.radius)
        color = circle_color_locked if node.locked else circle_color_unlocked
        pygame.draw.circle(screen, color, center, radius)
    pygame.display.flip()


if __name__ == "__main__":
    main()

