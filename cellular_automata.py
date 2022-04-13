from turtle import title
import numpy as np
import random
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

class CA_Generator:

    def __init__(self, dim = 1, rule ='rule_30', n_cells = 1000, neighbourhood = 'moore'):

        
        self.dim = dim
        self.rule = rule
        if self.dim == 1:
            rule_int = int(self.rule.split('_')[1])
            # rule_bin = bin(int)
            self.rule_8bit = list(reversed(list(f'{rule_int:08b}')))
            self.rule_map = {f'{cell_state:03b}': self.rule_8bit[cell_state] for cell_state in range(8)}
            self.name = f'Elementary CA with rule {rule_int}'

        self.grid_padding = 5
        self.N1 = n_cells + 2*self.grid_padding
        self.curr_state = np.zeros((self.N1,))
        self.history = []
        self.initialize()

    def initialize(self):
        if self.dim == 1:
            mid_cell = self.N1//2
            self.curr_state[mid_cell] = 1
        return self
       
    
    def update(self):
        temp_state = self.curr_state.copy()
        if len(self.history) == 0:
            self.history.append(temp_state)   
        for cell in range(self.grid_padding,self.N1-self.grid_padding):
            cell_state = [temp_state[cell-1],temp_state[cell], temp_state[cell+1]]
            bin_state = ''.join([str(int(i)) for i in cell_state])
            new_cell_state = int(self.rule_map[bin_state])
            self.curr_state[cell] = new_cell_state
        curr_state = self.curr_state.copy()
        self.history.append(curr_state)
        return self

    def simulate(self, n_steps=50):
        for step in range(n_steps):
            self.update()
        return self
    
    def plot_static(self, n_steps= 100, display_width = 200, cmap='RdGy', save=False):
        
        self.simulate(n_steps=n_steps)
        static_history = np.zeros((n_steps,display_width))
        xlim_0 = self.N1//2 - display_width//2
        xlim_1 = xlim_0 + display_width 
        full_history = np.array(self.history).reshape(n_steps+1, self.N1)
        static_history = full_history[:,xlim_0:xlim_1]

        fig, axis = plt.subplots(1,1,figsize=(8,8))
        axis.imshow(static_history, cmap=cmap)
        axis.set_title(self.name)
        plt.show()
        if save:
            save_path = 'test_path'
            pass

    def plot_animate(self, n_steps =100, display_width=200, cmap='Spectral_r', save=False):

        fig, axis = plt.subplots(1,1, figsize = (10,10))
        curr_array = np.zeros((n_steps,display_width))
        xlim_0 = self.N1//2 - display_width//2
        xlim_1 = xlim_0 + display_width 
        state_init = self.curr_state.copy()
        curr_array[0,:] = state_init[xlim_0:xlim_1]
        img1 = plt.imshow(curr_array, animated=True, cmap=cmap)
        
        def animate_func(*args):
            t = len(self.history) + 1
            self.update()
            if t >= n_steps:
                for row in range(n_steps):
                    curr_array[row,:] = self.history[t-n_steps+row][xlim_0:xlim_1]
            else :
                for row in range(t):
                    curr_array[row,:] = self.history[row][xlim_0:xlim_1]
            img1.set_array(curr_array)
            return img1,

        anim = FuncAnimation(fig, animate_func, blit=True)
        axis.set_title(self.name)
        axis.axis('off')
        plt.show()



if __name__ == "__main__":

    test = CA_Generator(rule='rule_137')
    # test.plot_animate()
    test.plot_static()
    