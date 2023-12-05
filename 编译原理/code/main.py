# -*-Coding =utf-8 -*-
# @Time :2023/11/29 13:46 
# @Author :linhaifeng
# @File:main.py

import tkinter as tk
import os
from tkinter import Button
from tkinter.scrolledtext import ScrolledText
from tkinter.filedialog import *
from tkinter import messagebox

# 建立主窗口
root = tk.Tk()
root.title('吾爱编译')
# 设置窗口长宽！
root.geometry('{}x{}+{}+{}'.format(1600, 780, 0, 0))
# 添加皮卡丘图标！
root.iconbitmap('love.ico')
# 放几个按钮
frame = tk.Frame(root, bg='black')
button1 = Button(frame, text='新文件', font=('微软雅黑', 10, 'bold'), fg='white', bg='black')
button2 = Button(frame, text='读 取', font=('微软雅黑', 10, 'bold'), fg='white', bg='black')
button3 = Button(frame, text='另存为', font=('微软雅黑', 10, 'bold'), fg='white', bg='black')
button4 = Button(frame, text='词 法', font=('微软雅黑', 10, 'bold'), fg='white', bg='black')
button5 = Button(frame, text='语 法', font=('微软雅黑', 10, 'bold'), fg='white', bg='black')
button6 = Button(frame, text='语 义', font=('微软雅黑', 10, 'bold'), fg='white', bg='black')
button7 = Button(frame, text='输 出', font=('微软雅黑', 10, 'bold'), fg='white', bg='black')
button8 = Button(frame, text='编 译', font=('微软雅黑', 10, 'bold'), fg='white', bg='black')
button9 = Button(frame, text='退 出', font=('微软雅黑', 10, 'bold'), fg='white', bg='black')
button10 = Button(frame, text='使用说明', font=('微软雅黑', 10, 'bold'), fg='white', bg='black')
button1.pack(side=tk.LEFT)
button2.pack(side=tk.LEFT)
button3.pack(side=tk.LEFT)
button4.pack(side=tk.LEFT)
button5.pack(side=tk.LEFT)
button6.pack(side=tk.LEFT)
button7.pack(side=tk.LEFT)
button8.pack(side=tk.LEFT)
button10.pack(side=tk.LEFT)
button9.pack(side=tk.LEFT)
frame.pack(side=tk.TOP, fill=tk.BOTH)

input_area = ScrolledText(font=('consolas', 25), fg='white', bg='black', height=3, insertbackground="white")
input_area.pack(fill=tk.BOTH, expand=1)
input_area.focus_set()

terminal = ScrolledText(font=('consolas', 15), fg='white', bg='black', height=6, insertbackground="white")
terminal.pack(fill=tk.BOTH)


# 其实就是删除所有内容！
def btn_1():
    input_area.delete(1.0, tk.END)


def btn_2():
    filename = askopenfilename(defaultextension='.txt')
    if filename != '':
        # 先删除之前的
        input_area.delete(1.0, tk.END)
        # 再把文件里的数据读出来！
        f = open(filename, 'r', encoding='utf-8', errors='ignore')
        input_area.insert(1.0, f.read())
        f.close()


def btn_3():
    filename = asksaveasfilename(initialfile='newfile', defaultextension='.txt')
    if filename != '':
        f = open(filename, 'w', encoding='utf-8', errors='ignore')
        data = input_area.get(1.0, tk.END)
        f.write(data)
        f.close()


def btn_7():
    os.system('notepad.exe output.txt')


# 为按钮设置功能
button1['command'] = lambda: btn_1()
button2['command'] = lambda: btn_2()
button3['command'] = lambda: btn_3()


# 这里把tab设成了4个空格，默认是8个有点不习惯！
def tab_pressed(event):
    input_area.insert("insert", " " * 4)
    return "break"


input_area.bind("<Tab>", tab_pressed)


def high_light(row, col, length):
    left, right = f'{row}.{col - 1}', f'{row}.{col + length - 1}'
    input_area.tag_add("highlight", left, right)
    input_area.tag_config("highlight", background="red", font=('consolas', 25), foreground="white", borderwidth=0.5,
                          relief="solid")


"""  
词法分析
"""
# 定义关键字
keywords = {'begin': 1, 'end': 2, 'if': 3, 'then': 4, 'and': 5, 'or': 6, 'not': 7, 'true': 8, 'false': 9}
# 定义符号
signs = {'+': 10, '-': 11, '*': 12, '=': 13, ':': 14, '>': 15, '<': 16, '(': 22, ')': 23, ';': 24}
number = ''  # 代表数字
word = ''  # 代表标识符
sign = ''  # 代表符号
kind = None  # 代表单词的种类
row = 1  # 当前所处的行
col = 1  # 当前所处的列
idx1, idx2 = 1, 1  # idx1表示读入字符的下标，idx2表示识别得到的单词的下标！
flag = True  # flag为False表示程序已经读完了所有的单词，结束扫描！


# 输入
class In:
    def __init__(self):
        self.value = None
        self.row = None
        self.col = None


In_lst = []


# 输出
class Out:
    def __init__(self):
        self.type = None
        self.value = None
        self.row = None
        self.col = None


Out_lst = []


def init_lexical():
    global row, col, idx1, idx2, kind, word, number, sign, flag, In_lst, Out_lst
    number = ''  # 代表数字
    word = ''  # 代表标识符
    sign = ''  # 代表符号
    kind = None  # 代表单词的种类
    row = 1  # 当前所处的行
    col = 1  # 当前所处的列
    idx1, idx2 = 1, 1  # idx1表示读入字符的下标，idx2表示识别得到的单词的下标！
    flag = True  # flag为False表示程序已经读完了所有的单词，结束扫描！
    In_lst = [In() for _ in range(1000)]
    Out_lst = [Out() for _ in range(1000)]
    flag = True  # flag为False表示程序已经读完了所有的单词，结束扫描！
    data = input_area.get(1.0, tk.END)
    # 去除末尾回车！
    lst = list(data)
    lst = lst[:-1]
    data = ''.join(lst)
    input_area.delete(1.0, tk.END)
    input_area.insert(1.0, data)
    terminal.delete(1.0, tk.END)


# 存储每个字符，及其对应的坐标【为之后的报错位置精准定位做准备！】
def readfile():
    global row, col
    i = 1
    f = input_area.get(1.0, tk.END)
    for x in f:
        if x == '\n':
            In_lst[i].value = '@'
            In_lst[i].row = row
            In_lst[i].col = col
            col = 1
            row += 1
            i += 1
        elif x == ' ':
            if In_lst[i - 1].value == '~':
                col += 1
                continue
            else:
                In_lst[i].value = '~'
                In_lst[i].row = row
                In_lst[i].col = col
            i += 1
            col += 1
        else:
            In_lst[i].value = x
            In_lst[i].row = row
            In_lst[i].col = col
            i += 1
            col += 1


def scanfile():
    global idx1, idx2, kind, word, number, sign, flag
    cur = In_lst[idx1].value
    idx1 += 1
    if cur is None:
        flag = False
    # 字母
    elif cur.isalpha() or cur == '_':
        # print(cur)
        Out_lst[idx2].row = In_lst[idx1 - 1].row
        Out_lst[idx2].col = In_lst[idx1 - 1].col
        while cur.isalpha() or cur == '_':
            word += cur
            cur = In_lst[idx1].value
            idx1 += 1
            if cur is None:
                flag = False
                break
        if flag:
            # 如果字母后边是空格或者换行或者符号，代表当前word是合法的！
            if cur == '~' or cur == '@' or cur in signs:
                idx1 -= 1
                kind = keywords.get(word, 26)
            # 如果字母后边是数字，然后数字后边又是字母，这种情况下的循环判断！
            elif cur.isdigit() or cur.isalpha() or cur == '_':
                while cur.isdigit() or cur.isalpha() or cur == '_':
                    word += cur
                    cur = In_lst[idx1].value
                    idx1 += 1
                    if cur is None:
                        flag = False
                        break
                if cur == '~' or cur == '@' or cur in signs or not flag:
                    idx1 -= 1
                    kind = keywords.get(word, 26)
                else:
                    while cur != '~':
                        if cur in signs:
                            idx1 -= 1
                            break
                        word += cur
                        cur = In_lst[idx1].value
                        idx1 += 1
                        # 表示非法标识符
                        kind = -1
                        if cur is None:
                            flag = False
                            break
            # 如果出现了其他的东西就是非法的！
            else:
                while cur != '~':
                    if cur in signs:
                        idx1 -= 1
                        break
                    word += cur
                    cur = In_lst[idx1].value
                    idx1 += 1
                    # 表示非法标识符
                    kind = -1
                    if cur is None:
                        flag = False
                        break
            Out_lst[idx2].value = word
            Out_lst[idx2].type = kind
            idx2 += 1
        # 中止的话，直接合法
        else:

            Out_lst[idx2].value = word
            Out_lst[idx2].type = keywords.get(word, 26)
            idx2 += 1
    # 数字
    elif cur.isdigit():
        Out_lst[idx2].row = In_lst[idx1 - 1].row
        Out_lst[idx2].col = In_lst[idx1 - 1].col
        while cur.isdigit():
            number += cur
            cur = In_lst[idx1].value
            idx1 += 1
            if cur is None:
                flag = False
                break
        if flag:
            # 如果数字后边是空格、换行符、或者符号的话！
            if cur == '~' or cur == '@' or cur in signs:
                kind = -1
                idx1 -= 1
            else:
                while cur != '~' and flag:
                    if cur in signs:
                        idx1 -= 1
                        break
                    number += cur
                    cur = In_lst[idx1].value
                    idx1 += 1
                    if cur is None:
                        flag = False
                        break
                # 表示非法数字
                kind = -1
            Out_lst[idx2].value = number
            Out_lst[idx2].type = kind
            idx2 += 1
        else:
            Out_lst[idx2].value = number
            Out_lst[idx2].type = 25
            idx2 += 1
    # 其他字符
    else:
        if cur == '<':
            Out_lst[idx2].row = In_lst[idx1 - 1].row
            Out_lst[idx2].col = In_lst[idx1 - 1].col
            sign += cur
            cur = In_lst[idx1].value
            idx1 += 1
            if cur == '>':
                kind = 21
                sign += cur
            elif cur == '=':
                kind = 19
                sign += cur
            else:
                kind = 17
                idx1 -= 1
                if cur is None:
                    flag = False

            Out_lst[idx2].value = sign
            Out_lst[idx2].type = kind
            idx2 += 1
        elif cur == '>':
            Out_lst[idx2].row = In_lst[idx1 - 1].row
            Out_lst[idx2].col = In_lst[idx1 - 1].col
            sign += cur
            cur = In_lst[idx1].value
            idx1 += 1
            if cur == '=':
                kind = 18
                sign += cur
            else:
                kind = 16
                idx1 -= 1
                if cur is None:
                    flag = False
            Out_lst[idx2].value = sign
            Out_lst[idx2].type = kind
            idx2 += 1
        elif cur == ':':
            Out_lst[idx2].row = In_lst[idx1 - 1].row
            Out_lst[idx2].col = In_lst[idx1 - 1].col
            sign += cur
            cur = In_lst[idx1].value
            idx1 += 1
            if cur == '=':
                kind = 15
                sign += cur
            else:
                # 非法符号
                kind = -3
                idx1 -= 1
                if cur is None:
                    flag = False

            Out_lst[idx2].value = sign
            Out_lst[idx2].type = kind
            idx2 += 1

        elif cur == '=':
            Out_lst[idx2].row = In_lst[idx1 - 1].row
            Out_lst[idx2].col = In_lst[idx1 - 1].col
            sign += cur
            cur = In_lst[idx1].value
            idx1 += 1
            if cur == '=':
                kind = 20
                sign += cur
            else:
                # 非法符号
                kind = -3
                idx1 -= 1
                if cur is None:
                    flag = False

            Out_lst[idx2].value = sign
            Out_lst[idx2].type = kind
            idx2 += 1

        # '~'表示空格
        elif cur == '~':
            pass
        # '@'表示换行符
        elif cur == '@':
            pass


        elif cur in signs:
            Out_lst[idx2].row = In_lst[idx1 - 1].row
            Out_lst[idx2].col = In_lst[idx1 - 1].col
            kind = signs[cur]
            sign = cur
            Out_lst[idx2].value = sign
            Out_lst[idx2].type = kind
            idx2 += 1

        else:
            # 非法符号
            kind = -1
            Out_lst[idx2].type = kind
            Out_lst[idx2].row = In_lst[idx1 - 1].row
            Out_lst[idx2].col = In_lst[idx1 - 1].col
            while cur != '~':
                sign += cur
                cur = In_lst[idx1].value
                idx1 += 1
                if cur in signs:
                    idx1 -= 1
                    break
                if cur is None:
                    flag = False
                    break
            Out_lst[idx2].value = sign
            idx2 += 1


def btn_4():
    global number, word, sign, kind, idx1, idx2, root, flag, col
    init_lexical()
    readfile()
    # for i in range(1,100):
    #     x = In_lst[i]
    #     print(x.value,x.row,x.col)
    f1 = open('output.txt', 'w', encoding='utf-8')
    print("┌-----------------------------------lexical analysis activate-------------------------------------┐")
    f1.write("┌-----------------------------------lexical analysis activate-------------------------------------┐\n")
    while flag:
        number = ''
        word = ''
        sign = ''
        kind = None
        scanfile()
    Out_lst[idx2].value = '#'
    Out_lst[idx2].type = 0
    try:
        Out_lst[idx2].row = Out_lst[idx2 - 1].row + 1
        Out_lst[idx2].col = 1
    except:
        terminal.insert(tk.END, f'Nothing in the data area!Please input something!')
        return
    terminal.delete(1.0, tk.END)
    cnt = 0
    for i in range(1, idx2 + 1):
        x = Out_lst[i]
        length = 0
        print(f"|<{x.value},{x.type}> {(8 - len(x.value) - len(str(x.type))) * ' '}({x.row},{x.col})",
              end=f'{(6 - len(str(x.row)) - len(str(x.col))) * " "}---->   ')
        f1.write(
            f"|<{x.value},{x.type}> {(8 - len(x.value) - len(str(x.type))) * ' '}({x.row},{x.col}){(6 - len(str(x.row)) - len(str(x.col))) * ' '}---->   ")
        if x.type == -1:
            if not flag:
                terminal.config(fg='red')
                terminal.insert(tk.END,
                                f'---------------------------------------------------------Lexical Analysis Fail----------------------------------------------------\n')
            length += len(
                f'\033[0;31;40mNot valid identifier! It happens on row:{Out_lst[i].row} col:{Out_lst[i].col}\033[0m')
            print(f'\033[0;31;40mNot valid identifier! It happens on row:{Out_lst[i].row} col:{Out_lst[i].col}\033[0m',
                  end='')
            f1.write(f'Not valid identifier! It happens on row:{Out_lst[i].row} col:{Out_lst[i].col}')
            print((82 - length) * ' ' + '|')
            f1.write((82 - length) * ' ' + '|')
            f1.write('\n')
            terminal.insert(tk.END,
                            f'error({cnt})  Not valid identifier! It happens on row:{Out_lst[i].row} col:{Out_lst[i].col}\n')
            cnt += 1
            flag = True
            r, c, l = x.row, x.col, len(x.value)
            high_light(r, c, l)

        # 这一部分删除，后边发现根本没有涉及到数字！
        # elif Out_lst[i].type == -2:
        #     flag1 = False
        #     length += len(f'\033[0;31;40mNot valid number! It happens on row:{Out_lst[i].row} col:{Out_lst[i].col}\033[0m')
        #     print(f'\033[0;31;40mNot valid number! It happens on row:{Out_lst[i].row} col:{Out_lst[i].col}\033[0m',end='')
        #     print((82 - length) * ' ' + '|')

        elif x.type == -3:
            if not flag:
                terminal.config(fg='red')
                terminal.insert(tk.END,
                                f'-------------------------------------------------Lexical Analysis Fail------------------------------------------------------------\n')
            length += len(
                f'\033[0;31;40mNot valid sign! It happens on row:{Out_lst[i].row} col:{Out_lst[i].col}\033[0m')
            print(f'\033[0;31;40mNot valid sign! It happens on row:{Out_lst[i].row} col:{Out_lst[i].col}\033[0m',
                  end='')
            print((82 - length) * ' ' + '|')
            f1.write('Not valid sign! It happens on row:{Out_lst[i].row} col:{Out_lst[i].col}' + (
                    82 - length) * ' ' + '|' + '\n')
            terminal.insert(tk.END,
                            f'error({cnt})  Not valid sign! It happens on row:{Out_lst[i].row} col:{Out_lst[i].col}\n')
            cnt += 1
            flag = True
            r, c, l = x.row, x.col, max(1, Out_lst[i + 1].col - x.col)
            high_light(r, c, l)
        else:
            length += len('\033[0;32;40mValid!\033[0m')
            print('\033[0;32;40mValid!\033[0m', end='')
            print((82 - length) * ' ' + '|')
            f1.write('Valid!' + (82 - length) * ' ' + '|' + '\n')
    if flag:
        terminal.config(fg='red')
        terminal.insert(tk.END,
                        f'------------------------------------------------------------Total {cnt} errors!-----------------------------------------------------------')
    else:
        terminal.config(fg='white')
        terminal.insert(tk.END,
                        f'--------------------------------------------------------Lexical Analysis Success----------------------------------------------------------\n')
    print("└------------------------------------  lexical analysis over  ------------------------------------┘")
    f1.write("└------------------------------------  lexical analysis over  ------------------------------------┘")
    return flag == False


button4['command'] = lambda: btn_4()

token_type = {'begin': 1, 'end': 2, 'if': 3, 'then': 4, ';': 5, 'id': 6,
              ':=': 7, '+': 8, '*': 9, '-': 10, '(': 11, ')': 12, 'or': 13,
              'and': 14, 'not': 15, 'rop': 16, 'true': 17, 'false': 18,
              '#': 19, 'S': 20, 'C': 21, 'L': 22, 'A': 23, 'B': 24, 'K': 25,
              'E': 26}

formulas = {0: ["S'", ["S"]], 1: ['S', ['C', 'S']], 2: ['S', ['begin', 'L', 'end']], 3: ['S', ['A']],
            4: ['C', ['if', 'B', 'then']],
            5: ['L', ['S']], 6: ['L', ['K', 'S']], 7: ['K', ['L', ';']], 8: ['A', ['id', ':=', 'E']],
            9: ['E', ['E', '+', 'E']], 10: ['E', ['E', '*', 'E']],
            11: ['E', ['-', 'E']], 12: ['E', ['(', 'E', ')']], 13: ['E', ['id']], 14: ['B', ['B', 'or', 'B']],
            15: ['B', ['B', 'and', 'B']],
            16: ['B', ['not', 'B']], 17: ['B', ['(', 'B', ')']], 18: ['B', ['E', 'rop', 'E']], 19: ['B', ['true']],
            20: ['B', ['false']]}

slr_table = [
    [0, 3, 0, 6, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 1, 2, 0, 4, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 200, 0, 0, 0, 0, 0, 0, 0],
    [0, 3, 0, 6, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 7, 2, 0, 4, 0, 0, 0],
    [0, 3, 0, 6, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 9, 2, 8, 4, 0, 10, 0],
    [0, 0, 103, 0, 0, 103, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 103, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 11, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 19, 0, 0, 0, 18, 14, 0, 0, 0, 13, 0, 16, 17, 0, 0, 0, 0, 0, 12, 0, 15],
    [0, 0, 101, 0, 0, 101, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 101, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 20, 0, 0, 21, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 105, 0, 0, 105, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 3, 0, 6, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 22, 2, 0, 4, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 19, 0, 0, 0, 18, 24, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 23],
    [0, 0, 0, 0, 25, 0, 0, 0, 0, 0, 0, 0, 0, 26, 27, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 19, 0, 0, 0, 18, 14, 0, 0, 0, 13, 0, 16, 17, 0, 0, 0, 0, 0, 28, 0, 15],
    [0, 0, 0, 0, 0, 0, 19, 0, 0, 0, 18, 14, 0, 0, 0, 13, 0, 16, 17, 0, 0, 0, 0, 0, 29, 0, 30],
    [0, 0, 0, 0, 0, 0, 0, 0, 32, 33, 0, 0, 0, 0, 0, 0, 31, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 119, 0, 0, 0, 0, 0, 0, 0, 119, 119, 119, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 120, 0, 0, 0, 0, 0, 0, 0, 120, 120, 120, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 19, 0, 0, 0, 18, 24, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 34],
    [0, 0, 113, 0, 113, 113, 0, 0, 113, 113, 0, 0, 113, 113, 113, 0, 113, 0, 0, 113, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 102, 0, 0, 102, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 102, 0, 0, 0, 0, 0, 0, 0],
    [0, 107, 0, 107, 0, 0, 107, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 106, 0, 0, 106, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 108, 0, 0, 108, 0, 0, 32, 33, 0, 0, 0, 0, 0, 0, 0, 0, 0, 108, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 19, 0, 0, 0, 18, 24, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 35],
    [0, 104, 0, 104, 0, 0, 104, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 19, 0, 0, 0, 18, 14, 0, 0, 0, 13, 0, 16, 17, 0, 0, 0, 0, 0, 36, 0, 15],
    [0, 0, 0, 0, 0, 0, 19, 0, 0, 0, 18, 14, 0, 0, 0, 13, 0, 16, 17, 0, 0, 0, 0, 0, 37, 0, 15],
    [0, 0, 0, 0, 116, 0, 0, 0, 0, 0, 0, 0, 116, 116, 116, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 38, 26, 27, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 32, 33, 0, 0, 39, 0, 0, 0, 31, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 19, 0, 0, 0, 18, 24, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 40],
    [0, 0, 0, 0, 0, 0, 19, 0, 0, 0, 18, 24, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 41],
    [0, 0, 0, 0, 0, 0, 19, 0, 0, 0, 18, 24, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 42],
    [0, 0, 111, 0, 111, 111, 0, 0, 111, 111, 0, 0, 111, 111, 111, 0, 111, 0, 0, 111, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 32, 33, 0, 0, 39, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 114, 0, 0, 0, 0, 0, 0, 0, 114, 114, 27, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 115, 0, 0, 0, 0, 0, 0, 0, 115, 115, 115, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 117, 0, 0, 0, 0, 0, 0, 0, 117, 117, 117, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 112, 0, 112, 112, 0, 0, 112, 112, 0, 0, 112, 112, 112, 0, 112, 0, 0, 112, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 118, 0, 0, 0, 32, 33, 0, 0, 118, 118, 118, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 109, 0, 109, 109, 0, 0, 109, 33, 0, 0, 109, 109, 109, 0, 109, 0, 0, 109, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 110, 0, 110, 110, 0, 0, 110, 110, 0, 0, 110, 110, 110, 0, 1010, 0, 0, 110, 0, 0, 0, 0, 0, 0, 0],
]


class Node:
    def __init__(self, token=None, id=-1):
        # 节点对应的字符
        self.token = token
        # 节点对应的产生式id
        self.id = id
        # 节点扩展出来的子节点
        self.next = []
        # 这个name主要是为之后生成四元式时，非终结符的临时名字，比如T1、T2
        self.name = ''


class TAC:
    def __init__(self, op, src1, src2, dst):
        # 操作符
        self.op = op
        # 源地址
        self.src1 = src1
        self.src2 = src2
        # 目的地址
        self.dst = dst

    # 打印函数
    def print(self, i, file):
        print(f"|{i:>2}:({self.op:<5},{self.src1:<5},{self.src2:<5},{self.dst:<5})")
        file.write(f"|{i:>2}:({self.op:<5},{self.src1:<5},{self.src2:<5},{self.dst:<5})\n")


roots = None
st = []
stk_formulas = []  # 存放表达式
stk_state = []  # 状态栈
stk_sign = []  # 符号栈


def init_syntactic():
    global roots, st, stk_formulas, stk_state, stk_sign
    roots = Node('S')
    st = [roots]
    stk_formulas = []  # 存放表达式
    stk_state = [0]  # 状态栈
    stk_sign = ['#']  # 符号栈
    data = input_area.get(1.0, tk.END)
    lst = list(data)
    lst = lst[:-1]
    data = ''.join(lst)
    input_area.delete(1.0, tk.END)
    input_area.insert(tk.END, data)
    terminal.delete(1.0, tk.END)


def btn_5():
    global roots, st, stk_formulas, stk_state, stk_sign, input_area
    init_syntactic()
    token = Out_lst
    n = idx2
    f2 = open('output.txt', 'a', encoding='utf-8')
    print('\n\n\n┌-----------------------------------syntactic analysis activate-----------------------------------┐')
    f2.write(
        '\n\n\n┌-----------------------------------syntactic analysis activate-----------------------------------┐\n')
    i = 1  # 输入串的下标
    cur = 0  # 当前状态
    flag = True
    error_state, error_value, error_row, error_col, error_type, error_sign = None, None, None, None, None, None
    while 1:
        # 代表标识符
        if token[i].value in ['>=', '==', '<=', '>', '<', '<>']:
            x = 16
        elif token[i].type == 26:
            x = 6  # 当前输入字符
        else:
            x = token_type[token[i].value]

        cur = slr_table[stk_state[-1]][x]

        if cur == 200:
            f2.write('|--------success-------- ' + (80 - len('success')) * ' ' + '|' + '\n')
            print('|\033[0;32;40m--------success--------\033[0m', end=' ')
            print((80 - len('success')) * ' ' + '|')
            terminal.config(fg='white')
            terminal.insert(tk.END,
                            f'------------------------------------------------------Syntactic Analysis Success----------------------------------------------------------\n')
            break
        elif cur < 100:
            stk_state.append(cur)
            if cur == 0:
                f2.write('|--------error--------' + (81 - len('error')) * ' ' + '|' + '\n')
                print('|\033[0;31;40m--------error--------\033[0m', end='')
                print((81 - len('error')) * ' ' + '|')
                flag = False
                error_state, error_value, error_row, error_col, error_type, error_sign = stk_state[-1], token[i].value, \
                    token[i].row, token[i].col, token[i].type, stk_sign[-1]
                # print(f'|[{stk_state[-1]}] -- [{token[i].value},({token[i].row},{token[i].col})]-- [{stk_sign[-1]}]')
                break
            if x == 6:
                stk_sign.append((x, token[i].value))
            elif x == 16:
                stk_sign.append([x, token[i].value])
            else:
                stk_sign.append(x)
            i += 1
        else:
            cur %= 100
            # 产生式的左右部！
            left, right = formulas[cur]
            # 要规约的符号
            right1 = stk_sign[-len(right):]

            stk_sign = stk_sign[:-len(right)]
            stk_state = stk_state[:-len(right)]

            stk_sign.append(left)
            stk_state.append(slr_table[stk_state[-1]][token_type[left]])

            if type(right1[0]) is tuple:
                right[0] = 'id' + '(' + right1[0][1] + ')'
                stk_formulas.append([left + '->' + ' '.join(right), cur])
            elif len(right1) == 3 and type(right1[1]) is list:
                # print(right)
                # print(right1)
                right[1] = 'rop' + '(' + right1[1][1] + ')'
                stk_formulas.append([left + '->' + ' '.join(right), cur])
            else:
                stk_formulas.append([left + '->' + ' '.join(right), cur])

    generate_formulas = stk_formulas[::-1]
    for j, x in enumerate(generate_formulas):
        f2.write('|' + f"{j:<2} {x[0]}" + (94 - len(x[0])) * ' ' + '|' + '\n')
        print('|', end='')
        print(f"{j:<2} {x[0]}", end='')
        print((94 - len(x[0])) * ' ' + '|')

    # 根据规约的生成式产生语法树！
    for formula in generate_formulas:
        left, right = formula[0].split('->')
        try:
            cur = st.pop()
        except:
            break
        cur.id = formula[1]
        for x in right.split(' '):
            if '(' in x and ')' in x:
                tmp = Node(x)
                x = x[:x.index('(')]
            else:
                tmp = Node(x)
            if token_type[x] >= 20:
                st.append(tmp)
            cur.next.append(tmp)

    # 根据规约的语法树打印出对应的叶子节点，输入的式子，如果正确就与输入完全相同，如果错误，则只会与一部分相同！
    input_data = []
    for j in range(1, n):
        input_data.append(token[j].value)
    generate_data = []

    def dfs(x):
        if not x.next:
            cur = x.token
            if '(' in cur and ')' in cur:
                generate_data.append((cur[cur.index('(') + 1:cur.index(')')]))
                # print(cur[cur.index('(') + 1:cur.index(')')], end=' ')
            else:
                generate_data.append(cur)
                # print(cur, end=' ')
            return
        for y in x.next:
            dfs(y)

    dfs(roots)
    if not flag:
        begin_num = input_data.count('begin')
        end_num = input_data.count('end')
        terminal.config(fg='red')
        terminal.insert(tk.END,
                        f'-------------------------------------------------------Syntactic Analysis Fail------------------------------------------------------------\n')
        length = len(generate_data)
        start = 0
        while start + length < len(input_data):
            if input_data[start:start + length] == generate_data:
                break
            # print(input_data[start:start + length],generate_data)
            start += 1
        end = start + length - 1
        print(input_data)
        print(generate_data)
        print(start, end, error_row, error_col)
        print(error_value)
        flag1 = True
        # 错误1
        if generate_data == ['S'] and flag1:
            print('语法错误，出现孤立不合法语句')
            if error_type in [1, 3, 26]:
                error_row, error_col, error_value = token[i - 1].row, token[i - 1].col, token[i - 1].value
                terminal.insert(tk.END, f'复合语句错误，缺少分号，它出现在{error_row}行,{error_col}列！\n')
            else:
                if error_value == '#':
                    error_row, error_col, error_value = token[i].row, token[i].col, token[i].value
                terminal.insert(tk.END, f'语法错误，出现孤立不合法语句，它出现在{error_row}行,{error_col}列！\n')
            high_light(error_row, error_col, len(error_value))
            flag1 = False
        # 错误2
        if error_type == 26 or error_value == ':=' and flag1:
            print('语法错误，出现不合法的字符(比较运算符、赋值运算符、孤立标识符)！')
            terminal.insert(tk.END,
                            f'字符错误:出现不合法的字符(比较运算符、赋值运算符、孤立标识符)<{error_value}>,它出现在{error_row}行,{error_col}列！\n')
            high_light(error_row, error_col, len(error_value))
            flag1 = False

        # 错误3
        if end + 1 != len(input_data) and input_data[end + 1] == ';' and flag1:
            print('复合语句异常:分号位置不合法')
            error_row, error_col, error_value = token[end + 2].row, token[end + 2].col, ';'
            terminal.insert(tk.END, f'复合语句异常:分号位置不合法，它出现在{error_row}行,{error_col}列！\n')
            high_light(error_row, error_col, len(error_value))
            flag1 = False

        # 错误4
        if input_data[end] == 'then' and flag1:
            print('条件语句异常:then后出现不合法语句')
            terminal.insert(tk.END, f'条件语句异常：then后出现不合法语句，它出现在{error_row}行,{error_col}列！\n')
            high_light(error_row, error_col, len(error_value))
            flag1 = False

        # 错误5
        if begin_num != end_num and start - 1 >= 0 and end + 1 < len(input_data) and input_data[
            start - 1] == 'begin' and input_data[end + 1] not in [';', 'end'] and flag1:
            print('结束语句异常1:begin后缺少end')
            error_row, error_col, error_value = token[i + 1].row, token[i + 1].col, ';'
            terminal.insert(tk.END, f'开始语句异常1:begin后缺少end，它出现在{error_row}行,{error_col}列！\n')
            input_area.insert(f'{error_row}.0', 'end')
            high_light(error_row, error_col, 3)
            flag1 = False

        if begin_num != end_num and input_data[start] == 'begin' and input_data[end] == 'end' and input_data[
            0] == 'begin' and flag1:
            print('结束语句异常2:begin后缺少end')
            input_area.insert(f'{error_row}.0', 'end')
            terminal.insert(tk.END, f'开始语句异常2:begin后缺少end，它出现在{error_row}行,{error_col}列！\n')
            high_light(error_row, error_col, 3)
            flag1 = False

        if begin_num != end_num and error_value == '#' and flag1:
            print('结束语句异常3:begin后缺少end')
            input_area.insert(f'{error_row}.0', 'end')
            terminal.insert(tk.END, f'开始语句异常3:begin后缺少end，它出现在{error_row}行,{error_col}列！\n')
            high_light(error_row, error_col, 3)
            flag1 = False

        if end + 2 < len(input_data) and input_data[end + 1] == 'end' and flag1:
            if input_data[end + 2] != ';':
                error_row, error_col, error_value = token[i - 1].row, token[i - 1].col, token[i - 1].value
                terminal.insert(tk.END, f'复合语句错误，缺少分号，它出现在{error_row}行,{error_col}列！\n')
                high_light(error_row, error_col, len(error_value))
                flag1 = False

        if token[i - 1].value != ';' and flag1:
            print(token[i - 1].value, token[i].value, token[i + 1].value)
            error_row, error_col, error_value = token[i - 1].row, token[i - 1].col, token[i - 1].value
            terminal.insert(tk.END, f'复合语句错误，缺少分号，它出现在{error_row}行,{error_col}列！\n')
            high_light(error_row, error_col, len(error_value))
            flag1 = False

        if flag1:
            terminal.insert(tk.END, f'其他错误，它出现在{error_row}行,{error_col}列！\n')
            high_light(error_row, error_col, len(error_value))

    print('└----------------------------------  syntactic analysis over  ------------------------------------┘')
    f2.write('└----------------------------------  syntactic analysis over  ------------------------------------┘\n')
    return flag == True


button5['command'] = lambda: btn_5()


def init_semantic():
    pass


cnt = 0


def generate_name():
    global cnt
    cnt += 1
    return f"{'T'}{cnt}"


def btn_6():
    global roots, cnt
    cnt = 0
    f3 = open('output.txt', 'a', encoding='utf-8')
    print(
        '\n\n\n┌-----------------------------------semantic analysis activate-----------------------------------------------------------------------')
    f3.write(
        '\n\n\n┌-----------------------------------semantic analysis activate-----------------------------------------------------------------------\n')
    print('|Syntactic tree\n|')
    f3.write('|Syntactic tree\n|\n')

    def bfs(pre, depth):
        # 此处使用双数组模拟队列进行bfs
        while pre:
            cur = pre[::-1]
            pre = []
            f3.write(f"|{depth:>2}:")
            print(f"|{depth:>2}:", end=' ')
            while cur:
                node = cur.pop()
                f3.write(f"【{node.token, node.id}】  ")
                print(f"【{node.token, node.id}】", end=' ')
                for x in node.next:
                    pre.append(x)
            print()
            f3.write('\n')
            depth += 1

    bfs([roots], 0)
    tacs = []

    def back_patch(idx):
        tacs[idx].dst = len(tacs)

    def cal_tac(root):
        # 表示这个是终结符
        if not root.next:
            return
        id = root.id
        # S -> CS
        if id == 1:
            # a: C -> if B then
            # b: S -> ...
            a, b = root.next
            # a1:B -> E rop E
            a1 = a.next[1]
            cal_tac(a1)
            tacs.append(TAC('j=', a1.name, 'true', len(tacs) + 2))
            tacs.append(TAC('j', '_', '_', None))  # None表示等待回填
            back = len(tacs) - 1
            cal_tac(b)
            back_patch(back)
        # A -> id:=E
        elif id == 8:
            # c: E-> ...
            a, _, c = root.next
            cal_tac(c)
            tacs.append(TAC(":=", c.name, '_', a.token[a.token.index('(') + 1:a.token.index(')')]))
        # E -> E + E
        elif id == 9:
            a, _, c = root.next
            cal_tac(a)
            cal_tac(c)
            root.name = generate_name()
            tacs.append(TAC('+', a.name, c.name, root.name))
        # E -> E * E
        elif id == 10:
            a, _, c = root.next
            cal_tac(a)
            cal_tac(c)
            root.name = generate_name()
            tacs.append(TAC('*', a.name, c.name, root.name))
        # E -> -E
        elif id == 11:
            b = root.next[1]
            cal_tac(b)
            root.name = generate_name()
            tacs.append(TAC('-', b.name, '_', root.name))
        # E -> (E)
        elif id == 12:
            b = root.next[1]
            cal_tac(b)
            root.name = b.name
        # E -> id
        elif id == 13:
            a = root.next[0]
            root.name = a.token[a.token.index('(') + 1:a.token.index(')')]
        # B -> B or B
        elif id == 14:
            a, _, c = root.next
            cal_tac(a)
            cal_tac(c)
            root.name = generate_name()
            tacs.append(TAC('or', a.name, c.name, root.name))
        # B -> B and B
        elif id == 15:
            a, _, c = root.next
            cal_tac(a)
            cal_tac(c)
            root.name = generate_name()
            tacs.append(TAC('and', a.name, c.name, root.name))
        # B -> not B
        elif id == 16:
            b = root.next[1]
            cal_tac(b)
            root.name = generate_name()
            tacs.append(TAC('not', b.name, '_', root.name))
        # B -> (B)
        elif id == 17:
            b = root.next[1]
            cal_tac(b)
            root.name = b.name
        # B -> E rop E
        elif id == 18:
            a, b, c = root.next
            cal_tac(a)
            cal_tac(c)
            root.name = generate_name()
            tacs.append(TAC(b.token[b.token.index('(') + 1:b.token.index(')')], a.name, c.name, root.name))
        # B -> true
        elif id == 19:
            root.name = 'true'
        # B -> false
        elif id == 20:
            root.name = 'false'
        else:
            for x in root.next:
                cal_tac(x)

    f3.write('|\n')
    cal_tac(roots)
    print('|Three-Address Code')
    f3.write(
        "|Three-Address Code\n|\n")
    for i, x in enumerate(tacs):
        x.print(i, f3)

    print(
        "└------------------------------------ semantic analysis over ------------------------------------------------------------------------")
    f3.write(
        "└------------------------------------ semantic analysis over ------------------------------------------------------------------------")
    terminal.delete(1.0, tk.END)
    terminal.config(fg='white')
    terminal.insert(tk.END,
                    f'---------------------------------------------------------Semantic Analysis Success--------------------------------------------------------\n')


button6['command'] = lambda: btn_6()

terminal.config(fg='red')


def btn_8():
    if btn_4():
        if btn_5():
            btn_6()
            terminal.delete(1.0, tk.END)
            terminal.config(fg='white')
            terminal.insert(tk.END,
                            '-----------------------------------------成功，无词法错误，无语法错误，完成静态语义分析及四元式生成--------------------------------\n')
        else:
            terminal.insert(tk.END, '\n------------------------语法分析出现错误------------------------\n')
    else:
        terminal.insert(tk.END, '\n------------------------词法分析出现错误------------------------\n')


button7['command'] = lambda: btn_7()
button8['command'] = lambda: btn_8()
button9['command'] = lambda: root.destroy()


def btn_10():
    messagebox.showinfo('使用说明',
                        '本程序默认使用txt文件'
                        '\n新文件---------刷新输入区，重新输入'
                        '\n读    取---------打开指定文件夹文件'
                        '\n另存为---------将源代码保存为其他名字的文件'
                        '\n词    法---------对源程序进行词法分析，信息在终端输出，结果点输出按钮'
                        '\n语    法---------对源程序进行语法分析，信息在终端输出，结果点输出按钮'
                        '\n语    义---------对源程序进行语义分析，信息在终端输出，结果点输出按钮'
                        '\n编    译---------对源程序先后进行词法分析、语法分析、语义分析，信息在终端输出，结果点输出按钮')


button10['command'] = lambda: btn_10()
root.mainloop()
