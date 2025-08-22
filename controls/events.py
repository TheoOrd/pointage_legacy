from models.employee import Employee

class Events:

    def __init__(self):

        self.get = {}

    def link(self, name: str, object):

        self.get[name] = object

    def showMessage(self, message: str):

        self.get['scan'].showMessage(message)

    def scan(self, barCode: str):

        self.get['logic'].scan(barCode)

    def createTable(self):

        employees = self.get['logic'].getEmployees()
        self.get['table'].createTable(employees)

    def updateTable(self, employee: Employee):

        self.get['table'].updateTable(employee)

    def updateDate(self):

        # Mise à jour sur l'IHM
        self.get['scan'].updateDate()

        # Actualisation toutes les 29 secondes (pour etre juste a la minute)
        self.get['scan'].after(29000, self.updateDate)

    def updateEmployees(self):

        self.get['logic'].updateEmployees()
