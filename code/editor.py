import pygame, sys
from pygame.math import Vector2 as vector
from pygame.mouse import get_pressed as mouse_buttons
from pygame.mouse import get_pos as mouse_pos
from settings import *
from menu import Menu

class Editor:
    def __init__(self):
        # экран
        self.display_surface = pygame.display.get_surface()
        self.canvas_data = {}

        # навигация
        self.origin = vector()
        self.pan_active = False
        self.pan_offset = vector()

        # вспомогательные линии
        self.support_line_surf = pygame.Surface((WINDOW_WIDTH, WINDOW_HEIGHT))
        self.support_line_surf.set_colorkey('green')
        self.support_line_surf.set_alpha(30)

        # выбор
        self.selection_index = 2
        self.last_selected_cell = None

        # меню
        self.menu = Menu()

    # помощь
    def get_current_cell(self):
        distance_to_origin = vector(mouse_pos()) - self.origin

        if distance_to_origin.x > 0:
            col = int(distance_to_origin.x / TILE_SIZE)
        else:
            col = int(distance_to_origin.x / TILE_SIZE) - 1

        if distance_to_origin.y > 0:
            row = int(distance_to_origin.y / TILE_SIZE)
        else:
            row = int(distance_to_origin.y / TILE_SIZE) - 1

        return col, row

    # ввод
    def event_loop(self): # цикл событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # проверяем решил ли выйти пользователь из игры
                pygame.quit()
                sys.exit()
            self.pan_input(event)
            self.selection_hotkeys(event)
            self.menu_click(event)
            self.canvas_add()

    def pan_input(self, event):
        # проверка нажатия на среднюю кнопку мыши
        if event.type  == pygame.MOUSEBUTTONDOWN and mouse_buttons()[1]:
            self.pan_active = True
            # коодинаты вектора "разница" для сдвига камеры
            self.pan_offset = vector(mouse_pos()) - self.origin

        if not mouse_buttons()[1]:
            self.pan_active = False


        if event.type == pygame.MOUSEWHEEL:
            # передвижение камеры вниз/вверх
            if pygame.key.get_pressed()[pygame.K_LCTRL]:
                self.origin.y -= event.y * 50
            # передвижение камеры вперед/назад
            else:
                self.origin.x -= event.y * 50

        # сдвиг камеры
        if self.pan_active:
            self.origin = vector(mouse_pos()) - self.pan_offset

    def selection_hotkeys(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT and self.selection_index < RIGHT_VALUE_EDITOR_DATA:
                self.selection_index +=1
            elif event.key == pygame.K_LEFT and self.selection_index > LEFT_VALUE_EDITOR_DATA:
                self.selection_index -= 1

    def menu_click(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and self.menu.rect.collidepoint(mouse_pos()):
            self.selection_index = self.menu.click(mouse_pos(), mouse_buttons())

    def canvas_add(self):
        if mouse_buttons()[0] and not self.menu.rect.collidepoint(mouse_pos()):
            current_cell = self.get_current_cell()

            if current_cell != self.last_selected_cell:

                if current_cell in self.canvas_data:
                    self.canvas_data[current_cell].add_id(self.selection_index)
                else:
                    self.canvas_data[current_cell] = CanvasTile(self.selection_index)
                self.last_selected_cell = current_cell

        for key, value in self.canvas_data.items():
            print(f'{key}: {value.has_terrain}')
    # рисование
    def draw_tile_lines(self):
        cols = WINDOW_WIDTH // TILE_SIZE
        rows = WINDOW_HEIGHT // TILE_SIZE

        origin_offset = vector(
            x = self.origin.x - int(self.origin.x / TILE_SIZE) * TILE_SIZE,
            y = self.origin.y - int(self.origin.y / TILE_SIZE) * TILE_SIZE)

        self.support_line_surf.fill('green')

        for col in range(cols + 1):
            x = origin_offset.x + col * TILE_SIZE
            pygame.draw.line(self.support_line_surf, LINE_COLOR, (x,0), (x,WINDOW_HEIGHT))

        for row in range(rows + 1):
            y = origin_offset.y + row * TILE_SIZE
            pygame.draw.line(self.support_line_surf, LINE_COLOR, (0, y),(WINDOW_WIDTH, y))

        self.display_surface.blit(self.support_line_surf, (0,0))

    def draw_level(self):
        for cell_pos, tile in self.canvas_data.items():
            pos = self.origin + vector(cell_pos) * TILE_SIZE
            print(self.origin, pos, cell_pos, tile)

            # вода
            if tile.has_water:
                test_surf = pygame.Surface((TILE_SIZE, TILE_SIZE))
                test_surf.fill('blue')
                self.display_surface.blit(test_surf, pos)

            # местность
            if tile.has_terrain:
                test_surf = pygame.Surface((TILE_SIZE, TILE_SIZE))
                test_surf.fill('brown')
                self.display_surface.blit(test_surf, pos)

            # монеты
            if tile.coin:
                test_surf = pygame.Surface((TILE_SIZE, TILE_SIZE))
                test_surf.fill('yellow')
                self.display_surface.blit(test_surf, pos)

            # враги
            if tile.enemy:
                test_surf = pygame.Surface((TILE_SIZE, TILE_SIZE))
                test_surf.fill('red')
                self.display_surface.blit(test_surf, pos)

    # обновление
    def run(self, dt):
        self.event_loop()

        # рисование
        self.display_surface.fill('gray')
        self.draw_level()
        self.draw_tile_lines()
        pygame.draw.circle(self.display_surface, 'red', self.origin, 10)
        self.menu.display(self.selection_index)

class CanvasTile:
    def __init__(self, tile_id):

        # местность
        self.has_terrain = False
        self.terrain_neighbors = []

        # вода
        self.has_water = False
        self.water_on_top = False

        # монеты
        self.coin = None

        # враги
        self.enemy = None

        # обьекты
        self.objects = []

        self.add_id(tile_id)

    def add_id(self, tile_id):
        options = {key: value['style'] for key, value in EDITOR_DATA.items()}
        match options[tile_id]:
            case 'terrain': self.has_terrain = True
            case 'water': self.has_water = True
            case 'coin': self.coin = tile_id
            case 'enemy': self.enemy = tile_id