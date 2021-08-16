import pygame
import sys
from random import choice

pygame.init()
SCREENWIDTH, SCREENHEIGHT = 500, 500
screen = pygame.display.set_mode((SCREENWIDTH, SCREENHEIGHT), 0, 32)
pygame.display.set_caption("Mouse Escape")
white_color = (255, 255, 255)
black_color = (0, 0, 0)
blue_color = (50, 80, 100)
green_color = (50, 150, 80)
red_color = (180, 40, 50)
grey_color = (150, 150, 150)

number_of_tiles = 7
side_spaces = 2
tiles_width = int(SCREENWIDTH / (number_of_tiles + side_spaces))
tiles_height = tiles_width
seperation_line_width = 1

initial_x = tiles_width
initial_y = initial_x

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
frame_width = frame_height
frame = pygame.Surface((frame_height, frame_width))
frame.fill(white_color)
frame_rect = frame.get_rect()
frame_rect.x = tiles_width - 2
frame_rect.y = tiles_width - 2


mouse_died = False

number_of_moves = 0
game_won = False
clock = pygame.time.Clock()
fps = 5

angle = 0


def handle_events():

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()


def make_rectangles():
    global initial_x, initial_y, tiles_width, tiles_height
    # Use global here because we will need to modify these variables which were already defined
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
        initial_y += tiles_width + seperation_line_width


def draw_board():
    # Draw the frame , these are the arguments(surface, color, rectangle, width)
    pygame.draw.rect(screen, white_color, frame_rect, 2)

    # Draw all the rectangles on top of that surface
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
    global mouse, mouse_rectangle, cat, cat_rectangle
    cat_x = choice(allowed_x)
    cat_y = choice(allowed_y)

    mouse_x = [x for x in allowed_x if not x == cat_x]
    mouse_y = [y for y in allowed_y if not y == cat_y]

    cat = pygame.image.load("cat.png")
    cat = pygame.transform.scale(cat, (tiles_width, tiles_height))
    cat_rectangle = cat.get_rect()
    cat_rectangle.x = cat_x
    cat_rectangle.y = cat_y

    mouse = pygame.image.load("mouse_normal.png")
    mouse = pygame.transform.scale(mouse, (tiles_width, tiles_height))
    mouse_rectangle = mouse.get_rect()
    mouse_rectangle.x = choice(mouse_x)
    mouse_rectangle.y = choice(mouse_y)


create_mouse_and_cat()


def update_mouse():
    global mouse, mouse_rectangle,  mouse_died, number_of_moves, game_won, angle

    direction = choice(["Vertical", "Horizontal"])
    motion_distance = int(tiles_width + seperation_line_width)
    orientation = choice([-motion_distance, motion_distance])


    if direction == "Vertical":
        if orientation == -motion_distance:
            angle = 180
        else:
            angle = 0
        mouse_rectangle.y += orientation

    else:
        if orientation == -motion_distance:
            angle = -90
            look_left = True
        else:
            angle = 90
            
        mouse_rectangle.x += orientation
    number_of_moves += 1


    if (mouse_rectangle.x, mouse_rectangle.y) in forbidden:
        mouse_died = True

    if mouse_rectangle.x == cat_rectangle.x and mouse_rectangle.y == cat_rectangle.y:
        mouse_died = True

    if number_of_moves == 20:
        mouse_died = True

    if mouse_rectangle.x == bridge_rectangle[0].x and mouse_rectangle.y == bridge_rectangle[0].y:
        game_won = True


def draw_mouse_and_cat():
    mouse_rotated = pygame.transform.rotate(mouse, angle)

    screen.blit(mouse_rotated, mouse_rectangle)
    screen.blit(cat, cat_rectangle)

def game_end():
    wining_image = pygame.image.load("Victory")
    wining_image = pygame.transform.scale(wining_image, (SCREENWIDTH, SCREENHEIGHT))
    screen.blit(wining_image, (0, 0))


while True:
    screen.fill(black_color)
    handle_events()
    angle = 0
    
    if game_won:
        game_end()

    else:
        draw_board()
        if not mouse_died:
            update_mouse()
        else:
            create_mouse_and_cat()
            number_of_moves = 0
            mouse_died = False
        draw_mouse_and_cat()
    
    clock.tick(fps)

    pygame.display.update()


