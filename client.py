import random
import sys
import pygame
import os
from network import Network
import time

# Font initializer.
pygame.font.init()
# Sounds initializer.
pygame.mixer.init()

WIDTH, HEIGHT = 900, 500
# Setting up the display size.
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
# Defining the window title.
pygame.display.set_caption("FABAMAQ Bingo Server")

# Setting up the frame rate.
FPS = 60
# Storing the RGB for black color.
BLACK = (0, 0, 0)

# Setting the path to all assets.
# Could either use the hardcoded path or the os.path.join method, which is Linux friendly.
GAME_START = pygame.mixer.Sound(os.path.join('assets', 'game_start.ogg'))
GAME_PRIZE = pygame.mixer.Sound(os.path.join('assets', 'game_prize.mp3'))
GAME_OVER = pygame.mixer.Sound(os.path.join('assets', 'game_over.wav'))
BACKGROUND = pygame.transform.scale(pygame.image.load(os.path.join('assets', 'bingo_background.jpg')), (WIDTH, HEIGHT))
# Setting up the font name and size.
MESSAGE_FONT = pygame.font.SysFont('comicsans', 30)


# This function will generate a new card with 10 unique numbers from 1 to 50.
# The point is to store it in a variable, so it can be passed on to another function.
def draw_card():
    card = random.sample(range(1, 51), 10)
    return card


# This function will simulate someone shouting all the numbers from 1 to 50, one by one with 1 second interval.
# Everytime any shouted number matches any number from the Player card, a message is displayed showing the match and
# the remaining numbers in the Player card.
# If that remaining number is zero, a winning message is displayed and the game is over.
def call_and_check_card_numbers(player_card):
    for _ in random.sample(range(1, 51), 50):
        print("Draw number is:", _)
        # Could either use pygame.time.delay(milliseconds) or time.sleep(seconds).
        # As this is displayed on console, I've used the time.sleep() method.
        time.sleep(1)
        # This if statements is the method I've chose so I wouldn't repeat drew numbers.
        # Everytime there's a number match, that number is removed from the card list.
        # That way i can use the length as I please.
        if _ in player_card:
            print("-------------------")
            print("\t{} in card".format(_))
            player_card.remove(_)
            if len(player_card) != 0:
                print("   ", len(player_card), "remaining")
                print("-------------------")
                # pygame.time.delay(1000)
                time.sleep(1)
            else:
                print("\n-*--*--*--*--*--*--*--*-")
                print("\tCard complete!!!\n\t  Prize Won!!!")
                print("-*--*--*--*--*--*--*--*-")
                # pygame.time.delay(1000)
                time.sleep(1)
                break


# This function sets up an image as the background and updates all the display components.
# As it works frame by frame, everything needs to be updated in order for changes to be visible.
def show_background(image):
    WIN.blit(image, (0, 0))
    pygame.time.delay(3000)
    pygame.display.update()


# This function receives text, sets the desired font already set up at the beginning, and sets the color.0
# With the help of blit, the message will be displayed at the very center of the screen.
# If there's a need to use int numbers when dividing, simply use // instead of /. Example: 2//3 = 0
def draw_text(text):
    draw_message = MESSAGE_FONT.render(text, 1, BLACK)
    WIN.blit(draw_message, (WIDTH/2 - draw_message.get_width()/2, HEIGHT/2 - draw_message.get_height()/2))
    pygame.display.update()


# Run the server.py before running this client.py, client.py can be ran in parallel as well.
# A console input will be prompt, the game will run and messages will be sent to the server.
def main():
    clock = pygame.time.Clock()
    run = True
    n = Network()
    player_counter = 0
    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            else:
                player_counter += 1
                print(n.send("Player {} connected".format(player_counter)))
                show_background(BACKGROUND)
                GAME_START.play()
                draw_text("Player connected!")
                pygame.time.delay(2000)
                show_background(BACKGROUND)
                pygame.display.update()
                GAME_START.stop()
                draw_text("1: Start new Game | 2: Exit")
                bet = int(input("1: Draw new card\n2: Exit\n"))
                if bet == 1:
                    card = draw_card()
                    print("Card numbers:", card)
                    n.send("Player {} card given: {}".format(player_counter, card))
                    n.send("Game Started - shouting numbers")
                    print(call_and_check_card_numbers(card))
                    n.send("Player {} won!".format(player_counter))
                    GAME_PRIZE.play()
                    pygame.time.delay(7500)
                    sys.exit()
                elif bet == 2:
                    n.send("Player {} has left the game".format(player_counter))
                    exit = "Exiting"
                    flag = True
                    for _ in range(1, 4):
                        if flag:
                            print("{}.".format(exit), end="")
                            time.sleep(1)
                            flag = False
                        else:
                            print(".", end="")
                            time.sleep(1)
                    GAME_OVER.play()
                    pygame.time.delay(2000)
                    pygame.quit()
                    sys.exit()
                else:
                    print("Invalid input")
                    n.send("Player {} invalid input".format(player_counter))
                    break


# VERSION: 0.4
if __name__ == "__main__":
    main()
