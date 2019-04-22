import numpy as np
import utils
import random


class Agent:
    
    def __init__(self, actions, Ne, C, gamma):
        self.actions = actions
        self.Ne = float(Ne) # used in exploration function
        self.C = float(C)
        self.gamma = float(gamma)

        # Defaults
        self.Rplus = 1.0
        self.points = 0.0
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
        self.points = 0.0
        self.s = None
        self.a = None

    def get_state_space(self, stateEnv):
        # State Env: [snake_head_x, snake_head_y, snake_body, food_x, food_y]
        # Initialize Array
        stateSpace = [0,0,0,0,0,0,0,0]
        # adjoining_wall_x
        if stateEnv[0] == 40:
            stateSpace[0] = 1
        elif stateEnv[0] == 480:
            stateSpace[0] = 2
        else:
            stateSpace[0] = 0
        # adjoining_wall_y
        if stateEnv[1] == 40:
            stateSpace[1] = 1
        elif stateEnv[1] == 480:
            stateSpace[1] = 2
        else:
            stateSpace[1] = 0
        # food_dir_x
        food_dir_x = stateEnv[0] - stateEnv[3]
        if food_dir_x > 0:
            stateSpace[2] = 1
        elif food_dir_x < 0:
            stateSpace[2] = 2
        else:
            stateSpace[2] = 0
        # food_dir_y
        food_dir_y = stateEnv[1] - stateEnv[4]
        if food_dir_y > 0:
            stateSpace[3] = 1
        elif food_dir_y < 0:
            stateSpace[3] = 2
        else:
            stateSpace[3] = 0
        # adjoining_body_top
        adjoining_body_top = (stateEnv[0], stateEnv[1]-40)
        if adjoining_body_top in stateEnv[2]:
            stateSpace[4] = 1
        else:
            stateSpace[4] = 0
        # adjoining_body_bottom
        adjoining_body_bottom = (stateEnv[0], stateEnv[1]+40)
        if adjoining_body_bottom in stateEnv[2]:
            stateSpace[5] = 1
        else:
            stateSpace[5] = 0
        # adjoining_body_left
        adjoining_body_left = (stateEnv[0]-40, stateEnv[1])
        if adjoining_body_left in stateEnv[2]:
            stateSpace[6] = 1
        else:
            stateSpace[6] = 0
        # adjoining_body_right
        adjoining_body_right = (stateEnv[0]+40, stateEnv[1])
        if adjoining_body_right in stateEnv[2]:
            stateSpace[7] = 1
        else:
            stateSpace[7] = 0

        return stateSpace

    def get_q_and_n(self, stateSpace, action):
        q0, q1, q2, q3, q4, q5, q6, q7 = stateSpace[0], stateSpace[1], stateSpace[2], stateSpace[
            3], stateSpace[4], stateSpace[5], stateSpace[6], stateSpace[7]
        return self.Q[q0, q1, q2, q3, q4, q5, q6, q7, action], self.N[q0, q1, q2, q3, q4, q5, q6, q7, action]

    def get_reward(self, points, dead):
        if dead:
            return -1.0
        if points > self.points:
            return 1.0
        return -0.1

    def get_max_Q(self, stateSpace):
        maxQ = 0.0
        for i in range(len(self.actions)):
            q, n = self.get_q_and_n(stateSpace, i)
            if q > maxQ:
                maxQ = q
        return maxQ

    def update_Q_table(self, points, dead, stateSpace):
        if self.s is None and self.a is None or self._train is False:
            return
        
        pastQ, pastN = self.get_q_and_n(self.s, self.a)
        learn_rate = self.C/(self.C + pastN)
        reward = self.get_reward(points, dead)
        maxQ = self.get_max_Q(stateSpace)

        q0, q1, q2, q3, q4, q5, q6, q7 = self.s[0], self.s[1], self.s[2], self.s[
            3], self.s[4], self.s[5], self.s[6], self.s[7]

        self.Q[q0, q1, q2, q3, q4, q5, q6, q7, self.a] = pastQ + learn_rate * (reward + self.gamma*maxQ - pastQ)

        return
    
    def get_action_train(self, stateSpace):
        action, score = 0, -999.999
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

    def get_action_test(self, stateSpace):
        q0, q1, q2, q3, q4, q5, q6, q7 = stateSpace[0], stateSpace[1], stateSpace[2], stateSpace[
            3], stateSpace[4], stateSpace[5], stateSpace[6], stateSpace[7]
        actionList = self.Q[q0, q1, q2, q3, q4, q5, q6, q7]
        maxScore = -999.999
        action = 0
        for i in range(len(self.actions)):
            if actionList[i] >= maxScore:
                action = i
                maxScore = actionList[i]
        return action
    
    def get_action(self, stateSpace):
        if self._train is True:
            return self.get_action_train(stateSpace)
        return self.get_action_test(stateSpace)

    def update_N_table(self, stateSpace, action):
        if self._train is False:
            return

        q0, q1, q2, q3, q4, q5, q6, q7 = stateSpace[0], stateSpace[1], stateSpace[2], stateSpace[
            3], stateSpace[4], stateSpace[5], stateSpace[6], stateSpace[7]
        self.N[q0, q1, q2, q3, q4, q5, q6, q7, action] += 1
        return

    def save_p_s_a(self, points, stateSpace, action):
        if self._train is False:
            return

        self.points = points
        self.s = stateSpace.copy()
        self.a = action
        return

    def act(self, state, points, dead):
        # Get State Space
        stateSpace = self.get_state_space(state)

        # Q-Learning Algorithm
        # 1. Update Q-Table
        self.update_Q_table(points, dead, stateSpace)

        # Check if Dead
        if dead:
            self.reset()
            return None

        # 2. Choose Action
        action = self.get_action(stateSpace)
        # 3. Update N-Table
        self.update_N_table(stateSpace, action)
        
        # Save Past State & Action
        self.save_p_s_a(points, stateSpace, action)

        # print(stateEnv)
        # print(stateSpace)
        # input("-->")

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