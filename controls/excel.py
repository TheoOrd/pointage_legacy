import xlwt
import calendar
import datetime
import controls.tools as tools
from models.employee import Employee
from models.dateRecord import DateRecord

#------------ Variables ------------#

NOM_FEUILLE        = 'pointages'
NOM_PREMIERE_CASE  = 'Date'

ABREV_SAMEDI   = 'Samedis'
ABREV_DIMANCHE = 'Dimanches'
ABREV_TOTAL    = 'Total'
ABREV_RETARD   = 'Quarts d\'heure de retard'

JOURS_SEMAINE = ['LUN', 'MAR', 'MER', 'JEU', 'VEN', 'SAM', 'DIM']

A   = '  A  '
M   = '  M  '
E   = '  E  '
AT  = ' AT  '
MP  = ' MP  '
CP  = ' CP  '
CE  = ' CE  '
CSS = ' CSS '

ROUGE  = xlwt.easyxf('pattern: pattern solid, fore_color red')
ORANGE = xlwt.easyxf('pattern: pattern solid, fore_color orange')
ROSE   = xlwt.easyxf('pattern: pattern solid, fore_color pink')
VIOLET = xlwt.easyxf('pattern: pattern solid, fore_color violet')
BRUN   = xlwt.easyxf('pattern: pattern solid, fore_color brown')
VERT   = xlwt.easyxf('pattern: pattern solid, fore_color light_green')
STYLES = {
    A   : ROUGE,
    M   : ORANGE,
    CP  : ROSE,
    CE  : ROSE,
    CSS : ROSE,
    MP  : VIOLET,
    AT  : VIOLET,
    E   : BRUN
}

#---------- Création excel ----------#

def genererExcel(lireMois, lireAnnee):

    try:
        mois = int(lireMois())
        annee = int(lireAnnee())
    except:
        r = DateRecord()
        mois = int(r.mm)
        annee = int(r.yy)

    if annee < 100:
        annee += 2000
    nbJoursMois = calendar.monthrange(annee, mois)[1]

    workbook = xlwt.Workbook()
    sheet = workbook.add_sheet(NOM_FEUILLE, cell_overwrite_ok=True)
    sheet.write(0, 0, NOM_PREMIERE_CASE)

    for i in range(1, nbJoursMois + 1):

        sheet.write(0, i, datetime.date(annee, mois, i), style = xlwt.easyxf(num_format_str = 'DD'))
        sheet.write(1, i, JOURS_SEMAINE[calendar.weekday(annee, mois, i)])

    sheet.write(0, 32, ABREV_SAMEDI)
    sheet.write(0, 33, ABREV_DIMANCHE)
    sheet.write(0, 34, ABREV_TOTAL)
    sheet.write(0, 35, ABREV_RETARD)

    if mois < 10:
        mois = '0'+ str(mois)
    else:
        mois = str(mois)

    #---------- Parcours des fichiers ----------#

    ligneExcel = 2
    employees = []
    for f in tools.listFiles():
        
        if f[:2] != mois:
            continue

        #---------- Lecture d'un fichier ----------#

        s = Employee(f[:2], f[3:])
        s = tools.load(s)
        employees.append(s)

    def quicksort(lst):
        if not lst:
            return []
        return (quicksort([x for x in lst[1:] if x.name <  lst[0].name])
                + [lst[0]] +
                quicksort([x for x in lst[1:] if x.name >= lst[0].name]))

    employees = quicksort(employees)

    for s in employees:
        
        s: Employee
        sheet.write(ligneExcel, 0, s.name)

        for p in s.pointings:
            p: DateRecord
            if len(p.hhmmss) == 8:
                sheet.write(ligneExcel, int(p.dd), p.hhmmss[:-3], style=VERT)
            else:
                sheet.write(ligneExcel, int(p.dd), p.hhmmss, style=STYLES[p.hhmmss])

        sheet.write(ligneExcel, 32, s.saturdays())
        sheet.write(ligneExcel, 33, s.sundays())
        sheet.write(ligneExcel, 34, len(s.pointings))
        sheet.write(ligneExcel, 35, s.getDelays())
        ligneExcel += 1

    with open('/home/pi/Desktop/Pointages '+ str(annee) +' '+ mois +'.xls', 'wb+') as flux:
        workbook.save(flux)
