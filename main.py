import pygame
import os
import sys

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
BULLET_SPEED = 15
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

class Button(pygame.sprite.Sprite):
	def __init__(self, img, scale, x, y):
		super(Button, self).__init__()
		
		self.scale = scale
		self.image = pygame.transform.scale(img, self.scale)
		self.rect = self.image.get_rect()
		self.rect.x = x
		self.rect.y = y

		self.clicked = False

	def update_image(self, img):
		self.image = pygame.transform.scale(img, self.scale)

	def draw(self, win):
		action = False
		pos = pygame.mouse.get_pos()
		if self.rect.collidepoint(pos):
			if pygame.mouse.get_pressed()[0] and not self.clicked:
				action = True
				self.clicked = True

			if not pygame.mouse.get_pressed()[0]:
				self.clicked = False

		WIN.blit(self.image, self.rect)
		return action


# importing ship images
whiteship_img = pygame.transform.rotate(pygame.transform.scale(pygame.image.load(os.path.join('Assets/Spaceships', 'spaceship1.png')), (spaceship_width, spaceship_height)), 90)

blackship_img = pygame.transform.rotate(pygame.transform.scale(pygame.image.load(os.path.join('Assets/Spaceships', 'spaceship2.png')), (spaceship_width, spaceship_height)), -90)



# Button Image
play_img = pygame.image.load('Assets/start.png')
left_arrow = pygame.image.load('Assets/arrow.png')
right_arrow = pygame.transform.flip(left_arrow, True, False)

play_btn = Button(play_img, (150, 150), WIDTH-500, HEIGHT-200)
la_btn1 = Button(left_arrow, (32, 42), 50, 240)
ra_btn1 = Button(right_arrow, (32, 42), WIDTH-510, 240)
la_btn2 = Button(left_arrow, (32, 42), 460, 240)
ra_btn2 = Button(right_arrow, (32, 42), WIDTH-70, 240)

# importing fire image
BULLET_WIDTH = 30
BULLET_HEIGHT = 30
rightship_bullet_fire = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'bullet.png')), (BULLET_WIDTH, BULLET_HEIGHT))
leftship_bullet_fire = pygame.transform.rotate(pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'bullet.png')), (BULLET_WIDTH, BULLET_HEIGHT)), -180)


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
            # pygame.draw.rect(WIN, bullets_color, bullet)
            WIN.blit(rightship_bullet_fire, (bullet.x, bullet.y - 13))
            
        for bullet in left_bullets:
            # pygame.draw.rect(WIN, bullets_color, bullet)
            WIN.blit(leftship_bullet_fire, (bullet.x, bullet.y - 13))
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
    
    
def show_intro_screen():
    
    # LIST OF SPACESHIPS
    spaceships = []
    spaceship_type = 0
    for i in range(1, 24):
        img = pygame.image.load(f'Assets/Spaceships/spaceship{i}.png')
        img = pygame.transform.scale(img, (200, 200))
        spaceships.append(img)
    
    # Initialize player 1 and player 2 spaceship selections
    player1_spaceship = 0
    player2_spaceship = 0
    player1_selected = False
    player2_selected = False
    
    intro_font = pygame.font.Font('Assets/static/RubikIso-Regular.ttf', 33)
    select_font = pygame.font.Font('Assets/static/BebasNeue-Regular.ttf', 25)
    players_font = pygame.font.Font('Assets/static/ModernAntiqua-Regular.ttf', 20)
    
    intro_text = intro_font.render("Welcome to Faiz's 2D Spaceship Shooter Game", True, WHITE)
    text_rect = intro_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 250))
    
    selectship_text = select_font.render("Select Your Spaceship", True, WHITE)
    selectship_text_rect = selectship_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 170))
    
    Player1_text = players_font.render("Player 1", True, WHITE)
    Player1Text_rect = Player1_text.get_rect(center=(WIDTH // 2 - 210, HEIGHT // 2 - 130))
    Player2_text = players_font.render("Player 2", True, WHITE)
    Player2Text_rect = Player2_text.get_rect(center=(WIDTH // 2 + 210, HEIGHT // 2 - 130))
    

    intro = True
    while intro:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()  # Exit the script when the window is closed
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    intro = False
                    sys.exit()
                elif event.key == pygame.K_RETURN:
                    # intro = False
                    if not player1_selected:
                        player1_selected = True
                    elif not player2_selected:
                        player2_selected = True
                        intro = False

        # WIN.fill((0, 0, 0))  # Fill the screen with black
        intro_bg_image = pygame.transform.scale(pygame.image.load(os.path.join('Assets', 'bg1.jpg')), (WIDTH, HEIGHT))
        WIN.blit(intro_bg_image, (0, 0))
        WIN.blit(intro_text, text_rect)
        WIN.blit(selectship_text, selectship_text_rect)
        WIN.blit(Player1_text, Player1Text_rect)
        WIN.blit(Player2_text, Player2Text_rect)
        
        
        # Display player 1 spaceship options
        WIN.blit(spaceships[player1_spaceship], (WIDTH // 4 - 100, 170))
        if la_btn1.draw(WIN):
            player1_spaceship -= 1
            if player1_spaceship < 0:
                player1_spaceship = len(spaceships) - 1
        if ra_btn1.draw(WIN):
            player1_spaceship += 1
            if player1_spaceship >= len(spaceships):
                player1_spaceship = 0

        # Display player 2 spaceship options
        WIN.blit(spaceships[player2_spaceship], (3 * WIDTH // 4 - 100, 170))
        if la_btn2.draw(WIN):
            player2_spaceship -= 1
            if player2_spaceship < 0:
                player2_spaceship = len(spaceships) - 1
        if ra_btn2.draw(WIN):
            player2_spaceship += 1
            if player2_spaceship >= len(spaceships):
                player2_spaceship = 0

        if player1_selected and player2_selected:
            # Update the main spaceship images with selected ones
            global whiteship_img, blackship_img
            
            blackship_img = pygame.transform.rotate(pygame.transform.scale(spaceships[player1_spaceship],(spaceship_width, spaceship_height)), -90)
            
            whiteship_img = pygame.transform.rotate(pygame.transform.scale(spaceships[player2_spaceship],(spaceship_width, spaceship_height)), 90)

            intro = False
        if play_btn.draw(WIN):
            intro = False
            
        
        pygame.display.update()

def main():
    show_intro_screen()
    white = pygame.Rect(700, 270, spaceship_width, spaceship_height)
    black = pygame.Rect(50, 270, spaceship_width, spaceship_height)
    
    left_bullets = []    
    right_bullets = []
    
    myspaceships = []
    
    
    leftship_health  = 10
    rightship_health = 10
    bg_sound = BG_SOUND.play()
    bg_sound.set_volume(0.8)
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
            winner_txt = "Player 1 SpaceShip wins"
        if rightship_health <= 0:
            winner_txt = "Player 2 SpaceShip wins"
        
        if winner_txt != "":
            draw_winner(winner_txt)
            break
                
        # white.x += 1                    
        keys_pressed = pygame.key.get_pressed()
        whiteship_movement(keys_pressed, white)
        blackship_movement(keys_pressed, black)
        
        # spaceships_options(myspaceships)
        draw_on_win(white, black, right_bullets, left_bullets, rightship_health, leftship_health)
        handle_bullets_hitting_ship(left_bullets, right_bullets, black, white)
        
    main()
    
    
if __name__ == '__main__':
    main()