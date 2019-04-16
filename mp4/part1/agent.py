import numpy as np
import utils
import random


class Agent:
    
    def __init__(self, actions, Ne, C, gamma):
        self.actions = actions
        self.Ne = Ne # used in exploration function
        self.C = C
        self.gamma = gamma

        # Defaults
        self.Rplus = 1
        self.points = 0
        self.s = None
        self.a = None

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

    def get_state_space(self, stateEnv):
        # Initialize Array
        stateSpace = np.zeros(8, dtype=int)
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
        adjoining_body_top = (stateEnv[0]*40, stateEnv[1]*40-40)
        stateSpace[4] = 1 if adjoining_body_top in stateEnv[2] else 0
        # adjoining_body_bottom
        adjoining_body_bottom = (stateEnv[0]*40, stateEnv[1]*40+40)
        stateSpace[5] = 1 if adjoining_body_bottom in stateEnv[2] else 0
        # adjoining_body_left
        adjoining_body_left = (stateEnv[0]*40-40, stateEnv[1]*40)
        stateSpace[6] = 1 if adjoining_body_left in stateEnv[2] else 0
        # adjoining_body_right
        adjoining_body_right = (stateEnv[0]*40+40, stateEnv[1]*40)
        stateSpace[7] = 1 if adjoining_body_right in stateEnv[2] else 0

        return stateSpace

    def get_q_and_n(self, stateSpace, action):
        q0, q1, q2, q3, q4, q5, q6, q7 = stateSpace[0], stateSpace[1], stateSpace[2], stateSpace[
            3], stateSpace[4], stateSpace[5], stateSpace[6], stateSpace[7]
        return self.Q[q0, q1, q2, q3, q4, q5, q6, q7, action], self.N[q0, q1, q2, q3, q4, q5, q6, q7, action]

    def get_action(self, stateSpace):
        action, score = 0, 0.0
        # For all actions (up=0, down=1, left=2, right=3)
        for i in range(len(self.actions)):
            scoreTemp = 0.0
            # Get Quality and n of each action
            u, n = self.get_q_and_n(stateSpace, i)
            # Calculate exploration function
            if n < self.Ne:
                scoreTemp = self.Rplus
            else:
                scoreTemp = u
            # Choose attribute based on max
            # Tie break using priority:
            # right > left > down > up
            if scoreTemp >= score:
                action = i
                score = scoreTemp
                
        return action

    def get_reward(self, stateSpace):
        return 1

    def update_N_table(self, stateSpace, action):
        return

    def update_Q_table(self):
        return

    def act(self, state, points, dead):
        # Get ENV State
        stateEnv = [state[0]//40, state[1]//40, state[2], state[3]//40, state[4]//40]
        # Get State Space
        stateSpace = self.get_state_space(stateEnv)
        print(stateEnv)
        print(stateSpace)

        # Q-Learning Algorithm
        # 1. Choose Action
        action = self.get_action(stateSpace)
        # 2. Update N-Table
        self.update_N_table(stateSpace, action)
        # 3. Update Q-Table
        self.update_Q_table()

        input("-->")

        return self.actions[action]


        '''
        act
        
        :param state: a list of [snake_head_x, snake_head_y, snake_body, food_x, food_y] from environment.
        :param points: float, the current points from environment
        :param dead: boolean, if the snake is dead
        :return: the index of action. 0,1,2,3 indicates up,down,left,right separately

        Description:
        Return the index of action the snake needs to take, according to the state and points known from environment.
        Tips: you need to discretize the state to the state space defined on the webpage first.
        (Note that [adjoining_wall_x=0, adjoining_wall_y=0] is also the case when snake runs out of the 480x480 board)

        ### GAME VALUES ###
        Board: 1 <= x and y <= 12; drawn from top-left to bottom-right
        Border: x or y == 0 || 13
        State Env: [snake_head_x, snake_head_y, snake_body, food_x, food_y]
        Snake Body: stored as tuples
        State Space: (adjoining_wall_x, adjoining_wall_y, food_dir_x, food_dir_y, adjoining_body_top,
                      adjoining_body_bottom, adjoining_body_left, adjoining_body_right)
        Actions: (up, down, left, right)
        Rewards: +1 Get Food, -1 Die, -0.1 Otherwise
        Q/N-Table:  (NUM_ADJOINING_WALL_X_STATES, NUM_ADJOINING_WALL_Y_STATES, NUM_FOOD_DIR_X, NUM_FOOD_DIR_Y,
					 NUM_ADJOINING_BODY_TOP_STATES, NUM_ADJOINING_BODY_BOTTOM_STATES, NUM_ADJOINING_BODY_LEFT_STATES,
					 NUM_ADJOINING_BODY_RIGHT_STATES, NUM_ACTIONS)

        Q-Learning Main Steps:
        1. Choose Action: Exploration Policy
        2. Measure Reward: Reward Policy
        3. Update Q-Table: Q(s,a) ← Q(s,a) + α(R(s) + γmaxa′Q(s′,a′)−Q(s,a) )

        Links for Understanding:
        https://medium.freecodecamp.org/an-introduction-to-q-learning-reinforcement-learning-14ac0b4493cc
        https://www.geeksforgeeks.org/q-learning-in-python/
        https://courses.engr.illinois.edu/cs440/sp2019/slides/hj22.pdf
        https://courses.engr.illinois.edu/cs440/sp2019/mp4/index.html

        '''

        # get_action mock snake movement:
        # # Mock Snake Movements
        # if stateSpace[3] == 1:
        #     return 0
        # if stateSpace[3] == 2:
        #     return 1
        # if stateSpace[2] == 1:
        #     return 2
        # if stateSpace[2] == 2:
        #     return 3