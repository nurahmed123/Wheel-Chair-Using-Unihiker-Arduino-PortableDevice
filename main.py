import pygame
import serial
import time

# Setup PySerial to communicate with Arduino
arduino = serial.Serial('/dev/ttyUSB0', 9600)  # Adjust this to your correct port
time.sleep(2)  # Give time for the connection to establish

# Initialize pygame
pygame.init()

# Set up display (240x320 resolution for landscape Unihiker)
screen = pygame.display.set_mode((240, 320), pygame.FULLSCREEN)
pygame.display.set_caption("WheelChair Control")

# Define colors
WHITE = (255, 255, 255)
GREEN = (76, 175, 80)   # Modern green color
RED = (244, 67, 54)     # Modern red color
LIGHT_GREY = (240, 240, 240)  # Light background color
DARK_GREY = (50, 50, 50)
SHADOW = (169, 169, 169)

# Button dimensions and animation scaling factor
button_width = 80
button_height = 50
button_scale_factor = 1.05  # Scaling factor for hover animation

# Fonts
font = pygame.font.Font(None, 36)
small_font = pygame.font.Font(None, 24)

# Calculate center of the screen for landscape mode
screen_width, screen_height = 240, 320
center_y = screen_height // 2  # Centered vertically

# Button and title positions (aligned horizontally)
title_rect = pygame.Rect(10, center_y - 130, 220, 40)

# Adjust spacing between buttons to 5 pixels
button_spacing = 15  # Space between buttons

# Define command buttons positions
stop_button_rect = pygame.Rect(30, center_y - 65, button_width, button_height)

# Define movement buttons positions
forward_button_rect = pygame.Rect(30, center_y + 10, button_width, button_height)
backward_button_rect = pygame.Rect(forward_button_rect.x + button_width + button_spacing, center_y + 10, button_width, button_height)
left_button_rect = pygame.Rect(30, center_y + 90, button_width, button_height)
right_button_rect = pygame.Rect(left_button_rect.x + button_width + button_spacing, center_y + 90, button_width, button_height)

# Button state tracking for animation
stop_button_hovered = False
forward_button_hovered = False
backward_button_hovered = False
left_button_hovered = False
right_button_hovered = False

# Functions to send commands to Arduino
def send_stop_command():
    arduino.write(b'S\n')  # Sending 'STOP' command to Arduino

def send_forward_command():
    arduino.write(b'F\n')  # Sending 'FORWARD' command to Arduino

def send_backward_command():
    arduino.write(b'B\n')  # Sending 'BACKWARD' command to Arduino

def send_left_command():
    arduino.write(b'L\n')  # Sending 'LEFT' command to Arduino

def send_right_command():
    arduino.write(b'R\n')  # Sending 'RIGHT' command to Arduino

# Draw rounded rectangle
def draw_rounded_rect(surface, color, rect, corner_radius):
    pygame.draw.rect(surface, color, rect, border_radius=corner_radius)

# Draw button with animation and modern styling
def draw_button(rect, color, text, hovered):
    if hovered:
        # Apply scaling effect when hovered
        scaled_rect = rect.inflate(button_width * (button_scale_factor - 1), button_height * (button_scale_factor - 1))
    else:
        scaled_rect = rect
    
    shadow_rect = scaled_rect.move(3, 3)  # Create shadow by offsetting the button
    draw_rounded_rect(screen, SHADOW, shadow_rect, 15)
    draw_rounded_rect(screen, color, scaled_rect, 15)

    text_surface = font.render(text, True, WHITE)
    text_rect = text_surface.get_rect(center=scaled_rect.center)
    screen.blit(text_surface, text_rect)

# Main loop
running = True
while running:
    screen.fill(LIGHT_GREY)  # Fill background with light grey for a modern look

    # Draw title (horizontally aligned to the left in landscape mode)
    title_text = font.render("WheelChair Control", True, DARK_GREY)
    title_text_rect = title_text.get_rect(center=title_rect.center)
    screen.blit(title_text, title_text_rect)

    # Track mouse position to detect hover state
    mouse_pos = pygame.mouse.get_pos()

    stop_button_hovered = stop_button_rect.collidepoint(mouse_pos)
    forward_button_hovered = forward_button_rect.collidepoint(mouse_pos)
    backward_button_hovered = backward_button_rect.collidepoint(mouse_pos)
    left_button_hovered = left_button_rect.collidepoint(mouse_pos)
    right_button_hovered = right_button_rect.collidepoint(mouse_pos)

    # Draw "STOP", "FORWARD", "BACKWARD", "LEFT", "RIGHT" buttons with hover animation
    draw_button(stop_button_rect, RED, "STOP", stop_button_hovered)
    draw_button(forward_button_rect, GREEN, "FRD", forward_button_hovered)
    draw_button(backward_button_rect, RED, "BCK", backward_button_hovered)
    draw_button(left_button_rect, GREEN, "LEFT", left_button_hovered)
    draw_button(right_button_rect, RED, "RIGHT", right_button_hovered)

    # Check for events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if stop_button_rect.collidepoint(event.pos):
                send_stop_command()
            elif forward_button_rect.collidepoint(event.pos):
                send_forward_command()
            elif backward_button_rect.collidepoint(event.pos):
                send_backward_command()
            elif left_button_rect.collidepoint(event.pos):
                send_left_command()
            elif right_button_rect.collidepoint(event.pos):
                send_right_command()

    # Update display
    pygame.display.flip()

# Close the serial connection when the GUI closes
arduino.close()
pygame.quit()
