import numpy as np
from numba import jit
from numba.cuda.random import create_xoroshiro128p_states
import time

NUM_FOOD = 100
NUM_EPOCHS = 10
NUM_STEPS = 500


# iterate through blockIdx 100 iterations

# have one global (or shared) matrix for results, 100 x 500, each row has 500 items,
# each item is number of food collected at i-th step (i = column index)

@jit(nopython=True, parallel=True)
def search_agent(num_food, num_steps, num_epochs):
    stat_mat = np.zeros((num_epochs, num_steps), dtype=np.int8)

    for epoch in range(num_epochs):
        food_list = []
        for i in range(num_food):
            food = (np.random.randint(1, 200), np.random.randint(1, 200))
            food_list.append(food)

        current_x, current_y = 100, 100
        food_sighted = False
        nearest_x = 0
        nearest_y = 0
        for index in range(1, num_steps + 1):
            if food_sighted:
                if current_y > nearest_y:  # SOUTH
                    current_y -= 1
                elif current_y < nearest_y:  # NORTH
                    current_y += 1
                elif current_x > nearest_x:  # WEST
                    current_x -= 1
                elif current_x < nearest_x:  # EAST
                    current_x += 1
                else:
                    food_list.remove((current_x, current_y))
                    current_y += 1

            else:
                value = np.random.randint(1, 5)
                # if distribution_type == "Gaussian":
                #     step_size_ = round(np.random.normal(STEP_SIZE_MEAN, scale=STEP_SIZE_STD))
                #     while step_size_ < 0:
                #         step_size_ = round(np.random.normal(STEP_SIZE_MEAN, scale=STEP_SIZE_STD))
                # elif distribution_type == "Exponential":
                #     step_size_ = round(np.random.exponential(STEP_SIZE_MEAN))
                #     while step_size_ < 0:
                #         step_size_ = round(np.random.exponential(STEP_SIZE_MEAN))
                # else:
                step_size_ = 2

                if value == 1:  # NORTH
                    current_y += step_size_
                elif value == 2:  # EAST
                    current_x += step_size_
                elif value == 3:  # SOUTH
                    current_y -= step_size_
                elif value == 4:  # WEST
                    current_x -= step_size_

                if current_x > 200:
                    current_x = 199
                elif current_x < 0:
                    current_x = 1
                elif current_y > 200:
                    current_y = 199
                elif current_y < 0:
                    current_y = 1

            food_sighted = False
            nearest_food_list = []

            for f_ in food_list:
                for x_ in range(current_x - 5, current_x + 5):
                    for y_ in range(current_y - 5, current_y + 5):
                        if f_[0] == x_ and f_[1] == y_:
                            nearest_food_list.append((f_[0], f_[1]))
                            food_sighted = True
            if food_sighted:
                diff = np.array(nearest_food_list) - np.array([current_x, current_y])
                abs_value = np.absolute(diff)
                min_index = np.argmin(abs_value.sum(1))
                nearest_x = nearest_food_list[min_index][0]
                nearest_y = nearest_food_list[min_index][1]

            stat_mat[epoch][index - 1] = len(food_list)

    stat_mat = stat_mat - np.array(num_food)
    stat_mat_abs = np.absolute(stat_mat)
    return stat_mat_abs


if __name__ == '__main__':
    start = time.time()
    mat = search_agent(NUM_FOOD, NUM_STEPS, NUM_EPOCHS)
    end = time.time()
    avg_mat = np.mean(mat, axis=0)
    print(avg_mat)
    print(end - start)

    start = time.time()
    mat = search_agent(NUM_FOOD, NUM_STEPS, NUM_EPOCHS)
    end = time.time()
    avg_mat = np.mean(mat, axis=0)
    print(avg_mat)
    print(end - start)
