# [方法（左），方法（右），图片序号，选择（左或右），选择的方法]
from tkinter import *
from PIL import Image, ImageTk
import random

method_num = 3  # 方法数量
picture_num = 4  # 图片数量
list_a = []
list_b = []
# choice为用户的选择，由0和1组成。0表示选择左图，1表示选择右图
choice = []


# “left”、“right”按钮所对应的指令
def data_append():
    choice.append(data.get())  # 将用户选择“左”或“右”加入choice列表
    root.destroy()  # 终止本次循环，进入下一组选择


# 从各种方法中取2种组合，并随机打乱顺序
for i in range(1, method_num):
    for j in range(i + 1, method_num + 1):
        tmp = [i, j]
        random.shuffle(tmp)
        # list_a用来记录这些方法的组合。以3种方法为例，list_a可以为：[[2, 1], [1, 3], [3, 2]]
        list_a.append(tmp)

# 每张图片都要经过list_a的组合进行比较，用list_b来记录，元素格式为：[方法（左），方法（右），图片序号]
for i in list_a:
    for j in range(1, picture_num + 1):
        list_b.append(i + [j])

random.shuffle(list_b)
# 以4张图片为例，随机排序后的list_b可以为：
# [[2, 1, 1], [2, 1, 2], [2, 1, 3], [2, 1, 4], [3, 1, 1], [3, 1, 2],
# [3, 1, 3], [3, 1, 4], [3, 2, 1], [3, 2, 2], [3, 2, 3], [3, 2, 4]]


for i in range(len(list_b)):
    root = Tk()

    # 加载左图。路径与list_b中的列表项有关
    load = Image.open("methods/" + str(list_b[i][0]) + "/" + str(list_b[i][2]) + ".jpg")
    render = ImageTk.PhotoImage(load)
    img = Label(root, image=render)
    img.image = render
    img.place(x=0, y=0)  # 设置图片放置位置

    # 加载右图。路径与list_b中的列表项有关
    load2 = Image.open("methods/" + str(list_b[i][1]) + "/" + str(list_b[i][2]) + ".jpg")
    render2 = ImageTk.PhotoImage(load2)
    img2 = Label(root, image=render2)
    img2.image = render2
    img2.place(x=load.size[0] + 100, y=0)  # 设置图片放置位置

    # 设置窗口的大小
    width = load.size[0] + load2.size[0] + 100
    height = max(load.size[1], load2.size[1])
    root.geometry('%dx%d' % (width, height))
    # K: 固定窗口位置不然晃来晃去的有点麻烦
    root.geometry("+100+50")
    root.title("Choose The Better One")

    data = IntVar()
    # 设置“左”与“右”按钮
    left_button = Radiobutton(root, text="Left", variable=data, value=0, padx=20, pady=5, command=data_append).pack()
    right_button = Radiobutton(root, text="Right", variable=data, value=1, padx=20, pady=5, command=data_append).pack()
    root.mainloop()

# list_b中元素原本的格式为：[方法（左），方法（右），图片序号]，现在加上用户的选择（0或1），与0、1对应的方法
# 更改后格式：[方法（左），方法（右），图片序号，选择（左或右），选择的方法]
for i in range(len(list_b)):
    list_b[i].append(choice[i])
    list_b[i].append(list_b[i][choice[i]])

# method_count所记录的是每一个方法由一名用户选择的数量，如：[1, 6, 5]，表示方法1选择1次，方法2选择6次，方法3选择5次
method_count = [0 for i in range(method_num)]
for i in range(len(list_b)):
    method_count[list_b[i][4] - 1] += 1

print(list_b)
print(method_count)

# 将本次用户的选择存入文档
with open('methods/results.txt', 'a') as fw:
    fw.write(' '.join([str(i) for i in method_count])+'\n')

# 读取所有用户的选择
results = []
with open('methods/results.txt', 'r') as fr:
    for line in fr:
        results.append(list(line.strip('\n').split(' ')))
user_count = 0
for result in results:
    print("Choices made by user ", user_count, result)
    user_count += 1

# method_sum为所有用户的选择
method_sum = [0 for i in range(method_num)]
for i in range(len(results)):
    for j in range(method_num):
        method_sum[j] += int(results[i][j])
method_num = 1
for score in method_sum:
    print("Score for method", method_num, ": ", score)
    method_num += 1
