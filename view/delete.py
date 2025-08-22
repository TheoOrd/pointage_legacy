from tkinter import Frame, Button, Label
from models.employee import Employee
from view.grid import Grid
from view.param import FONT
import controls.tools as tools

class Delete:

    def __init__(self, parent, grid: Grid, backCommand):

        self.__backCommand = backCommand
        self.__grid = grid

        self.__frame = Frame(parent)
        self.__label = Label(self.__frame, font=FONT)
        self.__yes = Button(self.__frame, font=FONT, text='Oui')
        self.__no = Button(self.__frame, font=FONT, text='Non', command=self.__back)

        self.__label.grid(row=0, column=0, columnspan=2, pady=20)
        self.__yes.grid(row=1, column=0, padx=10, pady=10)
        self.__no.grid(row=1, column=1, padx=10, pady=10)

    def go(self, employee: Employee):

        self.__label.config(text='Confirmez-vous la suppression de '+ employee.name)
        self.__yes.config(command=lambda: self.__delete(employee))
        self.__frame.grid()

    def __delete(self, employee: Employee):

        tools.delete(employee)
        self.__grid.destroyLine(employee.name)
        self.__back()

    def __back(self):

        self.__frame.grid_forget()
        self.__backCommand()
