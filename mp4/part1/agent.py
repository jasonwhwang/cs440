import numpy as np
import utils
import random


class Agent:
    
    def __init__(self, actions, Ne, C, gamma):
        self.actions = actions
        self.Ne = Ne # used in exploration function
        self.C = C
        self.gamma = gamma

        # Create the Q and N Table to work with
        self.Q = utils.create_q_table()
        self.N = utils.create_q_table()

    def train(self):
        self._train = True
        
    def eval(self):
        self._train = False

    # At the end of training save the trained model
    def save_model(self,model_path):
        utils.save(model_path, self.Q)

    # Load the trained model for evaluation
    def load_model(self,model_path):
        self.Q = utils.load(model_path)

    def reset(self):
        self.points = 0
        self.s = None
        self.a = None

    def initialize_state_space(self, state):
        # Simplify State
        stateEnv = [state[0]//40, state[1]//40, state[2], state[3]//40, state[4]//40]
        
        ### INITIALIZE STATE SPACE ###
        stateSpace = np.zeros(8)
        # adjoining_wall_x
        stateSpace[0] = 1 if (stateEnv[0]==1) else 2 if (stateEnv[0]==13) else 0
        # adjoining_wall_y
        stateSpace[1] = 1 if (stateEnv[1]==1) else 2 if (stateEnv[1]==13) else 0
        # food_dir_x
        food_dir_x = stateEnv[0] - stateEnv[3]
        stateSpace[2] = 1 if (food_dir_x>0) else 2 if (food_dir_x<0) else 0
        # food_dir_y
        food_dir_y = stateEnv[1] - stateEnv[4]
        stateSpace[3] = 1 if (food_dir_y>0) else 2 if (food_dir_y<0) else 0
        # adjoining_body_top
        adjoining_body_top = (state[0], state[1]-40)
        stateSpace[4] = 1 if adjoining_body_top in state[2] else 0
        # adjoining_body_bottom
        adjoining_body_bottom = (state[0], state[1]+40)
        stateSpace[5] = 1 if adjoining_body_bottom in state[2] else 0
        # adjoining_body_left
        adjoining_body_left = (state[0]-40, state[1])
        stateSpace[6] = 1 if adjoining_body_left in state[2] else 0
        # adjoining_body_right
        adjoining_body_right = (state[0]+40, state[1])
        stateSpace[7] = 1 if adjoining_body_right in state[2] else 0

        return stateSpace

    def act(self, state, points, dead):
        '''
        :param state: a list of [snake_head_x, snake_head_y, snake_body, food_x, food_y] from environment.
        :param points: float, the current points from environment
        :param dead: boolean, if the snake is dead
        :return: the index of action. 0,1,2,3 indicates up,down,left,right separately

        TODO: write your function here.
        Return the index of action the snake needs to take, according to the state and points known from environment.
        Tips: you need to discretize the state to the state space defined on the webpage first.
        (Note that [adjoining_wall_x=0, adjoining_wall_y=0] is also the case when snake runs out of the 480x480 board)

        '''
        ### GAME VALUES ###
        # Board: 1 <= x and y <= 12; drawn from top-left to bottom-right
        # Border: x or y == 0 || 13
        # State Env: [snake_head_x, snake_head_y, snake_body, food_x, food_y]
        # Snake Body: stored as tuples
        # State Space: (adjoining_wall_x, adjoining_wall_y, food_dir_x, food_dir_y, adjoining_body_top,
        #               adjoining_body_bottom, adjoining_body_left, adjoining_body_right)
        
        # Simplify State
        stateEnv = [state[0]//40, state[1]//40, state[2], state[3]//40, state[4]//40]
        # Initialize State Space
        stateSpace = self.initialize_state_space(state)

        print(stateEnv)
        print(stateSpace)
        input("-->")

        # Mock Snake Movements
        if stateSpace[3] == 1:
            return self.actions[0]
        if stateSpace[3] == 2:
            return self.actions[1]
        if stateSpace[2] == 1:
            return self.actions[2]
        if stateSpace[2] == 2:
            return self.actions[3]

        return self.actions[0]
