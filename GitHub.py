import pygame
import sys
import random
import time

# Inicijalizacija Pygame-a
pygame.init()

# Parametri ekrana
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('GitCat')

# Boje
WHITE = (255, 255, 255)

# Učitaj slike ljubimca
pet_image_normal = pygame.image.load('normal_cat.jpg')  # Slika ljubimca kada je normalan
pet_image_sleeping = pygame.image.load('sleep_cat.jpg')  # Slika ljubimca kada spava
pet_image_angry = pygame.image.load('angry_cat.jpg')  # Slika ljubimca kada je ljut
pet_image_eating = pygame.image.load('hungry_cat.jpg')  # Slika ljubimca kada jede

# Učitaj pozadinsku sliku
background_image = pygame.image.load('room.jpg')  # Slika pozadine
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))  # Skaliranje pozadine

# Skaliranje slika ljubimca
pet_image_normal = pygame.transform.scale(pet_image_normal, (150, 150))
pet_image_sleeping = pygame.transform.scale(pet_image_sleeping, (150, 150))
pet_image_angry = pygame.transform.scale(pet_image_angry, (150, 150))
pet_image_eating = pygame.transform.scale(pet_image_eating, (150, 150))

# Klasa ljubimca
class Pet:
    def __init__(self, name):
        self.name = name
        self.mood = 'neutral'
        self.x = SCREEN_WIDTH // 2 - 75  # Početna pozicija na sredini ekrana
        self.y = SCREEN_HEIGHT // 2 - 75
        self.speed = 5  # Brzina pomeranja ljubimca
        self.is_dragging = False  # Da li je ljubimac u procesu prevlačenja
        self.last_state_change = time.time()  # Zapamti vreme poslednje promene stanja
        self.state_change_interval = 5  # Interval za promenu stanja (u sekundama)
        self.direction = random.choice(['left', 'right', 'up', 'down'])  # Nasumični početni pravac

    def draw(self, screen):
        """Prikazivanje slike ljubimca u zavisnosti od njegovog stanja"""
        if self.mood == 'umoran':
            screen.blit(pet_image_sleeping, (self.x, self.y))  # Ako je umoran, prikazuje spavanje
        elif self.mood == 'ljut':
            screen.blit(pet_image_angry, (self.x, self.y))  # Ako je ljut, prikazuje ljutu macu
        elif self.mood == 'gladan':
            screen.blit(pet_image_eating, (self.x, self.y))  # Ako je gladan, prikazuje macu koja jede
        else:
            screen.blit(pet_image_normal, (self.x, self.y))  # Inače, prikazuje normalnu macu
        
        # Prikazivanje stanja ljubimca
        font = pygame.font.SysFont(None, 36)
        mood_text = font.render(f'{self.name} je {self.mood}', True, WHITE)
        screen.blit(mood_text, (10, 10))

    def feed(self):
        self.mood = 'srećan'
        self.speed = 8  # Brži je kada je srećan

    def play(self):
        self.mood = 'zabavljen'
        self.speed = 7  # Brži je kada se igra

    def sleep(self):
        self.mood = 'umoran'
        self.speed = 3  # Sporiji je kada spava

    def get_hungry(self):
        self.mood = 'gladan'
        self.speed = 0  # Ne pomera se dok jede

    def get_angry(self):
        self.mood = 'ljut'
        self.speed = 6  # Brži je kada je ljut

    def move(self):
        """Pomera ljubimca u nasumičnom pravcu, osim kada je gladan (ne pomera se)"""
        if self.mood != 'gladan':  # Ako nije gladan, onda se pomera
            if self.direction == 'left':
                self.x -= self.speed
            elif self.direction == 'right':
                self.x += self.speed
            elif self.direction == 'up':
                self.y -= self.speed
            elif self.direction == 'down':
                self.y += self.speed

            # Držanje ljubimca unutar granica ekrana
            self.x = max(0, min(self.x, SCREEN_WIDTH - 150))  # Ograničenje horizontalnog kretanja
            self.y = max(0, min(self.y, SCREEN_HEIGHT - 150))  # Ograničenje vertikalnog kretanja

    def change_mood(self):
        """Nasumično menja stanje ljubimca"""
        moods = ['neutral', 'gladan', 'srećan', 'umoran', 'ljut']
        self.mood = random.choice(moods)
        self.last_state_change = time.time()  # Resetuje vreme poslednje promene stanja

    def click_check(self, mouse_pos):
        """Proverava da li je ljubimac kliknut"""
        pet_rect = pygame.Rect(self.x, self.y, 150, 150)  # Pravougaonik koji obuhvata ljubimca
        if pet_rect.collidepoint(mouse_pos):  # Ako je kliknut unutar tog pravougaonika
            self.get_angry()  # Ako je kliknut, ljubimac postaje ljut

    def start_drag(self, mouse_pos):
        """Počinje prevlačenje ljubimca"""
        pet_rect = pygame.Rect(self.x, self.y, 150, 150)
        if pet_rect.collidepoint(mouse_pos):  # Ako je kliknut ljubimac
            self.is_dragging = True  # Počinje prevlačenje

    def stop_drag(self):
        """Završava prevlačenje ljubimca"""
        self.is_dragging = False  # Zaustavlja prevlačenje

    def drag(self, mouse_pos):
        """Prevlači ljubimca sa mišem"""
        if self.is_dragging:
            self.x = mouse_pos[0] - 75  # Pozicija ljubimca se ažurira prema poziciji miša
            self.y = mouse_pos[1] - 75

# Kreiranje ljubimca
pet_name = "Git"  # Postavi ime ljubimca ovde
my_pet = Pet(pet_name)

# Glavna petlja igre
running = True
last_move_time = time.time()
change_direction_interval = 3  # Interval za promenu pravca (u sekundama)

while running:
    # Prikazivanje pozadinske slike
    screen.blit(background_image, (0, 0))  # Popunjava celu površinu ekrana pozadinskom slikom

    # Pomeri ljubimca
    my_pet.move()  # Pozivanje move() da ljubimac automatski menja poziciju
    my_pet.drag(pygame.mouse.get_pos())  # Pomoću miša prevlači ljubimca
    my_pet.draw(screen)

    # Menjaj stanje ljubimca svakih nekoliko sekundi
    if time.time() - my_pet.last_state_change > my_pet.state_change_interval:
        my_pet.change_mood()

    # Promeni pravac nakon intervala
    if time.time() - last_move_time > change_direction_interval:
        my_pet.direction = random.choice(['left', 'right', 'up', 'down'])
        last_move_time = time.time()

    # Obrada događaja
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:  # Provera da li je levi klik
                my_pet.start_drag(event.pos)  # Počinje prevlačenje
                my_pet.click_check(event.pos)  # Ako je kliknut, postane ljut
        if event.type == pygame.MOUSEBUTTONUP:
            if event.button == 1:  # Provera da li je levi klik
                my_pet.stop_drag()  # Zaustavi prevlačenje

    # Ažuriranje ekrana
    pygame.display.flip()

    # Ograničavanje broja frejmova
    pygame.time.Clock().tick(60)

# Zatvaranje Pygame-a
pygame.quit()
sys.exit()