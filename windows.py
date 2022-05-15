import pygame


class Menu:
    def __init__(self, screen_size):
        self.running = True
        self.window = 'menu'
        self.window_name = 'menu'
        self.screen_size = screen_size
        self.generate_image()

    def update(self, screen):
        screen.blit(self.background, (0, 0))
        screen.blit(self.play_button, self.play_button_rect)
        screen.blit(self.leaderboard_button, self.leaderboard_button_rect)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.play_button_rect.collidepoint(event.pos):
                    self.window = 'game'
                elif self.leaderboard_button_rect.collidepoint(event.pos):
                    self.window = 'leaderboard'

    def generate_image(self):
        self.background = pygame.image.load("assets/background.jpg")
        self.background = pygame.transform.scale(self.background, self.screen_size)

        self.play_button = pygame.image.load("assets/play_button.png")
        self.play_button_rect = self.play_button.get_rect()
        self.play_button_rect.x = 140
        self.play_button_rect.y = 350

        self.leaderboard_button = pygame.image.load("assets/leaderboard_button.png")
        self.leaderboard_button_rect = self.leaderboard_button.get_rect()
        self.leaderboard_button_rect.x = 90
        self.leaderboard_button_rect.y = 500


class Leaderboard:
    def __init__(self, screen_size):
        self.running = True
        self.window = 'leaderboard'
        self.window_name = 'leaderboard'
        self.screen_size = screen_size
        self.generate_image()
        self.font_score = pygame.font.Font("zorque.regular.otf", 25)

    def update(self, screen):
        screen.blit(self.background, (0, 0))
        screen.blit(self.scoreboard, self.scoreboard_rect)
        screen.blit(self.pause, self.pause_rect)
        self.blit_score(screen, 350)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.pause_rect.collidepoint(event.pos):
                    self.window = 'pause'

    def blit_score(self, screen, x):
        y = 152
        with open('files/bestScore.txt') as f:
            scores = f.readlines()
            for element in scores:
                element = str(element)
                element = element[0:-1]
                screen.blit(self.font_score.render(self.setup_font(element), True, (110, 110, 110)), (x, y))
                y += 65

    def setup_font(self, text):
        i = 0
        text_list = []
        for element in text[-1::-1]:
            text_list.append(element)
            i += 1
            if i == 3:
                text_list.append(" ")
                i = 0
        text_list = text_list[-1::-1]
        text = "".join(text_list)
        return text

    def generate_image(self):
        self.background = pygame.image.load("assets/background.jpg")
        self.background = pygame.transform.scale(self.background, self.screen_size)

        self.scoreboard = pygame.image.load("assets/scoreboard.png")
        self.scoreboard_rect = self.scoreboard.get_rect()
        self.scoreboard_rect.x = 0
        self.scoreboard_rect.y = 0

        self.pause = pygame.image.load("assets/pause.png")
        self.pause_rect = self.pause.get_rect()
        self.pause_rect.x = 2
        self.pause_rect.y = 7


class GameOver:
    def __init__(self, screen_size):
        self.running = True
        self.window = 'gameover'
        self.window_name = 'gameover'
        self.screen_size = screen_size
        self.font_score = pygame.font.Font("zorque.regular.otf", 33)
        self.last_puntos = 0
        self.generate_image()

    def update(self, screen):
        screen.blit(self.background, (0, 0))
        screen.blit(self.play_button, self.play_button_rect)
        screen.blit(self.menu_button, self.menu_button_rect)
        points, lenght = self.setup_font(str(int(self.last_puntos)))
        self.blit_text(f"Tu as fait {points} points  BG!", (192, 19, 243), 62, 200, screen, lenght)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.play_button_rect.collidepoint(event.pos):
                    self.window = 'game'
                if self.menu_button_rect.collidepoint(event.pos):
                    self.window = 'menu'

    def setup_font(self, text):
        i = 0
        text_list = []
        for element in text[-1::-1]:
            text_list.append(element)
            i += 1
            if i == 3:
                text_list.append(" ")
                i = 0
        text_list = text_list[-1::-1]
        text = "".join(text_list)
        return text, len(text)

    def blit_text(self, text, color, x, y, screen, lenght):
        image = self.font_score.render(text, True, color)
        screen.blit(image, (x - 6.5*lenght, y))

    def generate_image(self):
        self.background = pygame.image.load("assets/background.jpg")
        self.background = pygame.transform.scale(self.background, self.screen_size)

        self.play_button = pygame.image.load("assets/play_button.png")
        self.play_button_rect = self.play_button.get_rect()
        self.play_button_rect.x = 140
        self.play_button_rect.y = 320

        self.menu_button = pygame.image.load("assets/menu_button.png")
        self.menu_button_rect = self.menu_button.get_rect()
        self.menu_button_rect.x = 140
        self.menu_button_rect.y = 440


class Pause:
    def __init__(self, screen_size):
        self.running = True
        self.window_before = ''
        self.window = 'pause'
        self.window_name = 'pause'
        self.screen_size = screen_size
        self.pause = True
        self.generate_image()

    def update(self, screen):
        screen.blit(self.pause_background, self.pause_background_rect)
        screen.blit(self.play_button, self.play_button_rect)
        screen.blit(self.menu_button, self.menu_button_rect)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.play_button_rect.collidepoint(event.pos):
                    self.window = self.window_before
                    self.pause = False
                if self.menu_button_rect.collidepoint(event.pos):
                    self.window = 'menu'
                    self.pause = False

    def generate_image(self):
        self.pause_background = pygame.image.load("assets/pause_background.png")
        self.pause_background_rect = self.pause_background.get_rect()
        self.pause_background_rect.x = 50
        self.pause_background_rect.y = 240

        self.play_button = pygame.image.load("assets/play_button.png")
        self.play_button_rect = self.play_button.get_rect()
        self.play_button_rect.x = 140
        self.play_button_rect.y = 320

        self.menu_button = pygame.image.load("assets/menu_button.png")
        self.menu_button_rect = self.menu_button.get_rect()
        self.menu_button_rect.x = 140
        self.menu_button_rect.y = 440


