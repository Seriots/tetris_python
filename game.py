import pygame
from tetrisPiece import Piece
import os


class Game:
    def __init__(self, hauteur, screen_size):
        self.running = True
        self.window = 'game'
        self.window_name = 'game'
        self.screen_size = screen_size

        self.instant_fall = False

        self.hauteur = hauteur
        self.score = 0
        self.grid = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
        self.falling_piece = True
        self.slow = 100
        self.compteur = 0
        self.slow_grid = self.slow/2
        self.compteur_grid = 0
        self.slow_fall = 0
        self.multiplier = 1
        self.new_multiplier = 1
        self.nb_row_complete = 0
        self.last_ten_row = 0
        self.level = 0
        self.puntos = 0

        self.collide_check = True
        self.shape_onenamarredetevoir = []

        self.hold_buffer = True

        self.piece = Piece(self)

        self.piece.shape = self.piece.create_shape(self.piece.shape, y=self.hauteur-115)
        self.preview = [Piece(self)]
        self.preview.append(Piece(self))
        self.preview.append(Piece(self))

        for i in range(len(self.preview)):
            self.make_preview(470, 10+self.hauteur+75*i, self.preview[i])

        self.hold = None

        self.generate_image()

        self.font_score = pygame.font.Font("zorque.regular.otf", 25)

        if not os.path.exists("files/bestScore.txt"):
            file = open("files/bestScore.txt", "w+")
            file.write("0\n")
            file.close()

        if not os.path.exists("files/nameScore.txt"):
            file = open("files/nameScore.txt", "w+")
            file.write("Player\n")
            file.close()

        self.max_score = self.setup_max_score()

    def update(self, screen):
        screen.blit(self.background, (0, 0))
        #if self.falling_piece and self.collide_check:
        self.falling_piece = self.piece.check_hauteur(self.piece.shape, self.hauteur+765)
        self.collide_check = self.check_grid()

        if not self.falling_piece or not self.collide_check:
            if self.compteur_grid >= self.slow_grid:
                self.copy_in_grid()

                self.row_complete()
                if self.multiplier != self.new_multiplier:
                    self.multiplier = self.new_multiplier
                else:
                    self.new_multiplier, self.multiplier = 1, 1

                self.new_piece()
                self.instant_fall = False

                self.hold_buffer = True
            else:
                self.compteur_grid += 1

        if self.falling_piece and self.collide_check:
            if self.compteur >= self.slow:
                self.piece.fall()
                self.slow_fall = 2
                self.compteur = 0
                self.compteur_grid = 0
            else:
                self.compteur += 1

        for element in self.grid[1]+self.grid[0]:
            if element != 0:
                self.save_score()
                #self.reset()
                self.window = 'gameover'

                break

        for element in self.piece.shape:
            for value in element:
                if value != 0 and value != 1:
                    if value.top >= self.hauteur+5:
                        pygame.draw.rect(screen, self.piece.color, value)

        for i in range(len(self.grid)):
            for j in range(10):
                if self.grid[i][j] != 0:
                    pygame.draw.rect(screen, self.grid[i][j], pygame.Rect(20+40*j, self.hauteur-130+15+40*(i+1), 38, 38))

        if self.last_ten_row >= 10:
            self.level_up()

        screen.blit(self.grid_image, self.grid_rect_image)
        screen.blit(self.features, self.features_rect)
        screen.blit(self.hold_button, self.hold_button_rect)
        screen.blit(self.pause, self.pause_rect)

        for shape in self.preview:
            for element in shape.shape:
                for value in element:
                    if value != 0:
                        pygame.draw.rect(screen, shape.color, value)

        if self.hold is not None:
            for element in self.hold.shape:
                for value in element:
                    if value != 0:
                        pygame.draw.rect(screen, self.hold.color, value)

        self.blit_text(str(self.nb_row_complete), self.piece.colors['purple'], 498, self.hauteur+278, screen)

        self.blit_text(str(int(self.puntos)), self.piece.colors['purple'], 498, self.hauteur+333, screen)

        self.blit_text(str(self.max_score), self.piece.colors['purple'], 498, self.hauteur+390, screen)

        self.blit_text(str(self.level), self.piece.colors['purple'], 498, self.hauteur+447, screen)

        pygame.display.flip()

        if self.slow_fall > 0:
            self.slow_fall -= 1

        for event in pygame.event.get():
            # que l'evenement est fermeture de fenetre
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if self.slow_fall <= 0 and not self.instant_fall:
                    if event.key == pygame.K_e:
                        if self.piece.check_rotate_hauteur() and self.piece.check_rotate_right() and self.check_grid_rotate_right():
                            self.piece.shape = self.piece.rotate_right()
                            self.compteur_grid -= 5
                    elif event.key == pygame.K_a:
                        if self.piece.check_rotate_hauteur() and self.piece.check_rotate_left() and self.check_grid_rotate_left():
                            self.piece.shape = self.piece.rotate_left()
                            self.compteur_grid -= 5
                    elif event.key == pygame.K_DOWN:
                        self.piece.shape = self.piece.fall()
                    elif event.key == pygame.K_LEFT:
                        if self.check_grid_left():
                            self.piece.move_left()
                            self.collide_check = self.check_grid()
                            self.compteur_grid -= 5
                    elif event.key == pygame.K_RIGHT:
                        self.piece.move_right()
                        self.collide_check = self.check_grid()
                        self.compteur_grid -= 5

                    elif event.key == pygame.K_SPACE:
                        if self.piece.hauteur >= 0:
                            self.piece.instant_fall()
                    elif event.key == pygame.K_r:
                        if self.hold_buffer:
                            self.hold_piece()
                    elif event.key == pygame.K_t:
                        self.puntos *= 10

            elif event.type == pygame.MOUSEBUTTONDOWN:
                if self.hold_button_rect.collidepoint(event.pos):
                    if self.hold_buffer:
                        self.hold_piece()

                if self.pause_rect.collidepoint(event.pos):
                    self.window = 'pause'

    def save_score(self):
        with open('files/bestScore.txt', "r") as f:
            scores = f.readlines()
            insert = False
            i = 0
            for element in scores:
                element = element[0:-1]
                if int(element) < self.puntos:
                    scores.insert(i, str(int(self.puntos)) + "\n")
                    insert = True
                    break
                i += 1
            if not insert:
                scores.append(str(int(self.puntos)) + "\n")
            f.close()

        with open('files/bestScore.txt', "w+") as f:
            if len(scores) > 10:
                scores = scores[0:10]
            for element in scores:
                f.write(element)

            f.close()

    def setup_max_score(self):
        with open('files/bestScore.txt', "r") as f:
            max_score = f.readline()
            max_score = max_score[0:-1]
            f.close()
            return max_score

    def new_piece(self):
        self.piece = self.preview[0]
        del self.preview[0]
        self.piece.shape = self.piece.create_shape(self.piece.shape, y=self.hauteur-115)
        self.preview.append(Piece(self))
        for i in range(len(self.preview)):
            self.make_preview(470, 10 + self.hauteur + 75 * i, self.preview[i])

        self.falling_piece = True
        self.collide_check = True
        self.compteur_grid = 0

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

    def blit_text(self, text, color, x, y, screen):
        text, lenght = self.setup_font(text)
        image = self.font_score.render(text, True, color)
        screen.blit(image, (x - 6.5*lenght, y))

    def make_preview(self, x, y, element):
        # modifier pour mettre au bon endroit dans la preview
        lenght = len(element.shape)
        if lenght <= 2:
            element.shape = element.create_shape(element.shape, x - 10*(lenght-3), y+20*(3-lenght), 20, 20)
        else:
            element.shape = element.create_shape(element.shape, x - 10 * (lenght - 3), y, 20, 20)

    def copy_in_grid(self):
        for i in range(len(self.piece.shape)):
            for j in range(len(self.piece.shape)):
                if self.piece.shape[i][j] != 0:
                    self.grid[self.piece.hauteur + i-1][self.piece.largeur + j] = self.piece.color

    def row_complete(self):
        nb_row_complete_before = self.nb_row_complete
        for row in self.grid:
            if 0 not in row:
                self.nb_row_complete += 1
                self.last_ten_row += 1
                self.grid.remove(row)
                self.grid.insert(0, [0, 0, 0, 0, 0, 0, 0, 0, 0, 0])

        if self.nb_row_complete - nb_row_complete_before > 0:
            self.puntos += 2**(self.nb_row_complete - nb_row_complete_before)*(200-self.slow)*self.multiplier
            self.new_multiplier *= 1.25**(self.nb_row_complete-nb_row_complete_before)

    def check_grid(self):
        for i in range(len(self.piece.shape)):
            for j in range(len(self.piece.shape)):
                if self.piece.shape[i][j] != 0:
                    if self.grid[self.piece.hauteur + i][self.piece.largeur + j] != 0:
                        return False
        else:
            return True

    def check_grid_right(self):
        for i in range(len(self.piece.shape)):
            for j in range(len(self.piece.shape)):
                if self.piece.shape[i][j] != 0:
                    if self.grid[self.piece.hauteur + i-1][self.piece.largeur + j + 1] != 0:
                        return False
        else:
            return True

    def check_grid_left(self):
        for i in range(len(self.piece.shape)):
            for j in range(len(self.piece.shape)):
                if self.piece.shape[i][j] != 0:
                    if self.grid[self.piece.hauteur + i - 1][self.piece.largeur + j - 1] != 0:
                        return False
        else:
            return True

    def check_grid_rotate_right(self):
        new_shape = self.piece.rotate_right()
        for i in range(len(new_shape)):
            for j in range(len(new_shape)):
                if new_shape[i][j] != 0:
                    if self.grid[self.piece.hauteur + i - 1][self.piece.largeur + j] != 0:
                        return False
        else:
            return True

    def check_grid_rotate_left(self):
        new_shape = self.piece.rotate_left()
        for i in range(len(new_shape)):
            for j in range(len(new_shape)):
                if new_shape[i][j] != 0:
                    if self.grid[self.piece.hauteur + i - 1][self.piece.largeur + j] != 0:
                        return False
        else:
            return True

    def hold_piece(self):
        color = [k for (k, val) in self.piece.colors.items() if val == self.piece.color]
        if self.hold is None:
            self.hold = Piece(self, piece=color[0])
            self.make_preview(470, self.hauteur+500, self.hold)
            self.new_piece()
        else:
            self.hold, self.piece = Piece(self, piece=color[0]), self.hold
            self.make_preview(470, self.hauteur+500, self.hold)
            self.piece.shape = self.piece.create_shape(self.piece.shape, y=self.hauteur-115)

        self.hold_buffer = False

    def level_up(self):
        self.slow -= 5
        self.slow_grid -= 2
        self.level += 1
        self.last_ten_row -= 10

    def reset(self):
        self.running = True
        self.window = 'game'
        self.window_name = 'game'
        self.instant_fall = False
        self.score = 0
        self.grid = [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                     [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
        self.falling_piece = True
        self.slow = 100
        self.compteur = 0
        self.slow_grid = self.slow / 2
        self.compteur_grid = 0
        self.slow_fall = 0
        self.multiplier = 1
        self.new_multiplier = 1
        self.nb_row_complete = 0
        self.last_ten_row = 0
        self.level = 0
        self.puntos = 0

        self.collide_check = True
        self.shape_onenamarredetevoir = []

        self.hold_buffer = True

        self.piece = Piece(self)

        self.piece.shape = self.piece.create_shape(self.piece.shape, y=self.hauteur - 115)
        self.preview = [Piece(self)]
        self.preview.append(Piece(self))
        self.preview.append(Piece(self))

        for i in range(len(self.preview)):
            self.make_preview(470, 10 + self.hauteur + 75 * i, self.preview[i])

        self.hold = None

        self.generate_image()

        self.font_score = pygame.font.Font("zorque.regular.otf", 25)

        if not os.path.exists("files/bestScore.txt"):
            file = open("files/bestScore.txt", "w+")
            file.write("0\n")
            file.close()

        if not os.path.exists("files/nameScore.txt"):
            file = open("files/nameScore.txt", "w+")
            file.write("Player\n")
            file.close()

        self.max_score = self.setup_max_score()

    def generate_image(self):
        self.background = pygame.image.load("assets/background.jpg")
        self.background = pygame.transform.scale(self.background, self.screen_size)

        self.grid_image = pygame.image.load("assets/grid.png")
        # grid = pygame.transform.scale(grid, (300, 600))
        self.grid_rect_image = self.grid_image.get_rect()
        self.grid_rect_image.x = 15
        self.grid_rect_image.y = self.hauteur

        self.features = pygame.image.load("assets/in_game_features.jpg")
        self.features_rect = self.features.get_rect()
        self.features_rect.x = 15 + 400 + 15
        self.features_rect.y = self.hauteur

        self.hold_button = pygame.image.load("assets/hold_button.png")
        self.hold_button_rect = self.hold_button.get_rect()
        self.hold_button_rect.x = 15 + 400 + 15
        self.hold_button_rect.y = self.hauteur+590

        self.pause = pygame.image.load("assets/pause.png")
        self.pause_rect = self.pause.get_rect()
        self.pause_rect.x = 15
        self.pause_rect.y = 15


