import os
from models.employee import Employee

FOLDER = '/home/pi/Desktop/pointages/'

def save(employee: Employee):

    with open(FOLDER + employee.month + ' ' + employee.name, 'w+', encoding='utf-8') as file:
        file.write(employee.saveJson())

def load(employee: Employee) -> Employee:
    
    if exist(employee):
        with open(FOLDER + employee.month + ' ' + employee.name, 'r', encoding='utf-8') as file:
            employee.loadJson(file.read())
    
    return employee

def exist(employee: Employee) -> bool:

    return os.path.isfile(FOLDER + employee.month + ' ' + employee.name)

def listFiles():

    return os.listdir(FOLDER)

def delete(employee: Employee):

    if exist(employee):
        os.remove(FOLDER + employee.month + ' ' + employee.name)

def loadCards() -> dict:

    dic = {}
    if os.path.isfile('codebarres.txt'):
        with open('codebarres.txt', 'r', encoding='utf-8') as file:
            for line in file.readlines():
                split = line.rstrip().split(' : ')
                dic[split[0]] = split[1]
    return dic

def saveCards(dic: dict):

    with open('codebarres.txt', 'w+', encoding='utf-8') as file:
        for k, v, in dic.items():
            file.write('{} : {}\n'.format(k, v))
