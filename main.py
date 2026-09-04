import pygame
import random
import math
import os

# Pygame start =======================
pygame.init()

# Initialize mixer for sound
pygame.mixer.init()
icon = pygame.image.load('assets/fish.png')
pygame.display.set_icon(icon)
clock = pygame.time.Clock()
w, h = pygame.display.Info().current_w, pygame.display.Info().current_h

# screen ===========================================================
screen = pygame.display.set_mode((w, h))
pygame.display.set_caption("River Adventure")

# Fonts
title_font = pygame.font.Font(None, 80)
font = pygame.font.Font(None, 36)
big_font = pygame.font.Font(None, 50)

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (50, 150, 255)
DARK_BLUE = (20, 80, 180)
YELLOW = (255, 255, 0)
GRAY = (150, 150, 150)
LIGHT_BLUE = (135, 206, 235)

# Load images
def load_image(path, scale=None):
    """Load an image with optional scaling"""
    try:
        image = pygame.image.load(path).convert_alpha()
        if scale:
            image = pygame.transform.scale(image, scale)
        return image
    except pygame.error as e:
        print(f"Error loading image {path}: {e}")
        # Create a placeholder surface if image not found
        surf = pygame.Surface((50, 50))
        surf.fill(RED)
        return surf

# Load sounds
def load_sound(path):
    """Load a sound file"""
    try:
        sound = pygame.mixer.Sound(path)
        return sound
    except pygame.error as e:
        print(f"Error loading sound {path}: {e}")
        return None

# Load assets
try:
    # Images
    fish_img = load_image("assets/fish.png", (50, 50))
    algae_img = load_image("assets/algae.png", (40, 30))
    meat_img = load_image("assets/meat.png", (30, 25))
    crab_img = load_image("assets/crab.png", (60, 50))
    king_fisher_img = load_image("assets/king_fisher.png", (60, 50))
    
    # Sounds
    eat_sound = load_sound("assets/eat.mp3")
    game_sound = load_sound("assets/game.mp3")
    lobby_sound = load_sound("assets/lobby.mp3")
    crab_sound = load_sound("assets/crab.mp3")
    king_fisher_sound = load_sound("assets/king_fisher.mp3")
    
    print("All assets loaded successfully!")
except:
    print("Some assets not found. Using fallbacks.")
    # Create placeholders
    fish_img = pygame.Surface((50, 50))
    fish_img.fill(RED)
    algae_img = pygame.Surface((40, 30))
    algae_img.fill((0, 255, 0))
    meat_img = pygame.Surface((30, 25))
    meat_img.fill((255, 0, 0))
    crab_img = pygame.Surface((60, 50))
    crab_img.fill((255, 165, 0))
    king_fisher_img = pygame.Surface((60, 50))
    king_fisher_img.fill((0, 255, 0))
    
    eat_sound = None
    game_sound = None
    lobby_sound = None
    crab_sound = None
    king_fisher_sound = None

# Play lobby music
if lobby_sound:
    lobby_sound.play(-1)  # -1 loops indefinitely

# Create sky gradient surface
def create_sky_gradient():
    sky_surface = pygame.Surface((w, 300))
    for y in range(300):
        # Day sky gradient: dark blue to light blue
        color_value = int(135 + (y / 300) * 100)
        r = int(25 + (y / 300) * 110)
        g = int(50 + (y / 300) * 156)
        b = int(150 + (y / 300) * 56)
        pygame.draw.line(sky_surface, (r, g, b), (0, y), (w, y))
    return sky_surface

def create_night_sky_gradient():
    night_surface = pygame.Surface((w, 300))
    for y in range(300):
        # Night sky gradient: very dark to dark blue
        r = int(5 + (y / 300) * 20)
        g = int(10 + (y / 300) * 30)
        b = int(25 + (y / 300) * 50)
        pygame.draw.line(night_surface, (r, g, b), (0, y), (w, y))
    return night_surface

# Create water gradient with waves
def create_water_surface():
    water_surface = pygame.Surface((w, h - 350))
    for y in range(h - 350):
        # Water gradient: dark blue to lighter blue
        r = int(0 + (y / (h - 350)) * 30)
        g = int(60 + (y / (h - 350)) * 80)
        b = int(100 + (y / (h - 350)) * 80)
        pygame.draw.line(water_surface, (r, g, b), (0, y), (w, y))
    return water_surface

# Create ground with grass and dirt texture
def create_ground_surface():
    ground_surface = pygame.Surface((w, 50))
    for y in range(50):
        if y < 15:
            # Grass layer
            r = int(30 + (y / 15) * 20)
            g = int(100 + (y / 15) * 40)
            b = int(20 + (y / 15) * 10)
            color = (r, g, b)
        else:
            # Dirt layer with subtle variation
            r = 60 + int(math.sin(y * 0.5) * 5)
            g = 40 + int(math.sin(y * 0.5 + 1) * 5)
            b = 20 + int(math.sin(y * 0.5 + 2) * 5)
            color = (r, g, b)
        pygame.draw.line(ground_surface, color, (0, y), (w, y))
    
    # Add grass blades on top
    for x in range(0, w, 3):
        height = random.randint(2, 6)
        for i in range(height):
            pygame.draw.line(ground_surface, (40 + i * 5, 120 + i * 10, 30), 
                           (x + random.randint(-1, 1), 15 - i), 
                           (x + random.randint(-1, 1), 15 - i - 1))
    
    return ground_surface

# Create pre-rendered surfaces
sky_day = create_sky_gradient()
sky_night = create_night_sky_gradient()
water_surface = create_water_surface()
ground_surface = create_ground_surface()

# Stars for night sky
stars = []
for _ in range(200):
    stars.append({
        'x': random.randint(0, w),
        'y': random.randint(0, 300),
        'size': random.randint(1, 3),
        'twinkle': random.random() * 6.28
    })

# Clouds
clouds = []
for _ in range(8):
    clouds.append({
        'x': random.randint(0, w),
        'y': random.randint(20, 200),
        'width': random.randint(80, 200),
        'height': random.randint(20, 40),
        'speed': random.uniform(0.1, 0.3),
        'alpha': random.randint(180, 230)
    })

# Water bubbles for decoration
bubbles = []
for _ in range(20):
    bubbles.append({
        'x': random.randint(0, w),
        'y': random.randint(300, h - 50),
        'size': random.randint(3, 8),
        'speed': random.uniform(0.2, 0.8),
        'phase': random.random() * 6.28
    })

def draw_sky():
    if day:
        screen.blit(sky_day, (0, 0))
        # Draw sun with glow
        sun_radius = 30
        for i in range(10, 0, -1):
            glow_radius = sun_radius + i * 8
            alpha = 30 - i * 3
            if alpha > 0:
                glow_surface = pygame.Surface((glow_radius * 2, glow_radius * 2), pygame.SRCALPHA)
                pygame.draw.circle(glow_surface, (255, 223, 0, alpha), 
                                 (glow_radius, glow_radius), glow_radius)
                screen.blit(glow_surface, (int(sun_x - glow_radius), int(sun_y - glow_radius)))
        pygame.draw.circle(screen, (255, 223, 0), (int(sun_x), int(sun_y)), sun_radius)
    else:
        screen.blit(sky_night, (0, 0))
        # Draw stars with twinkle
        for star in stars:
            twinkle = math.sin(pygame.time.get_ticks() / 1000 + star['twinkle']) * 0.5 + 0.5
            brightness = int(100 + 155 * twinkle)
            pygame.draw.circle(screen, (brightness, brightness, brightness), 
                             (star['x'], star['y']), star['size'])
        
        # Draw moon with glow
        moon_radius = 25
        for i in range(8, 0, -1):
            glow_radius = moon_radius + i * 6
            alpha = 25 - i * 3
            if alpha > 0:
                glow_surface = pygame.Surface((glow_radius * 2, glow_radius * 2), pygame.SRCALPHA)
                pygame.draw.circle(glow_surface, (240, 240, 210, alpha), 
                                 (glow_radius, glow_radius), glow_radius)
                screen.blit(glow_surface, (int(sun_x - glow_radius), int(sun_y - glow_radius)))
        pygame.draw.circle(screen, (240, 240, 210), (int(sun_x), int(sun_y)), moon_radius)
        # Moon crater details
        pygame.draw.circle(screen, (200, 200, 180), (int(sun_x - 8), int(sun_y - 5)), 5)
        pygame.draw.circle(screen, (200, 200, 180), (int(sun_x + 7), int(sun_y + 8)), 4)
        pygame.draw.circle(screen, (200, 200, 180), (int(sun_x + 2), int(sun_y - 10)), 3)

def draw_clouds():
    for cloud in clouds:
        cloud_surface = pygame.Surface((cloud['width'], cloud['height']), pygame.SRCALPHA)
        # Draw puffy cloud
        for i in range(5):
            circle_x = int(i * cloud['width'] / 5)
            circle_y = int(cloud['height'] / 2 + math.sin(i * 1.5) * cloud['height'] / 4)
            circle_radius = int(cloud['height'] / 2 + math.sin(i * 2) * 5)
            pygame.draw.circle(cloud_surface, (255, 255, 255, cloud['alpha']), 
                             (circle_x, circle_y), circle_radius)
        screen.blit(cloud_surface, (cloud['x'], cloud['y']))
        cloud['x'] += cloud['speed']
        if cloud['x'] > w:
            cloud['x'] = -cloud['width']

def draw_water():
    screen.blit(water_surface, (0, 300))
    # Draw wave lines
    for i in range(5):
        wave_y = 320 + i * 40 + math.sin(pygame.time.get_ticks() / 1000 + i) * 5
        wave_width = 2 + math.sin(i * 0.5) * 1
        for x in range(0, w, 2):
            wave_offset = math.sin(x / 50 + pygame.time.get_ticks() / 1500 + i) * 3
            alpha = 50 - i * 8
            if alpha > 0:
                pygame.draw.circle(screen, (100, 180, 255, alpha), 
                                 (x, int(wave_y + wave_offset)), wave_width)

def draw_bubbles():
    for bubble in bubbles:
        bubble_y = bubble['y'] - math.sin(pygame.time.get_ticks() / 2000 + bubble['phase']) * 20
        # Bubble with gradient
        for i in range(bubble['size'], 0, -2):
            alpha = 50 - i * 5
            if alpha > 0:
                pygame.draw.circle(screen, (200, 230, 255, alpha), 
                                 (int(bubble['x'] + math.sin(pygame.time.get_ticks() / 1000 + bubble['phase']) * 10), 
                                  int(bubble_y)), i)
        # Highlight
        pygame.draw.circle(screen, (255, 255, 255, 100), 
                         (int(bubble['x'] + math.sin(pygame.time.get_ticks() / 1000 + bubble['phase']) * 10 - 2), 
                          int(bubble_y - 2)), 2)

def draw_ground():
    screen.blit(ground_surface, (0, h - 50))
    # Draw some grass details on top
    for x in range(0, w, 5):
        if random.random() < 0.3:
            height = random.randint(2, 5)
            blade_x = x + math.sin(pygame.time.get_ticks() / 3000 + x) * 1
            pygame.draw.line(screen, (50, 150, 40), 
                           (blade_x, h - 50), 
                           (blade_x + math.sin(pygame.time.get_ticks() / 2000 + x) * 2, h - 50 - height), 1)

# rects==========================================================================
ground_rect = pygame.Rect(0, h - 50, w, 50)
sky_rect = pygame.Rect(0, 0, w, 300)
w_h = h-350
water_rect = pygame.Rect(0, h-w_h-50, w, h-50-300)
king_fisher_rect = pygame.Rect(w//4, 100, 60, 50)
crab_rect = pygame.Rect(w//2, h+100, 60, 50)

# Button class
class Button:
    def __init__(self, x, y, width, height, text, color, hover_color, text_color=WHITE):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.text_color = text_color
        self.is_hovered = False
    
    def draw(self, screen):
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(screen, color, self.rect, border_radius=10)
        pygame.draw.rect(screen, WHITE, self.rect, 2, border_radius=10)
        
        text_surf = font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        screen.blit(text_surf, text_rect)
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.is_hovered = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.is_hovered:
                return True
        return False

#constructor classes
class FoodItem:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        self.type = random.choice(['algae', 'meat'])
        
        # Set different sizes for each type
        if self.type == 'algae':
            self.width = 40
            self.height = 30
            self.image = algae_img
            self.color = (0, 255, 0)
        else:  # meat
            self.width = 30
            self.height = 25
            self.image = meat_img
            self.color = (255, 0, 0)
        
        # Make sure it fits within screen
        min_y = 300
        max_y = screen_height - 60 - self.height
        self.y = random.randint(min_y, max_y)
        
        # Start from the right edge
        self.x = screen_width
        
        # Movement speed (can vary slightly)
        self.speed = random.randint(3, 6)
    
    def update(self):
        """Move the item from right to left"""
        self.x -= self.speed
    
    def draw(self, screen):
        """Draw the item using image if available, otherwise rectangle"""
        try:
            # Draw the image
            screen.blit(self.image, (self.x, self.y))
        except:
            # Fallback to rectangle if image fails
            pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))
    
    def is_off_screen(self):
        """Check if item has moved completely off screen"""
        return self.x + self.width < 0
    
    def get_rect(self):
        """Return pygame Rect for collision detection"""
        return pygame.Rect(self.x, self.y, self.width, self.height)

class Shark:
    def __init__(self, screen_width, screen_height):
        self.screen_width = screen_width
        self.screen_height = screen_height
        
        # Random size
        self.width = random.randint(80, 180)
        self.height = random.randint(50, 120)
        self.color = (100, 100, 100)  # Gray
        
        # Random y position in water (between sky and ground)
        min_y = 300 + 50
        max_y = screen_height - 50 - self.height
        self.y = random.randint(min_y, max_y)
        
        # Start from the right edge
        self.x = screen_width + random.randint(0, 200)  # Stagger spawns
        
        # Random speed (sharks are fast!)
        self.speed = random.randint(5, 10)
        
        # Random fin movement
        self.fin_offset = 0
    
    def update(self):
        """Move shark from right to left"""
        self.x -= self.speed
        # Slight bobbing motion
        self.fin_offset += 0.05
    
    def draw(self, screen):
        """Draw shark with fin"""
        # Body
        shark_rect = pygame.Rect(self.x, self.y, self.width, self.height)
        pygame.draw.rect(screen, self.color, shark_rect)
        
        # Fin (triangle on top)
        fin_points = [
            (self.x + self.width//2, self.y - 15 + math.sin(self.fin_offset) * 3),
            (self.x + self.width//2 - 15, self.y),
            (self.x + self.width//2 + 15, self.y)
        ]
        pygame.draw.polygon(screen, (80, 80, 80), fin_points)
        
        # Eye
        pygame.draw.circle(screen, WHITE, 
                          (int(self.x + self.width - 15), int(self.y + self.height//2)), 5)
        pygame.draw.circle(screen, BLACK, 
                          (int(self.x + self.width - 13), int(self.y + self.height//2)), 3)
        
        # Teeth (just for show)
        for i in range(3):
            tooth_x = int(self.x + self.width - 5)
            tooth_y = int(self.y + self.height//2 - 5 + i * 10)
            pygame.draw.polygon(screen, WHITE, 
                              [(tooth_x, tooth_y), (tooth_x + 10, tooth_y - 3), (tooth_x + 10, tooth_y + 3)])
    
    def is_off_screen(self):
        """Check if shark has moved completely off screen"""
        return self.x + self.width < 0
    
    def get_rect(self):
        """Return pygame Rect for collision detection"""
        return pygame.Rect(self.x, self.y, self.width, self.height)

#=================================PLAYER=======================================================
def reset_game():
    global player_x, player_y, g_player, score, player, can_move
    global food_items, sharks, king_fisher_rect, crab_rect, game_over
    global spawn_timer, shark_spawn_timer
    
    player_x = 100
    player_y = h//2
    g_player = 2.5
    score = 0
    player = pygame.Rect(100, h//2, 50, 50)
    can_move = True
    game_over = False
    food_items.clear()
    sharks.clear()
    spawn_timer = 0
    shark_spawn_timer = 0
    king_fisher_rect.x = w//4
    king_fisher_rect.y = 100
    crab_rect.x = w//2
    crab_rect.y = h+100

# Initialize game variables
player_x = 100
player_y = h//2
g_player = 2.5
score = 0
player = pygame.Rect(100, h//2, 50, 50)

# Sun state
sun_x = float(w-50)
sun_y = 50.0

#king fisher movement variables
g_king_fisher = 2.5
target = None

# Food items and sharks lists
food_items = []
sharks = []
spawn_timer = 0
shark_spawn_timer = 0

# Game states
MENU = 0
PLAYING = 1
GAME_OVER = 2
HOW_TO_PLAY = 3
PAUSED = 4

# game loop ======================================================
day = True
t = 0
running = True
can_move = True
game_over = False
game_state = MENU

# Create buttons
play_button = Button(w//2 - 100, h//2 - 50, 200, 60, "PLAY", BLUE, DARK_BLUE)
how_button = Button(w//2 - 100, h//2 + 30, 200, 60, "HOW TO PLAY", GREEN, (0, 150, 0))
quit_button = Button(w//2 - 100, h//2 + 110, 200, 60, "QUIT", RED, (150, 0, 0))

# Death screen buttons
play_again_button = Button(w//2 - 100, h//2 + 20, 200, 60, "PLAY AGAIN", BLUE, DARK_BLUE)
home_button = Button(w//2 - 100, h//2 + 100, 200, 60, "HOME", GRAY, (100, 100, 100))

# How to play back button
back_button = Button(w//2 - 80, h - 150, 160, 50, "BACK", GRAY, (100, 100, 100))

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        
        # Handle menu state
        if game_state == MENU:
            if play_button.handle_event(event):
                # Stop lobby music, start game music
                if lobby_sound:
                    lobby_sound.stop()
                if game_sound:
                    game_sound.play(-1)
                reset_game()
                game_state = PLAYING
            if how_button.handle_event(event):
                game_state = HOW_TO_PLAY
            if quit_button.handle_event(event):
                running = False
        
        # Handle how to play state
        elif game_state == HOW_TO_PLAY:
            if back_button.handle_event(event):
                game_state = MENU
        
        # Handle game over state
        elif game_state == GAME_OVER:
            if play_again_button.handle_event(event):
                if game_sound:
                    game_sound.stop()
                if lobby_sound:
                    lobby_sound.play(-1)
                reset_game()
                game_state = MENU
            if home_button.handle_event(event):
                if game_sound:
                    game_sound.stop()
                if lobby_sound:
                    lobby_sound.play(-1)
                reset_game()
                game_state = MENU
        
        # Handle playing state
        elif game_state == PLAYING:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r and game_over:
                    reset_game()
                    game_state = PLAYING
                if event.key == pygame.K_ESCAPE:
                    game_state = PAUSED
    
    # Game logic
    if game_state == PLAYING and not game_over:
        # Player movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and can_move:
            player_y -= 20  
        if (keys[pygame.K_LEFT] or keys[pygame.K_a]) and can_move:
            player_x -= 5
        if (keys[pygame.K_RIGHT] or keys[pygame.K_d]) and can_move:
            player_x += 5
        
        player.x = player_x
        player.y = player_y
        
        t += 0.01
        if t > 10:
            t = 0
            day = not day
        
        player_y += g_player
        player.y = player_y
        
        # Spawn food items
        spawn_timer += 1
        if spawn_timer >= 30:
            if random.random() < 0.2:
                food_items.append(FoodItem(w, h))
            spawn_timer = 0
        
        # Spawn sharks
        shark_spawn_timer += 1
        if shark_spawn_timer >= 120:
            if random.random() < 0.95:
                sharks.append(Shark(w, h))
            shark_spawn_timer = 0
        
        # Update food items
        for food in food_items[:]:
            food.update()
            if food.is_off_screen():
                food_items.remove(food)
            elif player.colliderect(food.get_rect()):
                # Play eat sound
                if eat_sound:
                    eat_sound.play()
                if food.type == 'algae':
                    score += 10
                else:
                    score += 20
                food_items.remove(food)
        
        # Update sharks
        for shark in sharks[:]:
            shark.update()
            if shark.is_off_screen():
                sharks.remove(shark)
            elif player.colliderect(shark.get_rect()):
                game_over = True
                game_state = GAME_OVER
                sharks.remove(shark)
        
        # Death mechanics - Crab
        if player.colliderect(ground_rect):
            target_x = player.x
            can_move = False
            g_player = 0
            crab_rect.x += (target_x - crab_rect.x) * 0.05
            crab_rect.y += (h-100 - crab_rect.y) * 0.05
        
        if crab_rect.colliderect(player):
            if crab_sound:
                crab_sound.play()
            can_move = True
            g_player = 2.5
            game_over = True
            game_state = GAME_OVER
        
        # Death mechanics - King Fisher
        if player.colliderect(sky_rect):
            target_x = player.x
            target_y = player.y
            king_fisher_rect.x += (target_x - king_fisher_rect.x) * 0.05
            king_fisher_rect.y += (target_y - king_fisher_rect.y) * 0.05
            can_move = False
            g_player = 0

        if king_fisher_rect.colliderect(player):
            if king_fisher_sound:
                king_fisher_sound.play()
            can_move = True
            g_player = 2.5
            game_over = True
            game_state = GAME_OVER
    
    # Rendering
    screen.fill(BLACK)
    
    if game_state == MENU:
        # Background gradient
        for i in range(h):
            color_value = int(20 + (i / h) * 60)
            pygame.draw.line(screen, (color_value, color_value, color_value + 50), (0, i), (w, i))
        
        # Title
        title_text = title_font.render("SUBMERGED", True, WHITE)
        title_rect = title_text.get_rect(center=(w//2, 150))
        screen.blit(title_text, title_rect)
        
        # Subtitle
        subtitle = font.render("There is no end to this journey", True, YELLOW)
        subtitle_rect = subtitle.get_rect(center=(w//2, 210))
        screen.blit(subtitle, subtitle_rect)
        
        # Decorative fish
        for i in range(5):
            x = 100 + i * 150 + math.sin(pygame.time.get_ticks() / 1000 + i) * 20
            y = 250 + math.sin(pygame.time.get_ticks() / 800 + i * 2) * 15
            pygame.draw.ellipse(screen, BLUE, (x, y, 30, 15))
            pygame.draw.polygon(screen, BLUE, [(x + 30, y + 7), (x + 40, y), (x + 30, y + 14)])
        
        # Draw buttons
        play_button.draw(screen)
        how_button.draw(screen)
        quit_button.draw(screen)
        
        # Version info
        version = font.render("v1.0", True, GRAY)
        screen.blit(version, (10, h - 30))
    
    elif game_state == HOW_TO_PLAY:
        # Background
        screen.fill((20, 30, 50))
        
        # Title
        title = big_font.render("HOW TO PLAY", True, WHITE)
        title_rect = title.get_rect(center=(w//2, 80))
        screen.blit(title, title_rect)
        
        # Instructions
        instructions = [
            " Use ARROW KEYS or WASD to move the fish",
            "⬆ Press SPACE to jump",
            " Collect GREEN algae for +10 points",
            " Collect RED meat for +20 points",
            " Avoid SHARKS or you die!",
            " Avoid CRAB on the ground",
            " Avoid KING FISHER in the sky",
            " Day/Night cycle changes every 10 seconds",
            " Press ESC to pause"
        ]
        
        for i, instruction in enumerate(instructions):
            text = font.render(instruction, True, WHITE)
            text_rect = text.get_rect(center=(w//2, 150 + i * 45))
            screen.blit(text, text_rect)
        
        back_button.draw(screen)
    
    elif game_state == PLAYING or game_state == PAUSED:
        # Draw sky with gradient
        draw_sky()
        
        # Draw clouds
        draw_clouds()
        
        # Draw water
        draw_water()
        
        # Draw bubbles
        draw_bubbles()
        
        # Draw ground
        draw_ground()
        
        # Draw food items
        for food in food_items:
            food.draw(screen)
        
        # Draw sharks
        for shark in sharks:
            shark.draw(screen)
        
        # Draw player (Fish!)
        screen.blit(fish_img, (player.x, player.y))
        
        # Draw king fisher
        screen.blit(king_fisher_img, (king_fisher_rect.x, king_fisher_rect.y))
        
        # Draw crab
        screen.blit(crab_img, (crab_rect.x, crab_rect.y))
        
        # Display score
        score_text = font.render(f"Score: {score}", True, WHITE)
        # Add semi-transparent background for readability
        score_bg = pygame.Surface((score_text.get_width() + 20, 40))
        score_bg.set_alpha(150)
        score_bg.fill(BLACK)
        screen.blit(score_bg, (5, 5))
        screen.blit(score_text, (15, 10))
        
        food_count = font.render(f"Food: {len(food_items)}", True, WHITE)
        food_bg = pygame.Surface((food_count.get_width() + 20, 40))
        food_bg.set_alpha(150)
        food_bg.fill(BLACK)
        screen.blit(food_bg, (5, 45))
        screen.blit(food_count, (15, 50))
        
        shark_count = font.render(f"Sharks: {len(sharks)}", True, (255, 100, 100))
        shark_bg = pygame.Surface((shark_count.get_width() + 20, 40))
        shark_bg.set_alpha(150)
        shark_bg.fill(BLACK)
        screen.blit(shark_bg, (5, 85))
        screen.blit(shark_count, (15, 90))
        
        # Pause overlay
        if game_state == PAUSED:
            overlay = pygame.Surface((w, h))
            overlay.set_alpha(180)
            overlay.fill(BLACK)
            screen.blit(overlay, (0, 0))
            
            paused_text = big_font.render("PAUSED", True, WHITE)
            paused_rect = paused_text.get_rect(center=(w//2, h//2 - 50))
            screen.blit(paused_text, paused_rect)
            
            resume_text = font.render("Press ESC to resume", True, WHITE)
            resume_rect = resume_text.get_rect(center=(w//2, h//2 + 20))
            screen.blit(resume_text, resume_rect)
            
            home_text = font.render("Press H to go home", True, WHITE)
            home_rect = home_text.get_rect(center=(w//2, h//2 + 70))
            screen.blit(home_text, home_rect)
            
            # Pause key handling
            keys = pygame.key.get_pressed()
            if keys[pygame.K_ESCAPE]:
                game_state = PLAYING
            if keys[pygame.K_h]:
                if game_sound:
                    game_sound.stop()
                if lobby_sound:
                    lobby_sound.play(-1)
                reset_game()
                game_state = MENU
    
    elif game_state == GAME_OVER:
        # Game over screen
        overlay = pygame.Surface((w, h))
        overlay.set_alpha(200)
        overlay.fill(BLACK)
        screen.blit(overlay, (0, 0))
        
        # Animated "YOU DIED" text
        pulse = abs(math.sin(pygame.time.get_ticks() / 300))
        color = (255, int(50 + 100 * pulse), int(50 + 100 * pulse))
        game_over_text = title_font.render("YOU DIED!", True, color)
        game_over_rect = game_over_text.get_rect(center=(w//2, h//2 - 120))
        screen.blit(game_over_text, game_over_rect)
        
        # Final score
        score_text = big_font.render(f"Final Score: {score}", True, WHITE)
        score_rect = score_text.get_rect(center=(w//2, h//2 - 50))
        screen.blit(score_text, score_rect)
        
        # Stats
        stats_text = font.render(f"Food Collected: {score // 10}", True, WHITE)
        stats_rect = stats_text.get_rect(center=(w//2, h//2))
        screen.blit(stats_text, stats_rect)
        
        # Buttons
        play_again_button.draw(screen)
        home_button.draw(screen)
    
    pygame.display.update()
    clock.tick(60)

pygame.quit()