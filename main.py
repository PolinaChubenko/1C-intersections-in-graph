import matplotlib.image as mpimg
import numpy as np
import math


class Graph:
    def __init__(self, edge_thickness=0):
        self.img = None
        self.edge_thickness = edge_thickness
        self.height = 0
        self.width = 0
        self.intersections = 0

    def set_image(self, path):
        row_img = mpimg.imread(path)
        self.height, self.width, dim = row_img.shape
        self.img = np.zeros(shape=(self.height, self.width), dtype=int)
        for i in range(self.height):
            for j in range(self.width):
                self.img[i][j] = int(row_img[i][j][0])
        if not self.edge_thickness:
            self.find_edge_thickness()

    def is_cell_black(self, i, j, is_swap=0):
        if is_swap:
            i, j = j, i
        return not self.img[i][j]

    def count_same_pixels(self, fixed, motion, a, b, step=1):
        cnt = 0
        swapping = 0 if motion == 'col' else 1
        for i in range(a, b, step):
            if self.is_cell_black(i, fixed, swapping):
                cnt += 1
            else:
                break
        return cnt

    def thickness_by_directions(self, x, y):
        count_blacks_col = 1
        count_blacks_col += self.count_same_pixels(fixed=y, motion='col', a=x+1, b=self.height)
        count_blacks_col += self.count_same_pixels(fixed=y, motion='col', a=x-1, b=-1, step=-1)

        count_blacks_row = 1
        count_blacks_row += self.count_same_pixels(fixed=x, motion='row', a=y+1, b=self.width)
        count_blacks_row += self.count_same_pixels(fixed=x, motion='row', a=y-1, b=-1, step=-1)

        return min(count_blacks_row, count_blacks_col)

    def find_edge_thickness(self):
        thicknesses = []
        for i in range(self.height):
            for j in range(self.width):
                if not self.img[i][j]:
                    thicknesses.append(self.thickness_by_directions(i, j))
        self.edge_thickness = math.floor(np.mean(thicknesses))

    @classmethod
    def is_window_black_enough(cls, window):
        sz = window.shape[0]
        blackness = ((sz**2) - np.cumsum(window)[-1]) / (sz**2)
        return 0.9 < blackness < 1

    def find_intersection_quantity(self):
        count = 0
        window_sz = self.edge_thickness * 2
        for i in range(0, self.height - window_sz, self.edge_thickness):
            for j in range(0, self.width - window_sz, self.edge_thickness):
                if self.is_window_black_enough(self.img[i:(i + window_sz), j:(j + window_sz)]):
                    count += 1
        return count


if __name__ == '__main__':
    graph = Graph()
    graph.set_image(input("Enter the path to the image: "))
    print("In this graph there are {} intersections".format(graph.find_intersection_quantity()))

