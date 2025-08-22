from tkinter import Frame, Label, Canvas
from models.releveDate import ReleveDate
import calendar


joursSemaine = ['LUN', 'MAR', 'MER', 'JEU', 'VEN', 'SAM', 'DIM']

class Tableau(Frame):

    def __init__(self, parent, evenements):

        Frame.__init__(self, parent)
        evenements.lier('Tableau', self)
        self.cases = []

    def creerTableau(self, listeSalaries):

        self.date = ReleveDate()
        self.rowconfigure(len(listeSalaries) + 2)
        self.columnconfigure(self.date.nbJoursMois + 4)

        for ligne in self.cases:
            for case in ligne:
                case.destroy()
        self.cases = []
        self.www = int(self.winfo_screenwidth() / 40)
        self.hhh = int(self.winfo_screenheight() / 40)

        self.__ligne1()
        self.__ligne2()
        self.__lignesSalaries(listeSalaries)

        l = 0
        for ligne in self.cases:
            c = 0
            for case in ligne:
                case.grid(row=l, column=c)
                c += 1
            l += 1

    def __ligne1(self):

        ligne = [self.caseLabel()]
        for i in range(1, self.date.nbJoursMois + 1):
            if i < 10:
                jour = '0'+ str(i)
            else:
                jour = str(i)
            ligne.append(self.caseLabel(text=jour))
        
        # ligne.append(self.caseLabel(text='SAM'))
        # ligne.append(self.caseLabel(text='DIM'))
        ligne.append(self.caseLabel(text='TOT'))
        self.cases.append(ligne)

    def __ligne2(self):

        ligne = [self.caseLabel()]
        for i in range(1, self.date.nbJoursMois + 1):
            txt = joursSemaine[calendar.weekday(int(self.date.aa), int(self.date.mm), i)]
            ligne.append(self.caseLabel(text=txt))
        self.cases.append(ligne)

    def __lignesSalaries(self, listeSalaries):

        for s in listeSalaries:

            ligne = []
            nom = s.nom
            if len(nom) > 15:
                nom = nom[:13] + '...'

            ligne.append(self.caseLabel(width=4 * self.www, text=nom))

            for i in range(0, self.date.nbJoursMois):
                ligne.append(self.case())

            for p in s.pointages:
                if p.entree:
                    couleur = 'orange'
                else:
                    couleur = 'green'
                ligne[int(p.jj)]['bg'] = couleur
            
            # ligne.append(self.caseLabel(text=s.nbSamedis()))
            # ligne.append(self.caseLabel(text=s.nbDimanches()))
            ligne.append(self.caseLabel(text=str(s.nbJoursTravail())))
            self.cases.append(ligne)

    def case(self, width=-1):

        if width == -1:
            width = self.www
        
        canvas = Canvas(self, width=width, height=self.hhh, borderwidth=1, relief='solid')
        return canvas

    def caseLabel(self, width=-1, text=''):
        
        canvas = self.case(width=width)
        label = Label(canvas, text=str(text), font='helvetica 12')
        label.grid(row=0, column=0)
        return canvas

    def actualiserTableau(self, salarie):
        
        self.date = ReleveDate()
        jour = int(self.date.jj)

        if salarie.pointages[-1].entree:
            couleur = 'orange'
        else:
            couleur = 'green'

        existe    = False
        for i in range(2, len(self.cases)):

            canvas = self.cases[i][0]
            label = canvas.winfo_children()[0]

            if label['text'] == salarie.nom:

                existe = True
                self.cases[i][jour]['bg'] = couleur

                self.__actualiserLabel(i, -1, salarie.nbJoursTravail())
                # self.__actualiserLabel(i, -2, salarie.nbDimanches())
                # self.__actualiserLabel(i, -3, salarie.nbSamedis())
        
        if not existe:

            nom = salarie.nom
            if len(nom) > 15:
                nom = nom[:13] + '...'
            ligne = [self.caseLabel(width=4 * self.www, text=nom)]

            for i in range(0, self.date.nbJoursMois):
                ligne.append(self.case())

            ligne[jour]['bg'] = couleur
            
            # ligne.append(self.caseLabel(text=salarie.nbSamedis()))
            # ligne.append(self.caseLabel(text=salarie.nbDimanches()))
            ligne.append(self.caseLabel(text=str(salarie.nbJoursTravail())))

            c = 0
            for case in ligne:
                case.grid(row=len(self.cases), column=c)
                c += 1
            self.cases.append(ligne)

    def __actualiserLabel(self, ligne, colonne, text):

        canvas = self.cases[ligne][colonne]
        label = canvas.winfo_children()[0]
        label['text'] = str(text)
