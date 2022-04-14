from tkinter import N
import numpy as np
import pygame


class Conways_GameGrid:

    def __init__(self, n_rows=20, n_cols=20, width=15, height=15, margin=2, neighbourhood='moore'):
        self.width = width
        self.height = height
        self.margin = margin

        self.n_rows = n_rows
        self.n_cols = n_cols
        self.neighbourhood = neighbourhood
        self.buttons = {}
        self.button_height = 40
        self.button_width = 100
        self.button_margin = 15
        self.y_offset = self.button_height + self.button_margin

        self.button_state = 'reset'  # default state
        if type == 'empty':
            self.data_array = np.zeros((self.n_rows, self.n_cols))
        # create a bunch of events
        self.button_messages = {'start': 'Starting animation now... Click reset to start over',
                                'pause': 'Pausing animation now... Click start to continue',
                                'reset': 'Grid is going to be reset.... once reset, you can initialize \
                                      the grid by clicking cells of your chocie'}

        self.initialize(type='random')
        self.display_grid()

    def initialize(self, type='empty'):
        self.button_state = 'reset'  # default state
        if type == 'empty':
            self.data_array = np.zeros((self.n_rows, self.n_cols))
        elif type == 'random':
            k = 0.5
            seed_array = np.random.rand(self.n_rows, self.n_cols)
            self.data_array = np.zeros((self.n_rows, self.n_cols))
            self.data_array[np.where(seed_array > k)] = 1

    def mouse_to_grid(self, mouse_pos):
        if mouse_pos[1] > self.y_offset:
            mouse_pos_y = mouse_pos[1] - self.y_offset
            i_row = (mouse_pos[0] - self.margin)//(self.margin + self.height)
            i_col = (mouse_pos_y - self.margin)//(self.margin + self.width)
            grid_pos = ['grid_click', i_row, i_col]
        else:
            button_x = (mouse_pos[0] - self.button_margin) / \
                (self.button_margin + self.button_width)

            grid_pos = ['button_click', button_x, 0]

        return grid_pos

    def handle_buttonclick(self, button_x):
        margin_ratio = self.button_margin / \
            (self.button_width + self.button_margin)
        if (button_x >= 0) & (button_x+margin_ratio <= 1):
            self.button_state = 'start'
        elif (button_x >= 1) & (button_x+margin_ratio <= 2):
            self.button_state = 'pause'
        elif (button_x >= 2) & (button_x+margin_ratio <= 3):
            self.button_state = 'reset'
        print(self.button_messages[self.button_state])

    def run_ca(self):
        if np.count_nonzero(self.data_array) == 0:
            pass
        else:
            update_state = np.zeros_like(self.data_array)
            for row in range(1, self.data_array.shape[0]-1):
                for col in range(1, self.data_array.shape[1]-1):

                    if self.neighbourhood == 'neumann1':
                        neighbours = self.curr_state[row-1, col] + self.curr_state[row, col-1] + \
                            self.curr_state[row, col+1] + self.curr_state[row + 1, col] 
                    elif self.neighbourhood == 'neumann2':
                        neighbours = self.curr_state[row-1, col] + self.curr_state[row-2, col] + \
                            self.curr_state[row, col-1] + self.curr_state[row, col-2] + \
                            self.curr_state[row, col+1] + self.curr_state[row, col+2] + \
                            self.curr_state[row + 1, col] + self.curr_state[row+2, col] + \
                            self.curr_state[row-1, col-1] + self.curr_state[row-1, col+1] +\
                            self.curr_state[row+1, col-1] + self.curr_state[row+1, col+1]
                    else:
                        neighbours = self.data_array[row-1, col-1] + self.data_array[row-1, col] + self.data_array[row-1, col+1] + \
                            self.data_array[row, col-1] + self.data_array[row, col+1] + \
                            self.data_array[row+1, col-1] + self.data_array[row +
                                                                            1, col] + self.data_array[row+1, col+1]
                    if neighbours == 2:
                        update_state[row, col] = self.data_array[row, col]
                    elif neighbours == 3:
                        update_state[row, col] = 1
                    elif neighbours < 2:
                        update_state[row, col] = 0
                    elif neighbours > 3:
                        update_state[row, col] = 0
            self.data_array = update_state

        return self

    def draw_buttons(self):

        WHITE = (255, 255, 255)
        RED = (255, 0, 0)
        for i, butt in enumerate(['start', 'pause', 'reset']):
            x0 = i * (self.button_margin + self.button_width) + \
                self.button_margin
            y0 = self.button_margin
            rect = [x0, y0, self.button_width, self.button_height]
            pygame.draw.rect(self.window, WHITE, rect, 2)
            self.window.blit(self.font.render(butt, True, RED), (x0+5, y0+5))
            self.buttons[butt] = rect
        return self

    def draw_grid(self):

        for i_row in range(self.n_rows):
            for i_col in range(self.n_cols):
                x0 = i_row * (self.margin + self.height) + self.margin
                y0 = i_col * (self.margin + self.width) + \
                    self.margin + self.y_offset
                rect = [x0, y0, self.width, self.height]
                if self.data_array[i_row, i_col] == 0:
                    rect_color = (255, 255, 255)
                elif self.data_array[i_row, i_col] == 1:
                    rect_color = (0, 0, 0)
                else:
                    rect_color = (255, 0, 0)
                pygame.draw.rect(self.window, rect_color, rect)
        return self

    def display_grid(self, window_size=(1000, 1000), caption="Cellular Automata", fps=60):
        pygame.init()
        self.window = pygame.display.set_mode(window_size)
        self.font = pygame.font.SysFont('Arial', 25)
        pygame.display.set_caption(caption)
        self.clock = pygame.time.Clock()
        BLACK = (0, 0, 0)
        # notification = ""
        flag = True
        grid_cycle = 0
        ca_cycle = 0
        while flag:
            grid_cycle += 1
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    flag = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    mouse_pos = pygame.mouse.get_pos()
                    click_target, grid_pos_x, grid_pos_y = self.mouse_to_grid(
                        mouse_pos)

                    if click_target == 'button_click':
                        # if button , then raise an event to reset or pause or start
                        self.handle_buttonclick(grid_pos_x)
                        if self.button_state == 'reset':
                            self.initialize()
                            grid_cycle = 0
                            ca_cycle = 0
                    elif (click_target == 'grid_click') & (self.button_state == 'reset'):
                        # print(grid_pos_x, grid_pos_y)
                        self.data_array[grid_pos_x, grid_pos_y] = 1

            # Game Logic
            if (self.button_state == 'start') & (grid_cycle % 20 == 0):
                ca_cycle += 1
                self.run_ca()

            # Screen-clearning

            # Draw
            self.window.fill(BLACK)
            self.window.blit(self.font.render(
                f'Gen:{ca_cycle}', True, (0, 0, 255)), (400, self.button_margin))
            self.draw_buttons()
            self.draw_grid()

            pygame.display.update()
            self.clock.tick(fps)

        pygame.quit()


if __name__ == "__main__":

    test = Conways_GameGrid(n_cols=50, n_rows=100)
