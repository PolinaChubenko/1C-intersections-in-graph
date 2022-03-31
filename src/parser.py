import matplotlib.image as mpimg
import numpy as np
import math


class Graph:
    def __init__(self):
        self._img = None
        self._height = 0
        self._width = 0
        self._vertices = 0
        self._edge_thickness = 0
        self._intersections = list()

    @property
    def vertices(self):
        '''
        Получение числа вершин в графе
        '''
        return self._vertices

    @vertices.setter
    def vertices(self, vertices):
        """
        Задание числа вершин в графе
        """
        self._vertices = int(vertices)

    @property
    def edge_thickness(self):
        """
        Получение толщины ребра в графе
        """
        return self._edge_thickness

    @edge_thickness.setter
    def edge_thickness(self, edge_thickness):
        """
        Задание толщины ребра в графе
        """
        self._edge_thickness = int(edge_thickness)

    def set_image(self, path):
        """
        Загрузка и обработка изображение
        """
        row_img = mpimg.imread(path)
        self._height, self._width, dim = row_img.shape
        self._img = np.zeros(shape=(self._height, self._width), dtype=int)
        for i in range(self._height):
            for j in range(self._width):
                self._img[i][j] = int(row_img[i][j][0])
        if not self._edge_thickness:
            self.find_edge_thickness()

    def __is_cell_black(self, i, j, is_swap=0):
        """
        Проверка является ли пиксель черным (т.е. равен 0)
        """
        if is_swap:
            i, j = j, i
        return not self._img[i][j]

    def __count_same_pixels(self, fixed, motion, a, b, step=1):
        """
        Вспомогательная функций подсчета числа черных пикселей
        по направлению от фиксированного пикселя
        """
        cnt = 0
        swapping = 0 if motion == 'col' else 1
        for i in range(a, b, step):
            if self.__is_cell_black(i, fixed, swapping):
                cnt += 1
            else:
                break
        return cnt

    def __thickness_by_directions(self, x, y):
        """
        Подсчет числа соседних черных пикселей по колонке и по
        строке относительно заданного пикселя
        """
        count_blacks_col = 1
        count_blacks_col += self.__count_same_pixels(fixed=y, motion='col', a=x+1, b=self._height)
        count_blacks_col += self.__count_same_pixels(fixed=y, motion='col', a=x-1, b=-1, step=-1)

        count_blacks_row = 1
        count_blacks_row += self.__count_same_pixels(fixed=x, motion='row', a=y+1, b=self._width)
        count_blacks_row += self.__count_same_pixels(fixed=x, motion='row', a=y-1, b=-1, step=-1)

        return min(count_blacks_row, count_blacks_col)

    def find_edge_thickness(self):
        """
        Оценка толщины ребра в графе
        """
        if self._img is None:
            raise ValueError("There is no image to analyse")
        thicknesses = []
        for i in range(self._height):
            for j in range(self._width):
                if not self._img[i][j]:
                    thicknesses.append(self.__thickness_by_directions(i, j))
        self._edge_thickness = math.floor(np.median(thicknesses))

    @classmethod
    def __is_window_black_enough(cls, window):
        """
        Оценка закрашенности окна черным цветом
        """
        sz = window.shape[0]
        blackness = ((sz**2) - np.cumsum(window)[-1]) / (sz**2)
        return blackness > 0.7

    def __make_it_white(self, i, j, window_sz):
        """
        Замена пикселей из подматрицы на белые
        """
        self._img[i:(i + window_sz), j:(j + window_sz)] = np.ones(shape=(window_sz, window_sz))

    def find_intersection_quantity(self):
        """
        Подсчет числа пересечений ребер в графе
        """
        if self._img is None:
            raise ValueError("There is no image to analyse")
        window_sz = self._edge_thickness * 2
        for i in range(0, self._height - window_sz, self._edge_thickness):
            for j in range(0, self._width - window_sz, self._edge_thickness):
                if self.__is_window_black_enough(self._img[i:(i + window_sz), j:(j + window_sz)]):
                    self._intersections.append((i, j))
                    self.__make_it_white(i, j, int(2 * window_sz))
        return len(self._intersections) - self._vertices

    @property
    def intersections(self):
        """
        Получение координат пересечений ребер в графе
        """
        return self._intersections
