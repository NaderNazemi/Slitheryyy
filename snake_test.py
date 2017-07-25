import pygame, random
pygame.init()
red, green, blue, black, white = (200,0,0), (0,155,0), (0,0,200), (0,0,0), (255,255,255)
bright_red, bright_green = (255,0,0), (0,255,0)
display_width, display_height = 800, 600
gameDisplay = pygame.display.set_mode((display_width, display_height))
pygame.display.set_caption('Slithery Snake')
clock = pygame.time.Clock()
crash_sound = pygame.mixer.Sound('Crash.wav')
eat_sound = pygame.mixer.Sound('Eat.wav')
snake_block = 20 
apple_block = 20 
FPS = 25
direction = 'right'
screen_font = pygame.font.SysFont(None, 50)
button_font = pygame.font.SysFont(None, 30)
score_font = pygame.font.SysFont(None, 20)
snake_img = pygame.image.load('snake2.png') 
apple_img = pygame.image.load('apple2.png')  
pause = False
###############################################################################
def upper_screen_boundary():
    pygame.draw.line(gameDisplay, black, (0,0),(800,0),1)
###############################################################################
def game_quit(): 
    pygame.quit()
    quit()
###############################################################################
def button(msg, x, y ,w, h, inactive_color, active_color, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if x < mouse[0] < (x+w) and y < mouse[1] < (y+h):
        pygame.draw.rect(gameDisplay, active_color, (x,y,w,h))
        if click[0] == 1 and action != None:
            action()
    else:
        pygame.draw.rect(gameDisplay, inactive_color, (x,y,w,h))
    
    button_text = button_font.render(msg, True, black)
    gameDisplay.blit(button_text, ((x+(w/4.5)),(y+(h/2))))
###############################################################################
def screen_message(msg, color):
    pygame.mixer.Sound.play(crash_sound)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_quit()     
        screen_text = screen_font.render(msg, True, color)
        gameDisplay.blit(screen_text, [display_width/2.5, display_height/2])       
        button('Quit', 550, 450, 140, 50, bright_red, red, game_quit)
        button('Play Again', 150, 450, 140, 50, bright_green, green, game_loop)        
        pygame.display.update()
        clock.tick(15)
###############################################################################
def game_intro():
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        gameDisplay.fill(white)
        screen_text = screen_font.render('Slithery', True, black)
        gameDisplay.blit(screen_text, [display_width/2.5, display_height/2]) 
        
        screen_text = screen_font.render('Eat Apples to Grow', True, black)
        gameDisplay.blit(screen_text, [display_width/3.5, display_height/4])
        
        button('START', 150, 450, 110, 50, bright_green, green, game_loop)
        button('QUIT', 550, 450, 100, 50, bright_red, red, game_quit)            
        pygame.display.update()
        clock.tick(15)        
###############################################################################
def paused(): 
    screen_text = screen_font.render('PAUSED', True, black)
    gameDisplay.blit(screen_text, [display_width/5, display_height/3])     
    while pause:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()            
        button('Continue', 150, 450, 120, 50, bright_green, green, unpaused)
        button('QUIT', 550, 450, 100, 50, bright_red, red, game_quit)            
        pygame.display.update()
        clock.tick(15)   
###############################################################################
def unpaused():
    global pause
    pause = False        
###############################################################################
def draw_snake(snake_block, snake_list):
    
    if direction == 'right':
        rotated_snake_img = pygame.transform.rotate(snake_img, 270) # counter clock-wise
    if direction == 'left':
        rotated_snake_img = pygame.transform.rotate(snake_img, 90)
    if direction == 'up':
        rotated_snake_img = pygame.transform.rotate(snake_img, 0)
    if direction == 'down':
        rotated_snake_img = pygame.transform.rotate(snake_img, 180)
    gameDisplay.blit(rotated_snake_img, (snake_list[-1][0], snake_list[-1][1]))
    for XnY in snake_list[:-1]:
        pygame.draw.rect(gameDisplay, green, [XnY[0], XnY[1], snake_block, snake_block]) 
###############################################################################
def draw_apple(apple_x, apple_y, apple_block):
    gameDisplay.blit(apple_img, (apple_x, apple_y))
###############################################################################
def score_counter(score):
    text = score_font.render('Score: ' + str(score), True, black)
    gameDisplay.blit(text, (0,0))
###############################################################################
def game_loop():
    lead_x = (display_width * 0.5)
    lead_y = (display_height * 0.5)
    lead_x_change = 10 
    lead_y_change = 0
    apple_x = random.randrange(0, display_width - apple_block, apple_block) 
    apple_y = random.randrange(0, display_height - apple_block, apple_block) 
    score = 0
    snake_list = []
    snake_length = 1
    global direction
    global pause
    direction = 'right'
    gameExit = False
    while not gameExit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    lead_x_change = -snake_block
                    lead_y_change = 0
                    direction = 'left'
                elif event.key == pygame.K_RIGHT:
                    lead_x_change = +snake_block
                    lead_y_change = 0
                    direction = 'right'
                elif event.key == pygame.K_UP:
                    lead_y_change = -snake_block
                    lead_x_change = 0
                    direction = 'up'
                elif event.key == pygame.K_DOWN:
                    lead_y_change = +snake_block
                    lead_x_change = 0
                    direction = 'down'
                elif event.key == pygame.K_SPACE:
                    pause = True
                    paused()
        
        lead_x += lead_x_change
        lead_y += lead_y_change
        
        if lead_x > (display_width - snake_block) or lead_x < 0 or lead_y > (display_height - snake_block) or lead_y < 0:
            screen_message('Game Over', red)
               
        if lead_x + snake_block > apple_x and lead_x < apple_x + apple_block:
            if lead_y + snake_block > apple_y and lead_y < apple_y + apple_block:
                apple_x = round(random.randrange(0, display_width-snake_block))
                apple_y = round(random.randrange(0, display_height-snake_block))
                score += 1
                snake_length +=1 
                pygame.mixer.Sound.play(eat_sound) 
               
        gameDisplay.fill(white)
        upper_screen_boundary()
        draw_apple(apple_x, apple_y, apple_block)
        snake_head = []
        snake_head.append(lead_x)
        snake_head.append(lead_y)
        snake_list.append(snake_head)

        if len(snake_list) > snake_length:
            del snake_list[0]
            
        for square_coordinates in snake_list[:-1]:
            if square_coordinates == snake_head:
                screen_message('Game Over', red)
        
        draw_snake(snake_block, snake_list)
        score_counter(score)
        pygame.display.update()
        clock.tick(FPS)
    
game_intro()    
game_loop()