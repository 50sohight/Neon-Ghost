import pygame

pygame.init()
window = pygame.display.set_mode((500, 500))
pygame.display.set_caption('Neon Ghost')

square = pygame.Surface((50, 100))
square.fill("Blue")

my_font = pygame.font.Font('Times New Roman')

run = True
while run:

    window.fill((255, 255, 255))

    window.blit(square, (100, 0))

    pygame.draw.circle(window, (23, 54, 65), (250, 150), 30)

    pygame.display.update()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
            pygame.quit()

