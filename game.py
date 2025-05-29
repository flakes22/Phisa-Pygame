import pygame
import random

pygame.init()

WIDTH = 600
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Phineas and Isabella Game")

background = pygame.image.load("assets/images/background.png")
background = pygame.transform.scale(background, (WIDTH, HEIGHT))

common_width = 60
common_height = 80

phineas_image = pygame.transform.scale(
    pygame.image.load("assets/images/phineas_flipped.png"), (common_width, common_height)
)
isabella_image = pygame.transform.scale(
    pygame.image.load("assets/images/isabella.png"), (common_width, common_height)
)

start_font = pygame.font.SysFont("Times New Roman", 36, bold=True)
heading_font = pygame.font.SysFont("Times New Roman", 60, bold=True)

start_screen = True
while start_screen:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            start_screen = False

    screen.blit(background, (0, 0))

    heading_text = heading_font.render("Welcome!!", True, (255, 255, 200))
    start_text = start_font.render("Press ENTER to Start", True, (255, 255, 255))

    screen.blit(heading_text, (WIDTH // 2 - heading_text.get_width() // 2, HEIGHT // 3))
    screen.blit(start_text, (WIDTH // 2 - start_text.get_width() // 2, HEIGHT // 2 + 50))

    pygame.display.flip()

phineas_x, phineas_y = 100, 0
phineas_vx, phineas_vy = 200, 0

isabella_x, isabella_y = 300, 0
isabella_vx, isabella_vy = 200, 0

gravity = 560

p_width = i_width = common_width
p_height = i_height = common_height

phineas_score = 0
isabella_score = 0

green_rects = []
pink_rects = []
diamonds = []

message = ""
message_time = 0

clock = pygame.time.Clock()
running = True

while running:
    dt = clock.tick(60) / 1000

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    if keys[pygame.K_SPACE]:
        phineas_vy = -400
    if keys[pygame.K_RIGHT]:
        phineas_x += phineas_vx * dt
    if keys[pygame.K_LEFT]:
        phineas_x -= phineas_vx * dt

    if keys[pygame.K_w]:
        isabella_vy = -400
    if keys[pygame.K_d]:
        isabella_x += isabella_vx * dt
    if keys[pygame.K_a]:
        isabella_x -= isabella_vx * dt

    screen.blit(background, (0, 0))

    if random.randint(0, 2000) > 1897:
        green_rects.append(pygame.Rect(WIDTH, random.randint(0, HEIGHT - 100), 10, 100))

    if random.randint(0, 2000) > 1897:
        pink_rects.append(pygame.Rect(WIDTH, random.randint(0, HEIGHT - 100), 10, 100))

    if random.randint(0, 3000) > 2995:
        diamonds.append(pygame.Rect(WIDTH, random.randint(0, HEIGHT - 50), 15, 15))

    phineas_rect = pygame.Rect(phineas_x, phineas_y, p_width, p_height)
    isabella_rect = pygame.Rect(isabella_x, isabella_y, i_width, i_height)

    for rect in green_rects[:]:
        pygame.draw.rect(screen, (0, 255, 0), rect)
        rect.x -= int(200 * dt)
        if phineas_rect.colliderect(rect):
            green_rects.remove(rect)
            phineas_score += 1
        elif isabella_rect.colliderect(rect):
            green_rects.remove(rect)

    for rect in pink_rects[:]:
        pygame.draw.rect(screen, (255, 105, 180), rect)
        rect.x -= int(200 * dt)
        if isabella_rect.colliderect(rect):
            pink_rects.remove(rect)
            isabella_score += 1
        elif phineas_rect.colliderect(rect):
            pink_rects.remove(rect)

    for diamond in diamonds[:]:
        pygame.draw.rect(screen, (0, 200, 255), diamond)
        diamond.x -= int(150 * dt)
        if phineas_rect.colliderect(diamond):
            diamonds.remove(diamond)
            phineas_score += 3
            message = "Great job!"
            message_time = pygame.time.get_ticks()
        elif isabella_rect.colliderect(diamond):
            diamonds.remove(diamond)
            isabella_score += 3
            message = "Great job!"
            message_time = pygame.time.get_ticks()

    phineas_vy += gravity * dt
    phineas_y += phineas_vy * dt
    if phineas_y > HEIGHT - p_height:
        phineas_y = HEIGHT - p_height
        phineas_vy = 0

    isabella_vy += gravity * dt
    isabella_y += isabella_vy * dt
    if isabella_y > HEIGHT - i_height:
        isabella_y = HEIGHT - i_height
        isabella_vy = 0

    screen.blit(phineas_image, (phineas_x, phineas_y))
    screen.blit(isabella_image, (isabella_x, isabella_y))

    font = pygame.font.SysFont(None, 30, bold=True)
    p_score_text = font.render(f"Phineas Score: {phineas_score}", True, (255, 255, 255))
    i_score_text = font.render(f"Isabella Score: {isabella_score}", True, (255, 182, 193))
    screen.blit(p_score_text, (10, 10))
    screen.blit(i_score_text, (10, 40))

    if message and pygame.time.get_ticks() - message_time < 1000:
        msg_font = pygame.font.SysFont("Arial", 36, bold=True)
        msg_text = msg_font.render(message, True, (255, 255, 0))
        screen.blit(msg_text, (WIDTH // 2 - msg_text.get_width() // 2, HEIGHT // 2 - 20))
    else:
        message = ""

    pygame.display.flip()
print(f"Phineas' final score: {phineas_score}")
print(f"Isabella's final score: {isabella_score}")
print("And the Winner is: ")
if phineas_score > isabella_score:
    print("Phineas!!")
elif isabella_score > phineas_score:
    print("Isabella!!")
else:
    print("It's a tie!")

pygame.quit()
