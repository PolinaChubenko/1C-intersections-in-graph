from src.parser import Graph

if __name__ == '__main__':
    graph = Graph()
    graph.set_image(input("Enter the path to the image: "))
    graph.vertices = input('Enter the number of vertices in the graph: ')
    print("In this graph there are {} intersections".format(graph.find_intersection_quantity()))
