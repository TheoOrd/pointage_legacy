from tkinter import ALL, DISABLED, NORMAL, END, NS, NSEW, NW, VERTICAL, Button, Canvas, Entry, Frame, Label, Scrollbar
from controls.events import Events
import controls.excel as excel
import controls.tools as tools

FONT = 'Helvetica 24'
PAD = 20
CANVAS_WIDTH = 1000
CANVAS_HEIGHT = 500
BAR_WIDTH = 30

class Param:

    def __init__(self, parent, backCommand, events: Events):
        
        self.__backCommand = backCommand
        self.__frame = Frame(parent)
        parent = self.__frame
        self.__events = events

        Button(parent, font=FONT, text='Retour', command=self.__back).grid(row=0, column=0, padx=PAD, pady=PAD, sticky=NW)
        Label(parent,  font=FONT, text='Génération du fichier Excel').grid(row=1, column=0, padx=PAD, pady=PAD, columnspan=2)
        Label(parent,  font=FONT, text='Mois  : ').grid(row=2, column=0, padx=PAD, pady=PAD)
        Label(parent,  font=FONT, text='Année : ').grid(row=3, column=0, padx=PAD, pady=PAD)

        vcmd = (parent.register(self.__onValidateDate), '%i')
        self.__month = Entry(parent, font=FONT, width=4, validate='key', validatecommand=vcmd)
        self.__year  = Entry(parent, font=FONT, width=4, validate='key', validatecommand=vcmd)
        self.__month.grid(row=2, column=1, padx=PAD, pady=PAD)
        self.__year.grid(row=3, column=1, padx=PAD, pady=PAD)

        self.__validate = Button(parent, font=FONT, text='Valider', command=self.__excel)
        self.__validate.grid(pady=PAD)
        self.__confim = Label(parent, font=FONT)
        self.__confim.grid(pady=PAD)

        Label(parent, font=FONT, text='Cartes existantes').grid(row=1, column=1, columnspan=2, padx=PAD, pady=PAD)

        scrollArea = Frame(parent)
        scrollArea.grid(row=2, column=2, rowspan=1000, sticky=NW)
        canvas = Canvas(scrollArea, width=CANVAS_WIDTH, height=CANVAS_HEIGHT)
        canvas.grid(row=0, column=0, sticky=NSEW)
        bar = Scrollbar(scrollArea, orient=VERTICAL, command=canvas.yview, width=BAR_WIDTH)
        bar.grid(row=0, column=1, sticky=NS)
        canvas.configure(yscrollcommand=bar.set)
        self.__scroll = Frame(canvas)
        canvas.create_window((0, 0), window=self.__scroll, anchor=NW)
        self.__scroll.bind('<Configure>', lambda e: canvas.configure(scrollregion=canvas.bbox(ALL)))

    def go(self):

        self.__cardsArea = Frame(self.__scroll)
        self.__cardsArea.grid()
        self.__codes = []
        self.__names = []

        r = 0
        cards = tools.loadCards()
        for k, v in cards.items():
            self.__newCard(r)
            self.__codes[-1].insert(0, k)
            self.__names[-1].insert(0, v)
            r += 1

        for i in range(5):
            self.__newCard(r + i)

        self.__frame.grid()

    def __newCard(self, r: int):

        vcmd = (self.__cardsArea.register(self.__onValidateCard), '%i')
        code = Entry(self.__cardsArea, font=FONT, validate='key', validatecommand=vcmd)
        name = Entry(self.__cardsArea, font=FONT)
        code.grid(row=r, column=0, padx=5, pady=5)
        name.grid(row=r, column=1, padx=5, pady=5)
        self.__codes.append(code)
        self.__names.append(name)

    def __onValidateDate(self, i: str) -> bool:

        return int(i) < 2

    def __onValidateCard(self, i: str) -> bool:

        return True
        # return int(i) < 4

    def __back(self):

        cards = {}
        for i in range(len(self.__codes)):
            code = self.__codes[i].get()
            name = self.__names[i].get()
            if code != '' and name != '':
                cards[code] = name
        tools.saveCards(cards)

        self.__cardsArea.destroy()
        self.__frame.grid_forget()
        self.__events.updateEmployees()
        self.__backCommand()

    def __excel(self):

        self.__validate.config(state=DISABLED)
        excel.genererExcel(self.__month.get, self.__year.get)
        self.__confim.config(text='Fichier Excel généré avec succès !')
        self.__month.delete(0, END)
        self.__year.delete(0, END)
        self.__frame.after(3000, lambda: self.__confim.config(text=''))
        self.__frame.after(3000, lambda: self.__validate.config(state=NORMAL))
