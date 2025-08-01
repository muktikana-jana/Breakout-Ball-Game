import pygame
import random

# initializing the game
pygame.init()

# window setting
winWidth = 800
winHeight = 500
window = pygame.display.set_mode((winWidth,winHeight))
pygame.display.set_caption("Breakout Ball game")
default_font = pygame.font.Font(None, 36)

# Background music setting
pygame.mixer.music.load("Background_Music.mp3")
pygame.mixer.music.play(-1)
pygame.mixer.music.set_volume(0.6)

# sound setting
brickHit_sound = pygame.mixer.Sound("Brick_Hit.wav") 
brickHit_sound.set_volume(0.2)
gameOver_sound = pygame.mixer.Sound("Game_Over.wav") 

# paddle setting
paddle_x = winWidth//2-50 # paddle position in horizontally
paddle_y = 400 # paddle position in vertically
paddle_width = 100
paddle_height = 20
paddle_speed = 35

# ball setting
ball_x = winWidth//2 # ball position in horizontally
ball_y = winHeight//2 # ball position in vertically
ball_radius = 10
ball_speed_x = 15
ball_speed_y = -15

# bricks setting
bricks_arr = []
bricks_cols = 8
bricks_rows = 5
bricks_width = winWidth // bricks_cols
bricks_height = 20
for row in range (bricks_rows):
    for col in range (bricks_cols):
        bricks_x = bricks_width*col
        bricks_y = bricks_height*row
        color = (random.randint(50,255),random.randint(50,255),random.randint(50,255))
        bricks_arr.append({"rect": pygame.Rect(bricks_x, bricks_y, bricks_width, bricks_height), "color":color})

# after losing a live the ball will be reset
def reset_ball():
    global ball_x,ball_y,ball_speed_x,ball_speed_y
    ball_x = winWidth//2 
    ball_y = winHeight//2 
    ball_speed_x = 15
    ball_speed_y = -15

# before starting the game
start_text = default_font.render("Press SPACE to Start", False, (255, 255, 255)) # render is used to tool for drawing / True is used to smoothness draw
window.blit(start_text, (winWidth // 2-120 , winHeight // 2)) # draw the text on the window 
pygame.display.update() #updating display over the frame rate

score = 0 # inialize the score
lives = 3 # initialize the lives

# initialize gaming state
running = False
paused = False

# executing code start at the here
run = True
while run:
    # frame rate
    pygame.time.delay(50)
    
    # changing gaming state by the user
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False   # game will be closed use Close button
        if event.type == pygame.KEYDOWN: # for using keyboard keys
            if event.key == pygame.K_SPACE: 
                if running == False:
                    running = True  # game will be start
                else:
                    paused = not paused   # game will be paused or resume

    if running and not paused:
        # moving the paddle
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and paddle_x > 0:
            paddle_x -= paddle_speed
        if keys[pygame.K_RIGHT] and paddle_width+paddle_x < winWidth:
            paddle_x += paddle_speed

        # moving the ball
        ball_x += ball_speed_x
        ball_y += ball_speed_y

        # collison with wall
        if (ball_x<=0 or ball_x+ball_radius>=winWidth):
            ball_speed_x *= -1

        # collison with top
        if (ball_y<=0):
            ball_speed_y *= -1

        # collison with paddle
        if (paddle_y<=ball_y+ball_radius<=paddle_y+paddle_height and paddle_x<=ball_x+ball_radius<=paddle_x+paddle_width):
            ball_speed_y *= -1

        # collision with brick
        for brick in bricks_arr:
            if (brick["rect"].collidepoint(ball_x, ball_y)):
                bricks_arr.remove(brick)
                ball_speed_y *= -1
                brickHit_sound.play()
                score += 10

        # missing paddle
        if (ball_y>=paddle_y+paddle_height): #(ball_y+ball_radius>=paddle_y+paddle_height)
            lives -= 1
            if lives>0:
                reset_ball()
            else:
                gameOver_sound.play()
                run = False

        # drawing everything
        window.fill((0,0,0))
        # bgImg = pygame.image.load("bg2.png")
        # window.blit (bgImg, (160,10))
        pygame.draw.rect(window,(255,255,255),(paddle_x,paddle_y,paddle_width,paddle_height))
        pygame.draw.circle(window,(255,255,255),(ball_x,ball_y),ball_radius)
        for brick in bricks_arr:
            pygame.draw.rect(window,brick["color"],brick["rect"])

        #displaying scoreboard
        score_txt = default_font.render(f"Score:{score}            Lives:{lives}", True, (255,255,255))
        window.blit(score_txt, (260,450))
        
        pygame.display.update() #updating display over the frame rate

# after game over showing Final Scoreboard
window.fill((0,0,0))
Gameover_txt = default_font.render("Game Over", True, (255,255,255))
finalScore_txt = default_font.render(f"Your Score is : {score}", True, (41, 41, 41), (235, 234, 232))
window.blit(Gameover_txt, (winWidth//2-80,winHeight//2-30))
window.blit(finalScore_txt, (winWidth//2-120,winHeight//2+40))

pygame.display.update() #updating display over the frame rate

# waiting for user closing input
waiting = True
while waiting:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            waiting = False

# ending the game
pygame.quit()