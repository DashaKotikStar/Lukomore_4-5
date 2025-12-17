# Wheel_Aprons.py
import pygame
import random
import math

class DiceWheel:
    def __init__(self, center_x, center_y, radius, font_large, font_huge):
        self.center_x = center_x
        self.center_y = center_y
        self.radius = radius
        self.angle = 0
        self.spinning = False
        self.speed = 0
        self.dice = 0
        self.colors = [
            (203, 65, 84),      # 1
            (255, 127, 0),      # 2
            (255, 207, 64),     # 3
            (140, 203, 94),     # 4
            (66, 133, 180),     # 5
            (123, 104, 238),    # 6
        ]
        self.font = font_large
        self.font_huge = font_huge
        self.light_blue = (0, 153, 125)
        self.PURPLE = (100, 0, 200)
        self.arrow_angle = math.pi

    def spin(self):
        self.spinning = True
        self.speed = random.uniform(10, 20)
        self.dice = 0

    def update(self):
        if not self.spinning:
            return

        self.speed *= 0.98
        if self.speed < 0.1:
            self.speed = 0
            self.spinning = False
            self._calculate_dice_from_angle()
        self.angle += self.speed

    def _calculate_dice_from_angle(self):
        step = 2 * math.pi / 6
        best_i = 0
        min_diff = float('inf')
        for i in range(6):
            sector_center = (self.angle + i * step + step / 2) % (2 * math.pi)
            diff = abs((sector_center - self.arrow_angle + math.pi) % (2 * math.pi) - math.pi)
            if diff < min_diff:
                min_diff = diff
                best_i = i
        self.dice = best_i + 1

    def draw(self, screen):
        pygame.draw.circle(screen, self.PURPLE, (self.center_x, self.center_y), self.radius + 10)
        pygame.draw.circle(screen, (255, 255, 255), (self.center_x, self.center_y), self.radius, 5)

        for i in range(6):
            start_angle = self.angle + i * (2 * math.pi / 6)
            end_angle = start_angle + (2 * math.pi / 6)
            points = [(self.center_x, self.center_y)]
            for j in range(100):
                angle = start_angle + (end_angle - start_angle) * j / 100
                x = self.center_x + self.radius * math.cos(angle)
                y = self.center_y + self.radius * math.sin(angle)
                points.append((x, y))
            points.append((self.center_x, self.center_y))
            pygame.draw.polygon(screen, self.colors[i], points)

            text_angle = start_angle + (2 * math.pi / 12)
            text_x = self.center_x + (self.radius - 50) * math.cos(text_angle)
            text_y = self.center_y + (self.radius - 50) * math.sin(text_angle)
            text_surface = self.font.render(str(i + 1), True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=(text_x, text_y))
            screen.blit(text_surface, text_rect)

        button_radius = 80
        button_color = self.light_blue
        if self.spinning:
            button_color = (2, 139, 87)
        pygame.draw.circle(screen, button_color, (self.center_x, self.center_y), button_radius)

        if not self.spinning:
            arrow = self.font_huge.render("start", True, (255, 255, 255))
            arrow_rect = arrow.get_rect(center=(self.center_x, self.center_y))
            screen.blit(arrow, arrow_rect)

        triangle_points = [
            (self.center_x - self.radius, self.center_y - 15),
            (self.center_x - self.radius, self.center_y + 15),
            (self.center_x - self.radius + 30, self.center_y)
        ]
        pygame.draw.polygon(screen, (0, 0, 0), triangle_points)

    def is_spinning(self):
        return self.spinning

    def get_dice_result(self):
        return self.dice