# Author: Zimehr Abbasi
# Course: COSC 1
# Date: 02/02/2020
# Purpose: Pong

from cs1lib import *
import random
import math

# Window settings
FRAMERATE = 100
WIDTH = 600
HEIGHT = 400

# Paddle settings
SPEED = HEIGHT/80
player_1_length = HEIGHT/5
player_2_length = HEIGHT/5
PLAYER1_STARTING_POSITION = (HEIGHT-player_1_length)/2
PLAYER2_STARTING_POSITION = (HEIGHT-player_2_length)/2
current_position_player1 = PLAYER1_STARTING_POSITION
current_position_player2 = PLAYER2_STARTING_POSITION
WIDTH_PLAYER1 = 10
WIDTH_PLAYER2 = 10

# The location of the start of the ball
STARTING_VALUE_BALL_X = WIDTH/2
STARTING_VALUE_BALL_Y = HEIGHT/2

# Current value of balls
x = STARTING_VALUE_BALL_X
y = STARTING_VALUE_BALL_Y

# Speed settings of the ball
SPEED_MULTIPLIER = WIDTH/400
x_speed = 0
y_speed = 0

def set_speed():
    global x_speed, y_speed

    x_speed = (random.randint(-1, 1)) * SPEED_MULTIPLIER
    y_speed = (random.randint(-1, 1)) * SPEED_MULTIPLIER

    if x_speed == 0 or y_speed == 0:
        set_speed()

set_speed()
MAX_SPEED = WIDTH/40

# Variables to check key input
a_press = False
z_press = False
k_press = False
m_press = False

# User scores
score_player_1 = 0
score_player_2 = 0

# Start and Pause boolean
start = False
pause = False

# Display settings of the ball
r = random.randint(25, 255) / 255
g = random.randint(25, 255) / 255
b = random.randint(25, 255) / 255
BALL_SIZE = WIDTH/75

# Paddle 1 color
rp1 = 1
gp1 = 1
bp1 = 1

# Paddle 2 color
rp2 = 1
gp2 = 1
bp2 = 1

# Power up deciders and display variables
last_touch = ''
active = False
x_power = 200
y_power = 200
choice = 6
POWER_RADIUS = 10

# Booleans to check powerups
invincibilityp1 = False
invincibilityp2 = False
distortion = False
invertp1 = False
invertp2 = False
slowp1 = False
slowp2 = False

# Finisher settings
factor = 1
shoot = False
finisherp1 = False
finisherp2 = False
FINISHER_VIEW = HEIGHT/10

# Trajectory of ball during finisher
x_change = 0
y_change = 0

# User touches
player1_touches = 0
player2_touches = 0

# Minimum and Maximum touches required to enable power up
MAX_POWER = 40
MIN_POWER = 0

# Power up time, text scaling factor
count = 0
TIME = 5
MAX_COUNT = TIME * FRAMERATE
COUNT_SCALE_FACTOR_FOR_TEXT = 2/5

# Randomised speed converter
speed_converter = 0.1/MAX_SPEED

# Font settings
FONT_SIZE = math.sqrt(HEIGHT)
FONT_NAME = 'Monaco'
SCORE_HEIGHT_FROM_TOP = 15 + FONT_SIZE

# Check which key has been pressed
def get_key_down(key):
    global a_press, z_press, k_press, m_press

    if str(key) == 'a':
        a_press = True

    if str(key) == 'z':
        z_press = True

    if str(key) == 'k':
        k_press = True

    if str(key) == 'm':
        m_press = True


# Check which key has been pressed
def get_key_up(key):
    global current_position_player1, current_position_player2, SPEED, a_press, z_press, k_press, m_press, x, y, x_speed, \
        y_speed, score_player_1, score_player_2, start, player1_touches, player2_touches, finisherp1, finisherp2, shoot, last_touch, \
        STARTING_VALUE_BALL_X, STARTING_VALUE_BALL_Y, WIDTH, HEIGHT, MAX_POWER, SPEED_MULTIPLIER

    if str(key) == 'a':
        a_press = False

    if str(key) == 'z':
        z_press = False

    if str(key) == 'k':
        k_press = False

    if str(key) == 'm':
        m_press = False

    if not finisherp1 and not finisherp2:

        # Restarts game
        if str(key) == ' ' and not start:
            reset_game()
            start = True
    else:

        # Enables finisher
        if str(key) == ' ':
            if finisherp1 or finisherp2:
                shoot = True

    if str(key) == 'q':
        quit()

    # Finisher for Player 1
    if str(key) == 'w':
        if player1_touches >= MAX_POWER and last_touch == 'P2' and x < WIDTH/2:
            finisherp1 = True
            last_touch = "P1"
            player2_touches = MAX_POWER/2

    # Finisher for Player 2
    if str(key) == 'i':
        if player2_touches >= MAX_POWER and last_touch == 'P1' and x > WIDTH/2:
            finisherp2 = True
            last_touch = "P2"
            player1_touches = MAX_POWER/2


def reset_game():
    global current_position_player1, current_position_player2, x, y, x_speed, y_speed

    current_position_player1 = PLAYER1_STARTING_POSITION
    current_position_player2 = PLAYER2_STARTING_POSITION
    x = STARTING_VALUE_BALL_X
    y = STARTING_VALUE_BALL_Y
    set_speed()



# Paddle Display updated
def update_paddles():
    global current_position_player1, current_position_player2, player_1_length, player_2_length, rp1, rp2, gp1,gp2, bp1, bp2, WIDTH, \
        BALL_SIZE, WIDTH_PLAYER1, WIDTH_PLAYER2

    set_fill_color(rp1, gp1, bp1)
    draw_rectangle(0, current_position_player1, WIDTH_PLAYER1, player_1_length)

    set_fill_color(rp2, gp2, bp2)
    draw_rectangle(WIDTH - WIDTH_PLAYER2, current_position_player2, WIDTH_PLAYER2, player_2_length)


# Ball display updated
def update_ball():
    global x, y, r, g, b, img

    set_stroke_color(r, g, b)
    set_fill_color(r, g, b)
    if r < 0.2 and g < 0.2:
        set_stroke_color(1, 1, 1)
    elif b < 0.2 and g < 0.2:
        set_stroke_color(1, 1, 1)
    elif b < 0.2 and r < 0.2:
        set_stroke_color(1, 1, 1)

    draw_circle(x, y, 7)


def contact():
    global x, y, x_speed, y_speed, current_position_player1, current_position_player2, a_press, z_press, k_press, \
        m_press, score_player_1, score_player_2, r, g, b, last_touch, x_power, y_power, choice, active, player_2_length, player_1_length, \
        invincibilityp1, invincibilityp2, speed_converter, player1_touches, player2_touches, STARTING_VALUE_BALL_X, \
        STARTING_VALUE_BALL_Y, WIDTH, HEIGHT, BALL_SIZE, WIDTH_PLAYER1, WIDTH_PLAYER2, POWER_RADIUS, SPEED_MULTIPLIER, \
        MAX_SPEED, start

    # Bouncing ball off the top and bottom bounds of the window
    if y <= BALL_SIZE:

        # Reverse direction of motion in y axis
        y_speed = -y_speed

        # Random bouncing
        x_speed = x_speed + (random.randint(0, 200) - 100) / 50
        speed_converter = 0
        y = BALL_SIZE

    elif y >= HEIGHT - BALL_SIZE:

        # Reverse direction of motion in y axis
        y_speed = -y_speed

        # Random bouncing
        x_speed = x_speed + (random.randint(0, 200) - 100) / 50
        speed_converter = 0
        y = HEIGHT - BALL_SIZE

    else:
        speed_converter = 0.1/MAX_SPEED

    # Ball bounce off paddle 1
    if current_position_player1 <= y <= current_position_player1 + player_1_length and x <= WIDTH_PLAYER1 + BALL_SIZE:

        # Reverse direction of motion in x axis
        x_speed = -x_speed

        # Randomise the bounce
        y_speed = y_speed + (random.randint(0, 200) - 100) / 50

        # Add half the speed of the paddle to the ball
        if a_press:
            y_speed -= SPEED/2
        elif z_press:
            y_speed += SPEED/2

        # Randomise color of ball
        r = random.randint(25, 255) / 255
        g = random.randint(25, 255) / 255
        b = random.randint(25, 255) / 255

        # The ball last touches P1 if a power up is not currently active
        if not active:
            last_touch = 'P1'

        # Increase the number of touches of P1
        player1_touches = player1_touches + 20

    # Ball bounce off paddle 2
    if current_position_player2 <= y <= current_position_player2 + player_2_length and x >= WIDTH - (WIDTH_PLAYER2 + BALL_SIZE):

        # Reverse direction of motion in x axis
        x_speed = -x_speed

        # Randomise the bounce
        y_speed = y_speed + (random.randint(0, 200) - 100) / 50

        # Add half the speed of the paddle to the ball
        if k_press:
            y_speed -= SPEED/2
        elif m_press:
            y_speed += SPEED/2

        # Randomise color of ball
        r = random.randint(25, 255) / 255
        g = random.randint(25, 255) / 255
        b = random.randint(25, 255) / 255

        # The ball last touches P2 if a power up is not currently active
        if not active:
            last_touch = 'P2'

        # Increase the number of touches of P2
        player2_touches = player2_touches + 20

    # Check if the ball collides with the power up
    if x_power - POWER_RADIUS < x < x_power + POWER_RADIUS and y_power - POWER_RADIUS < y < y_power + POWER_RADIUS:
        active = True

    # Contact with the vertical ball of P1 when P1 is not invincible
    if x <= WIDTH - WIDTH and not invincibilityp1:

        # Increase score of P2
        score_player_2 += 1

        # Remove a touch from P1
        player1_touches = player1_touches - 1

        # Restart game
        reset_game()

        # Assign empty string to last touch at the beginning of game
        last_touch = ''

        start = False

    # Contact with the vertical ball of P1 when P1 is invincible
    elif x <= WIDTH - WIDTH and invincibilityp1:

        # Behave like a wall
        x_speed = -x_speed

    # Contact with the vertical ball of P2 when P2 is not invincible
    if x >= WIDTH and not invincibilityp2:

        # Increase score of P1
        score_player_1 += 1

        # Remove a touch from P2
        player1_touches = player1_touches - 1

        # Restart game
        reset_game()

        # Assign empty string to last touch at the beginning of game
        last_touch = ''

        start = False

    # Contact with the vertical ball of P2 when P2 is invincible
    elif x >= WIDTH and invincibilityp2:

        # Behave like a wall
        x_speed = -x_speed


# Randomise location and type of power up
def power_ups():
    global x_power, y_power, choice

    x_power = random.randint(WIDTH//15, WIDTH - WIDTH//15)
    y_power = random.randint(HEIGHT//20, HEIGHT - HEIGHT//20)
    choice = random.randint(1, 15)


# Display Power up
def draw_power_ups():
    global x_power, y_power, choice, POWER_RADIUS

    if 1 <= choice <= 5:
        set_stroke_color(1, 1, 1)
        set_fill_color(1, 0, 0)
        draw_circle(x_power, y_power, POWER_RADIUS)
    elif 5 < choice <= 9:
        set_stroke_color(1, 1, 1)
        set_fill_color(0, 1, 0)
        draw_circle(x_power, y_power, POWER_RADIUS)
    elif 9 < choice <= 12:
        set_stroke_color(1, 1, 1)
        set_fill_color(0, 0, 1)
        draw_circle(x_power, y_power, POWER_RADIUS)
    elif 12 < choice <= 14:
        set_stroke_color(1, 1, 1)
        set_fill_color(0, 1, 1)
        draw_circle(x_power, y_power, POWER_RADIUS)
    elif 14 < choice <= 15:
        set_stroke_color(1, 1, 1)
        set_fill_color(1, 1, 0)
        draw_circle(x_power, y_power, POWER_RADIUS)


# Assigns power up to player
def assign_power_ups(player):
    global choice, player_1_length, player_2_length, rp1, rp2, gp1,gp2, bp1, bp2, invincibilityp1, invincibilityp2, distortion, \
        invertp1, invertp2, slowp1, slowp2, LENGTH_FACTOR, WIDTH, HEIGHT

    if player == 'P1':
        if 1 <= choice <= 5:
            player_1_length = HEIGHT/4
            rp1 = 1
            gp1 = 0
            bp1 = 0
        elif 6 <= choice <= 9:
            invincibilityp1 = True
            rp1 = 0
            gp1 = 1
            bp1 = 0
        elif 10 <= choice <= 12:
            distortion = True
            rp1 = 0
            gp1 = 0
            bp1 = 1
        elif 13 <= choice <= 14:
            invertp2 = True
            rp1 = 0
            gp1 = 1
            bp1 = 1
        elif choice == 15:
            slowp2 = True
            rp1 = 1
            gp1 = 1
            bp1 = 0
        else:
            pass
    elif player == 'P2':
        if 1 <= choice <= 5:
            player_2_length = HEIGHT/4
            rp2 = 1
            gp2 = 0
            bp2 = 0
        elif 6 <= choice <= 9:
            invincibilityp2 = True
            rp2 = 0
            gp2 = 1
            bp2 = 0
        elif 10 <= choice <= 12:
            distortion = True
            rp2 = 0
            gp2 = 0
            bp2 = 1
        elif 13 <= choice <= 14:
            invertp1 = True
            rp2 = 0
            gp2 = 1
            bp2 = 1
        elif choice == 15:
            slowp1 = True
            rp2 = 1
            gp2 = 1
            bp2 = 0
        else:
            pass
    else:
        pass


# Main loop
def game():
    global current_position_player1, current_position_player2, SPEED, x, y, x_speed, y_speed, score_player_1, score_player_2, active, \
        choice, last_touch, player_1_length, player_2_length, count, rp1, rp2, gp1, gp2, bp1, bp2, invincibilityp1, invincibilityp2, \
        speed_converter, distortion, invertp2, invertp1, slowp1, slowp2, player1_touches, player2_touches, finisherp1, finisherp2, \
        pause, x_change, y_change, factor, shoot, WIDTH, HEIGHT, LENGTH_FACTOR, MAX_COUNT, COUNT_SCALE_FACTOR_FOR_TEXT, \
        FINISHER_VIEW, MAX_SPEED, MIN_POWER

    set_clear_color(0, 0, 0)
    clear()

    # Creates the background
    set_fill_color(0, 0, 0)
    enable_stroke()
    set_stroke_color(1, 1, 1)
    draw_circle(WIDTH/2, HEIGHT/2, HEIGHT/4)
    draw_line(WIDTH/2, 0, WIDTH/2, HEIGHT/4)
    draw_line(WIDTH/2, HEIGHT - HEIGHT/4, WIDTH/2, HEIGHT)

    # Checks whether the game has begun
    if start:

        # Checks if the game has paused
        if not pause:

            # Individual speed of paddles
            speed_p1 = SPEED
            speed_p2 = SPEED

            # If slow power up is active, slow speed of respective player
            if slowp1:
                speed_p1 = SPEED/2
            elif slowp2:
                speed_p2 = SPEED/2

            # Paddles movement
            if a_press:
                if current_position_player1 > 0 and not invertp1:
                    current_position_player1 = current_position_player1 - speed_p1
                elif current_position_player1 < HEIGHT - player_1_length and invertp1:
                    current_position_player1 = current_position_player1 + speed_p1
            if z_press:
                if current_position_player1 < HEIGHT - player_1_length and not invertp1:
                    current_position_player1 = current_position_player1 + speed_p1
                elif current_position_player1 > 0 and invertp1:
                    current_position_player1 = current_position_player1 - speed_p1
            if k_press:
                if current_position_player2 > 0 and not invertp2:
                    current_position_player2 = current_position_player2 - speed_p2
                elif current_position_player2 < HEIGHT - player_2_length and invertp2:
                    current_position_player2 = current_position_player2 + speed_p2
            if m_press:
                if current_position_player2 < HEIGHT - player_2_length and not invertp2:
                    current_position_player2 = current_position_player2 + speed_p2
                elif current_position_player2 > 0 and invertp2:
                    current_position_player2 = current_position_player2 - speed_p2
            else:
                pass

            # Check whether the speed threshold has been reached, and prevents speed from incrementing further
            if abs(x_speed) > MAX_SPEED:
                if x_speed < 0:
                    x_speed = -MAX_SPEED
                elif x_speed >= 0:
                    x_speed = MAX_SPEED
            if abs(y_speed) > MAX_SPEED/2:
                if y_speed < 0:
                    y_speed = -MAX_SPEED/2
                elif y_speed >= 0:
                    y_speed = MAX_SPEED/2

            # Speed checker and direction manager
            if not distortion:
                if abs(x_speed) < abs(y_speed):
                    if y_speed >= 0:
                        y_speed -= speed_converter
                        if x_speed >= 0:
                            x_speed += speed_converter
                        elif x_speed < 0:
                            x_speed -= speed_converter
                    elif y_speed < 0:
                        y_speed += speed_converter
                        if x_speed >= 0:
                            x_speed += speed_converter
                        elif x_speed < 0:
                            x_speed -= speed_converter
                elif abs(x_speed) > abs(y_speed):
                    if abs(x_speed) < MAX_SPEED/5:
                        if x_speed >= 0:
                            x_speed += speed_converter
                        elif x_speed < 0:
                            x_speed -= speed_converter
            elif distortion:
                speed_converter = (random.randint(0, 10)-5)/10
                x_speed += speed_converter
                y_speed += speed_converter

            # Update location of the ball
            x = x + x_speed
            y = y + y_speed

            # Check for collision
            contact()

            # Power up Manager
            if not active:

                # If power up is not active, draw the power up ball
                draw_power_ups()
                count = 0

            elif active:

                # If time limit for the power ups has been reached
                if count >= MAX_COUNT:

                    # Reset the power ups
                    active = False
                    player_2_length = HEIGHT/5
                    player_1_length = HEIGHT/5
                    invincibilityp1 = False
                    invincibilityp2 = False
                    distortion = False
                    invertp1 = False
                    invertp2 = False
                    slowp1 = False
                    slowp2 = False
                    rp1 = 1
                    gp1 = 1
                    bp1 = 1
                    rp2 = 1
                    gp2 = 1
                    bp2 = 1
                    power_ups()

                # Assign the power up to the respective player
                elif count == 1:
                    assign_power_ups(last_touch)

                # Display text for which power up is enabled and for which player
                elif count <= MAX_COUNT * COUNT_SCALE_FACTOR_FOR_TEXT and last_touch != '':
                    set_stroke_color(1, 1, 1)
                    if 1 <= choice <= 5:
                        draw_text(f"{last_touch} elongated for 5 seconds", WIDTH/2 - get_text_width(f"{last_touch} elongated for 5 seconds")/2, HEIGHT/2)
                    elif 6 <= choice <= 9:
                        draw_text(f"{last_touch} invincible for 5 seconds", WIDTH/2 - get_text_width(f"{last_touch} invincible for 5 seconds")/2, HEIGHT/2)
                    elif 10 <= choice <= 12:
                        draw_text(f"{last_touch} distorted reality for 5 seconds", WIDTH/2 - get_text_width(f"{last_touch} distorted reality for 5 seconds")/2, HEIGHT/2)
                    elif 13 <= choice <= 14:
                        if invertp1:
                            draw_text(f"P2 inverted P1 for 5 seconds", WIDTH/2 - get_text_width(f"P2 inverted P1 for 5 seconds")/2, HEIGHT/2)
                        elif invertp2:
                            draw_text(f"P1 inverted P2 for 5 seconds", WIDTH/2 - get_text_width(f"P1 inverted P2 for 5 seconds")/2, HEIGHT/2)
                    elif choice == 15:
                        if slowp1:
                            draw_text(f"P2 slowed P1 for 5 seconds", WIDTH/2 - get_text_width(f"P2 slowed P1 for 5 seconds")/2, HEIGHT/2)
                        elif slowp2:
                            draw_text(f"P1 slowed P2 for 5 seconds", WIDTH/2 - get_text_width(f"P1 slowed P2 for 5 seconds")/2, HEIGHT/2)
                else:
                    pass

                count = count + 1

        # Check if the finisher for player 1 is true
        if finisherp1:

            # Stop movement of both players
            pause = True

            # Relocate player 1 and the ball
            current_position_player1 = HEIGHT/2 - player_1_length/2
            x = WIDTH_PLAYER1 + 30
            y = HEIGHT/2
            x_change = WIDTH-WIDTH+100
            y_change = y_change + factor

            # Bound ball trajectory
            if y_change <= - FINISHER_VIEW:
                factor = -factor
            elif y_change >= FINISHER_VIEW:
                factor = -factor

            # Show ball trajectory
            set_stroke_color(1, 0, 0)
            draw_line(x, y, x_change, y_change + HEIGHT/2)

            # Ball movement and direction when player shoots
            if shoot:
                x_speed = 10
                y_speed = (y_change)/5
                pause = False
                finisherp1 = False
                player1_touches = 0
                shoot = False

        # Check if the finisher for player 1 is true
        if finisherp2:

            # Stop movement of both players
            pause = True

            # Relocate player 1 and the ball
            current_position_player2 = HEIGHT/2 - player_2_length/2
            x = WIDTH - (WIDTH_PLAYER1 + 30)
            y = HEIGHT/2
            x_change = WIDTH-100
            y_change = y_change + factor

            # Bound ball trajectory
            if y_change <= - FINISHER_VIEW:
                factor = -factor
            elif y_change >= FINISHER_VIEW:
                factor = -factor

            # Show ball trajectory
            set_stroke_color(66/255, 135/255, 245/255)
            draw_line(x, y, x_change, y_change + HEIGHT/2)

            # Ball movement and direction when player shoots
            if shoot:
                x_speed = -10
                y_speed = (y_change)/5
                pause = False
                finisherp2 = False
                player2_touches = 0
                shoot = False

        # Display User scores
        set_stroke_color(1, 1, 1)
        set_font_size(FONT_SIZE)
        set_font(FONT_NAME)
        draw_text(str(score_player_1), 10 + WIDTH_PLAYER1, SCORE_HEIGHT_FROM_TOP)
        draw_text(str(score_player_2), WIDTH - 20 - WIDTH_PLAYER2, SCORE_HEIGHT_FROM_TOP)

        # Update position of paddle and ball
        update_paddles()
        update_ball()

        # Outline settings of P1's Powerup bar
        set_stroke_color(1, 1, 1)
        set_fill_color(0, 0, 0, 0)
        draw_rectangle(50, 30, 40, 20)

        # Display Power up bar
        set_stroke_color(1, 0, 0)
        set_fill_color(1, 0, 0)

        # Check if threshold has been met
        if player1_touches >= MAX_POWER:
            player1_touches = MAX_POWER
            set_stroke_color(1, 1, 0)
        if player1_touches <= MIN_POWER:
            player1_touches = MIN_POWER

        draw_rectangle(50, 30, player1_touches, 20)

        # Outline settings of P2's Powerup bar
        set_stroke_color(1, 1, 1)
        set_fill_color(0, 0, 0, 0)
        draw_rectangle(WIDTH-90, 30, 40, 20)

        # Display Power up bar
        set_stroke_color(66/255, 135/255, 245/255)
        set_fill_color(66/255, 135/255, 245/255)

        # Check if threshold has been met
        if player2_touches >= MAX_POWER:
            player2_touches = MAX_POWER
            set_stroke_color(1, 1, 0)
        if player2_touches <= MIN_POWER:
            player2_touches = MIN_POWER

        draw_rectangle(WIDTH-90, 30, player2_touches, 20)
        
        # Display last touch
        if last_touch == 'P1':
            set_stroke_color(1, 0, 0)
            draw_text(last_touch, WIDTH / 2 - get_text_width(last_touch) - 10, 20)
        elif last_touch == 'P2':
            set_stroke_color(66/255, 135/255, 245/255)
            draw_text(last_touch, WIDTH / 2 + 10, 20)

    else:

        # Display User scores
        set_stroke_color(1, 1, 1)
        set_font_size(FONT_SIZE)
        set_font(FONT_NAME)
        draw_text(str(score_player_1), 10 + WIDTH_PLAYER1, SCORE_HEIGHT_FROM_TOP)
        draw_text(str(score_player_2), WIDTH - 20 - WIDTH_PLAYER2, SCORE_HEIGHT_FROM_TOP)

        # Update position of paddle and ball
        update_paddles()
        update_ball()

        set_stroke_color(1, 1, 1)
        draw_text("Press 'Space' to start", WIDTH/2 - get_text_width("Press 'Space' to start")/2, HEIGHT/3)


start_graphics(game, framerate=FRAMERATE, width=WIDTH, height=HEIGHT, key_press=get_key_down, key_release=get_key_up)
