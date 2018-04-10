import numpy as np
import deep_maxent as deep_maxent
from value_iteration import find_policy


def main(grid_size, discount, n_objects, n_colours, n_trajectories, epochs,
         learning_rate, structure):
    """
    Run deep maximum entropy inverse reinforcement learning on the objectworld
    MDP.
    Plots the reward function.
    grid_size: Grid size. int.
    discount: MDP discount factor. float.
    n_objects: Number of objects. int.
    n_colours: Number of colours. int.
    n_trajectories: Number of sampled trajectories. int.
    epochs: Gradient descent iterations. int.
    learning_rate: Gradient descent learning rate. float.
    structure: Neural network structure. Tuple of hidden layer dimensions, e.g.,
        () is no neural network (linear maximum entropy) and (3, 4) is two
        hidden layers with dimensions 3 and 4.
    """

    wind = 0.3
    trajectory_length = 8
    l1 = l2 = 0

    filename = 'trajectories.csv'
    raw_data = open(filename, 'rt')
    # Load Expert Examples from file
    trajectories = numpy.loadtxt(raw_data, delimiter=",")

    r = deep_maxent.irl((feature_matrix.shape[1],) + structure, feature_matrix,
        ow.n_actions, discount, ow.transition_probability, trajectories, epochs,
        learning_rate, l1=l1, l2=l2)

if __name__ == '__main__':
    main(10, 0.9, 15, 2, 20, 50, 0.01, (3, 3))
