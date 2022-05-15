import pygame
import random
import copy


class Piece:
    def __init__(self, game, piece='random'):
        self.piece = piece
        self.game = game
        self.hauteur = 0
        self.largeur = 4
        self.largeur_default, self.hauteur_default = self.largeur, self.hauteur
        self.all_shapes = generate_schematic_piece()

        self.colors = {'cyan': (53, 245, 242), 'red': (238, 33, 33), 'green': (28, 198, 46), 'pink': (241, 102, 227),
                      'blue': (36, 49, 209), 'orange': (255, 97, 28), 'yellow': (255, 213, 25), 'purple': (192, 19, 243)}

        if self.piece == 'random':
            self.shape, self.color = self.generate_piece()
        else:
            self.shape, self.color = self.copy(), self.colors[self.piece]
    
    def generate_piece(self):
        shape_valide = False
        while not shape_valide:
            new_shape = random.choice(self.all_shapes)
            for element in self.game.shape_onenamarredetevoir:
                if new_shape[0] == element[0]:
                    break
            else:
                shape_valide = True

        self.game.shape_onenamarredetevoir.insert(0, new_shape)
        if len(self.game.shape_onenamarredetevoir) > 3:
            self.game.shape_onenamarredetevoir.pop(-1)

        self.hauteur = self.hauteur_default
        self.largeur = self.largeur_default

        return new_shape[1], self.colors[new_shape[0]]

    def copy(self):
        new_shape = [element for element in self.all_shapes if self.piece in element]
        new_shape = new_shape[0]

        return new_shape[1]

    def create_shape(self, schematic, x=180, y=15, height=38, width=38):
        y_save = y
        for i in range(len(schematic)):
            for j in range(len(schematic)):
                if schematic[j][i] != 0:
                    schematic[j][i] = pygame.Rect(x, y, height, width)
                y += height + 2
            y = y_save
            x += width + 2
        return schematic

    def fall(self):
        if self.check_hauteur(self.shape, self.game.hauteur+765):
            if self.game.collide_check:
                for i in range(len(self.shape)):
                    for j in range(len(self.shape)):
                        if self.shape[j][i] != 0:
                            self.shape[j][i].top += 40
                self.hauteur += 1
        return self.shape

    def instant_fall(self):
        self.game.instant_fall = True
        while self.check_hauteur(self.shape, self.game.hauteur+765) and self.game.check_grid():
            for i in range(len(self.shape)):
                for j in range(len(self.shape)):
                    if self.shape[j][i] != 0:
                        self.shape[j][i].top += 40
            self.hauteur += 1
        self.game.falling_piece = False
        self.game.compteur_grid = self.game.slow_grid

    def check_hauteur(self, shape, value_max=895):
        for i in range(len(shape)):
            for j in range(len(shape)):
                if shape[j][i] != 0 and shape[j][i] != 1:
                    if shape[j][i].top >= value_max:
                        return False
        else:
            return True

    def move_right(self):
        if self.check_move_right(self.shape):
            if self.game.check_grid_right():
                for i in range(len(self.shape)):
                    for j in range(len(self.shape)):
                        if self.shape[j][i] != 0:
                            self.shape[j][i].left += 40
                self.largeur += 1
        return self.shape

    def check_move_right(self, shape, value_max=380):
        for i in range(len(shape)):
            for j in range(len(shape)):
                if shape[j][i] != 0:
                    if shape[j][i].left == value_max:
                        return False
        else:
            return True

    def move_left(self):
        if self.check_move_left(self.shape):
            if self.game.check_grid_left():
                for i in range(len(self.shape)):
                    for j in range(len(self.shape)):
                        if self.shape[j][i] != 0:
                            self.shape[j][i].left -= 40
                self.largeur -= 1
            return self.shape

    def check_move_left(self, shape, value_max=20):
        for i in range(len(shape)):
            for j in range(len(shape)):
                if shape[j][i] != 0:
                    if shape[j][i].left == value_max:
                        return False
        else:
            return True


    def check_rotate_hauteur(self):
        new_shape = self.rotate_left()
        left = self.check_hauteur(new_shape, value_max=self.game.hauteur+805)
        new_shape = self.rotate_right()
        right = self.check_hauteur(new_shape, value_max=self.game.hauteur+805)
        if left and right:
            return True
        else:
            return False

    def check_rotate_right(self):
        new_shape = self.rotate_right()
        right = self.check_move_right(new_shape, value_max=420)
        new_shape = self.rotate_left()
        left = self.check_move_right(new_shape, value_max=-20)
        if left and right:
            return True
        else:
            return False

    def check_rotate_left(self):
        new_shape = self.rotate_left()
        left = self.check_move_left(new_shape, value_max=-20)
        new_shape = self.rotate_right()
        right = self.check_move_left(new_shape, value_max=420)
        if left and right:
            return True
        else:
            return False

    def rotate_right(self):
        lenght = len(self.shape)
        new_shape = []
        i = 0
        while i <= lenght - 1:
            j = lenght - 1
            new_row = []
            while j >= 0:
                new_row.append(self.shape[j][i])
                j -= 1
            new_shape.append(new_row)
            i += 1
        new_shape = self.create_shape(new_shape, 20+40*self.largeur, self.game.hauteur-130+15+40*self.hauteur)
        return new_shape

    def rotate_left(self):
        lenght = len(self.shape)
        new_shape = []
        i = lenght - 1
        while i >= 0:
            j = 0
            new_row = []
            while j <= lenght - 1:
                new_row.append(self.shape[j][i])
                j += 1
            new_shape.append(new_row)
            i -= 1
        new_shape = self.create_shape(new_shape, 20+40*self.largeur, self.game.hauteur-130+15+40*self.hauteur)
        return new_shape


def generate_schematic_piece():
    cyan = 'cyan', [[0, 0, 0, 0],
            [1, 1, 1, 1],
            [0, 0, 0, 0],
            [0, 0, 0, 0]]
    pink = 'pink', [[0, 0, 0],
            [1, 1, 1],
            [0, 1, 0]]
    green = 'green', [[0, 0, 0],
             [1, 1, 0],
             [0, 1, 1]]
    red = 'red', [[0, 0, 0],
           [0, 1, 1],
           [1, 1, 0]]
    orange = 'orange', [[0, 0, 0],
              [1, 1, 1],
              [1, 0, 0]]
    blue = 'blue', [[0, 0, 0],
            [1, 1, 1],
            [0, 0, 1]]
    yellow = 'yellow', [[1, 1],
              [1, 1]]
    test = 'pink', [[0, 0, 1, 1, 0],
                    [1, 0, 1, 0, 0],
                    [1, 1, 1, 1, 1],
                    [0, 0, 1, 0, 1],
                    [0, 0, 0, 1, 1]]

    return [cyan, pink, red, green, orange, blue, yellow]  # [pink]
