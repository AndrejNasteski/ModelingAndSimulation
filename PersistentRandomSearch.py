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

    def __init__(self, n, start_x, start_y):
        self.n = n
        self.x = np.zeros(n, dtype=int)
        self.y = np.zeros(n, dtype=int)
        self.x[0] = start_x
        self.y[0] = start_y
        self.currentX = start_x
        self.currentY = start_y

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
            # print("sighted at: ", self.nearest_x, self.nearest_y)
            if self.currentY > self.nearest_y:
                self.y[i_] = self.y[i_ - 1] - 1
                self.x[i_] = self.x[i_ - 1]
                self.currentY = self.y[i_]
                self.currentX = self.x[i_]
            elif self.currentY < self.nearest_y:
                self.y[i_] = self.y[i_ - 1] + 1
                self.x[i_] = self.x[i_ - 1]
                self.currentY = self.y[i_]
                self.currentX = self.x[i_]
            elif self.currentX > self.nearest_x:
                self.x[i_] = self.x[i_ - 1] - 1
                self.y[i_] = self.y[i_ - 1]
                self.currentX = self.x[i_]
                self.currentY = self.y[i_]
            elif self.currentX < self.nearest_x:
                self.x[i_] = self.x[i_ - 1] + 1
                self.y[i_] = self.y[i_ - 1]
                self.currentX = self.x[i_]
                self.currentY = self.y[i_]
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
        if i_ > 1:
            val = np.random.random(1)

            ...
        else:
            val = random.randint(1, 4)
            if val == 1:  # EAST
                x[i_] = x[i_ - 1] + 1
                y[i_] = y[i_ - 1]
            elif val == 2:  # WEST
                x[i_] = x[i_ - 1] - 1
                y[i_] = y[i_ - 1]
            elif val == 3:  # NORTH
                x[i_] = x[i_ - 1]
                y[i_] = y[i_ - 1] + 1
            elif val == 4:  # SOUTH
                x[i_] = x[i_ - 1]
                y[i_] = y[i_ - 1] - 1

        if x[i_] > VERTICAL_RIGHT:  # borderless
            x[i_] = VERTICAL_RIGHT - 1
        elif x[i_] < VERTICAL_LEFT:
            x[i_] = VERTICAL_LEFT + 1
        elif y[i_] > HORIZONTAL_TOP:
            y[i_] = HORIZONTAL_TOP - 1
        elif y[i_] < HORIZONTAL_BOTTOM:
            y[i_] = HORIZONTAL_BOTTOM + 1

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
        # self.food_x = random.randint(2, VERTICAL_RIGHT-2)
        # self.food_y = random.randint(2, HORIZONTAL_TOP-2)
        self.food_x = random.randint(2, 50)
        self.food_y = random.randint(2, 50)


if __name__ == '__main__':
    steps = 400
    num_agents = 3
    creature_list = list()

    for c in range(num_agents):
        t = SearchingAgent(steps + 1, 25, 25)  # random.randint(5, 95), random.randint(20, 80))
        creature_list.append(t)

    # drawing borders
    plt.title("Random Walk ($n = " + str(steps) + "$ steps)")
    plt.plot([0, 100], [100, 100], color="black")
    plt.plot([0, 100], [0, 0], color="black")
    plt.plot([0, 0], [0, 100], color="black")
    plt.plot([100, 100], [0, 100], color="black")

    foodList = list()

    # for i in range(100):
    #     f = Food()
    #     foodList.append(f)
    #     plt.plot(f.food_x, f.food_y, 'o', color="black")

    foodList = list()

    for t in range(steps):
        for c in creature_list:
            foodList = c.walk(foodList)

    for c in creature_list:
        plt.plot(c.x, c.y)

    plt.show()
