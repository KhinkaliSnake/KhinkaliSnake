import pygame
import sys
import random
from pygame.math import Vector2
import os

class MainMenu:
    def __init__(self):
        self.font = pygame.font.Font(None, 76)
        self.title_text = self.font.render("Khinkali Snake", True, (4, 33, 6))
        self.title_rect = self.title_text.get_rect(center=(cell_number * cell_size // 2, cell_number * cell_size // 2.5))
        
        self.font2 = pygame.font.Font(None,36)
        self.start_text = self.font2.render("Press ENTER to Start", True, (255, 255, 255))
        self.start_rect = self.start_text.get_rect(center=(cell_number * cell_size // 2, cell_number * cell_size // 2))

        self.quit_text = self.font2.render("Press ESCAPE to Quit", True, (255, 255, 255))
        self.quit_rect = self.quit_text.get_rect(center=(cell_number * cell_size // 2, cell_number * cell_size // 1.8))

    def draw(self):
        screen.fill((80, 135, 84))
        screen.blit(self.title_text, self.title_rect)
        screen.blit(self.start_text, self.start_rect)
        screen.blit(self.quit_text, self.quit_rect)
        pygame.display.flip()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return "start"
                elif event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
        return None

class DifficultyMenu:
    def __init__(self):
        self.font = pygame.font.Font(None, 56)
        self.title_text = self.font.render("Select Difficulty:", True, (255, 255, 255))
        self.title_rect = self.title_text.get_rect(center=(cell_number * cell_size // 2, cell_number * cell_size // 2.5))

        self.font = pygame.font.Font(None, 40)
        self.easy_text = self.font.render("1 - Easy", True, (255, 255, 255))
        self.easy_rect = self.easy_text.get_rect(center=(cell_number * cell_size // 2, cell_number * cell_size // 2))

        self.medium_text = self.font.render("2 - Medium", True, (255, 255, 255))
        self.medium_rect = self.medium_text.get_rect(center=(cell_number * cell_size // 1.9, cell_number * cell_size // 1.8))

        self.hard_text = self.font.render("3 - Hard", True, (255, 255, 255))
        self.hard_rect = self.hard_text.get_rect(center=(cell_number * cell_size // 1.99, cell_number * cell_size // 1.63))

        self.selected_difficulty = None

    def draw(self):
        screen.fill((80, 135, 84))
        screen.blit(self.title_text, self.title_rect)
        screen.blit(self.easy_text, self.easy_rect)
        screen.blit(self.medium_text, self.medium_rect)
        screen.blit(self.hard_text, self.hard_rect)
        pygame.display.flip()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    self.selected_difficulty = 1
                    return True
                elif event.key == pygame.K_2:
                    self.selected_difficulty = 2
                    return True
                elif event.key == pygame.K_3:
                    self.selected_difficulty = 3
                    return True
        return False

class MAIN:
    def __init__(self):
        self.snake = SNAKE()
        self.fruit = FRUIT()
        self.return_to_menu = False
    
    def get_return_to_menu(self):
        return self.return_to_menu

    def update(self):
        self.snake.move_snake()
        self.check_collision()
        self.check_fail()
        if self.return_to_menu:
            return

    def draw_elements(self):
        self.draw_grass()
        self.fruit.draw_fruit()
        self.snake.draw_snake()
        self.draw_score()

    def check_collision(self):
        if self.fruit.pos == self.snake.body[0]:
            self.fruit.randomize()
            self.snake.add_block()
        for block in self.snake.body[1:]:
            if block == self.fruit.pos:
                self.fruit.randomize()

    def check_fail(self):
        if not 0 <= self.snake.body[0].x < cell_number or not 0 <= self.snake.body[0].y < cell_number:
            self.game_over()

        for block in self.snake.body[1:]:
            if block == self.snake.body[0]:
                self.game_over()
    def game_over(self):
        overlay_color = pygame.Color(0, 0, 0, 180) 
        screen.fill(overlay_color)  
        
        game_over_font = pygame.font.Font(None, 30)
        game_over_text = game_over_font.render("Game Over! Press R to restart or BACKSPACE to return to the menu!", True, (117, 11, 11))
        game_over_rect = game_over_text.get_rect(center=(cell_number * cell_size // 2, cell_number * cell_size // 2))
        screen.blit(game_over_text, game_over_rect)

        pygame.display.update()
        self.wait_for_restart()
    

    
    def wait_for_restart(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
                    self.reset_game()
                    return
                if event.type == pygame.KEYDOWN and event.key == pygame.K_BACKSPACE:
                    self.return_to_menu = True
                    return
                

    def reset_game(self):
        self.snake = SNAKE()
        self.fruit = FRUIT()
        self.return_to_menu = False
    

    def draw_grass(self):
        grass_color = (54, 110, 38)
        for row in range(cell_number):
            if row % 2 == 0:
                for col in range(cell_number):
                    if col % 2 == 0:
                        grass_rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
                        pygame.draw.rect(screen, grass_color, grass_rect)
            else:
                for col in range(cell_number):
                    if col % 2 != 0:
                        grass_rect = pygame.Rect(col * cell_size, row * cell_size, cell_size, cell_size)
                        pygame.draw.rect(screen, grass_color, grass_rect)

    def draw_score(self):
        score_text = str(len(self.snake.body) - 3)
        score_surface = game_font.render(score_text, True, (11, 36, 17))
        score_x = int(cell_size * cell_number - 20)
        score_y = int(cell_size * cell_number - 20)
        score_rect = score_surface.get_rect(center=(score_x, score_y))
        screen.blit(score_surface, score_rect)

class SNAKE:
    def __init__(self):
        self.body = [Vector2(5, 10), Vector2(4, 10), Vector2(3, 10)]
        self.direction = Vector2(1, 0)
        self.new_block = False

        self.head_up = pygame.image.load(headup).convert_alpha()
        self.head_down = pygame.image.load(headdown).convert_alpha()
        self.head_right = pygame.image.load(headright).convert_alpha()
        self.head_left = pygame.image.load(headleft).convert_alpha()

        self.tail_up = pygame.image.load(tailup).convert_alpha()
        self.tail_down = pygame.image.load(taildown).convert_alpha()
        self.tail_right = pygame.image.load(tailright).convert_alpha()
        self.tail_left = pygame.image.load(tailleft).convert_alpha()

        self.body_vertical = pygame.image.load(bodyv).convert_alpha()
        self.body_horizontal = pygame.image.load(bodyh).convert_alpha()

        self.body_tr = pygame.image.load(bodytr).convert_alpha()
        self.body_tl = pygame.image.load(bodytl).convert_alpha()
        self.body_br = pygame.image.load(bodybr).convert_alpha()
        self.body_bl = pygame.image.load(bodybl).convert_alpha()

    def draw_snake(self):
        self.update_head_graphics()
        self.update_tail_graphics()

        for index, block in enumerate(self.body):
            x_pos = int(block.x * cell_size)
            y_pos = int(block.y * cell_size)
            block_rect = pygame.Rect(x_pos, y_pos, cell_size, cell_size)

            if index == 0:
                screen.blit(self.head, block_rect)
            elif index == len(self.body) - 1:
                screen.blit(self.tail, block_rect)
            else:
                previous_block = self.body[index + 1] - block
                next_block = self.body[index - 1] - block

                if previous_block.x == next_block.x:
                    screen.blit(self.body_vertical, block_rect)
                elif previous_block.y == next_block.y:
                    screen.blit(self.body_horizontal, block_rect)
                else:
                    if previous_block.x == -1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == -1:
                        screen.blit(self.body_tl, block_rect)
                    elif previous_block.x == -1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == -1:
                        screen.blit(self.body_bl, block_rect)
                    elif previous_block.x == 1 and next_block.y == -1 or previous_block.y == -1 and next_block.x == 1:
                        screen.blit(self.body_tr, block_rect)
                    elif previous_block.x == 1 and next_block.y == 1 or previous_block.y == 1 and next_block.x == 1:
                        screen.blit(self.body_br, block_rect)

    def update_head_graphics(self):
        head_relation = self.body[1] - self.body[0]
        if head_relation == Vector2(1, 0):
            self.head = self.head_left
        elif head_relation == Vector2(-1, 0):
            self.head = self.head_right
        elif head_relation == Vector2(0, 1):
            self.head = self.head_up
        elif head_relation == Vector2(0, -1):
            self.head = self.head_down

    def update_tail_graphics(self):
        tail_relation = self.body[-2] - self.body[-1]
        if tail_relation == Vector2(1, 0):
            self.tail = self.tail_left
        elif tail_relation == Vector2(-1, 0):
            self.tail = self.tail_right
        elif tail_relation == Vector2(0, 1):
            self.tail = self.tail_up
        elif tail_relation == Vector2(0, -1):
            self.tail = self.tail_down

    def move_snake(self):
        if self.new_block == True:
            body_copy = self.body[:]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]
            self.new_block = False
        else:
            body_copy = self.body[:-1]
            body_copy.insert(0, body_copy[0] + self.direction)
            self.body = body_copy[:]

    def add_block(self):
        self.new_block = True

class FRUIT:
    def __init__(self):
        self.randomize()

    def draw_fruit(self):
        fruit_rect = pygame.Rect(int(self.pos.x * cell_size), int(self.pos.y * cell_size), cell_size, cell_size)
        screen.blit(food, fruit_rect)

    def randomize(self):
        self.x = random.randint(0, cell_number - 1)
        self.y = random.randint(0, cell_number - 1)
        self.pos = Vector2(self.x, self.y)

khinkali = os.path.join(os.getcwd(), "Graphics\khinkali.png")
headup = os.path.join(os.getcwd(), "Graphics\head_up.png")
headdown = os.path.join(os.getcwd(), "Graphics\head_down.png")
headright = os.path.join(os.getcwd(), "Graphics\head_right.png")
headleft = os.path.join(os.getcwd(), "Graphics\head_left.png")
tailup = os.path.join(os.getcwd(), "Graphics\Tail_up.png")
taildown = os.path.join(os.getcwd(), "Graphics\Tail_down.png")
tailright = os.path.join(os.getcwd(), "Graphics\Tail_right.png")
tailleft = os.path.join(os.getcwd(), "Graphics\Tail_left.png")
bodytr = os.path.join(os.getcwd(), "Graphics\Body_tr.png")
bodytl = os.path.join(os.getcwd(), "Graphics\Body_tl.png")
bodybr = os.path.join(os.getcwd(), "Graphics\Body_br.png")
bodybl = os.path.join(os.getcwd(), "Graphics\Body_bl.png")
bodyv = os.path.join(os.getcwd(), "Graphics\Body_vertical.png")
bodyh = os.path.join(os.getcwd(), "Graphics\Body_horizontal.png")

pygame.init()
cell_size = 40
cell_number = 20
screen = pygame.display.set_mode((cell_number * cell_size, cell_number * cell_size))
clock = pygame.time.Clock()
food = pygame.image.load(khinkali).convert_alpha()
game_font = pygame.font.Font(None, 25)

SCREEN_UPDATE = pygame.USEREVENT
pygame.time.set_timer(SCREEN_UPDATE, 150)

main_menu = MainMenu()
difficulty_menu = DifficultyMenu()
main_game = MAIN()

while True:
    main_menu.draw()
    pygame.display.update()

    if main_menu.handle_events() == "start":
        return_to_difficulty_menu = False  

        while not return_to_difficulty_menu:
            difficulty_menu.draw()
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1 or event.key == pygame.K_2 or event.key == pygame.K_3:
                        difficulty_menu.selected_difficulty = int(chr(event.key))
                        return_to_difficulty_menu = True

        snake_speeds = {1: 150, 2: 100, 3: 70}
        selected_speed = snake_speeds.get(difficulty_menu.selected_difficulty, 150)

        main_game.reset_game()
        pygame.time.set_timer(SCREEN_UPDATE, selected_speed)

        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == SCREEN_UPDATE:
                    main_game.update()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        if main_game.snake.direction.y != 1:
                            main_game.snake.direction = Vector2(0, -1)
                    if event.key == pygame.K_DOWN:
                        if main_game.snake.direction.y != -1:
                            main_game.snake.direction = Vector2(0, +1)
                    if event.key == pygame.K_LEFT:
                        if main_game.snake.direction.x != 1:
                            main_game.snake.direction = Vector2(-1, 0)
                    if event.key == pygame.K_RIGHT:
                        if main_game.snake.direction.x != -1:
                            main_game.snake.direction = Vector2(+1, 0)

            screen.fill((60, 120, 42))
            main_game.draw_elements()
            pygame.display.update()
            clock.tick(60)

            if main_game.get_return_to_menu():
                break