from tkinter import BOTTOM, DISABLED, LEFT, NORMAL, Entry, Frame, Label, StringVar, Toplevel
from controls.events import Events
from models.dateRecord import DateRecord

PAUSE = 2000
FONT = 'helvetica 24'
PAD = 5

class Scan(Toplevel):

    def __init__(self, events: Events):

        super().__init__()
        self.events = events
        self.events.link('scan', self)

        self.protocol('WM_DELETE_WINDOW', self.__doNothing)
        self.title('Lecteur de code barre')
        # self.attributes('-zoomed', True)
        
        # if sys.platform == 'linux':
        #     self.attributes('-zoomed', True)
        # else:
        #     self.state('zoomed')
        # self.attributes('-fullscreen', True)

        self.__message = Label(self, font=FONT)
        self.__message.pack(side=BOTTOM, pady=30)

        self.date = Label(self, font=FONT)
        self.date.pack(pady=PAD)

        frame = Frame(self)
        frame.pack(side=BOTTOM)

        label = Label(frame, font=FONT, text='PRESENTEZ VOTRE CARTE')
        label.pack(side=LEFT, padx=PAD, pady=PAD)

        self.codeBarre = StringVar()
        self.__entry = Entry(frame, font=FONT, textvariable=self.codeBarre, bg='bisque', fg='maroon')
        self.__entry.pack(side=LEFT, padx=PAD, pady=PAD) 
        self.__entry.bind('<Return>', self.__detection)
        self.__focus()

    def __doNothing(self):

        pass

    def showMessage(self, message):
        
        self.__message['text'] = message
        
    def updateDate(self):

        self.date.configure(text=DateRecord().toString())

    def __focus(self):

        self.__entry.focus_set()
        self.after(120000, self.__focus)

    def __detection(self, tkEvent):

        if self.__entry['state'] == NORMAL:

            self.__entry['state'] = DISABLED
            self.events.scan(self.codeBarre.get())
            self.after(PAUSE, self.__setAvailable)

    def __setAvailable(self):

        self.codeBarre.set('')
        self.__entry.config(state=NORMAL)
