from random import seed
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

class ConwaysGOL:

    def __init__(self, seed ='random_seeds', nx_cells=200, ny_cells=200, neighbourhood = 'moore', name='Conways Game of Life'):
        self.name = name
        self.seed = seed
        self.N1 = nx_cells
        self.N2 = ny_cells
        self.padding_x = 20
        self.padding_y = 20
        self.N1_inf = self.N1 + 2*self.padding_x
        self.N2_inf = self.N2 + 2*self.padding_y
        self.neighbourhood = neighbourhood
        self.curr_state = np.zeros((self.N1_inf, self.N2_inf))
        self.history = []
        self.initialize(self.seed)

    def initialize(self, init_cond = 'random_seeds', k = 0.8):
        if init_cond == 'random_seeds':
            seed_array = np.random.rand(self.N1_inf, self.N2_inf)
            self.curr_state[np.where(seed_array > k)] = 1
        elif init_cond == 'line':
            line_length = round(k * self.N2)
            mid_x = self.N1_inf//2
            ylim_0 = self.N2//2 - 2*self.padding_y
            ylim_1 = ylim_0 + line_length
            self.curr_state[mid_x, ylim_0:ylim_1] = 1
        elif init_cond == '2 lines':
            line_length = round(k * self.N2)
            ylim_0 = self.N2//2 - 2*self.padding_y
            ylim_1 = ylim_0 + line_length
            for line in range(1,3):
                mid_x = line * self.N1_inf//3
                self.curr_state[mid_x, ylim_0:ylim_1] = 1
        elif init_cond == 'cross':
            line_length = round(k * self.N2)
            mid_x = self.N1_inf//2
            ylim_0 = self.N2//2 - 2*self.padding_y
            ylim_1 = ylim_0 + line_length
            self.curr_state[mid_x, ylim_0:ylim_1] = 1
            self.curr_state[ylim_0:ylim_1, mid_x] = 1
        elif init_cond == 'box':
            line_length = round(k * self.N2)
            ylim_0 = self.N2//2 - 2*self.padding_y
            ylim_1 = ylim_0 + line_length
            for line in range(1,3):
                mid_x = line * self.N1_inf//3
                self.curr_state[mid_x, ylim_0:ylim_1] = 1
                self.curr_state[ylim_0:ylim_1, mid_x] = 1
        else:
            pass

    def update(self):
        if np.count_nonzero(self.curr_state) == 0:
            pass
        else:
            if len(self.history) == 0:
                prev_state = self.curr_state.copy()
                self.history.append(prev_state)
            update_state = np.zeros_like(self.curr_state)
            for row in range(2, self.curr_state.shape[0]-2):
                for col in range(2, self.curr_state.shape[1]-2):
                    
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
                        neighbours = self.curr_state[row-1, col-1] + self.curr_state[row-1, col] + self.curr_state[row-1, col+1] + \
                        self.curr_state[row, col-1] + self.curr_state[row, col+1] + \
                        self.curr_state[row+1, col-1] + self.curr_state[row +
                                                                        1, col] + self.curr_state[row+1, col+1] 

                    if neighbours == 2:
                        update_state[row, col] = self.curr_state[row, col]
                    elif neighbours == 3:
                        update_state[row, col] = 1
                    elif neighbours < 2:
                        update_state[row, col] = 0
                    elif neighbours > 3:
                        update_state[row, col] = 0
            self.curr_state = update_state
            self.history.append(update_state)
        return self

    def simulate(self, n_steps=100):
        for t in range(n_steps):
            self.update()
        return self

    def plot(self, n_steps=100, cmap='RdGy_r', color_scheme='binary', save=False):

        # To Do:
        # 1. Color according to history
        # 2. Optionally save animations

        
        xlim_0 = self.padding_x
        xlim_1 = xlim_0 + self.N1 + self.padding_x
        ylim_0 = self.padding_y
        ylim_1 = ylim_0 + self.N2 + self.padding_y
        
        static_history = self.curr_state.copy()

        fig, axes = plt.subplots(1,1, figsize = (10,10))
        img1 = plt.imshow(np.transpose(static_history[xlim_0:xlim_1, ylim_0:ylim_1]), animated=True, cmap=cmap)
        def animate_func(*args):
            t = len(self.history) + 1
            self.update()
            static_history = self.history[t-1].copy()
            img1.set_array(np.transpose(static_history[xlim_0:xlim_1, ylim_0:ylim_1]))
            return img1,
        anim = FuncAnimation(fig, animate_func, blit=True)
        plt.show()




if __name__ == "__main__":

    test = ConwaysGOL(seed='line', neighbourhood='moore')
    # test.plot_animate()
    test.plot()