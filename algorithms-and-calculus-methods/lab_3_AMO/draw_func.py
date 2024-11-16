import matplotlib.pyplot as plt


def draw_graph(data, graph_name, color):
    plt.title(graph_name)
    plt.xlabel('x')
    plt.ylabel('y')
    plt.plot(data[0], data[1], color=color, linewidth=1)
    plt.grid(True)


def overlay_graph(first_data, second_data):
    plt.title("Graph comparison")
    plt.xlabel('x')
    plt.ylabel('y')
    plt.plot(second_data[0], second_data[1], color='blue', linewidth=1)
    plt.plot(first_data[0], first_data[1], color='red', linewidth=1)
    plt.grid(True)


def main_draw(first_data, second_data, third_data):
    plt.figure(figsize=(9, 7))
    plt.subplot(221)
    draw_graph(first_data, "Default graph", "red")
    plt.subplot(222)
    draw_graph(second_data, "Interpolated graph", "blue")
    plt.subplot(223)
    overlay_graph(first_data, second_data)
    plt.subplot(224)
    draw_graph(third_data, "Mistakes", "orange")
    plt.subplots_adjust(top=0.95, bottom=0.1, left=0.10, right=0.95, hspace=0.3, wspace=0.3)
    plt.show()
