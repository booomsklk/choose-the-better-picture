# [方法（左），方法（右），图片序号，选择（左或右），选择的方法]
from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
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


def get_name(Event=None):
    name.append(En.get())
    root0.destroy()


def get_project_name(Event=None):
    global project_folder
    project = project_listbox.get(project_listbox.curselection())
    project = '\\' + project
    project_folder += project
    root_select_project.destroy()


def get_original_name(Event=None):
    global original_folder
    original = folder_listbox.get(folder_listbox.curselection())
    original_folder = '\\' + original
    root_select_original.destroy()


# 根据方法与原始图片名，找到该方法对应的图片名
def pic_name(var, pic):
    file_list = os.listdir(project_folder + '\\' + var)
    for file_name in file_list:
        if pic in file_name:
            return file_name
    return 'error'


# “left”、“right”按钮所对应的指令
def data_append():
    choice.append(data.get())  # 将用户选择“左”或“右”加入choice列表
    root.destroy()  # 终止本次循环，进入下一组选择


def save():
    method_count = [0 for i in range(method_num)]
    for i in range(len(list_b)):
        method_count[list_b[i][4] - 1] += 1
    if not os.path.exists(project_folder + '/results.txt'):
        file = open(project_folder + '/results.txt', 'w')
        file.write(str(method_dict) + '\n')
        file.close()
    with open(project_folder + '/results.txt', 'a') as fw:
        fw.write(' '.join([str(i) for i in method_count]) + ' ' + str(name[0]) + '\n')
        fw.close()


def close_with_saving():
    global list_b
    global item_to_delete
    for i in item_to_delete:
        list_b.remove(i)
    for i in range(len(list_b)):
        list_b[i].append(choice[i])
        list_b[i].append(list_b[i][choice[i]])
    save()
    exit()


def close_without_saving():
    exit()


# "exit" 按钮对应的指令
def on_exit():
    answer = messagebox.askyesno('Save', '是否保存当前评分信息?')
    if answer:
        close_with_saving()
    else:
        close_without_saving()


def reveal_label():
    label_2methods = Label(root, text="左图方法：" + method_dict[list_b[i][0]] + "  右图方法："
                                      + method_dict[list_b[i][1]], width=40, height=1, justify=LEFT, font=("黑体", 11))
    label_2methods.place(x=0, y=load_0.size[1] + 115)


def reveal_result():
    if not os.path.exists(project_folder + '/results.txt'):
        messagebox.showerror('Error', '尚无评分记录')
    else:
        records = []
        file = open(project_folder + '/results.txt', 'r')
        dic = file.readline()
        dic = re.sub('[{}:\']', '', dic)
        while True:
            line = file.readline()
            if line:
                records.append(list(line.strip('\n').split(' ')))
            else:
                break
        method_sum = [0 for i in range(method_num)]
        # method_sum为所有用户的选择
        for i in range(len(records)):
            for j in range(method_num):
                method_sum[j] += int(records[i][j])
        messagebox.showinfo('Records', dic + '得分情况：' + str(method_sum))

    
def resize(w_box, h_box, picture):
    width, height = picture.size  # 获取图像的原始大小
    f1 = 1.0 * w_box / width
    f2 = 1.0 * h_box / height
    factor = min([f1, f2])
    width = int(width * factor)
    height = int(height * factor)
    return picture.resize((width, height), Image.ANTIALIAS)


root0 = Tk()
root0.title("login")
# 昵称不要有空格
label = Label(root0, text='请输入您的昵称（非空）:', anchor='c').grid(row=0)
En = Entry(root0)
En.bind('<KeyRelease-Return>', get_name)
En.grid(row=0, column=1)
Button(root0, text='确定', anchor='c', width=6, height=1, command=get_name).grid(row=2, column=1)
root0.mainloop()
# 关闭窗口或者输入为空直接结束程序
if len(name) == 0 or name[0] == '':
    exit()

# 用字典为所有方法编号
project_folder = '.'
root_select_project = Tk()
root_select_project.title('Open Project(Double Click)')
# WARNING: 项目文件夹中不可包含 '.'
project_list = [path for path in os.listdir(project_folder) if '.' not in path]
listbox_len = 5 if len(project_list) < 5 else len(project_list)
project_listbox = Listbox(root_select_project, width=70, height=listbox_len, selectmode="browse")
project_listbox['font'] = ('consolas', 12)
project_listbox['listvariable'] = StringVar(value=project_list)
project_listbox.pack(side=TOP)
project_listbox.bind('<Double-Button-1>', get_project_name)
root_select_project.mainloop()
# 没有选择项目路径关闭窗口，或者所选文件夹下没有内容，直接退出程序
if project_folder == '.' or len([path for path in os.listdir(project_folder)]) == 0:
    exit()


# 用字典为所有图片编号
original_folder = ''
root_select_original = Tk()
root_select_original.title('Select folder that contains original images(Double Click)')
# WARNING: 项目中的方法文件夹中不可包含 '.'
folder_list = [path for path in os.listdir(project_folder) if '.' not in path]
listbox_len = 5 if len(folder_list) < 5 else len(folder_list)
folder_listbox = Listbox(root_select_original, width=70, height=listbox_len, selectmode="browse")
folder_listbox['font'] = ('consolas', 12)
folder_listbox['listvariable'] = StringVar(value=folder_list)
folder_listbox.pack(side=TOP)
folder_listbox.bind('<Double-Button-1>', get_original_name)
root_select_original.mainloop()
# 没有选择项目路径关闭窗口，或者所选文件夹下没有内容，直接退出程序
if original_folder == '' \
        or len([path for path in os.listdir(project_folder + original_folder)]) == 0:
    exit()

path_methods = project_folder
method_list = os.listdir(path_methods)
method_list = [w for w in method_list if not re.search('[\.]', w)]
method_list.remove(original_folder[1:])
method_dict = {}

for i in range(1, len(method_list) + 1):
    method_dict[i] = method_list[i - 1]
path_pictures = project_folder + original_folder
picture_list = os.listdir(path_pictures)
picture_list = [re.sub('\.png', '', w) for w in picture_list]
picture_dict = {}
for i in range(1, len(picture_list) + 1):
    picture_dict[i] = picture_list[i - 1]

method_num = len(method_list)  # 方法数量
picture_num = len(picture_list)  # 图片数量

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
    path_originalpic = project_folder + original_folder + "\\" + picture_dict[list_b[i][2]] + '.png'
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

        exit_button = Button(root, text="Exit", font=("黑体", 10), width=10, height=1, command=on_exit)
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

        label_original = Label(root, text="原始图像：" + picture_dict[list_b[i][2]], width=int(load_0.size[0] / 8), height=1, bg="LightSteelBlue", font=("黑体", 11))
        label_m1 = Label(root, text="方法1结果图", width=int(load_1.size[0] / 8), height=1, bg="LightSteelBlue", font=("黑体", 11))
        label_m2 = Label(root, text="方法2结果图", width=int(load_2.size[0] / 8), height=1, bg="LightSteelBlue", font=("黑体", 11))
        label_picture_num = Label(root, text="原始图片总数：" + str(picture_num), width=25, height=1, justify=LEFT, font=("黑体", 11))
        label_method_num = Label(root, text="生成方法总数：" + str(method_num), width=25, height=1, justify=LEFT, font=("黑体", 11))
        
        label_original.place(x=0, y=load_0.size[1] + 1)
        label_m1.place(x=load_0.size[0] + 100, y=load_1.size[1] + 1)
        label_m2.place(x=load_0.size[0] + load_1.size[0] + 200, y=load_2.size[1] + 1)
        label_picture_num.place(x=0, y=load_0.size[1] + 40)
        label_method_num.place(x=0, y=load_0.size[1] + 60)
        
        reveal_button = Button(root, text="点击查看左右图对应方法", width=25, height=1, font=("黑体", 11),
                               bg="LightGrey", command=reveal_label)
        reveal_button.place(x=35, y=load_0.size[1] + 90)
        result_button = Button(root, text="查看各类方法得分情况", width=23, height=1,  font=("黑体", 11),
                               bg="LightGrey", command=reveal_result)
        result_button.place(x=35, y=load_0.size[1] + 150)
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
'''
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
    method_num += 1 '''