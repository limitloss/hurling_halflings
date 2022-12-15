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
    
    for i in range(num_scatter):
        new_grid = np.zeros(grid_size,dtype=np.int32)
        cur_pos, new_grid = scatter(positions=cur_pos, current_grid=new_grid)
    
    return cur_pos, new_grid


def main():
    cur_pos, new_grid = scatter_n(num_scatter=3)
    
    fig, ax1 = plt.subplots(figsize=(7,7))
    plt.imshow(new_grid, cmap='plasma')
    
    # Nomralize and Percent Convert
    new_grid = (new_grid/new_grid.sum())*100
    
    # Add text labels to each grid square
    for (j,i),label in np.ndenumerate(new_grid):
        prec = 1
        label = np.around(label,prec)
        ax1.text(i,j,label,ha='center',va='center',color='black')
    plt.show() 
    
    pass




    

if __name__=='__main__':
    main()