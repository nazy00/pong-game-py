#!/usr/bin/env python3

import pygame
from random import randint
import tkinter as tk
from tkinter import messagebox

# Define some colors
BLACK = (0, 0, 0)
RED = (255, 0, 0)

pygame.init()

# Define sound
SOUND = pygame.mixer.Sound("sound.mp3")


class Ball(pygame.sprite.Sprite):
    # This class represents a ball. It derives from the "Sprite" class in Pygame.

    def __init__(self, color, width, height):
        # Call the parent class (Sprite) constructor
        super().__init__()

        # Pass in the color of the ball, its width and height.
        # Set the background color and set it to be transparent
        self.image = pygame.Surface([width, height])
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)

        # Draw the ball (a rectangle!)
        pygame.draw.rect(self.image, color, [0, 0, width, height])

        self.velocity = [4, randint(3, 7)]

        # Fetch the rectangle object that has the dimensions of the image.
        self.rect = self.image.get_rect()

    def update(self):
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]


class Paddle(pygame.sprite.Sprite):
    # This class represents a paddle. It derives from the "Sprite" class in Pygame.

    def __init__(self, color, width, height):
        # Call the parent class (Sprite) constructor
        super().__init__()

        # Pass in the color of the Paddle, its width and height.
        # Set the background color and set it to be transparent
        self.image = pygame.Surface([width, height])
        self.image.fill(BLACK)
        self.image.set_colorkey(BLACK)

        # Draw the paddle (a rectangle!)
        pygame.draw.rect(self.image, color, [0, 0, width, height])

        # Fetch the rectangle object that has the dimensions of the image.
        self.rect = self.image.get_rect()

    def moveUp(self, pixels):
        self.rect.y -= pixels
        # Check that you are not going too far (off the screen)
        if self.rect.y < 0:
            self.rect.y = 0

    def moveDown(self, pixels):
        self.rect.y += pixels
        # Check that you are not going too far (off the screen)
        if self.rect.y > 400:
            self.rect.y = 400


# This function prompts user to replay or quit game
def endGame(msg):
    pygame.mixer.Sound.play(SOUND)
    result = messagebox.askyesno(title="End of game", message=msg, detail="Play Again?")
    return result


def main():
    pygame.init()

    # Open a new window
    size = (700, 500)
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Pong")

    paddleA = Paddle(RED, 10, 100)
    paddleA.rect.x = 0
    paddleA.rect.y = 200

    paddleB = Paddle(RED, 10, 100)
    paddleB.rect.x = 690
    paddleB.rect.y = 200

    ball = Ball(RED, 10, 10)
    ball.rect.x = 345
    ball.rect.y = 195

    # This will be a list that will contain all the sprites we intend to use in our game.
    all_sprites_list = pygame.sprite.Group()

    # Add the 2 paddles and the ball to the list of objects
    all_sprites_list.add(paddleA)
    all_sprites_list.add(paddleB)
    all_sprites_list.add(ball)

    # The loop will carry on until the user exits the game (e.g. clicks the close button).
    carryOn = True

    # The clock will be used to control how fast the screen updates
    clock = pygame.time.Clock()

    # Initialise player scores
    scoreA = 0
    scoreB = 0

    # -------- Main Program Loop -----------
    while carryOn:
        # --- Main event loop
        for event in pygame.event.get():  # User did something
            if event.type == pygame.QUIT:  # If user clicked close
                carryOn = False  # Flag that we are done so we exit this loop

        # Check if either player won and prompt for replay or quit
        if scoreA >= 5:
            endG = endGame("YOU LOST")
            if endG:
                main()
            else:
                break

        if scoreB >= 5:
            endG = endGame("YOU WON")
            if endG:
                main()
            else:
                break

        # Moving the paddles
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            paddleB.moveUp(5)
        if keys[pygame.K_a]:
            paddleB.moveDown(5)
        if ball.rect.y < 500 or ball.rect.y > 0:
            paddleA.rect.y = ball.rect.y + (ball.rect.height - paddleA.rect.height) / 2

        # --- Game logic should go here
        all_sprites_list.update()

        # Check if the ball is bouncing against any of the 4 walls:
        if ball.rect.x >= 699:
            scoreA += 1
            ball.velocity[0] = -ball.velocity[0]
        if ball.rect.x <= 0:
            scoreB += 1
            ball.velocity[0] = -ball.velocity[0]
        if ball.rect.y > 499:
            ball.velocity[1] = -ball.velocity[1]
        if ball.rect.y < 0:
            ball.velocity[1] = -ball.velocity[1]

        # Detect collisions between the ball and the paddles
        if pygame.sprite.collide_mask(ball, paddleA) or pygame.sprite.collide_mask(
            ball, paddleB
        ):
            if (
                ball.rect.y <= paddleA.rect.y + 2
                or ball.rect.y <= paddleB.rect.y + 2
                or ball.rect.y >= (paddleB.rect.y + paddleB.rect.height) - 2
                or ball.rect.y >= (paddleA.rect.y + paddleA.rect.height) - 2
            ):
                ball.velocity[1] = -randint(3, 7)
            ball.velocity[0] = -ball.velocity[0]

        # --- Drawing code should go here
        # First, clear the screen to black.
        screen.fill(BLACK)

        # Now let's draw all the sprites in one go. (For now we only have 2 sprites!)
        all_sprites_list.draw(screen)

        # Display scores:
        font = pygame.font.Font(None, 50)
        text = font.render(str(scoreA), 1, RED)
        screen.blit(text, (250, 10))
        text = font.render(str(scoreB), 1, RED)
        screen.blit(text, (420, 10))

        # --- Go ahead and update the screen with what we've drawn.
        pygame.display.flip()

        # --- Limit to 60 frames per second
        clock.tick(60)

    # Once we have exited the main program loop we can stop the game engine:
    pygame.quit()


main()

