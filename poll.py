# [方法（左），方法（右），图片序号，选择（左或右），选择的方法]
from tkinter import *
from PIL import Image, ImageTk
import random
import re
import os

# choice为用户的选择，由0和1组成。0表示选择左图，1表示选择右图
choice = []
# 记录图像对与用户选择的列表
list_b = []
# 未能获得评分的图像对列表
item_to_delete = []
# 获取测试者的用户名
name = []


def get_name():
    name.append(En.get())
    root0.destroy()


# 根据方法与原始图片名，找到该方法对应的图片名
def pic_name(var, pic):
    file_list = os.listdir(project_folder + '\\' + var)
    pic += '_'
    for file_name in file_list:
        if pic in file_name:
            return file_name
    return 'error'
    '''
    return {
        'BiGAN': 'step9299_img_' + pic + '.png',
        'cr': pic + '_0.50_cr.png',
        'lg': pic + '_0.50_lg.png',
        'multiop': pic + '_0.50_multiop.png',
        'osa': pic + '_0.50_osa.png',
        'qp': pic + '_0.50_qp.png',
        'sc': pic + '_0.50_sc.png',
        'scl': pic + '_0.50_scl.png',
        'sv': pic + '_0.50_sv.png',
        'warp': pic + '_0.50_warp.png'
    }.get(var, 'error')  # 'error'为默认返回值，可自设置
'''


# “left”、“right”按钮所对应的指令
def data_append():
    choice.append(data.get())  # 将用户选择“左”或“右”加入choice列表
    root.destroy()  # 终止本次循环，进入下一组选择


def close_with_saving():
    global list_b
    global item_to_delete
    for i in item_to_delete:
        list_b.remove(i)
    for i in range(len(list_b)):
        list_b[i].append(choice[i])
        list_b[i].append(list_b[i][choice[i]])
    method_count = [0 for i in range(method_num)]
    for i in range(len(list_b)):
        method_count[list_b[i][4] - 1] += 1
    with open(project_folder + '/results.txt', 'a') as fw:
        fw.write(' '.join([str(i) for i in method_count]) + ' ' + str(name[0]) + '\n')
    exit()


def close_without_saving():
    exit()


# "exit" 按钮对应的指令
def exit_window():
    root_exit = Tk()
    Label(root_exit, text="是否保存当前评分信息?").grid(row=0, column=1)
    Button(root_exit, text="yes", width=10, height=1, command=close_with_saving).grid(row=1, column=0)
    Button(root_exit, text="no", width=10, height=1, command=close_without_saving).grid(row=1, column=2)
    root_exit.mainloop()


def resize(w_box, h_box, picture):
    width, height = picture.size  # 获取图像的原始大小
    f1 = 1.0 * w_box / width
    f2 = 1.0 * h_box / height
    factor = min([f1, f2])
    width = int(width * factor)
    height = int(height * factor)
    return picture.resize((width, height), Image.ANTIALIAS)


root0 = Tk()
# 昵称不要有空格
label = Label(root0, text='请输入您的昵称:', anchor='c').grid(row=0)
En = Entry(root0)
En.grid(row=0, column=1)
Button(root0, text='确定', anchor='c', width=6, height=1, command=get_name).grid(row=2, column=1)
root0.mainloop()


# 用字典为所有方法编号
# TODO: user select project
project_folder = '.\RetargetMe_dataset'
path_methods = project_folder
method_list = os.listdir(path_methods)
method_list = [w for w in method_list if not re.search('[\.]', w)]
method_list.remove('original_image')
method_dict = {}
for i in range(1, len(method_list) + 1):
    method_dict[i] = method_list[i - 1]
print(method_dict)

# 用字典为所有图片编号
# TODO: user select original_image
original_folder = '\original_image'
path_pictures = project_folder + original_folder
picture_list = os.listdir(path_pictures)
picture_list = [re.sub('\.png', '', w) for w in picture_list]
picture_dict = {}
for i in range(1, len(picture_list) + 1):
    picture_dict[i] = picture_list[i - 1]
print(picture_dict)

method_num = len(method_list)  # 方法数量
picture_num = len(picture_list)  # 图片数量
# TODO: GUI output
# print("method number:" + str(method_num))
# print("picture number:" + str(picture_num))


for k in range(1, picture_num + 1):
    list_a = []
    # 从各种方法中取2种组合，并随机打乱顺序
    for i in range(1, method_num):
        for j in range(i + 1, method_num + 1):
            tmp = [i, j]
            random.shuffle(tmp)
            # list_a用来记录这些方法的组合。以3种方法为例，list_a可以为：[[2, 1], [1, 3], [3, 2]]
            list_a.append(tmp)
    # 每张图片都要经过list_a的组合进行比较，用list_b来记录，元素格式为：[方法（左），方法（右），图片序号]
    list_b += [l + [k] for l in list_a]

random.shuffle(list_b)
# 以4张图片为例，随机排序后的list_b可以为：
# [[1, 2, 1], [1, 3, 1], [2, 3, 1], [1, 2, 2], [1, 3, 2], [2, 3, 2], [2, 1, 3],
#  [3, 1, 3], [2, 3, 3], [1, 2, 4], [1, 3, 4], [3, 2, 4]]

note_s = '''用户对方法1结果图、方法2结果图进行偏好选择，选择的依据是：
            图像是否看上去自然、美观、无明显的扭曲变形，以及完整的保持了原始图像中的重要内容'''
# K：最初将list_b的值赋给item_to_delete
# 随着每一个评分的完成将对应项从item_to_delete中去除
# 这样就能实现中途退出并保存评分结果
# 不过如果加上断点续评之后这个应该也不需要了
item_to_delete = [item for item in list_b]

for i in range(len(list_b)):
    path_originalpic = project_folder + original_folder + "\\" + picture_dict[list_b[i][2]] + ".png"
    path_leftpic = project_folder + "\\" + method_dict[list_b[i][0]] + "\\" + pic_name(method_dict[list_b[i][0]],
                                                                                       picture_dict[list_b[i][2]])
    path_rightpic = project_folder + "\\" + method_dict[list_b[i][1]] + "\\" + pic_name(method_dict[list_b[i][1]],
                                                                                        picture_dict[list_b[i][2]])

    if os.path.exists(path_originalpic) and os.path.exists(path_leftpic) and os.path.exists(path_rightpic):
        root = Tk()

        # 加载原图
        load_0 = Image.open(path_originalpic)
        load_0 = resize(440, 400, load_0)
        render_0 = ImageTk.PhotoImage(load_0)
        img_0 = Label(root, image=render_0)
        img_0.image = render_0
        img_0.place(x=0, y=0)  # 设置图片放置位置

        # 加载左图。路径与list_b中的列表项有关
        load_1 = Image.open(path_leftpic)
        load_1 = resize(300, 400, load_1)
        render_1 = ImageTk.PhotoImage(load_1)
        img_1 = Label(root, image=render_1)
        img_1.image = render_1
        img_1.place(x=load_0.size[0] + 100, y=0)  # 设置图片放置位置

        # 加载右图。路径与list_b中的列表项有关
        load_2 = Image.open(path_rightpic)
        load_2 = resize(300, 400, load_2)
        render_2 = ImageTk.PhotoImage(load_2)
        img_2 = Label(root, image=render_2)
        img_2.image = render_2
        img_2.place(x=load_0.size[0] + load_1.size[0] + 200, y=0)  # 设置图片放置位置

        exit_button = Button(root, text="Exit", font=("黑体", 10), width=10, height=1, command=exit_window)
        # K： 显示当前的评分进度
        exit_button.pack(side=BOTTOM, pady=10)
        progress = "\n" + "[Progress]: " + str(i) + " / " + str(len(list_b))
        note = Label(root, text=note_s, width=100, height=3, font=("黑体", 11))
        note.pack(side=BOTTOM)
        progress_label = Label(root, text=progress, width=50, height=2, font=("黑体", 9))
        progress_label.pack(side=BOTTOM)
        # note.place(x=0,y=max(load_0.size[1],load_1.size[1],load_2.size[1])+70)

        # 设置窗口的大小
        width = load_0.size[0] + load_1.size[0] + load_2.size[0] + 210
        height = max(load_1.size[1], load_2.size[1]) + 170
        # K: 固定窗口位置不然晃来晃去的有点麻烦
        root.geometry("+10+30")
        root.geometry('%dx%d' % (width, height))
        root.title("Choose The Better One")

        label_original = Label(root, text="原始图像", width=int(load_0.size[0] / 8), height=1, bg="grey", font=("黑体", 11))
        label_m1 = Label(root, text="方法1结果图", width=int(load_1.size[0] / 8), height=1, bg="grey", font=("黑体", 11))
        label_m2 = Label(root, text="方法2结果图", width=int(load_2.size[0] / 8), height=1, bg="grey", font=("黑体", 11))
        label_original.place(x=0, y=load_0.size[1] + 1)
        label_m1.place(x=load_0.size[0] + 100, y=load_1.size[1] + 1)
        label_m2.place(x=load_0.size[0] + load_1.size[0] + 200, y=load_2.size[1] + 1)

        data = IntVar()
        # 设置“左”与“右”按钮
        left_button = Radiobutton(root, text="Left", width=int(load_1.size[0] / 9), height=1, variable=data, value=0,
                                  bg="white", font=("黑体", 12), command=data_append)
        right_button = Radiobutton(root, text="Right", width=int(load_2.size[0] / 9), height=1, variable=data, value=1,
                                   bg="white", font=("黑体", 12), command=data_append)

        left_button.place(x=load_0.size[0] + 100, y=load_1.size[1] + 30)
        right_button.place(x=load_0.size[0] + load_1.size[0] + 200, y=load_2.size[1] + 30)

        root.mainloop()
        item_to_delete.remove(list_b[i])
    else:
        pass
        # item_to_delete.append(list_b[i])

for i in item_to_delete:
    list_b.remove(i)

# list_b中元素原本的格式为：[方法（左），方法（右），图片序号]，现在加上用户的选择（0或1），与0、1对应的方法
# 更改后格式：[方法（左），方法（右），图片序号，选择（左或右），选择的方法]
for i in range(len(list_b)):
    list_b[i].append(choice[i])
    list_b[i].append(list_b[i][choice[i]])

# method_count所记录的是每一个方法由一名用户选择的数量，如：[1, 6, 5]，表示方法1选择1次，方法2选择6次，方法3选择5次
method_count = [0 for i in range(method_num)]
for i in range(len(list_b)):
    method_count[list_b[i][4] - 1] += 1

# print(list_b)
# print(method_count)
# 将本次用户的选择存入文档
with open(project_folder + '/results.txt', 'a') as fw:
    fw.write(' '.join([str(i) for i in method_count]) + ' ' + str(name[0]) + '\n')
# 读取所有用户的选择
results = []
with open(project_folder + '/results.txt', 'r') as fr:
    for line in fr:
        results.append(list(line.strip('\n').split(' ')))
print(results)

for result in results:
    print("Choices made by user", result[-1], result[:-1])

# method_sum为所有用户的选择
method_sum = [0 for i in range(method_num)]
for i in range(len(results)):
    for j in range(method_num):
        method_sum[j] += int(results[i][j])
print(method_sum)

method_num = 1
for score in method_sum:
    print("Score for method", method_dict[method_num], ": ", score)
    method_num += 1

