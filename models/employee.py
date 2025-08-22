from models.dateRecord import DateRecord

SATURDAY = 'SAM'
SUNDAY = 'DIM'

class Employee:

    def __init__(self, month: str, name: str):

        self.month = month
        self.name = name
        self.pointings = []
        self.delays = 0

    def hasAlreadyPointed(self, today: DateRecord) -> bool:

        if len(self.pointings) > 0:
            for p in self.pointings:
                p: DateRecord
                if p.dd == today.dd:
                    return True
        return False

    def getDelays(self) -> int:

        total = 0
        for p in self.pointings:
            p: DateRecord
            hms = p.hhmmss
            if len(hms) == 8:
                hours = int(hms[0:2])
                minutes = int(hms[3:5])
                gap = (hours - 7) * 60 + minutes - 1
                if gap > 0:
                    total += int(gap / 15)
        return total

    def saturdays(self) -> int:

        return self.__countDays(SATURDAY)

    def sundays(self) -> int:

        return self.__countDays(SUNDAY)
    
    def __countDays(self, dayCode: str):

        jour = 0
        for p in self.pointings:
            p: DateRecord
            if p.weekDayName == dayCode:
                jour += 1
        return jour

    def saveJson(self):

        pointages = ''
        for p in self.pointings:
            p: DateRecord
            pointages += '{}\n-\n'.format(p.saveText())
        pointages = pointages[:-1]

        return 'mois : {}\nnom : {}\nretards : {}\npointages : {}'.format(self.month, self.name, self.delays, pointages)

    def loadJson(self, texte):

        try:
            lignes = texte.split('\n')
            def v(i):
                return lignes[i].split(' : ')[1]

            self.month = v(0)
            self.name = v(1)
            self.delays = int(v(2))
            
            self.pointings.clear()
            pointingText = texte.split('pointages : ')[1].split('\n-\n')
            for tp in pointingText:
                
                if len(tp) < 5:
                    continue

                p = DateRecord()
                p.loadText(tp)
                self.pointings.append(p)
        except:
            print('Erreur sur le fichier : '+ self.name)
