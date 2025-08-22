from threading import Thread
from tkinter import N, Button, Frame, Tk
from models.dateRecord import WEEKDAYS, DateRecord
from models.employee import Employee
from controls.events import Events
from view.delete import Delete
from view.edit import Edit
from view.grid import Grid
from view.param import Param
import calendar
import os

class Table(Tk):

    def __init__(self, events: Events, reloadCommand: str):

        super().__init__()
        events.link('table', self)
        self.__reloadCommand = reloadCommand
        
        self.title('Tableau')
        self.protocol('WM_DELETE_WINDOW', self.__reload)
        # self.attributes('-zoomed', True)

        self.__frame = Frame(self)
        self.__frame.grid()
        self.__grid = Grid(self.__frame)

        self.__param = Button(self, text='Paramètres', command=self.__goParam)
        self.__param.grid(row=0, column=1, sticky=N)

        self.__editPage = Edit(self, self.__back)
        self.__paramPage = Param(self, self.__back, events)
        self.__delete = Delete(self, self.__grid, self.__back)

    def __reload(self):

        self.destroy()
        Thread(target=lambda: os.system(self.__reloadCommand)).start()

    def createTable(self, employees: list):

        self.date = DateRecord()
        self.__grid.clear()
        self.__grid.setSize(len(employees) + 2, self.date.monthDays + 5)

        self.__header()
        self.__daysName()
        self.__employees(employees)

    def __header(self):

        grid = self.__grid
        grid.init_label('')
        for i in range(1, self.date.monthDays + 1):
            if i < 10:
                jour = '0' + str(i)
            else:
                jour = str(i)
            grid.init_label(jour)
        
        grid.init_label('SAM')
        grid.init_label('DIM')
        grid.init_label('TOT')

    def __daysName(self):

        grid = self.__grid
        grid.setRow(1)
        grid.setColumn(0)
        grid.init_label('')
        for i in range(1, self.date.monthDays + 1):
            index = calendar.weekday(int(self.date.yy), int(self.date.mm), i)
            grid.init_label(WEEKDAYS[index])

    def __employees(self, employees: list):

        grid = self.__grid
        for i, e in enumerate(employees):

            e: Employee
            grid.setRow(i + 2)
            grid.setColumn(0)
            grid.init_label(e.name, True)

            for j in range(0, self.date.monthDays):

                b = grid.init_button()
                b.config(command=lambda bb=b, ee=e, jj=j+1: self.__goEdit(bb, ee, jj))
                
            for p in e.pointings:
                
                p: DateRecord
                text = p.hhmmss
                if len(text) == 8:
                    text = text[:5]
                grid.init_active(p.dd, text)
            
            grid.init_label(e.saturdays(), True)
            grid.init_label(e.sundays(), True)
            grid.init_label(len(e.pointings), True)
            delete = grid.init_button()
            delete.config(text='    x    ', relief='raised', border=0, highlightthickness=0, command=lambda ee=e: self.__goDelete(ee))

    def updateTable(self, employee: Employee):

        self.date = DateRecord()
        name = employee.name
        grid = self.__grid
        button = grid.getButton(name, int(self.date.dd))

        if button != None:

            grid.active(button, self.date.hhmmss[:5])
            grid.totals(name, len(employee.pointings), employee.sundays(), employee.saturdays())
        
        else:

            grid.setRow()
            grid.setColumn(0)
            grid.init_label(name, True)

            for i in range(0, self.date.monthDays):

                button = grid.init_button()
                button.config(command=lambda b=button, e=employee, j=i+1: self.__goEdit(b, e, j))

            button = grid.getButton(name, int(self.date.dd))
            grid.active(button, self.date.hhmmss[:5])

            grid.init_label(employee.saturdays(), True)
            grid.init_label(employee.sundays(), True)
            grid.init_label(len(employee.pointings), True)

            delete = grid.init_button()
            delete.config(text='    x    ', relief='raised', border=0, highlightthickness=0, command=lambda e=employee: self.__goDelete(e))

    def __goEdit(self, button: Button, employee: Employee, dayNumber: int):

        self.__frame.grid_forget()
        self.__param.grid_forget()
        self.__editPage.go(button, employee, dayNumber)

    def __goParam(self):

        self.__frame.grid_forget()
        self.__param.grid_forget()
        self.__paramPage.go()

    def __goDelete(self, employee: Employee):

        self.__frame.grid_forget()
        self.__param.grid_forget()
        self.__delete.go(employee)

    def __back(self):

        self.__frame.grid()
        self.__param.grid(row=0, column=1, sticky=N)
