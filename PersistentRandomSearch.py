import random

import matplotlib.pyplot as plt
import numpy as np

#   boundaries
VERTICAL_LEFT = 0
VERTICAL_RIGHT = 100
HORIZONTAL_BOTTOM = 0
HORIZONTAL_TOP = 100


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
        food_list_changed = food_list_

        if self.food_sighted:  # if food is sighted, move towards the food
            if self.currentY > self.nearest_y:  # SOUTH
                self.y[i_] = self.y[i_ - 1] - 1
                self.x[i_] = self.x[i_ - 1]
                self.currentY = self.y[i_]
                self.currentX = self.x[i_]
                self.previous_action = [1, 1, 0, 1]  # NESW
            elif self.currentY < self.nearest_y:  # NORTH
                self.y[i_] = self.y[i_ - 1] + 1
                self.x[i_] = self.x[i_ - 1]
                self.currentY = self.y[i_]
                self.currentX = self.x[i_]
                self.previous_action = [0, 1, 1, 1]  # NESW
            elif self.currentX > self.nearest_x:  # WEST
                self.x[i_] = self.x[i_ - 1] - 1
                self.y[i_] = self.y[i_ - 1]
                self.currentX = self.x[i_]
                self.currentY = self.y[i_]
                self.previous_action = [1, 1, 1, 0]  # NESW
            elif self.currentX < self.nearest_x:  # EAST
                self.x[i_] = self.x[i_ - 1] + 1
                self.y[i_] = self.y[i_ - 1]
                self.currentX = self.x[i_]
                self.currentY = self.y[i_]
                self.previous_action = [1, 1, 1, 0]  # NESW
            else:
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

        x = self.x
        y = self.y
        if i_ > 1:  # weighted direction distribution
            value = np.random.random(1)
            direction_probabilities = [0.1, 0.1, 0.1, 0.1]
            direction_probabilities = [direction_probabilities[i] + (self.previous_action[i] * 0.2) for i in range(4)]
            # 0 < NORTH < 0.25 EAST < 0.5 < SOUTH < 0.75 < WEST < 1

            direction_cdf = []
            for k in range(3):
                prob_sum = 0
                for j in range(k + 1):
                    prob_sum += direction_probabilities[j]
                direction_cdf.append(prob_sum)

            if value < direction_cdf[0]:  # NORTH
                x[i_] = x[i_ - 1]
                y[i_] = y[i_ - 1] + 1
                self.previous_action = [0, 1, 1, 1]  # NESW
            elif direction_cdf[0] < value < direction_cdf[1]:  # EAST
                x[i_] = x[i_ - 1] + 1
                y[i_] = y[i_ - 1]
                self.previous_action = [1, 0, 1, 1]  # NESW
            elif direction_cdf[1] < value < direction_cdf[2]:  # SOUTH
                x[i_] = x[i_ - 1]
                y[i_] = y[i_ - 1] - 1
                self.previous_action = [1, 1, 0, 1]  # NESW
            elif direction_cdf[2] < value:  # WEST
                x[i_] = x[i_ - 1] - 1
                y[i_] = y[i_ - 1]
                self.previous_action = [1, 1, 1, 0]  # NESW
        else:  # uniform direction distribution
            value = random.randint(1, 4)
            if value == 1:  # EAST
                x[i_] = x[i_ - 1] + 1
                y[i_] = y[i_ - 1]
                self.previous_action = [1, 0, 1, 1]  # NESW
            elif value == 2:  # WEST
                x[i_] = x[i_ - 1] - 1
                y[i_] = y[i_ - 1]
                self.previous_action = [1, 1, 1, 0]  # NESW
            elif value == 3:  # NORTH
                x[i_] = x[i_ - 1]
                y[i_] = y[i_ - 1] + 1
                self.previous_action = [0, 1, 1, 1]  # NESW
            elif value == 4:  # SOUTH
                x[i_] = x[i_ - 1]
                y[i_] = y[i_ - 1] - 1
                self.previous_action = [1, 1, 0, 1]  # NESW

        if x[i_] > VERTICAL_RIGHT:  # borderless
            x[i_] = VERTICAL_RIGHT
        elif x[i_] < VERTICAL_LEFT:
            x[i_] = VERTICAL_LEFT
        elif y[i_] > HORIZONTAL_TOP:
            y[i_] = HORIZONTAL_TOP
        elif y[i_] < HORIZONTAL_BOTTOM:
            y[i_] = HORIZONTAL_BOTTOM

        self.currentX = x[i_]
        self.currentY = y[i_]
        self.x = x
        self.y = y
        self.index += 1
        self.search_food(food_list_)
        return food_list_changed


class Food:
    food_x = None
    food_y = None

    def __init__(self):
        self.food_x = random.randint(VERTICAL_LEFT + 2, VERTICAL_RIGHT - 2)
        self.food_y = random.randint(HORIZONTAL_BOTTOM + 2, HORIZONTAL_TOP - 2)


if __name__ == '__main__':
    steps = 400
    num_agents = 4
    creature_list = list()

    for c in range(num_agents):
        t = SearchingAgent(steps + 1, c * 25, c * 25)  # random.randint(5, 95), random.randint(20, 80))
        creature_list.append(t)

    # drawing borders
    plt.title("Random Walk ($n = " + str(steps) + "$ steps)")
    plt.plot([0, 100], [100, 100], color="black")
    plt.plot([0, 100], [0, 0], color="black")
    plt.plot([0, 0], [0, 100], color="black")
    plt.plot([100, 100], [0, 100], color="black")

    foodList = list()

    for i in range(100):
        f = Food()
        foodList.append(f)
        plt.plot(f.food_x, f.food_y, 'o', color="black")

    for t in range(steps):
        for c in creature_list:
            foodList = c.walk(foodList)

    for c in creature_list:
        plt.plot(c.x, c.y)

    plt.show()
