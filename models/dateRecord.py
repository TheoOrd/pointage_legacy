from datetime import datetime
import calendar

WEEKDAYS = ['LUN', 'MAR', 'MER', 'JEU', 'VEN', 'SAM', 'DIM']

class DateRecord:

    def __init__(self):

        date        = str(datetime.now())
        self.yy     = date[0:4]
        self.mm     = date[5:7]
        self.dd     = date[8:10]
        self.hhmmss = date[11:19]

        self.monthDays = calendar.monthrange(int(self.yy), int(self.mm))[1]
        self.weekDayNumber = calendar.weekday(int(self.yy), int(self.mm), int(self.dd))
        self.weekDayName    = WEEKDAYS[self.weekDayNumber]

    def toString(self) -> str:

        return self.dd + '/' + self.mm + '/' + self.yy + '   ' + self.hhmmss[:-3]

    def saveText(self) -> str:

        return 'aa : {}\nmm : {}\njj : {}\nhhmmss : {}\nnbJoursMois : {}\nnumeroJourSemaine : {}\nnomJourSemaine : {}'.format(
            self.yy, self.mm, self.dd, self.hhmmss, self.monthDays, self.weekDayNumber, self.weekDayName)

    def loadText(self, texte: str):

        ligne = texte.split('\n')
        def v(i):
            return ligne[i].split(' : ')[1]

        self.yy = v(0)
        self.mm = v(1)
        self.dd = v(2)
        self.hhmmss = v(3)
        self.monthDays = v(4)
        self.weekDayNumber = v(5)
        self.weekDayName = v(6)
