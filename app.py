from controls.events import Events
from controls.logic import Logic
from view.table import Table
from view.scan import Scan
from sys import platform

if platform == 'linux':
    cmd = 'python3'
else:
    cmd = 'python'
    
events = Events()
logic = Logic(events)
table = Table(events, cmd + ' app.py')
scan = Scan(events)
events.createTable()
events.updateDate()
table.mainloop()
