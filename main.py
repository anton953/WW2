import pygame
import random
import sys

# Инициализация Pygame
pygame.init()

# Константы
WIDTH, HEIGHT = 800, 600
FPS = 60
PLAYER_SPEED = 5
BULLET_SPEED = 7
ENEMY_SPEED = 3

# Цвета
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Создание окна
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Великая Отечественная Война 1941-1945")
clock = pygame.time.Clock()

# Загрузка изображений (замените на свои)
player_img = pygame.image.load('data/tanchiki.png')

enemy_img = pygame.image.load('data/tanchiki2.png')
enemy_img = pygame.transform.rotate(enemy_img, 180) 
bullet_img = pygame.Surface((10, 5))
bullet_img.fill(RED)

medkit_img = pygame.image.load('data/medkit.png').convert_alpha()
pygame.transform.scale(medkit_img, (50, 50))

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_img
        self.rect = self.image.get_rect(center=(WIDTH//2, HEIGHT-50))
        self.health = 100
        self.score = 0

    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_a] and self.rect.left > 0:
            self.rect.x -= PLAYER_SPEED
        if keys[pygame.K_d] and self.rect.right < WIDTH:
            self.rect.x += PLAYER_SPEED

    def shoot(self):
        return Bullet(self.rect.centerx, self.rect.top)

class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = enemy_img
        self.rect = self.image.get_rect(center=(random.randint(50, WIDTH-50), -20))
        self.speed = ENEMY_SPEED

    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.kill()

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = bullet_img
        self.rect = self.image.get_rect(center=(x, y))
    
    def update(self):
        self.rect.y -= BULLET_SPEED
        if self.rect.bottom < 0:
            self.kill()

class Medkit(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = medkit_img
        self.rect = self.image.get_rect(center=(random.randint(30, WIDTH-30), -20))
        self.speed = 2
    
    def update(self):
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.kill()

# Группы спрайтов
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
bullets = pygame.sprite.Group()
medkits = pygame.sprite.Group()

player = Player()
all_sprites.add(player)

# Таймеры
enemy_timer = pygame.USEREVENT + 1
pygame.time.set_timer(enemy_timer, 1500)

medkit_timer = pygame.USEREVENT + 2
pygame.time.set_timer(medkit_timer, 5000)

running = True
while running:
    clock.tick(FPS)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bullet = player.shoot()
                all_sprites.add(bullet)
                bullets.add(bullet)
        if event.type == enemy_timer:
            enemy = Enemy()
            all_sprites.add(enemy)
            enemies.add(enemy)
        if event.type == medkit_timer:
            medkit = Medkit()
            all_sprites.add(medkit)
            medkits.add(medkit)
    
    # Обновление
    all_sprites.update()
    
    # Столкновения пуль с врагами
    hits = pygame.sprite.groupcollide(enemies, bullets, True, True)
    for hit in hits:
        player.score += 10
    
    # Столкновение игрока с врагами
    if pygame.sprite.spritecollide(player, enemies, True):
        player.health -= 20
    
    # Подбор аптечек
    medkit_hits = pygame.sprite.spritecollide(player, medkits, True)
    for _ in medkit_hits:
        player.health = min(player.health + 30, 100)
    
    # Отрисовка
    screen.fill((0, 0, 0))
    all_sprites.draw(screen)
    
    # Интерфейс
    font = pygame.font.Font(None, 36)
    health_text = font.render(f"Здоровье: {player.health}", True, WHITE)
    score_text = font.render(f"Очки: {player.score}", True, WHITE)
    screen.blit(health_text, (10, 10))
    screen.blit(score_text, (10, 50))
    
    # Конец игры
    if player.health <= 0:
        game_over_text = font.render("GAME OVER", True, RED)
        screen.blit(game_over_text, (WIDTH//2 - 100, HEIGHT//2))
        pygame.display.flip()
        pygame.time.wait(3000)
        running = False
    
    pygame.display.flip()

pygame.quit()
sys.exit()