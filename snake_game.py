#!/usr/bin/env python3
"""
Snake Game - Terminal Version

HOW TO PLAY:
- Use arrow keys to control the snake's direction
- Eat food (displayed as '*') to grow longer and increase your score
- Avoid hitting the walls or the snake's own body
- Press 'q' at any time to quit the game

Requirements:
- Python 3.x
- curses library (windows-curses on Windows)
"""

import curses
import random
import time
from curses import KEY_RIGHT, KEY_LEFT, KEY_UP, KEY_DOWN

def main(stdscr):
    # Initialize colors
    curses.start_color()
    curses.init_pair(1, curses.COLOR_GREEN, curses.COLOR_BLACK)  # Snake color
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)    # Food color
    curses.init_pair(3, curses.COLOR_YELLOW, curses.COLOR_BLACK) # Score and message color
    
    # Hide cursor
    curses.curs_set(0)
    
    # Get screen dimensions
    sh, sw = stdscr.getmaxyx()
    
    # Create a new window
    win = curses.newwin(sh, sw, 0, 0)
    win.keypad(1)
    win.timeout(100)  # Refresh rate (lower = faster)
    
    # Initial snake position and food
    snake_x = sw // 4
    snake_y = sh // 2
    
    # Create the snake body
    snake = [
        [snake_y, snake_x],
        [snake_y, snake_x - 1],
        [snake_y, snake_x - 2]
    ]
    
    # Create initial food
    food = [sh // 2, sw // 2]
    win.addch(food[0], food[1], '*', curses.color_pair(2))
    
    # Initial direction
    key = KEY_RIGHT
    
    # Initial score
    score = 0
    
    # Draw border
    win.border(0)
    
    # Display initial score
    win.addstr(0, 2, f" Score: {score} ", curses.color_pair(3))
    
    # Game loop
    while True:
        # Display instructions
        win.addstr(0, sw - 25, " Press 'q' to quit ", curses.color_pair(3))
        
        # Get next key press (non-blocking)
        next_key = win.getch()
        
        # If user pressed a key, update direction
        if next_key != -1:
            key = next_key
        
        # Check if user wants to exit
        if key == ord('q'):
            break
        
        # Calculate new head position
        if key == KEY_DOWN:
            new_head = [snake[0][0] + 1, snake[0][1]]
        elif key == KEY_UP:
            new_head = [snake[0][0] - 1, snake[0][1]]
        elif key == KEY_LEFT:
            new_head = [snake[0][0], snake[0][1] - 1]
        elif key == KEY_RIGHT:
            new_head = [snake[0][0], snake[0][1] + 1]
        
        # Insert new head
        snake.insert(0, new_head)
        
        # Check if snake hits the border
        if (snake[0][0] in [0, sh-1] or 
            snake[0][1] in [0, sw-1] or 
            snake[0] in snake[1:]):
            
            # Game over message
            msg = " GAME OVER! "
            win.addstr(sh//2, (sw-len(msg))//2, msg, curses.color_pair(3) | curses.A_BOLD)
            win.addstr(sh//2 + 1, (sw-len(" Final Score: XX "))//2, f" Final Score: {score} ", curses.color_pair(3))
            win.addstr(sh//2 + 2, (sw-len(" Press any key to exit "))//2, " Press any key to exit ", curses.color_pair(3))
            win.timeout(-1)  # Wait indefinitely for a keypress
            win.getch()
            break
        
        # Check if snake eats the food
        if snake[0] == food:
            # Increase score
            score += 1
            win.addstr(0, 2, f" Score: {score} ", curses.color_pair(3))
            
            # Create new food
            while True:
                food = [random.randint(1, sh-2), random.randint(1, sw-2)]
                if food not in snake:
                    break
            
            # Add food to screen
            win.addch(food[0], food[1], '*', curses.color_pair(2))
        else:
            # Move snake (remove last segment)
            tail = snake.pop()
            win.addch(tail[0], tail[1], ' ')
        
        # Draw snake
        for i, segment in enumerate(snake):
            if i == 0:
                win.addch(segment[0], segment[1], 'O', curses.color_pair(1))  # Snake head
            else:
                win.addch(segment[0], segment[1], 'o', curses.color_pair(1))  # Snake body

if __name__ == "__main__":
    try:
        # Initialize curses
        curses.wrapper(main)
    except KeyboardInterrupt:
        print("Game terminated by user")
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        print("Thanks for playing Snake!")

