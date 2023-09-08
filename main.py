import pygame
import os

pygame.init()
pygame.font.init()
pygame.mixer.init()

WIDTH =  850
HEIGHT = 550
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Spaceship Shooter')

WHITE = (255, 255, 255)
bg_image = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'background.jpg')), (WIDTH, HEIGHT))
border_color_black = (0, 0, 0)
FPS = 60
SPEED = 5
BULLET_SPEED = 8
MAX_BULLET = 3
spaceship_width = 80
spaceship_height = 80
right_ship_hit = pygame.USEREVENT + 1
left_ship_hit = pygame.USEREVENT + 2
bullets_color = (255, 0, 0)

BORDER = pygame.Rect(WIDTH//2 - 5, 0, 10, HEIGHT)

BG_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'bg.mp3'))
BULLET_HIT_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'hit.mp3'))
BULLET_FIRE_SOUND = pygame.mixer.Sound(os.path.join('Assets', 'fire.mp3'))

HEALTH_FONT = pygame.font.SysFont('comicsans', 20)
WINNER_FONT = pygame.font.SysFont('comicsans', 70)

# importing ship images
whiteship_img = pygame.transform.rotate(pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'whiteship.png')), (spaceship_width, spaceship_height)), 90)

blackship_img = pygame.transform.rotate(pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'blackship.png')), (spaceship_width, spaceship_height)), -90)

# # importing fire image
# BULLET_WIDTH = 30
# BULLET_HEIGHT = 30
# rightship_bullet_fire = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'bullet.png')), (BULLET_WIDTH, BULLET_HEIGHT))


def draw_on_win(white, black, right_bullets, left_bullets, rightship_health, leftship_health):
        # WIN.fill(bg_color_white)
        WIN.blit(bg_image, (0, 0))
        pygame.draw.rect(WIN, border_color_black, BORDER)
        rightship_health_txt = HEALTH_FONT.render("Health " + str(rightship_health), 1, WHITE)
        leftship_health_txt = HEALTH_FONT.render("Health " + str(leftship_health), 1, WHITE)
        WIN.blit(leftship_health_txt, (WIDTH - leftship_health_txt.get_width() - 10, 10))
        WIN.blit(rightship_health_txt, (10, 10))
        WIN.blit(whiteship_img, (white.x, white.y))
        WIN.blit(blackship_img, (black.x, black.y))
        for bullet in right_bullets:
            pygame.draw.rect(WIN, bullets_color, bullet)
            # WIN.blit(rightship_bullet_fire, (white.x, white.y))
        for bullet in left_bullets:
            pygame.draw.rect(WIN, bullets_color, bullet)
        pygame.display.update()
        
def whiteship_movement(keys_pressed, white):
        if keys_pressed[pygame.K_RIGHT] and white.x + SPEED + white.width < WIDTH: # RIGHT
            white.x += SPEED
        if keys_pressed[pygame.K_LEFT] and white.x - SPEED > BORDER.x + BORDER.width + 1: # LEFT
            white.x -= SPEED
        if keys_pressed[pygame.K_UP] and white.y - SPEED > 0: # UP
            white.y -= SPEED
        if keys_pressed[pygame.K_DOWN] and white.y + SPEED + white.width < HEIGHT: # DOWN
            white.y += SPEED
            
def blackship_movement(keys_pressed, black):
        if keys_pressed[pygame.K_d] and black.x + SPEED + black.width < BORDER.x: # RIGHT
            black.x += SPEED
        if keys_pressed[pygame.K_a] and black.x - SPEED > 0: # LEFT
            black.x -= SPEED
        if keys_pressed[pygame.K_w] and black.y - SPEED > 0: # UP
            black.y -= SPEED
        if keys_pressed[pygame.K_s] and black.y + SPEED + black.width < HEIGHT: # DOWN
            black.y += SPEED
            
def handle_bullets_hitting_ship(left_bullets, right_bullets, black, white):
    for bullet in right_bullets:
        bullet.x -= BULLET_SPEED
        if black.colliderect(bullet):
            pygame.event.post(pygame.event.Event(left_ship_hit))
            right_bullets.remove(bullet)
        elif bullet.x < 0:
            right_bullets.remove(bullet)
    for bullet in left_bullets:
        bullet.x += BULLET_SPEED
        if white.colliderect(bullet):
            pygame.event.post(pygame.event.Event(right_ship_hit))
            left_bullets.remove(bullet)
        elif bullet.x > WIDTH:
            left_bullets.remove(bullet)
            
def bullet_fire(right_bullets, left_bullets, black, white, event):
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_x and len(left_bullets) < MAX_BULLET:
            bullet = pygame.Rect(black.x + black.width, black.y + black.height//2-2, 10, 5)
            left_bullets.append(bullet)
            BULLET_FIRE_SOUND.play()
        elif event.key == pygame.K_SPACE and len(right_bullets) < MAX_BULLET:
            bullet = pygame.Rect(white.x, white.y + white.height//2-2, 10, 5)
            right_bullets.append(bullet)
            BULLET_FIRE_SOUND.play()
        
def draw_winner(text):
    draw_text = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(draw_text, (WIDTH//2 - draw_text.get_width()//2, HEIGHT//2 - draw_text.get_height()//2))
    pygame.display.update()
    pygame.time.delay(5000)

def main():
    white = pygame.Rect(700, 270, spaceship_width, spaceship_height)
    black = pygame.Rect(50, 270, spaceship_width, spaceship_height)
    
    left_bullets = []    
    right_bullets = []
    
    leftship_health  = 10
    rightship_health = 10
    bg_sound = BG_SOUND.play()
    bg_sound.set_volume(0.5)
    clock = pygame.time.Clock()
    run = True
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
                    pygame.quit()


                    
            elif event.type == right_ship_hit:
                leftship_health -= 1
                BULLET_HIT_SOUND.play()
            elif event.type == left_ship_hit:
                rightship_health -= 1
                BULLET_HIT_SOUND.play()
            bullet_fire(right_bullets, left_bullets, black, white, event)
            
                
        winner_txt = ""
        if leftship_health <= 0:
            winner_txt = "Black SpaceShip wins"
        if rightship_health <= 0:
            winner_txt = "White SpaceShip wins"
        
        if winner_txt != "":
            draw_winner(winner_txt)
            break
                
        # white.x += 1                    
        keys_pressed = pygame.key.get_pressed()
        whiteship_movement(keys_pressed, white)
        blackship_movement(keys_pressed, black)
        
            
        handle_bullets_hitting_ship(left_bullets, right_bullets, black, white)
            
        draw_on_win(white, black, right_bullets, left_bullets, rightship_health, leftship_health)
    main()
    
    
if __name__ == '__main__':
    main()