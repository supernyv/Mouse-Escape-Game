import pygame
from sys import exit
from random import choice

pygame.mixer.init()
pygame.init()
SCREENWIDTH, SCREENHEIGHT = 700, 700
screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT), 0, 32)
pygame.display.set_caption("Mouse Escape")
white_color = (255, 255, 255)
black_color = (0, 0, 0)
blue_color = (50, 80, 100)
green_color = (50, 150, 80)
red_color = (180, 40, 50)
grey_color = (150, 150, 150)
die_sound = pygame.mixer.Sound("die.wav")
win_sound = pygame.mixer.Sound("win.wav")
eating_sound = pygame.mixer.Sound("eat.wav")

number_of_tiles = 9
side_spaces = 2
tiles_width = int(SCREENWIDTH / (number_of_tiles + side_spaces))
tiles_height = int(SCREENHEIGHT / (number_of_tiles + side_spaces))
seperation_line_width = 1

initial_x = tiles_width
initial_y = tiles_height

island_rectangles = []
water_rectangles = []
bridge_rectangle = []
# Create reference index to seperate board rectangles and water rectangles
water_references = []
for y in range(number_of_tiles):
    water_references.append((0, y))
    water_references.append((number_of_tiles - 1, y))
for y in range(1, number_of_tiles - 1):
    water_references.append((y, 0))
    water_references.append((y, number_of_tiles - 1))

# For the frame on  which the game board is
frame_height = int(number_of_tiles * (tiles_width + seperation_line_width) + 2 * seperation_line_width)
frame_width = int(number_of_tiles * (tiles_height + seperation_line_width) + 2 * seperation_line_width)
frame = pygame.Surface((frame_width, frame_height))
frame.fill(white_color)
frame_rect = frame.get_rect()
frame_rect.x = tiles_width - 2
frame_rect.y = tiles_height - 2

mouse_died = False
cheese_eaten = False

number_of_moves = 20
game_won = False
play_victory = False
clock = pygame.time.Clock()
speed = 5

angle = 0

def handle_events():

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

def make_rectangles():
    """Create rectangles to hold all the game tiles"""
    global initial_x, initial_y, tiles_width, tiles_height

    for x in range(number_of_tiles):
        for y in range(number_of_tiles):
            a_rectangle = pygame.Rect(initial_x, initial_y, tiles_width, tiles_height)
            if (x, y) in water_references:
                if (x, y) == (int(number_of_tiles / 2), number_of_tiles - 1):
                    bridge_rectangle.append(a_rectangle)
                else:
                    water_rectangles.append(a_rectangle)
            else:
                island_rectangles.append(a_rectangle)
            # Move to the next column
            initial_x += tiles_width + seperation_line_width
        # Now reinitialize x position to move down (reinitialize columns)
        initial_x = tiles_width
        # And move to the next row starting at first column
        initial_y += tiles_height + seperation_line_width


def draw_board():
    """Draw the game board"""
    # Draw the frame , these are the arguments(surface, color, rectangle, width)
    pygame.draw.rect(screen, white_color, frame_rect, 2)

    # Draw all the rectangles on top
    for rect in island_rectangles:
        pygame.draw.rect(screen, white_color, rect)

    for rect in water_rectangles:
        pygame.draw.rect(screen, blue_color, rect)

    # Display the bridge too
    pygame.draw.rect(screen, green_color, bridge_rectangle[0])


# Call the make_board function to create the board before the game starts
make_rectangles()

allowed_x = [rect.x for rect in island_rectangles]
allowed_y = [rect.y for rect in island_rectangles]

forbidden = [(rect.x, rect.y) for rect in water_rectangles]

def create_mouse_and_cat():
    """Load mouse and cat images and position them"""
    
    global mouse, mouse_rectangle, mouse_x, mouse_y, cat, cat_rectangle, cat_x, cat_y, flash
    cat_x = choice(allowed_x)
    cat_y = choice(allowed_y)

    mouse_x = choice([x for x in allowed_x if not x == cat_x])
    mouse_y = choice([y for y in allowed_y if not y == cat_y])

    cat = pygame.image.load("cat.png").convert_alpha()
    cat = pygame.transform.scale(cat, (tiles_width, tiles_height)).convert_alpha()
    cat_rectangle = cat.get_rect()
    cat_rectangle.x = cat_x
    cat_rectangle.y = cat_y

    mouse = pygame.image.load("mouse.png").convert_alpha()
    mouse = pygame.transform.scale(mouse, (tiles_width, tiles_height)).convert_alpha()
    mouse_rectangle = mouse.get_rect()
    mouse_rectangle.x = mouse_x
    mouse_rectangle.y = mouse_y
    flash = pygame.Surface((tiles_width, tiles_height))
    flash.fill(red_color)

def create_cheese():
    """Load cheese image and position it"""
    
    global cheese, cheese_rectangle
    locations = [(rect.x, rect.y) for rect in island_rectangles
                if not (rect.x, rect.y) == (cat_x, cat_y)
                and not (rect.x, rect.y) == (mouse_x, mouse_y)]

    cheese_x, cheese_y = choice(locations)
    cheese = pygame.image.load("cheese.png").convert_alpha()
    cheese = pygame.transform.scale(cheese, (tiles_width, tiles_height)).convert_alpha()
    cheese_rectangle = cheese.get_rect()
    cheese_rectangle.x = cheese_x
    cheese_rectangle.y = cheese_y

create_mouse_and_cat()
create_cheese()

def update_mouse():
    """Update the mouse position and state as the game proceeds"""
    
    global mouse, mouse_died, number_of_moves, game_won 
    global angle, play_victory, cheese_eaten

    direction = choice(["Vertical", "Horizontal"])
    motion_distance = int(tiles_width + seperation_line_width)
    orientation = choice([-motion_distance, motion_distance])

    _move_randomly(direction, orientation, motion_distance)
    
    number_of_moves -= 1
    #print("Number of moves left: ", number_of_moves)

    if (mouse_rectangle.x, mouse_rectangle.y) in forbidden:
        mouse_died = True
        #print("Drowned")
    if (mouse_rectangle.x, mouse_rectangle.y) == (cat_rectangle.x, cat_rectangle.y):
        mouse_died = True
        #print("Killed by Cat")
    if number_of_moves == 0:
        mouse_died = True
        #print("Out of moves")
    if (mouse_rectangle.x, mouse_rectangle.y) == (bridge_rectangle[0].x, bridge_rectangle[0].y):
        game_won = True
        play_victory = True

    if number_of_moves <= 10:
        if cheese_eaten == False:
            if (mouse_rectangle.x, mouse_rectangle.y) == (cheese_rectangle.x, cheese_rectangle.y):
                number_of_moves += 5
                cheese_eaten = True
                eating_sound.play()
                #print("Cheese Eaten!")

def _move_randomly(direction, orientation, motion_distance):
    """Random motion of the mouse without user input"""

    global angle, mouse_rectangle
    if direction == "Vertical":
        if orientation == -motion_distance:
            angle = 180
        else:
            angle = 0
        mouse_rectangle.y += orientation

    else:
        if orientation == -motion_distance:
            angle = -90
        else:
            angle = 90
        mouse_rectangle.x += orientation

def _move_following_cheese():
    pass

def show_mouse_and_cat():
    """Draw mouse and cat to the screen"""
    if mouse_died:
        screen.blit(flash, (mouse_rectangle.x, mouse_rectangle.y))
        
    mouse_rotated = pygame.transform.rotate(mouse, angle)

    screen.blit(mouse_rotated, mouse_rectangle)
    screen.blit(cat, cat_rectangle)

def show_cheese():
    """Draw the cheese to the screen"""
    global cheese_rectangle, cheese

    if cheese_eaten == False:
        screen.blit(cheese, cheese_rectangle)

def game_end():
    """End the game when the mouse reaches the bridge"""
    global play_victory
    wining_image = pygame.image.load("mouse.png").convert_alpha()
    wining_image = pygame.transform.scale(wining_image, (SCREENWIDTH, SCREENHEIGHT)).convert_alpha()
    screen.blit(wining_image, (0, 0))
    if play_victory == True:
        win_sound.play()
        play_victory = False

def speed_bar():
    """Chose the speed of the mouse"""
    speed_1 = 5
    speed_2 = 10
    speed_3 = 15
    speed_3 = 20

while True:
    screen.fill(black_color)
    handle_events()
    angle = 0
    clock.tick(speed)
    
    if game_won:
        game_end()

    else:
        draw_board()
        if number_of_moves <= 10:
            show_cheese()
            #print("Cheese appeared")
            
        if not mouse_died:
            update_mouse()
            
        else:
            create_mouse_and_cat()
            create_cheese()
            number_of_moves = 20
            die_sound.play()
            cheese_eaten = False
            mouse_died = False

        show_mouse_and_cat()

    pygame.display.update()


