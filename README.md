# Задача № 214

### Условие
На вход программе подаётся изображение некоторого графа.
Необходимо вывести количество пересечений его рёбер. При этом рёбра, встречающиеся в одной вершине, не дают пересечения.
Формат изображения - png. Рёбра изображены прямыми чёрными отрезками толщиной не менее 3 пикселей. Гарантируется, что никакие два ребра, выходящие из одной вершины, не лежат на одной прямой.

### Идея решения
Будем смотреть на изображение как на матрицу пикселей. Различать вершины и пересечения довольно трудно, поэтому будем передавать программе на вход не только изображение графа, но и число его вершин. Тогда задача свелась к тому, чтобы пройти сканирующим окном по всей матрице и найти места, где много черных пикселей, то есть черных пикселей больше 70% (логично, что в местах пересечения рёбер, черных пикселей больше). Для выбора размера сканирующего окна предварительно оценим толщину ребер, то есть найдем число пикселей. Тогда размер сканирующего окна можно взять как удвоенная толщина ребра. Окно двигается с нахлестом в половину его длины, поэтому, чтобы одно пересечение не учитывалось дважды, после нахождения пересечения, будем закрашивать все его пиксели белым цветом. Ответом будет разность числа найденных пересечений и количества вершин графа.

### Детали реализации
Код написан на языке Python3.8. Для работы с изображением использовалась библиотека matplotlib. Так как картинки графов состоят строго из двух цветов (черный и белый), то RGB/RGBA можно преобразовать в бинарный тип, то есть 0 - черный цвет, а 1 - белый. Для работы с матрицей пикселей будем использовать numpy. В результате работы программы мы получаем не только численный ответ, но и сохраняем в поле класса координаты точек пересечений (то есть номера пикселей, которые принадлежат пересечению).

### Что дальше?
Так как мы обладаем координатами точек из пересечения, то можно добавить нанесение на изображение меток мест (например, закрасить области каким-нибудь цветом), которые нашел алгоритм.

### Для сборки проекта:
- Склонируйте этот репозиторий
- Установите все зависимости: ```pip3 install -r requirements.txt```
- Запустите программу: ```python main.py```

Примеры графов можно взять из папки examples.

----

*Задание выполнила Чубенко Полина, Б05-022*
