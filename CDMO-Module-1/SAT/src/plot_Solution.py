import os
import re
import matplotlib.pyplot as plt

def importInstances(folder):
    def sorted_alphanumeric(data):
        convert = lambda text: int(text) if text.isdigit() else text.lower()
        alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ]
        return sorted(data, key=alphanum_key)
    instances = []
    files = sorted_alphanumeric(os.listdir(folder))
    print(files)
    for file in files:
        with open(folder + file) as f:
            content = f.readlines()
            content = [x.strip() for x in content]
            instances.append(content)
    return instances

def plotSolution(width, height, circuits, file=None):
    SIZE = 5
    fig, ax = plt.subplots()
    fig.set_size_inches(SIZE, SIZE * height / width)
    colors = ['tab:red','tab:orange', 'yellow', 'tab:green','tab:blue','tab:purple','tab:brown', 'tab:grey']
    for i in range(len(circuits)):
        ax.broken_barh([(circuits[i][2], circuits[i][0])], (circuits[i][3], circuits[i][1]),
                        facecolors=colors[i % len(colors)],
                        edgecolors=("black"),
                        linewidths=(2,),)
    ax.set_ylim(0, height)
    ax.set_xlim(0, width)
    ax.set_xticks(range(width + 1))
    ax.set_yticks(range(height + 1))
    ax.grid(color='b', linewidth = 1)
    if file is not None:
        plt.savefig(file)
        plt.close()
    else:
        plt.show()


def outputSolution(instance, height, start_x, start_y, file):
    solution = []
    for i, x in enumerate(instance):
        if i == 0:
            solution.append(x + ' ' + str(height))
        elif i == 1:
            solution.append(x)
        else:
            solution.append(x + ' ' + str(start_x[i-2]) + ' ' + str(start_y[i-2]))
    with open(file, 'w') as output:
        for item in solution:
            output.write(item)
            output.write('\n')