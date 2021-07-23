import random

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

#   PARAMETERS
BORDER_SIZE = 200
VERTICAL_LEFT = 0
VERTICAL_RIGHT = BORDER_SIZE
HORIZONTAL_BOTTOM = 0
HORIZONTAL_TOP = BORDER_SIZE
BT_RW = False  # Backtracking random walk algorithm
FC_BT_RW = True  # Forward Check + Backtracking random walk algorithm
STEP_SIZE_MEAN = 2
STEP_SIZE_STD = 1
UNIFORM_STEP_SIZE = 1
DISTRIBUTION_TYPE_LIST = ["Uniform", "Gaussian", "Exponential"]
DISTRIBUTION_TYPE = DISTRIBUTION_TYPE_LIST[2]
STEPS = 500
NUM_FOOD = 100
NUM_EPOCHS = 1000
difference = 0.1


class SearchingAgent:
    n = None  # number of steps
    x, y = None, None  # list of x and y steps
    currentX, currentY = None, None  # current coordinates
    index = 1  # keep track of the last element (coordinate) index in the list
    food_sighted = False
    nearest_x, nearest_y = None, None  # coordinates of nearest food
    previous_action = None  # if the previous action is EAST, its less likely to go WEST
    first_found = None  # first_found[0] -> steps until first found food

    # first_found[1] -> steps until found 10 food nodes

    # NESW, 0 - reduced probability, 1 - regular probability

    def __init__(self, n, start_x, start_y):
        self.n = n
        self.x = np.zeros(n, dtype=int)
        self.y = np.zeros(n, dtype=int)
        self.x[0] = start_x
        self.y[0] = start_y
        self.currentX = start_x
        self.currentY = start_y
        self.previous_action = [0.25, 0.25, 0.25, 0.25]  # NESW
        self.previous_action_fc = [0.25, 0.25, 0.25, 0.25]
        # NESW - 5 regular prob., 8 - increased prob., 2 - decreased prob.
        # front 0.45, left 0.25, right 0.2, back 0.1,
        # front 9, left 5, right 4, back 2,
        self.first_found = None

    def search_food(self, food_list):
        self.food_sighted = False  # reset for each step
        sight_range = 5  # in one direction
        nearest_food_list = []

        for f_ in food_list:
            for x_ in range(self.currentX - sight_range, self.currentX + sight_range):
                for y_ in range(self.currentY - sight_range, self.currentY + sight_range):
                    if f_.food_x == x_ and f_.food_y == y_:
                        nearest_food_list.append((f_.food_x, f_.food_y))
                        self.food_sighted = True

        if self.food_sighted:
            diff = np.array(nearest_food_list) - np.array([self.currentX, self.currentY])
            abs_value = np.absolute(diff)
            min_index = np.argmin(abs_value.sum(1))
            self.nearest_x = nearest_food_list[min_index][0]
            self.nearest_y = nearest_food_list[min_index][1]

    def walk(self, food_list_):
        i_ = self.index
        x_, y_ = self.x, self.y
        food_list_changed = food_list_

        if self.food_sighted:  # if food is sighted, move towards the food
            return self.slow_walk(food_list_)

        value = np.random.random(1)
        if i_ > 1 and BT_RW and not FC_BT_RW:  # backtracking algorithm only

            # direction_probabilities = [0.1, 0.1, 0.1, 0.1]
            # direction_probabilities = [direction_probabilities[i] + (self.previous_action[i] * 0.2) for i in
            #                            range(4)]
            # 0 < NORTH < 0.25 EAST < 0.5 < SOUTH < 0.75 < WEST < 1
            direction_cdf = []
            for k in range(3):
                prob_sum = 0
                for j in range(k + 1):
                    prob_sum += self.previous_action[j]
                direction_cdf.append(prob_sum)

            if value < direction_cdf[0]:  # NORTH
                x_, y_ = self.change_position(1)
            elif direction_cdf[0] < value < direction_cdf[1]:  # EAST
                x_, y_ = self.change_position(2)
            elif direction_cdf[1] < value < direction_cdf[2]:  # SOUTH
                x_, y_ = self.change_position(3)
            elif direction_cdf[2] < value:  # WEST
                x_, y_ = self.change_position(4)

        elif FC_BT_RW and i_ > 1:
            # direction_probabilities = [self.previous_action_fc[i] * 0.05 for i in range(4)]
            # 0 < NORTH < 0.25 EAST < 0.5 < SOUTH < 0.75 < WEST < 1
            direction_cdf = []
            for k in range(3):
                prob_sum = 0
                for j in range(k + 1):
                    prob_sum += self.previous_action_fc[j]
                direction_cdf.append(prob_sum)

            if value < direction_cdf[0]:  # NORTH
                x_, y_ = self.change_position(1)
            elif direction_cdf[0] < value < direction_cdf[1]:  # EAST
                x_, y_ = self.change_position(2)
            elif direction_cdf[1] < value < direction_cdf[2]:  # SOUTH
                x_, y_ = self.change_position(3)
            elif direction_cdf[2] < value:  # WEST
                x_, y_ = self.change_position(4)

        else:  # uniform direction distribution
            value = np.random.randint(1, 5)
            if value == 1:  # NORTH
                x_, y_ = self.change_position(1)
            elif value == 2:  # EAST
                x_, y_ = self.change_position(2)
            elif value == 3:  # SOUTH
                x_, y_ = self.change_position(3)
            elif value == 4:  # WEST
                x_, y_ = self.change_position(4)

        if x_[i_] > VERTICAL_RIGHT:
            x_[i_] = VERTICAL_RIGHT
        elif x_[i_] < VERTICAL_LEFT:
            x_[i_] = VERTICAL_LEFT
        elif y_[i_] > HORIZONTAL_TOP:
            y_[i_] = HORIZONTAL_TOP
        elif y_[i_] < HORIZONTAL_BOTTOM:
            y_[i_] = HORIZONTAL_BOTTOM

        self.currentX = x_[i_]
        self.currentY = y_[i_]
        self.x = x_
        self.y = y_
        self.index += 1
        self.search_food(food_list_)
        return food_list_changed

    def slow_walk(self, food_list_):
        i_ = self.index
        food_list_changed = food_list_
        if self.currentY > self.nearest_y:  # SOUTH
            self.y[i_] = self.y[i_ - 1] - 1
            self.x[i_] = self.x[i_ - 1]
            self.previous_action = [0.1, 0.3, 0.3, 0.3]  # NESW
            self.previous_action_fc = [0.1, 0.25 - difference, 0.4, 0.25 + difference]
            # self.previous_action_fc = [2, 4, 9, 5]
            # self.previous_action_fc = [2, 5, 8, 5]

        elif self.currentY < self.nearest_y:  # NORTH
            self.y[i_] = self.y[i_ - 1] + 1
            self.x[i_] = self.x[i_ - 1]
            self.previous_action = [0.3, 0.3, 0.1, 0.3]  # NESW
            self.previous_action_fc = [0.4, 0.25 + difference, 0.1, 0.25 - difference]
            # self.previous_action_fc = [9, 5, 2, 4]
            # self.previous_action_fc = [8, 5, 2, 5]

        elif self.currentX > self.nearest_x:  # WEST
            self.x[i_] = self.x[i_ - 1] - 1
            self.y[i_] = self.y[i_ - 1]
            self.previous_action = [0.3, 0.1, 0.3, 0.3]  # NESW
            self.previous_action_fc = [0.25 + difference, 0.1, 0.25 - difference, 0.4]
            # self.previous_action_fc = [5, 2, 4, 9]
            # self.previous_action_fc = [5, 2, 5, 8]

        elif self.currentX < self.nearest_x:  # EAST
            self.x[i_] = self.x[i_ - 1] + 1
            self.y[i_] = self.y[i_ - 1]
            self.previous_action = [0.3, 0.3, 0.3, 0.1]  # NESW
            self.previous_action_fc = [0.25 - difference, 0.4, 0.25 + difference, 0.1]
            # self.previous_action_fc = [4, 9, 5, 2]
            # self.previous_action_fc = [5, 8, 5, 2]

        else:  # food is on the same spot
            food_list_changed_ = []
            for item in food_list_changed:
                if item.food_x == self.currentX and item.food_y == self.currentY:
                    pass
                else:
                    food_list_changed_.append(item)

            self.y[i_] = self.y[i_ - 1] + 1
            self.x[i_] = self.x[i_ - 1]
            self.previous_action = [0.3, 0.3, 0.1, 0.3]
            self.previous_action_fc = [0.4, 0.25 + difference, 0.1, 0.25 - difference]
            # self.previous_action_fc = [9, 5, 2, 4]
            # self.previous_action_fc = [8, 5, 2, 5]

            food_list_changed = food_list_changed_
            if len(food_list_changed_) == NUM_FOOD - 1:
                self.first_found = i_

        self.currentX = self.x[i_]
        self.currentY = self.y[i_]
        self.index += 1
        self.search_food(food_list_changed)
        return food_list_changed

    def change_position(self, direction):
        x = self.x
        y = self.y
        i_ = self.index
        direction_ = direction
        if DISTRIBUTION_TYPE == "Gaussian":
            step_size_ = abs(round(np.random.normal(STEP_SIZE_MEAN, scale=STEP_SIZE_STD)))
        elif DISTRIBUTION_TYPE == "Exponential":
            step_size_ = abs(round(np.random.exponential(STEP_SIZE_MEAN)))
        else:
            step_size_ = UNIFORM_STEP_SIZE

        if direction_ == 1:  # NORTH
            x[i_] = x[i_ - 1]
            y[i_] = y[i_ - 1] + step_size_
            self.previous_action = [0.3, 0.3, 0.1, 0.3]  # NESW
            self.previous_action_fc = [0.4, 0.25 + difference, 0.1, 0.25 - difference]
            # self.previous_action_fc = [0.4, 0.25, 0.1, 0.25]
        elif direction_ == 2:  # EAST
            x[i_] = x[i_ - 1] + step_size_
            y[i_] = y[i_ - 1]
            self.previous_action = [0.3, 0.3, 0.3, 0.1]  # NESW
            self.previous_action_fc = [0.25 - difference, 0.4, 0.25 + difference, 0.1]
            # self.previous_action_fc = [0.25, 0.4, 0.25, 0.1]
        elif direction_ == 3:  # SOUTH
            x[i_] = x[i_ - 1]
            y[i_] = y[i_ - 1] - step_size_
            self.previous_action = [0.1, 0.3, 0.3, 0.3]  # NESW
            self.previous_action_fc = [0.1, 0.25 - difference, 0.4, 0.25 + difference]
            # self.previous_action_fc = [0.1, 0.25, 0.4, 0.25]
        elif direction_ == 4:  # WEST
            x[i_] = x[i_ - 1] - step_size_
            y[i_] = y[i_ - 1]
            self.previous_action = [0.3, 0.1, 0.3, 0.3]  # NESW
            self.previous_action_fc = [0.25 + difference, 0.1, 0.25 - difference, 0.4]
            # self.previous_action_fc = [0.25, 0.1, 0.25, 0.4]
        return x, y


class Food:
    food_x = None
    food_y = None

    def __init__(self):
        self.food_x = random.randint(VERTICAL_LEFT + 2, VERTICAL_RIGHT - 2)
        self.food_y = random.randint(HORIZONTAL_BOTTOM + 2, HORIZONTAL_TOP - 2)

    def __str__(self) -> str:
        return self.food_x.__str__() + self.food_y.__str__()

    def __repr__(self) -> str:
        return self.food_x.__str__() + "-" + self.food_y.__str__()


if __name__ == '__main__':

    # for c in range(NUM_AGENTS):
    #     t = SearchingAgent(STEPS + 1, c * 20 + 10, c * 20 + 10)  # random.randint(5, 95), random.randint(20, 80))
    #     agent_list.append(t)

    epoch_stats = list()

    for epoch in range(NUM_EPOCHS):
        foodList = list()

        for i in range(NUM_FOOD):
            f = Food()
            foodList.append(f)
            # plt.plot(f.food_x, f.food_y, 'o', color="black")

        agent = SearchingAgent(STEPS + 1, int(BORDER_SIZE / 2), int(BORDER_SIZE / 2))

        stats = dict()
        for t in range(STEPS):
            if t == 50:
                stats["Food collected in 50 steps:"] = NUM_FOOD - len(foodList)
            if t == 100:
                stats["Food collected in 100 steps:"] = NUM_FOOD - len(foodList)
            if t == 200:
                stats["Food collected in 200 steps:"] = NUM_FOOD - len(foodList)
            if t == STEPS - 1:
                stats["Food collected in 500 steps:"] = NUM_FOOD - len(foodList)
            foodList = agent.walk(foodList)

        stats["Steps until first found:"] = agent.first_found
        epoch_stats.append(stats)

    df = pd.DataFrame(epoch_stats)
    print("Step Distribution type:", DISTRIBUTION_TYPE)
    print("Step size mean:", STEP_SIZE_MEAN)
    print("Step size standard deviation:", STEP_SIZE_STD)
    print("Uniform step size:", UNIFORM_STEP_SIZE)
    print("Number of epochs:", NUM_EPOCHS)
    print("Probability difference:", difference)
    print("Ex.:", 0.25 - difference, 0.25 + difference)
    for col in df.columns:
        # print(col, df[col].mean())
        print(col, df[col].describe())

    # plotting random walk
    # plt.title("Random Walk ($n = " + str(STEPS) + "$ steps)")
    # plt.plot([0, BORDER_SIZE], [BORDER_SIZE, BORDER_SIZE], color="black")  # TOP
    # plt.plot([0, BORDER_SIZE], [0, 0], color="black")  # BOTTOM
    # plt.plot([0, 0], [0, BORDER_SIZE], color="black")  # LEFT
    # plt.plot([BORDER_SIZE, BORDER_SIZE], [0, BORDER_SIZE], color="black")  # RIGHT
    # plt.plot(agent.x, agent.y)
    # plt.show()
