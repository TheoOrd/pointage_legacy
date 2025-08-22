from controls.events import Events
from models.dateRecord import DateRecord
from models.employee import Employee
import controls.tools as tools

class Logic:

    def __init__(self, events: Events):

        self.events = events
        self.events.link('logic', self)
        self.mm = DateRecord().mm

        self.__cards = tools.loadCards()

    def scan(self, code: str):

        record = DateRecord()
                
        # Vérification du mois en cours
        if self.mm != record.mm:
            self.mm = record.mm
            self.events.createTable()

        if not self.__isEmployee(code):
            self.events.showMessage('Code-barre non reconnu : '+ code)
            return

        # Chargement du salarié
        s = Employee(self.mm, self.__cards[code])
        s = tools.load(s)

        # Vérification du pointage
        if s.hasAlreadyPointed(record):
            self.events.showMessage('Déjà pointé')

        # Ajout du pointage
        else:
            s.pointings.append(record)
            tools.save(s)
            self.events.showMessage(s.name + ' - Entrée validée, bonne journée !')
            self.events.updateTable(s)

    def getEmployees(self) -> list:

        employeeList = []
        for f in tools.listFiles():

            if f[:2] != self.mm:
                continue
            
            s = Employee(self.mm, f[3:])
            s = tools.load(s)
            employeeList.append(s)

        def quicksort(lst):
            if not lst:
                return []
            return (quicksort([x for x in lst[1:] if x.name <  lst[0].name])
                    + [lst[0]] +
                    quicksort([x for x in lst[1:] if x.name >= lst[0].name]))

        return quicksort(employeeList)

    def updateEmployees(self):

        self.__cards = tools.loadCards()

    def __isEmployee(self, code: str) -> bool:

        return code in self.__cards.keys()
