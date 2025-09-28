import pygame
import serial

pygame.init()

# Window setup
win_width, win_height = 800, 600
win = pygame.display.set_mode((win_width, win_height))
pygame.display.set_caption("Joystick Game")

# Character setup
character_size = 50
character_color = (0, 255, 0)  # Initial color
character_x, character_y = win_width // 2, win_height // 2
character_speed = 5
colors = [
    (255, 0, 0),     
    (0, 255, 0),     
    (0, 0, 255),     
    (255, 255, 0),   
    (255, 0, 255),   
    (0, 255, 255),   
    (255, 165, 0),   
    (128, 0, 128),   
]
current_color_index = 0


# Serial communication setup
arduino_port = 'COM6'  # Replace with your Arduino port
ser = serial.Serial(arduino_port, 9600, timeout=4)

running = True

# Store the character's previous position
prev_x, prev_y = character_x, character_y

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    try:
        line = ser.readline().decode(errors="ignore").strip()
        data = line.split(",")
        if len(data) == 3:
            joy_x, joy_y, button_state = map(int, data)
            print(f"X: {joy_x}, Y: {joy_y}, Button: {button_state}")

            # Calculate new character position based on joystick input
            new_x = character_x + (joy_x - 506) // 100 * character_speed
            new_y = character_y + (joy_y - 524) // 100 * character_speed

            # Ensure the character stays within the screen boundaries
            new_x = max(character_size // 2, min(win_width - character_size // 2, new_x))
            new_y = max(character_size // 2, min(win_height - character_size // 2, new_y))

            # Update character position only if it has moved
            if (new_x, new_y) != (prev_x, prev_y):
                character_x, character_y = new_x, new_y
                prev_x, prev_y = new_x, new_y

            # Change character color based on button state
            if button_state == 0:
               current_color_index = (current_color_index + 1) % len(colors)
            character_color = colors[current_color_index]


        else:
            print("Bad data:", line)

    except ValueError:
        print("Parse error:", line)

    # Draw everything
    win.fill((255, 255, 255))
    pygame.draw.circle(win, character_color, (character_x, character_y), character_size // 2)
    pygame.display.flip()

# Clean up
ser.close()
pygame.quit()
