import random

import matplotlib.pyplot as plt
import numpy as np

#   PARAMETERS
BORDER_SIZE = 200
VERTICAL_LEFT = 0
VERTICAL_RIGHT = BORDER_SIZE
HORIZONTAL_BOTTOM = 0
HORIZONTAL_TOP = BORDER_SIZE
BT_RW = True
FC_BT_RW = False
STEP_SIZE_MEAN = 2
STEP_SIZE_STD = 1
DISTRIBUTION_TYPE = "Gaussian"  # Gaussian, Exponential, Uniform(1)


class SearchingAgent:
    n = None  # number of steps
    x, y = None, None  # list of x and y steps
    currentX, currentY = None, None  # current coordinates
    index = 1  # keep track of the last element (coordinate) index in the list
    food_sighted = False
    nearest_x, nearest_y = None, None  # coordinates of nearest food
    previous_action = None  # if the previous action is EAST, its less likely to go WEST

    # NESW, 0 - reduced probability, 1 - regular probability

    def __init__(self, n, start_x, start_y):
        self.n = n
        self.x = np.zeros(n, dtype=int)
        self.y = np.zeros(n, dtype=int)
        self.x[0] = start_x
        self.y[0] = start_y
        self.currentX = start_x
        self.currentY = start_y
        self.previous_action = [1, 1, 1, 1]  # NESW
        self.previous_action_fc = [5, 5, 5, 5]  # NESW - 5 regular prob., 8 - increased prob., 2 - decreased prob.

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

        min_distance = np.infty
        nearest_food_temp = (None, None)
        for (x_, y_) in nearest_food_list:
            distance = abs(self.currentX - x_) + abs(self.currentY - y_)
            if distance < min_distance:
                min_distance = distance
                nearest_food_temp = (x_, y_)

        self.nearest_x = nearest_food_temp[0]
        self.nearest_y = nearest_food_temp[1]

    def walk(self, food_list_):
        i_ = self.index
        x_, y_ = self.x, self.y
        food_list_changed = food_list_

        if self.food_sighted:  # if food is sighted, move towards the food
            return self.slow_walk(food_list_)

        if i_ > 1 and (BT_RW or FC_BT_RW):  # weighted direction distribution
            if BT_RW and not FC_BT_RW:  # backtracking algorithm only
                value = np.random.random(1)
                direction_probabilities = [0.1, 0.1, 0.1, 0.1]
                direction_probabilities = [direction_probabilities[i] + (self.previous_action[i] * 0.2) for i in
                                           range(4)]
                # 0 < NORTH < 0.25 EAST < 0.5 < SOUTH < 0.75 < WEST < 1
                direction_cdf = []
                for k in range(3):
                    prob_sum = 0
                    for j in range(k + 1):
                        prob_sum += direction_probabilities[j]
                    direction_cdf.append(prob_sum)

                if value < direction_cdf[0]:  # NORTH
                    x_, y_ = self.change_position(1)
                elif direction_cdf[0] < value < direction_cdf[1]:  # EAST
                    x_, y_ = self.change_position(2)
                elif direction_cdf[1] < value < direction_cdf[2]:  # SOUTH
                    x_, y_ = self.change_position(3)
                elif direction_cdf[2] < value:  # WEST
                    x_, y_ = self.change_position(4)

            elif FC_BT_RW:
                value = np.random.random(1)
                direction_probabilities = [self.previous_action_fc[i] * 0.05 for i in range(4)]
                # 0 < NORTH < 0.25 EAST < 0.5 < SOUTH < 0.75 < WEST < 1
                direction_cdf = []
                for k in range(3):
                    prob_sum = 0
                    for j in range(k + 1):
                        prob_sum += direction_probabilities[j]
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
            value = random.randint(1, 4)
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
            self.change_position(1)

            self.y[i_] = self.y[i_ - 1] - 1
            self.x[i_] = self.x[i_ - 1]
            self.currentY = self.y[i_]
            self.currentX = self.x[i_]
            self.previous_action = [0, 1, 1, 1]  # NESW
            self.previous_action_fc = [2, 5, 8, 5]

        elif self.currentY < self.nearest_y:  # NORTH
            self.y[i_] = self.y[i_ - 1] + 1
            self.x[i_] = self.x[i_ - 1]
            self.currentY = self.y[i_]
            self.currentX = self.x[i_]
            self.previous_action = [1, 1, 0, 1]  # NESW
            self.previous_action_fc = [8, 5, 2, 5]

        elif self.currentX > self.nearest_x:  # WEST
            self.x[i_] = self.x[i_ - 1] - 1
            self.y[i_] = self.y[i_ - 1]
            self.currentX = self.x[i_]
            self.currentY = self.y[i_]
            self.previous_action = [1, 0, 1, 1]  # NESW
            self.previous_action_fc = [5, 2, 5, 8]

        elif self.currentX < self.nearest_x:  # EAST
            self.x[i_] = self.x[i_ - 1] + 1
            self.y[i_] = self.y[i_ - 1]
            self.currentX = self.x[i_]
            self.currentY = self.y[i_]
            self.previous_action = [1, 1, 1, 0]  # NESW
            self.previous_action_fc = [5, 8, 5, 2]

        else:  # food is on the same spot
            food_list_changed = \
                [item for item in food_list_changed
                 if item.food_x != self.currentY and item.food_y != self.currentY]
            self.x[i_] = self.x[i_ - 1]
            self.y[i_] = self.y[i_ - 1]
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
            step_size_ = round(np.random.normal(STEP_SIZE_MEAN, scale=STEP_SIZE_STD))
        elif DISTRIBUTION_TYPE == "Exponential":
            step_size_ = round(np.random.exponential(STEP_SIZE_MEAN))
        else:
            step_size_ = 1

        if direction_ == 1:  # NORTH
            x[i_] = x[i_ - 1]
            y[i_] = y[i_ - 1] + step_size_
            self.previous_action = [1, 1, 0, 1]  # NESW
            self.previous_action_fc = [8, 5, 2, 5]
        elif direction_ == 2:  # EAST
            x[i_] = x[i_ - 1] + step_size_
            y[i_] = y[i_ - 1]
            self.previous_action = [1, 1, 1, 0]  # NESW
            self.previous_action_fc = [5, 8, 5, 2]
        elif direction_ == 3:  # SOUTH
            x[i_] = x[i_ - 1]
            y[i_] = y[i_ - 1] - step_size_
            self.previous_action = [0, 1, 1, 1]  # NESW
            self.previous_action_fc = [2, 5, 8, 5]
        elif direction_ == 4:  # WEST
            x[i_] = x[i_ - 1] - step_size_
            y[i_] = y[i_ - 1]
            self.previous_action = [1, 0, 1, 1]  # NESW
            self.previous_action_fc = [5, 2, 5, 8]
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
        return self.food_x.__str__() + " " + self.food_y.__str__()


if __name__ == '__main__':
    steps = 400
    num_agents = 7
    creature_list = list()

    for c in range(num_agents):
        t = SearchingAgent(steps + 1, c * 20 + 10, c * 20 + 10)  # random.randint(5, 95), random.randint(20, 80))
        creature_list.append(t)

    # drawing borders
    plt.title("Random Walk ($n = " + str(steps) + "$ steps)")
    plt.plot([0, BORDER_SIZE], [BORDER_SIZE, BORDER_SIZE], color="black")  # TOP
    plt.plot([0, BORDER_SIZE], [0, 0], color="black")  # BOTTOM
    plt.plot([0, 0], [0, BORDER_SIZE], color="black")  # LEFT
    plt.plot([BORDER_SIZE, BORDER_SIZE], [0, BORDER_SIZE], color="black")  # RIGHT

    foodList = list()

    for i in range(1):
        f = Food()
        foodList.append(f)
        plt.plot(f.food_x, f.food_y, 'o', color="black")

    for t in range(steps):
        for c in creature_list:
            foodList = c.walk(foodList)

    for c in creature_list:
        plt.plot(c.x, c.y)

    plt.show()
