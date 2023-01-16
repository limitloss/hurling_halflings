# -*- coding: utf-8 -*-
"""
throw_tm_scatter.py

@author: 
    limitloss
"""

import numpy as np

import matplotlib.pyplot as plt


get_local_inds = lambda i,j: np.array([[i-1,j-1], [i-1,j], [i-1,j+1],
                              [i,j-1], [i,j+1], 
                              [i+1,j-1], [i+1,j], [i+1,j+1]])
# Note: does not return correct indices if i or j are on edge of array


def scatter(positions, current_grid):
    ''' Performs an individual scatter assuming one has happened before even if
    its just the ball landing in a single position.
    '''
    new_pos = np.empty((0,2),dtype=np.int32)
    # for each position we add +1 to all surrounding positions
    for position in positions:
        local_inds = get_local_inds(*position)

        # add mass and track the new positions
        current_grid[local_inds[:,0],local_inds[:,1]]+=1
        new_pos = np.concatenate((new_pos,local_inds),0)
        
    # normalizing Z should be same size as number of positions
    assert len(new_pos) == current_grid.sum()
    
    return new_pos, current_grid

def scatter_n(num_scatter=3, cur_pos=[[3,3]], grid_size=(7,7,)):
    ''' Calculates the spread of ball scatter on a grid after a specified number of scatters
    '''
    for i in range(num_scatter):
        new_grid = np.zeros(grid_size,dtype=np.int32)
        cur_pos, new_grid = scatter(positions=cur_pos, current_grid=new_grid)
    
    return cur_pos, new_grid

def print_tabdelim(array):
    ''' Quick and dirty function to print a numpy array with tab delimitation so 
    it can be copy-pasted into excel or sheets for ease
    '''
    print('Tab-Delim Array for Spreadsheets:\n')
    for row in array:
        print('\t'.join(row.astype(str)))
    print()
    return

def main():
    
    # FLAGS 
    save_svg = False                         # saves grid of scatter probs with matplotlib
    svg_savename = './imgs/grid_basic.svg'   # save location if saving
    print_tab_grid = False                   # dumps the non-normalized prob weight matrix to stdout 
                                             # for the
    
    
    # Starting Values for a half of blood bowl
    start_pos = [3,3] 
    grid_size = (7,7,)
    
    
    # Throwing with a tree is always 3 scatter rolls
    cur_pos, new_grid = scatter_n(num_scatter=3, cur_pos=[start_pos], grid_size=grid_size)
    
    # Fig size parity with grid size is coincidence
    fig, ax1 = plt.subplots(figsize=(7,7))
    plt.imshow(new_grid, cmap='plasma')
    
    if print_tab_grid:
        # prints the grid for use in a spreadsheet etc
        print_tabdelim(new_grid)
    
    # Normalize and Percent Convert
    new_grid = (new_grid/new_grid.sum())*100
    
    # Add text labels to each grid square
    for (j,i),label in np.ndenumerate(new_grid):
        prec = 1
        label = str(np.around(label,prec))+'%'
        ax1.text(i,j,label,ha='center',va='center',color='black')
    
    if save_svg:
        print(f'Saving SVG to {svg_savename}\n')
        plt.savefig(svg_savename,dpi=350)
    
    plt.show() 
    
    
    # Prob of landing in the donut around the aimed at square
    donut = get_local_inds(*start_pos)
    donut_prob = np.around(np.sum(new_grid[donut[:,0],donut[:,1]]),prec)    
    print(f'Prob. of Landing 1 Sq Off:\t\t{donut_prob}%')

    # Prob of landing and moving forward 
    start_i, start_j = start_pos
    fwd_prob = np.around(np.sum(new_grid[:start_i,:]),prec)
    print(f'Prob. of Landing Forward:\t\t{fwd_prob}%')
    print(f'Prob. of Landing Exactly:\t\t{np.around(new_grid[start_pos[0],start_pos[1]],prec)}%')

    


    return
    



    

if __name__=='__main__':
    main()