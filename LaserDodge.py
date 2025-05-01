import pygame
import time
import random
import os
import getpass
import colorama
import sys
import requests
import tempfile
from colorama import Fore
import subprocess



def check_for_update():
    VERSION = "1.0.0"  
    VERSION_URL = "https://raw.githubusercontent.com/Therm121/Laser-Dodge-Update/main/version.txt"
    SCRIPT_URL = "https://raw.githubusercontent.com/Therm121/Laser-Dodge-Update/main/LaserDodge.py"

    try:
        print(Fore.CYAN + "Checking for updates...")
        latest_version = requests.get(VERSION_URL).text.strip()
        if latest_version != VERSION:
            print(Fore.YELLOW + f"New version {latest_version} available. Updating...")

            
            response = requests.get(SCRIPT_URL)
            temp_script_path = os.path.join(tempfile.gettempdir(), "LaserDodge_updated.py")

            with open(temp_script_path, "wb") as f:
                f.write(response.content)

            print(Fore.GREEN + "Update complete.")

            
            
            print(Fore.GREEN + "Launching the updated version...")

            
            subprocess.Popen([sys.executable, temp_script_path])
            print(Fore.GREEN + "New version is now running.")

           
            sys.exit()

        else:
            print(Fore.GREEN + "You're running the latest version.")

    except Exception as e:
        print(Fore.RED + f"Update check failed: {e}")


colorama.init()
username = getpass.getuser()

print(Fore.YELLOW + "This is just pygame's bloatware ignore it")
print(Fore.RED + fr"IMPORTANT! Your latest score is stored in C:\Users\{username}\Documents\Laser Dodge")
print(Fore.RED + "IMPORTANT! Do not close the game after you die wait for it to close itself, it is saving your score")

pygame.font.init()


def resource_path(relative_path):
    """Returns the absolute path to the resource."""
    try:
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(__file__))
    except Exception:
        base_path = os.path.dirname(__file__)
    return os.path.join(base_path, relative_path)


print(Fore.GREEN + "Initializing pygame window...")

WIDTH, HEIGHT = 1000, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Laser Dodge")

bg_path = resource_path("bg.jpeg")
if not os.path.exists(bg_path):
    print(f"ERROR: Background image not found!")
    sys.exit()

BG = pygame.transform.scale(pygame.image.load(bg_path), (WIDTH, HEIGHT))

PLAYER_WIDTH = 30
PLAYER_HEIGHT = 50
PLAYER_VEL = 9
STAR_WIDTH = 10
STAR_HEIGHT = 40
STAR_VEL = 5

FONT = pygame.font.SysFont("comicsans", 30)


def draw(player, elapsed_time, stars):
    WIN.blit(BG, (0, 0))
    time_text = FONT.render(f"Time: {round(elapsed_time)}s", 1, "white")
    WIN.blit(time_text, (10, 10))
    pygame.draw.rect(WIN, "blue", player)
    for star in stars:
        pygame.draw.rect(WIN, "red", star)
    pygame.display.update()


def main():
    run = True
    player = pygame.Rect(200, HEIGHT - PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT)
    clock = pygame.time.Clock()
    start_time = time.time()
    elapsed_time = 0
    star_add_increment = 2000
    star_count = 0
    stars = []
    hit = False

    while run:
        star_count += clock.tick(60)
        elapsed_time = time.time() - start_time

        if star_count > star_add_increment:
            for _ in range(3):
                star_x = random.randint(0, WIDTH - STAR_WIDTH)
                star = pygame.Rect(star_x, -STAR_HEIGHT, STAR_WIDTH, STAR_HEIGHT)
                stars.append(star)

            star_add_increment = max(200, star_add_increment - 50)
            star_count = 0

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                break

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x - PLAYER_VEL >= 0:
            player.x -= PLAYER_VEL
        if keys[pygame.K_RIGHT] and player.x + PLAYER_VEL + player.width <= WIDTH:
            player.x += PLAYER_VEL

        for star in stars[:]:
            star.y += STAR_VEL
            if star.y > HEIGHT:
                stars.remove(star)
            elif star.colliderect(player):
                stars.remove(star)
                hit = True
                break

        if hit:
            lost_text = FONT.render("You Lost!", 1, "white")
            WIN.blit(lost_text, (WIDTH / 2 - lost_text.get_width() / 2, HEIGHT / 2 - lost_text.get_height() / 2))
            pygame.display.update()
            pygame.time.delay(4000)

            save_dir = os.path.join(os.path.expanduser("~"), "Documents", "Laser Dodge")
            os.makedirs(save_dir, exist_ok=True)
            with open(os.path.join(save_dir, "Times.txt"), "a") as file:
                file.write(f"You survived for {round(elapsed_time)} seconds.\n")

            break

        draw(player, elapsed_time, stars)

    pygame.quit()


if __name__ == "__main__":
    check_for_update()  
    main()
