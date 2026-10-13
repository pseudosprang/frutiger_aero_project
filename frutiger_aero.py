import os
import pygame
import math
import random
import sys

def resource_path(relative_path):
    """ Ottiene il percorso assoluto della risorsa, compatibile con PyInstaller """
    try:
        # PyInstaller crea una cartella temporanea e salva il percorso in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

pygame.init()

WIDTH, HEIGHT = 900, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Acquario Frutiger Aero")

# --- CARICAMENTO RISORSE ---
current_dir = os.path.dirname(os.path.abspath(__file__))
ASSET_DIR = os.path.join(current_dir, "assets")

def load_image(filename, scale_size=None):
    path = os.path.join(ASSET_DIR, filename)
    if os.path.exists(path):
        img = pygame.image.load(path).convert_alpha()
        if scale_size:
            img = pygame.transform.smoothscale(img, scale_size)
        return img
    else:
        fallback = pygame.Surface(scale_size if scale_size else (50, 50), pygame.SRCALPHA)
        fallback.fill((255, 0, 255, 150))
        return fallback

# Carica l'immagine originale pura
bg_original = load_image("sfondo.jpg")
bg_image = pygame.transform.smoothscale(bg_original, (WIDTH, HEIGHT))
bubble_img = load_image("bolla.png", (30, 30))

# --- CARICAMENTO LISTA PESCI MULTIPLI ---
# Inserisci qui i nomi di tutte le immagini di pesci che hai messo nella cartella assets
fish_filenames = ["pesce1.png", "pesce2.png", "pesce3.png"] 
fish_images = []

for filename in fish_filenames:
    img = load_image(filename, (80, 80)) # Puoi anche variare la dimensione per ogni pesce se vuoi
    fish_images.append(img)

class ImageFish:
    def __init__(self):
        self.reset()

    def reset(self):
        self.x = random.randint(-100, WIDTH + 100)
        self.y = random.randint(30, HEIGHT - 50)
        self.speed = random.uniform(1.0, 2.5)
        self.direction = random.choice([-1, 1])
        self.wobble_y = random.uniform(0, 100)
        
        # Assegna casualmente un'immagine tra quelle caricate nella lista
        self.original_image = random.choice(fish_images)

    def update(self):
        self.x += self.speed * self.direction
        self.wobble_y += 0.05
        self.y += math.sin(self.wobble_y) * 0.4

        if self.x > WIDTH + 100 and self.direction == 1:
            self.direction = -1
        elif self.x < -100 and self.direction == -1:
            self.direction = 1

    def draw(self, surface):
        current_fish_img = self.original_image
        # Specchia l'immagine correttamente in base alla direzione
        if self.direction == -1:
            current_fish_img = pygame.transform.flip(self.original_image, True, False)
            
        surface.blit(current_fish_img, (int(self.x), int(self.y)))

class ImageBubble:
    def __init__(self):
        self.reset()

    def reset(self):
        self.x = random.randint(50, WIDTH - 50)
        self.y = HEIGHT + random.randint(10, 100)
        self.speed = random.uniform(1.2, 2.5)
        self.wobble_speed = random.uniform(0.02, 0.05)
        self.wobble_offset = random.uniform(0, math.pi * 2)
        
        # --- GENERAZIONE DIMENSIONE CASUALE ---
        # Scegli un raggio casuale (es. tra 8 e 22 pixel)
        self.radius = random.randint(8, 22)
        diameter = self.radius * 2
        
        # Ridimensiona l'immagine originale della bolla per questa specifica istanza
        self.image = pygame.transform.smoothscale(bubble_img, (diameter, diameter))

    def update(self):
        self.y -= self.speed
        self.wobble_offset += self.wobble_speed
        self.x += math.sin(self.wobble_offset) * 0.8
        
        if self.y < -30:
            self.reset()

    def draw(self, surface):
        # Disegna l'immagine centrata rispetto alla coordinata x e y
        surface.blit(self.image, (int(self.x - self.radius), int(self.y - self.radius)))

fishes = [ImageFish() for _ in range(15)]
bubbles = [ImageBubble() for _ in range(25)]

clock = pygame.time.Clock()

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        # Gestione del ridimensionamento della finestra
        elif event.type == pygame.VIDEORESIZE:
            WIDTH, HEIGHT = event.w, event.h
            screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
            # Adatta lo sfondo alla nuova dimensione della finestra
            bg_image = pygame.transform.smoothscale(bg_original, (WIDTH, HEIGHT))

    for f in fishes:
        f.update()
    for b in bubbles:
        b.update()

    screen.blit(bg_image, (0, 0))

    for b in bubbles:
        b.draw(screen)
    for f in fishes:
        f.draw(screen)

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()