import z
path = z.getPath("transcript/BUY2high.txt")

with open(path) as f:
    lines = f.readlines()
import matplotlib.pyplot as plt
i = 0
for idx , line in enumerate(lines):
    if "cvalue" in line:
        plt.scatter(i, float(line.split(" ")[1]), color="red")
        i+=1

path = z.getPath("transcript/BUY2low.txt")
with open(path) as f:
    lines = f.readlines()
import matplotlib.pyplot as plt
i = 0
for idx , line in enumerate(lines):
    if "cvalue" in line:
        plt.scatter(i, float(line.split(" ")[1]), color="blue")
        i+=1

plt.show()

