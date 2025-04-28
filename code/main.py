import pygame

from pygame.image import load

from settings import *

from editor import Editor

class Main:
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.clock = pygame.time.Clock()

        self.editor = Editor()

        # инициализация курсора
        surf = load(CURSOR_PATH).convert_alpha()
        cursor = pygame.cursors.Cursor((0,0), surf)
        pygame.mouse.set_cursor(cursor)

    def run(self):
        while True:  # запускаем игру и обновляем ее
            dt = self.clock.tick() / 1000  # расчет сколько времени прошло между кадрами

            self.editor.run(dt) # обработка какого-либо взаимодействия
            pygame.display.update()  # обновляем кадр

if __name__ == '__main__':
    main = Main()
    main.run()