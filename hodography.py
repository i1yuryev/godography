import matplotlib                           #подключить библиотеку для графиков
matplotlib.use('TkAgg')                     #перейти в режим рисования графиков вместе с пользовательским интерфейсом tkinter
import numpy as np                          #подключить библиотеку для эффективной работы с массивами
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg  #импортировать только канвас из нужной "папки"
from matplotlib.figure import Figure        #импортировать фигуру
from tkinter import *                       #ui (windows forms) (* = импортировать все содержимое)
import math as m                            #импортировать функции для матеши
from datetime import datetime               #библиотека для дат, времени и т.д

#начало описания класса
class mclass:         #class - описание объекта
    def __init__(self,  window):            #конструктор, self = this
        self.window = window                #сообщаем классу на каком окне строить графики
        self.createWidgets()                #создать все кнопки, поля ввода, подписи
        self.createCanvas()                 #создать место где будет график
        self.currentPlot = 1                #количество прямых после нажатия кнопки Построить след.
        self.readall()                      #считать все, все начальные значения - это текст, поэтому задаются по умолчанию

        now = datetime.now()                            #получить текущее время (число в миллисекундах), объект

        current_time = now.strftime("%H:%M:%S")         # 13:51:53
        self.log.insert(END, "[" + current_time + "]Set up finished\n")

        self.log.see(END)
    #init
    def createCanvas(self):                 #создает начальное состояние полотна на котором булет график

        self.fig = Figure(figsize=(7,5))                                 # empty figure 7 inch * 5 inch
        self.p = self.fig.add_subplot(111)                                # empty plot 1 x 1 (1 раз)
        self.fig.subplots_adjust(left = 0.2,right = 0.8)                  # задаем поля
        self.p.set_title("Семейство годографов", fontsize=16)             # название всего графика
        self.p.set_ylabel("t в миллисекундах", fontsize=14)               # названия осей
        self.p.set_xlabel("x в метрах", fontsize=14)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.window)     # на каком окне должен нарисоваться канвас
        self.canvas.get_tk_widget().place(x=50,y=150)                     #поставить канвас на заданную позицию

        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        self.log.insert(END, "[" + current_time + "]Canvas Created\n")

        self.log.see(END)

    def createWidgets(self):                                              #создает пользовательский интерфейс

        v1_var = StringVar()                                              #текстовая переменная (String v1_var)
        self.v1_label = Label(window, textvariable=v1_var, relief=RAISED) #Подпись на прямоугольниках
        v1_var.set("<-V1")                                                #задаем значение текстовой переменной
        self.v1_label.place(x=350,y=0)                                    #разместить подпись (координаты эксперимент)

        v2_var = StringVar()
        self.v2_label = Label(window, textvariable=v2_var, relief=RAISED)
        v2_var.set("<-V2")
        self.v2_label.place(x=350, y=50)

        h_var = StringVar()
        self.h_label = Label(window, textvariable=h_var, relief=RAISED)
        h_var.set("<-H")
        self.h_label.place(x=350, y=100)

        phi1_var = StringVar()
        self.phi1_label = Label(window, textvariable=phi1_var, relief=RAISED)
        phi1_var.set("<-PHI_LOWER")
        self.phi1_label.place(x=750, y=0)

        phi2_var = StringVar()
        self.phi2_label = Label(window, textvariable=phi2_var, relief=RAISED)
        phi2_var.set("<-PHI_UPPER")
        self.phi2_label.place(x=750, y=50)

        phid_var = StringVar()
        self.phid_label = Label(window, textvariable=phid_var, relief=RAISED)
        phid_var.set("<-PHI_DELTA")
        self.phid_label.place(x=750, y=100)

        self.v1_textbox = Text(window, height=1, width=40)
        self.v1_textbox.place(x=0,y=0)
        self.v1_textbox.insert(END, chars="Введите v1")                     #добавить в конец

        self.v2_textbox = Text(window, height=1, width=40)
        self.v2_textbox.place(x=0,y=50)
        self.v2_textbox.insert(END, chars="Введите v2")

        self.h_textbox = Text(window, height=1, width=40)
        self.h_textbox.place(x=0,y=100)
        self.h_textbox.insert(END, chars="Введите h")

        self.phi1_textbox = Text(window, height=1, width=40)
        self.phi1_textbox.place(x=400,y=0)
        self.phi1_textbox.insert(END, chars="Введите нижнюю границу интервала phi")

        self.phi2_textbox = Text(window, height=1, width=40)
        self.phi2_textbox.place(x=400,y=50)
        self.phi2_textbox.insert(END, chars="Введите верхнюю границу интервала phi")

        self.dphi_textbox = Text(window, height=1, width=40)
        self.dphi_textbox.place(x=400,y=100)
        self.dphi_textbox.insert(END, chars="Введите delta phi")

        b1 = Button(window, text="Построить все", command=self.plotButtonOnClick) #command - какой метод вызывается при нажатии
        b1.place(x=850,y=0)

        b2 = Button(window, text="Построить следующий", command=self.plotNextButtonOnClick)
        b2.place(x=850,y=50)

        b3 = Button(window, text="Начать сначала", command=self.resetButtonOnClick)
        b3.place(x=850,y=100)

        b4 = Button(window, text="Считать данные", command=self.readall)
        b4.place(x=850,y=150)

        b4 = Button(window, text="Показать параметры", command=self.show_all)
        b4.place(x=850, y=200)

        self.log = Text(window, height=20, width=28) #создается прямоугольник в котором отображаюся произошедшие события
        self.log.place(x=760,y=250)                  #место куда он ставится

        start_text = "Events Log:"                        #начальный текст
        self.log.insert(END, start_text  + "\n")          # "abc" + "cba" = "abccba", "\n" - переход на новую строчку
        self.log.see(END)                                 # промотай в конец прямоугольника

        now = datetime.now()                              # объект, который берет дату
        current_time = now.strftime("%H:%M:%S")           # перевод в строчный формат  : часы:минуты:секунды
        self.log.insert(END, "["+current_time+"]Widgets Created\n") # виджет - любой элемент на форме помимо канваса

        self.log.see(END)                                 # промотай в конец прямоугольника


    @staticmethod                                                    #метод не привязанный к классу
    def degreeToRad(x):
        return x*m.pi/180                                            #convert to rad

    #input
    def getv1(self):
        try:
            self.v1 = float(self.v1_textbox.get("1.0",END))          #считает текст, пытается преобразовать в число
        except:
            self.v1 = 600                                            #значение по умолчанию

        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        self.log.insert(END, "[" + current_time + "]Read v1 = "+str(self.v1)+" m/s\n") #str - перевод в строчку
        self.log.see(END)
    def getv2(self):
        try:
            self.v2 = float(self.v2_textbox.get("1.0",END))

        except:
            self.v2 = 2000

        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        self.log.insert(END, "[" + current_time + "]Read v2 = " + str(self.v2) + " m/s\n")
        self.log.see(END)

    def geth(self):
        try:
            self.h = float(self.h_textbox.get("1.0", END))
        except:
            self.h = 15

        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        self.log.insert(END, "[" + current_time + "]Read h = " + str(self.h) + " m\n")
        self.log.see(END)

    def getphi1(self):
        try:
            self.phi1 = float(self.phi1_textbox.get("1.0", END))
        except:
            self.phi1 = 0

        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        self.log.insert(END, "[" + current_time + "]Read phi1 = " + str(self.phi1) + " deg\n")
        self.log.see(END)

    def getphi2(self):
        try:
            self.phi2 = float(self.phi2_textbox.get("1.0", END))
        except:
            self.phi2 = 20

        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        self.log.insert(END, "[" + current_time + "]Read phi2 = " + str(self.phi2) + " deg\n")
        self.log.see(END)

    def getdphi(self):
        try:
            self.delta_phi = float(self.dphi_textbox.get("1.0", END))
        except:
            self.delta_phi = 2

        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        self.log.insert(END, "[" + current_time + "]Read delta_phi = " + str(self.delta_phi) + " deg\n")
        self.log.see(END)

    def readall(self):                                                      #считывает все данные, для удобства
        self.getv1()
        self.getv2()
        self.geth()
        self.getphi1()
        self.getphi2()
        self.getdphi()


    #events

    def show_all(self):
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        self.log.insert(END, "[" + current_time + "]Parameters:\n" + "v1="+str(self.v1) + " m/s\n" + "v2="+str(self.v2) + " m/s\n" + "h="+
                        str(self.h)+" m\n"+"phi=["+str(self.phi1)+";"+str(self.phi2)+"] deg\n"+"delta_phi="+str(self.delta_phi)+" deg\n")
        self.log.see(END)
    def plotButtonOnClick(self):                                            #Построить все
        self.plot(True)                                                     #True - означает что нужно построить все сразу после нажатия
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        self.log.insert(END, "[" + current_time + "]Plot all finished\n")
        self.log.see(END)

    def plotNextButtonOnClick(self):                                        #Построить следующую линию
        self.plot(False)                                                    #False - означает что нужно добавить следующую линию на график
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        self.log.insert(END, "[" + current_time + "]Plot next finished\n")
        self.log.see(END)

    def resetButtonOnClick(self):
        self.currentPlot = 1
        self.p.clear()                                                      #удалить графики и конфигурацию (название графика, подписи осей)
        self.p.set_title("Семейство годографов", fontsize=16)               #заново добавляем название графики и подписи осей
        self.p.set_ylabel("t в миллисекундах", fontsize=14)  # названия осей
        self.p.set_xlabel("x в метрах", fontsize=14)
        self.canvas.draw()                                                  #отобразить полотно (а на нем находится наш график)
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        self.log.insert(END, "[" + current_time + "]Reset all\n")
        self.log.see(END)

    def plot (self, plotAll):                                               #метод построения

        self.p.clear()                                                      #стереть все

        i = m.asin(self.v1/self.v2)                                         #finding i

        t0 = 2*self.h*m.cos(i)/self.v1                                      #for the formula


        phis = mclass.degreeToRad(
            np.arange(self.phi1,self.phi2+self.delta_phi,self.delta_phi)    # нижняя граница. верхняя граница. шаг
        )                                                                   # all the possible values of phi in radians

        self.p.set_title("Семейство годографов", fontsize=16)               # название всего графика
        self.p.set_ylabel("t в миллисекундах", fontsize=14)                 # названия осей
        self.p.set_xlabel("x в метрах", fontsize=14)

        end = 200                                                           # по какое значение строятся графики
        step = 0.5                                                          # значения берутся с шагом 0.5

        x_pryam = np.arange(0,end,step)                                     # значения x для прямой волны [0, 0.5, 1 ... 200]
        self.p.plot(x_pryam, 1000 / self.v1 * x_pryam, label='Г. прямой\nволны', color='b') # b = синий цвет

        now = datetime.now()
        current_time = now.strftime("%H:%M:%S")
        self.log.insert(END, "[" + current_time + "] Upward wave:\n t = 1000/"+str(self.v1)+"(milliseconds)\n")
        self.log.see(END)

        #как работает np.arange
        # step = 0.5
        # left1 = 1
        # right = 10
        # current = left1
        # a = []
        # while current <= right:
           #  a.append(current)
           #  current = current + step

        start = 0

        if(plotAll):
            for phi in phis:
                start = 2*m.sin(i)*self.h/(m.cos(phi+i))                      #start of the second wave
                x_prelom = np.arange(start,end,step)                         # [start,.... , 200]
                t = (t0 +  m.sin(i+phi)/self.v1 * x_prelom)*1000              #vector x, умножаем x на число и добавляем число к каждому элементу x
                self.p.plot(x_prelom, t,label = 'phi='+str(phi/m.pi * 180))   #построй прямую для заданнаго phi
 
                now = datetime.now()
                current_time = now.strftime("%H:%M:%S")
                intersection = round(2 * self.h * m.cos(i) / (1 - m.sin(i + phi)), 2)  # 2 - знака после запятой
                self.log.insert(END, "[" + current_time + "] Plot phi=" + str(
                    180 / m.pi * phi) + ",\n" +
                                "Intersection: " + str(intersection) + "\nStart: " + str(round(start,2)) +"\n")
                self.log.see(END)
        else:
            for j in range(0,self.currentPlot):                             #j =0,1,2....currentPlot
                if j < phis.size:                                           #проверка на то что мы строим не больше линий чем у нас углов
                    start = 2 * m.sin(i) * self.h / (m.cos(phis[j] + i))    # start of the second wave
                    x_prelom = np.arange(start,end,step)                    # [0, 0.5, 1 .... , 200]
                    t = (t0 + m.sin(i + phis[j]) / self.v1 * x_prelom) * 1000      # vector x, умножаем x на число и добавляем число к каждому элементу x
                    self.p.plot(x_prelom, t, label = 'phi='+str(phis[j]/m.pi * 180))  #добаляем линию в конфигурацию графика

            if self.currentPlot <= phis.size:
                now = datetime.now()
                current_time = now.strftime("%H:%M:%S")
                intersection = round(2*self.h*m.cos(i)/(1-m.sin(i + phis[self.currentPlot-1])),2)
                self.log.insert(END, "[" + current_time + "] Plot phi="+str(180/m.pi * phis[self.currentPlot-1])+",\n"+
                                "Intersection: " + str(intersection)+"\nStart: " + str(round(start,2)) + "\n")
                self.log.see(END)

            self.currentPlot = self.currentPlot + 1                         #добавляем 1 к количеству линий которые будут построены после нажатия кнопки Построить след.
        self.p.legend(loc='upper left', bbox_to_anchor=(1.01, 1))           #см. интернет
        self.canvas.draw()                                                  #отображение на экран (рисует пиксели)

# начало программы (main)
window= Tk()                                                                #создаем окно для рисования
window.geometry("1000x670")                                                 #размер окна в пикселях
window.resizable(False,False)                                               #нельзя менять размер окна
window.title("Семейство годографов")                                        #название окна
mclass (window)                                                             #создание объекта  - он выступает как self так как он рассматривается сейчас
window.mainloop()                                                           #цикл приема событий (действий с окном) и их обработки
