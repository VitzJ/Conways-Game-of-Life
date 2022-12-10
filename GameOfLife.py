import random


class GameOfLife:

    def __init__(self, data):
        self.cords = {}
        self.data = data

        for i in range(len(data)):
            for k in range(len(data[i])):
                # if the value is in the first row: we only evaluate row + one row down (2 rows range)
                if i == 0:
                    rows_for_eval = [i, i + 1]

                # if the value is in the last row: we only evaluate row + one row up (2 rows range)
                elif i == len(data) - 1:
                    rows_for_eval = [i - 1, i]

                # otherwise, evaluate row above + row + row below (3 row range)
                else:
                    rows_for_eval = [i - 1, i + 1]

                # if the value is in the first column: we only evaluate column + column to the right (2 columns range)
                if k == 0:
                    columns_for_eval = [k, k + 1]

                # if the value is in the last column: we only evaluate column + one column to the left (2 columns range)
                elif k == len(data[i]) - 1:
                    columns_for_eval = [k - 1, k]

                # otherwise, evaluate column left + column + column right (3 column range)
                else:
                    columns_for_eval = [k - 1, k + 1]

                # for each point in the matrix, define a range within the matrix that needs to be evaluated in
                # order to compile the number of cells that are alive around the respective point
                self.cords[i, k] = [rows_for_eval, columns_for_eval]

        # dictionary for num_matrix
        self.num_dict = {}

    # for each space in our base array, figure out the cell counts
    def num_matrix(self):
        cord_keys = list(self.cords.keys())

        for i in range(len(cord_keys)):
            x = cord_keys[i][0]
            y = cord_keys[i][1]

            row = self.cords[x, y][0]
            column = self.cords[x, y][1]

            cell_ct = 0
            # we are testing adjacent cell presence values and storing in a variable
            for j in range(row[0], row[1] + 1):
                for k in range(column[0], column[1] + 1):
                    if self.data[j][k] == "X":
                        cell_ct += 1

            if self.check(x, y):
                # if it is a cell, subtract own status as a live cell from cell_ct
                self.num_dict[f"({x}, {y})"] = cell_ct - 1
            else:
                # otherwise leave cell cell_ct alone
                self.num_dict[f"({x}, {y})"] = cell_ct

        return self.num_dict

    def check(self, x, y):
        # if live cell
        if self.data[x][y] == "X":
            return True
        else:
            return False

    def new_phase(self):
        new_phase_list = []

        for i in range(len(self.data)):
            temp_list = []

            for j in range(len(self.data[i])):
                temp_cell = self.num_dict[f"({i}, {j})"]
                cell_bool = self.check(i, j)

                # these are the rules for cell propagation
                if cell_bool:
                    if temp_cell < 2:
                        temp_list.append(" ")
                    elif 1 < temp_cell < 4:
                        temp_list.append("X")
                    else:
                        temp_list.append(" ")
                else:
                    if temp_cell == 3:
                        temp_list.append("X")
                    else:
                        temp_list.append(" ")

            new_phase_list.append(temp_list)

        self.data = new_phase_list
        return self.data

    def iteration(self, number):
        # I want to check if a pattern stagnates; i.e. previous cell generation = current cell generation
        stagnate_check = []

        # I also want to check if cell generations oscillate
        oscillate_check = []

        self.display_data()

        for i in range(0, number):
            # 0.3 second delay
            # time.sleep(0.3)

            # aesthetics
            if i == 0:
                print("-" * len(self.data[0]) * 3)
                print(f"Base Input")
                print("-" * len(self.data[0]) * 3)

            # add to a list of Cell table elements for testing stagnation
            stagnate_check.append(self.data)

            # if list length = 2, check if elements are the same so that we can terminate loop
            if len(stagnate_check) == 2:
                if stagnate_check[0] == stagnate_check[1]:
                    print("The Game of Life has Stagnated.")
                    break
                stagnate_check.clear()
                stagnate_check.append(self.data)

            oscillate_check.append(self.data)

            if len(oscillate_check) == 3:
                first_eq_third = oscillate_check[0] == oscillate_check[2]
                if first_eq_third:
                    print(f"Oscillation between Generation {i - 2} and Generation {i}")
                    print("-" * len(self.data[0]) * 3)
                    break

                oscillate_check = oscillate_check[1:]

            # the actual iteration part is just num_matrix() and new_phase()
            self.num_matrix()
            self.new_phase()
            self.display_data()

            # aesthetics
            print("-" * len(self.data[0]) * 3)
            print(f"\nGeneration = {i + 1}\n\n")
            print("-" * len(self.data[0]) * 3)

    # displays original input in printed string format
    def display_data(self):
        for j in range(len(self.data)):
            print('  '.join(self.data[j]))


def create_base(x, y):
    base = []

    for j in range(x):
        temp_list = []

        for i in range(y):
            r = random.randint(0, 2)
            if r == 1:
                temp_list.append("X")
            else:
                temp_list.append(" ")

        base.append(temp_list)

    return GameOfLife(base)


# the dimensions of the base can be any value so long as x > 2 and y > 2
# the number of iterations is your choice
create_base(100, 50).iteration(2000)
