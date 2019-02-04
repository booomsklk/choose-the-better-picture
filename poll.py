from tkinter import *
from tkinter import messagebox
from tkinter import filedialog
from PIL import Image, ImageTk
import pickle
import random
import time
import re
import os

# 开发用：default_setting 自动填上初始窗口内容节约时间
default_setting = False
# 在程序初启动时才提示用户是否读取存档，之后的按键触发不提示
first_load = True
# login 表示用户是否成功输入用户名并且正确选择目录
login = False
# 用于表示读取存档是否成功
load_success = False
# check 表示是否选择了文件夹地址
pro_dir_check = False
ori_dir_check = False
# choice为用户的选择，由0和1组成。0表示选择左图，1表示选择右图
choice = []
method_list = []
picture_list = []
# 记录图像对与用户选择的列表
# [方法（左），方法（右），图片序号，选择（左或右），选择的方法]
list_b = []
# 未能获得评分的图像对列表
item_to_delete = []
step = 0
# 获取测试者的用户名
name = ''
project_folder = ''
original_folder = ''
save_folder = './save/'


def proceed(Event=None):
    global name
    name = En.get()
    # 关闭窗口或者输入为空直接结束程序
    if len(name) == 0 or name[0] == '':
        messagebox.showinfo(title='Error', message='请输入昵称')
    elif ' ' in name:
        messagebox.showinfo(title='Error', message='昵称中不可包含空格')
    elif not ori_dir_check or not pro_dir_check:
        messagebox.showinfo(title='Error', message='请指定项目及原始图像路径')
    else:
        global login
        login = True
        root0.destroy()


def check():
    valid = False

    if not os.path.exists(project_folder):
        messagebox.showerror('Error', '项目文件夹不存在')
        return valid
    elif not os.path.exists(project_folder + original_folder):
        messagebox.showerror('Error', '项目原始图像文件夹不存在')
        return valid

    re_path_methods = project_folder
    re_method_list = os.listdir(re_path_methods)
    re_method_list = [w for w in re_method_list if not re.search('[\.]', w)]
    re_method_list.remove(original_folder[1:])

    re_path_pictures = project_folder + original_folder
    re_picture_list = os.listdir(re_path_pictures)
    re_picture_list = [re.sub('\..+', '', w) for w in re_picture_list]

    if re_method_list != method_list:
        messagebox.showerror('Error', '项目生成方法文件夹丢失')
    elif re_picture_list != picture_list:
        messagebox.showerror('Error', '原始图像文件夹中图像丢失')
    else:
        valid = True

    return valid


# 使用pickle进行关键信息存档
def save():
    try:
        time_format = "_%Y%m%d%H%M"
        time_save = time.strftime(time_format)
        file_save = open(save_folder + project_folder[2:] + '_' + name + time_save + '.pkl', 'wb')
        files_need_saved = \
            [name, project_folder, original_folder, method_list, picture_list, list_b, item_to_delete, choice, step]
        for file in files_need_saved:
            pickle.dump(file, file_save)
        file_save.close()
    except IOError:
        print("Function save() failed.")
    pass


# 读取用户存档
def load():
    if not os.path.exists(save_folder):
        os.mkdir(save_folder)
    if len(os.listdir(save_folder)) > 0:
        if first_load:
            answer = messagebox.askyesno('Load', '检测到存档文件\n是否进行存档读取？')
        else:
            answer = True
        if answer:
            load_dir = filedialog.askopenfilename(title='选择存档进行读取', initialdir=save_folder)
            try:
                # print(load_dir)
                file_load = open(load_dir, 'rb')

                global name
                name = pickle.load(file_load)
                global project_folder
                project_folder = pickle.load(file_load)
                global original_folder
                original_folder = pickle.load(file_load)
                global method_list
                method_list = pickle.load(file_load)
                global picture_list
                picture_list = pickle.load(file_load)
                global list_b
                list_b = pickle.load(file_load)
                global item_to_delete
                item_to_delete = pickle.load(file_load)
                global choice
                choice = pickle.load(file_load)
                global step
                step = pickle.load(file_load)

                if check():
                    global load_success
                    load_success = True
                    global login
                    login = True
                    root0.destroy()

            except IOError:
                print("Function load() failed")


def get_project_dir(Event=None):
    global project_folder
    global pro_dir_check
    # global label_pro_dir
    project_dir = filedialog.askdirectory(title='选择工程文件夹', initialdir='.')
    if project_dir == '':
        return
    project_folder = '.' + project_dir[project_dir.rfind('/'):len(project_dir) + 1]
    label_pro_dir["text"] = project_folder
    pro_dir_check = True
    # print(project_folder)


def get_original_dir(Event=None):
    global original_folder
    global ori_dir_check
    project_abspath = os.path.abspath(project_folder)
    original_dir = filedialog.askdirectory(title='选择原始图像文件夹', initialdir=project_folder)
    original_abspath = os.path.abspath(original_dir)
    if original_dir == '':
        return
    elif project_abspath not in original_abspath or project_abspath == original_abspath:
        messagebox.showinfo(title='Error', message='原始图像文件夹不在项目文件夹下')
        return
    original_folder = original_dir[original_dir.rfind('/'):len(original_dir) + 1]
    label_ori_dir["text"] = project_folder + original_folder
    ori_dir_check = True
    # print(original_folder)


# 根据方法与原始图片名，找到该方法对应的图片名
def pic_name(var, pic):
    file_list = os.listdir(project_folder + '/' + var)
    for file_name in file_list:
        if pic in file_name:
            return file_name
    print("can't find \"" + pic + "\" in folder " + var)
    return 'error'


# “left”、“right”按钮所对应的指令
def data_append():
    choice.append(data.get())  # 将用户选择“左”或“右”加入choice列表
    if step + 1 == len(list_b):
        answer = messagebox.askyesno(title='Finished', message='项目评分完成！\n是否保存评分结果？')
        if answer:
            save_when_finished()
        exit()
    root.destroy()  # 终止本次循环，进入下一组选择


# 在评分完全结束时调用
def save_when_finished():
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
    if not os.path.exists(project_folder + '/results.txt'):
        file = open(project_folder + '/results.txt', 'w')
        file.write(str(method_dict) + '\n')
        file.close()
    with open(project_folder + '/results.txt', 'a') as fw:
        fw.write(' '.join([str(i) for i in method_count]) + ' ' + name + '\n')
        fw.close()


# "exit" 按钮对应的指令
def on_exit():
    answer = messagebox.askyesno('Save', '是否保存当前评分进度?')
    if answer:
        save()
    exit()


def reveal_label():
    label_2methods = Label(root, text="左图方法：" + method_dict[list_b[step][0]] + "  右图方法："
                                      + method_dict[list_b[step][1]], width=40, height=1, justify=LEFT, font=("黑体", 11))
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


# PHASE1: LOGIN
root0 = Tk()
root0.title("创建新项目")


# 昵称不要有空格
label = Label(root0, text='昵称（非空）', anchor='c').grid(row=0)
En = Entry(root0, width=35)
En.grid(row=0, column=1, columnspan=2, sticky=W, pady=10)

label_pro = Label(root0, text='项目路径').grid(row=1, column=0, sticky=W, padx=10)
label_pro_dir = Label(root0, text='选择项目路径...', width=50, bg='lightgray')
label_pro_dir.grid(row=1, column=1, sticky=W)
Button(root0, text='...', width=6, height=1, command=get_project_dir).grid(row=1, column=2, padx=10, pady=5)

label_ori = Label(root0, text='原始图像').grid(row=2, column=0, sticky=W, padx=10)
label_ori_dir = Label(root0, text='选择原始图像路径...', width=50, bg='lightgray')
label_ori_dir.grid(row=2, column=1, sticky=W)
Button(root0, text='...', width=6, height=1, command=get_original_dir).grid(row=2, column=2, padx=10, pady=5)
Button(root0, text='重新选择存档文件', width=20, height=1, command=load).grid(row=3, column=0, columnspan=2, padx=10, sticky=W)
Button(root0, text='创建', anchor='c', width=6, height=1, command=proceed).grid(row=3, column=2, pady=5)

# 进行自动填表的场合
if default_setting:
    default_user = StringVar()
    default_user.set("KaLuLas")
    En['textvariable'] = default_user
    label_pro_dir["text"] = "./RetargetMe_dataset"
    project_folder += "./RetargetMe_dataset"
    label_ori_dir["text"] = "./RetargetMe_dataset/original_image"
    original_folder += "/original_image"
    ori_dir_check = True
    pro_dir_check = True

load()
first_load = False
root0.mainloop()

if not login:
    exit()

# PHASE2: BUILD METHOD DICT & PICTURE DICT
if not load_success and login:
    path_methods = project_folder
    method_list = os.listdir(path_methods)
    method_list = [w for w in method_list if not re.search('[\.]', w)]
    method_list.remove(original_folder[1:])

    path_pictures = project_folder + original_folder
    picture_list = os.listdir(path_pictures)
    picture_list = [re.sub('\..+', '', w) for w in picture_list]

method_dict = {}
picture_dict = {}
# 用字典为所有方法编号
# 用字典为所有图片编号

for i in range(1, len(method_list) + 1):
    method_dict[i] = method_list[i - 1]
for i in range(1, len(picture_list) + 1):
    picture_dict[i] = picture_list[i - 1]

method_num = len(method_list)  # 方法数量
picture_num = len(picture_list)  # 图片数量

if not load_success and login:
    # PHASE3: BUILD LIST_B
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

    # K：最初将list_b的值赋给item_to_delete
    # 随着每一个评分的完成将对应项从item_to_delete中去除
    item_to_delete = [item for item in list_b]

note_s = '''用户对方法1结果图、方法2结果图进行偏好选择，选择的依据是：
            图像是否看上去自然、美观、无明显的扭曲变形，以及完整的保持了原始图像中的重要内容'''


# PHASE4: CHOOSE THE BETTER ONE
while step < len(list_b):
    path_originalpic = project_folder + original_folder + "/" + \
                       pic_name(original_folder[1:], picture_dict[list_b[step][2]])
    path_leftpic = project_folder + "/" + method_dict[list_b[step][0]] + "/" + pic_name(method_dict[list_b[step][0]],
                                                                                        picture_dict[list_b[step][2]])
    path_rightpic = project_folder + "/" + method_dict[list_b[step][1]] + "/" + pic_name(method_dict[list_b[step][1]],
                                                                                         picture_dict[list_b[step][2]])

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
        progress = "\n" + "[Progress]: " + str(step + 1) + " / " + str(len(list_b))
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

        label_original = Label(root, text="原始图像：" + picture_dict[list_b[step][2]], width=int(load_0.size[0] / 8), height=1, bg="LightSteelBlue", font=("黑体", 11))
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
        item_to_delete.remove(list_b[step])
    step += 1
