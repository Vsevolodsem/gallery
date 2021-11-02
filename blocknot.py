from os import path
import os
from tkinter import *
from tkinter import scrolledtext
from tkinter import messagebox
from tkinter.ttk import Progressbar
from tkinter import ttk
from tkinter import filedialog
from tkinter import Menu

list_open_files = []
notepadnames = [1]


def showModal():
    # messagebox
    # result = messagebox.askquestion("Заголовок", "Текст")
    result = messagebox._show("Заголовок", "Текст")
    if result != None:
        text_aria.insert(INSERT, result)
    # if result:
    #    text_aria.insert(INSERT, "Нажата кнопка Ок")
    # else:
    #    text_aria.insert(INSERT, "Нажата кнопка Cancel")


def openfile():
    print(globals())
    print('---------------------------------------------------------------')
    print(locals())
    print('---------------------------------------------------------------')
    path_file = filedialog.askopenfilename(filetypes=(("Text file", "*.txt"), ("All files", "*.*")),
                                           initialdir=path.dirname(__file__))
    if len(list_open_files) > 0:
        if list_open_files.count(path_file) > 0:
            messagebox.showerror('Ошибка', 'Файл с таким именем уже открыт')
        else:
            list_open_files.append(path_file)
            notepadnames.append(notepadnames[-1] + 1)
            text_file = open(path_file)
            namefile = path_file.split('/')
            # Создание новой вкладки
            globals()['tab' + str(notepadnames[-1])] = ttk.Frame(tab_control_main)
            globals()['tab_c' + str(notepadnames[-1])] = ttk.Notebook(globals()['tab' + str(notepadnames[-1])])
            tab_control_main.add(globals()['tab' + str(notepadnames[-1])], text=[namefile[-1]])
            tab_control_main.pack(expand=1, fill='both')
            globals()['tab_c' + str(notepadnames[-1])].pack(expand=1, fill='both')
            globals()['text_aria' + str(notepadnames[-1])] = scrolledtext.ScrolledText(
                globals()['tab_c' + str(notepadnames[-1])])
            globals()['text_aria' + str(notepadnames[-1])].pack(expand=True, fill=BOTH, anchor=NW)
            globals()['text_aria' + str(notepadnames[-1])].insert(INSERT, text_file.read())
            text_file.close()
    else:
        # Переименование вкладки
        list_open_files.append(path_file)
        window.title('Блокнот' + path_file)
        namefile = path_file.split('/')
        tab_control_main.tab('current', text=[namefile[-1]])
        text_file = open(path_file)

        text_aria.insert(INSERT, text_file.read())
        text_file.close()


def open_dir():
    print(__file__)
    path_dir = filedialog.askdirectory(initialdir=path.dirname(__file__))
    print(path_dir)


def save_file():
    if len(list_open_files) > 0:
        textfile = open(list_open_files[tab_control_main.index("current")], 'w')
        textfile.write(globals()['text_aria' + str(tab_control_main.index("current") + 1)].get(1.0, END))
        textfile.close()
    else:
        path_save_file = filedialog.asksaveasfilename(filetypes=(("Text files", "*.txt"), ("All files", "*.*")),
                                                      initialdir=path.dirname(__file__))
        file_name = path_save_file.split('/')
        file_name = file_name[-1]
        ext = file_name.split('.')
        ext = ext[-1]
        if ext != 'txt':
            file_name = file_name + '.txt'
            path_save_file = path_save_file + '.txt'
        text_file = open(path_save_file + "txt", 'w')
        text_file.write(text_aria.get(1.0, END))
        path_save_file = path_save_file.split('/')
        tab_control_main.tab(tab1, text=[path_save_file[-1] + ".txt"])
        window.title("Блокнот - " + file_name)
        text_file.close()


def save_as_file():
    path_save_file = filedialog.asksaveasfilename(filetypes=(("Text files", "*.txt"), ("All files", "*.*")),
                                                  initialdir=path.dirname(__file__))
    file_name = path_save_file.split('/')
    file_name = file_name[-1]
    ext = file_name.split('.')
    ext = ext[-1]
    if ext != 'txt':
        file_name = file_name + '.txt'
        path_save_file = path_save_file + '.txt'
    text_file = open(path_save_file, 'w')
    text_file.write(globals()['text_aria' + str(tab_control_main.index("current") + 1)])
    path_save_file = path_save_file.split('/')
    tab_control_main.tab(tab_control_main.index("current"), text=[path_save_file[-1]])
    window.title("Блокнот - " + file_name)
    text_file.close()


if __name__ == '__main__':
    window = Tk()
    window.iconbitmap(default='sketch.ico')
    window.title("Блокнот - Новый")
    window.resizable(True, True)

    tab_control_main = ttk.Notebook(window)
    tab1 = ttk.Frame(tab_control_main)

    tab_c1 = ttk.Notebook(tab1)

    tab_control_main.add(tab1, text='Новый')

    tab_control_main.pack(expand=1, fill='both')
    tab_c1.pack(expand=1, fill='both')

    text_aria = scrolledtext.ScrolledText(tab_c1)
    text_aria.pack(expand=True, fill=BOTH, anchor=NW)

    statusbar = Label(window, text='Statusbar', bd=1, relief=SUNKEN, anchor=W)
    statusbar.pack(side=BOTTOM, fill=X)

    # Menu
    menu = Menu(window)
    el_menu = Menu(menu, tearoff=0)
    el_menu.add_command(label='Создать')
    el_menu.add_command(label='Открыть', command=openfile)
    el_menu.add_command(label='Сохранить', command=save_file)
    el_menu.add_command(label='Сохранить как', command=save_as_file)
    menu.add_cascade(label='Файл', menu=el_menu)

    el2_menu = Menu(menu, tearoff=0)
    el2_menu.add_command(label='Отменить')
    el2_menu.add_separator()
    el2_menu.add_command(label='Вырезать')
    el2_menu.add_command(label='Копировать')
    el2_menu.add_command(label='Вставить')
    el2_menu.add_command(label='Удалить')
    el2_menu.add_separator()
    el2_menu.add_command(label='Найти')
    el2_menu.add_command(label='Найти далее')
    el2_menu.add_command(label='Заменить')
    el2_menu.add_command(label='Перейти')
    el2_menu.add_separator()
    el2_menu.add_command(label='Выделить все')
    el2_menu.add_command(label='Время и дата')
    menu.add_cascade(label='Правка', menu=el2_menu)

    el3_menu = Menu(menu, tearoff=0)
    el3_menu.add_command(label='Перенос по словам')
    el3_menu.add_command(label='Шрифт')
    menu.add_cascade(label='Формат', menu=el3_menu)

    el4_menu = Menu(menu, tearoff=0)
    el4_menu.add_command(label='Строка состояния')
    menu.add_cascade(label='Вид', menu=el4_menu)

    el5_menu = Menu(window, tearoff=0)
    el5_menu.add_command(label='О программе')
    menu.add_cascade(label='Справка', menu=el5_menu)
    window.config(menu=menu)

    history = Menu(el_menu, tearoff=0)
    history.add_command(label='doc_1')
    history.add_command(label='doc_2')
    history.add_command(label='doc_3')
    history.add_command(label='doc_4')
    el_menu.add_cascade(label='История', menu=history)

    el_menu.add_separator()
    el_menu.add_command(label='Выход')
    # menu.add_cascade(label='Файл', menu=el_menu)
    window.config(menu=menu)

    # Вычисляем положение и размеры окна
    # window.geometry('400x400')d
    window.update_idletasks()

    window_geometry = window.geometry()  ## 400x400+104+104
    print(window_geometry)

    window_geometry = window_geometry.split('+')  ## ['400x400', '104', '104']
    print(window_geometry)

    window_geometry = window_geometry[0].split('x')  ## ['400', '400']
    print(window_geometry)

    # h_window = int(window_geometry[1])
    # w_window = int(window_geometry[0])
    h_window = 400
    w_window = 600
    h_screen = window.winfo_screenheight() / 2 - h_window / 2
    w_screen = window.winfo_screenwidth() / 2 - w_window / 2

    window.geometry('%dx%d+%d+%d' % (w_window, h_window, w_screen, h_screen))
    ## ширина х высота + отступ_слева + отступ_сверху

    window.mainloop()
