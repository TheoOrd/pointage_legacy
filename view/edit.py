from tkinter import END, Button, Entry, Frame, Label
from models.dateRecord import WEEKDAYS, DateRecord
from models.employee import Employee
from view.grid import COLORS_DARK, COLORS_LIGHT, DARK_GREEN, EMPTY, LIGHT_GREEN, A, M, CP, CE, CSS, MP, AT, E
import controls.tools as tools
import calendar

class Edit:

    def __init__(self, parent, backCommand):

        FONT = 'Helvatica 24'
        self.__backCommand = backCommand

        self.__frame = Frame(parent)
        parent = self.__frame

        self.__entry = Entry(parent, font=FONT)
        self.__entry.grid(row=0, column=0, columnspan=2)
        Button(parent, font=FONT, text='Valider', command=self.__validate).grid(row=0, column=2)

        self.__message = Label(parent, font=FONT)
        self.__message.grid(row=1, columnspan=4)

        def button(text: str, key: str):
            return Button(parent, font=FONT, text=text, command=lambda: self.__justification(key), bg=COLORS_LIGHT.get(key, 'red'))

        buttons = [
            button('Absence',                 A),
            button('Congés payés',            CP),
            button('Congés exceptionnels',    CE),
            button('Congés sans solde',       CSS),
            button('Maladie',                 M),
            button('Ecole',                   E),
            button('Maladie professionnelle', MP),
            button('Accident du travail',     AT)
        ]
        row = 2
        col = 0
        for b in buttons:
            b.grid(row=row, column=col, padx=10, pady=10)
            col += 1
            if col == 4:
                col = 0
                row += 1
        
        Button(parent, font=FONT, text='Supprimer',               command=self.__delete).grid(row=4, columnspan=4, pady=20)

    def go(self, button: Button, employee: Employee, dayNumber: int):

        self.__button = button
        self.__dayNumber = dayNumber
        self.__message.config(text='')
        self.__employee = tools.load(Employee(employee.month, employee.name))

        text = button['text']
        if text == EMPTY:
            text = ''

        self.__entry.insert(0, text)
        self.__frame.grid()

    def __validate(self):

        try:
            entry = self.__entry.get().strip()
            if len(entry) != 5 or entry[2] != ':':
                self.__message.config(text='Vérifiez que votre saisie respecte le format 00:00')
                return
            hh = int(entry[:2])
            mm = int(entry[3:5])
        except:
            self.__message.config(text='Vérifiez que votre saisie respecte le format 00:00')
            return

        color = self.__button['bg']
        if color in COLORS_LIGHT.values():
            color = LIGHT_GREEN
        elif color in COLORS_DARK.values():
            color = DARK_GREEN

        self.__back(entry, color, True)

    def __delete(self):

        pointing = None
        dayNumber = self.__getDayNumber()

        for p in self.__employee.pointings:
            p: DateRecord
            if p.dd == dayNumber:
                pointing = p
                break

        if pointing != None:

            color = self.__button['bg']
            if color in COLORS_LIGHT.values() or color == LIGHT_GREEN:
                color = COLORS_LIGHT[EMPTY]
            elif color in COLORS_DARK.values() or color == DARK_GREEN:
                color = COLORS_DARK[EMPTY]

            self.__employee.pointings.remove(pointing)
            self.__button.config(bg=color, text=EMPTY)
            tools.save(self.__employee)

        self.__entry.delete(0, END)
        self.__frame.grid_forget()
        self.__backCommand()

    def __justification(self, text: str):

        color = self.__button['bg']
        if color in COLORS_LIGHT.values() or color == LIGHT_GREEN:
            color = COLORS_LIGHT[text]
        elif color in COLORS_DARK.values() or color == DARK_GREEN:
            color = COLORS_DARK[text]
        self.__back(text, color, False)

    def __back(self, entry: str, color: str, isHour: bool):

        # Formatage du numéro de jour
        dayNumber = self.__getDayNumber()

        # Formatage de l'heure
        if isHour:
            text = entry + ':00'
        else:
            text = entry

        # Modification d'un pointage
        for p in self.__employee.pointings:
            p: DateRecord
            if p.dd == dayNumber:
                p.hhmmss = text
                break
        # Ajout d'un pointage
        else:
            p = DateRecord()
            p.dd = dayNumber
            p.hhmmss = text
            p.weekDayNumber = calendar.weekday(int(p.yy), int(p.mm), int(p.dd))
            p.weekDayName = WEEKDAYS[p.weekDayNumber]
            self.__employee.pointings.append(p)

        tools.save(self.__employee)
        self.__entry.delete(0, END)
        self.__button.config(text=entry, bg=color)
        self.__frame.grid_forget()
        self.__backCommand()

    def __getDayNumber(self) -> str:

        dayNumber = int(self.__dayNumber)
        if dayNumber < 10:
            return '0'+ str(dayNumber)
        else:
            return str(dayNumber)
