from tkinter import FLAT, NSEW, Button, Frame, Label, Widget

HOUR = 'hour'
EMPTY = ''
FONT = 'Helvetica 8'

A   = '  A  '
M   = '  M  '
E   = '  E  '
AT  = ' AT  '
MP  = ' MP  '
CP  = ' CP  '
CE  = ' CE  '
CSS = ' CSS '

DARK_GREEN  = '#9ED554'
LIGHT_GREEN = '#BEF574'

COLORS_LIGHT = {
    A   : '#FFDED7',
    M   : '#FF9F40',
    CP  : '#FEC5D9',
    CE  : '#FEC5D9',
    CSS : '#FEC5D9',
    MP  : '#4A68CB',
    AT  : '#4A68CB',
    E   : '#C27C66',
    EMPTY : '#E0E0E0',
    HOUR : '#BEF574'
}

COLORS_DARK = {
    A   : '#DFAEA7',
    M   : '#DF7F20',
    CP  : '#DEA5B9',
    CE  : '#DEA5B9',
    CSS : '#DEA5B9',
    MP  : '#2A48AB',
    AT  : '#2A48AB',
    E   : '#A25C46',
    EMPTY : '#C0C0C0',
    HOUR : '#9ED554'
}

class Grid:

    def __init__(self, parent: Frame):

        self.__parent = parent
        self.__rows = {}
        self.__frame = Frame(parent)
        self.__frame.grid()
        self.__row = 0
        self.__col = 0
        self.__dark = False

    def clear(self):

        self.__rows.clear()
        self.__frame.destroy()
        self.__init__(self.__parent)

    def setSize(self, rows: int, columns: int):

        self.__frame.rowconfigure(rows)
        self.__frame.columnconfigure(columns)

    def setRow(self, row: int=-1):

        if row == -1:
            row = len(self.__rows)

        if row % 2 == 0:
            self.__dark = True
        else:
            self.__dark = False

        self.__row = row

    def setColumn(self, column: int):

        self.__col = column

    def init_label(self, text: str, alternate: bool=False) -> Label:

        label = Label(self.__frame, text=text, font=FONT)
        label.grid(sticky=NSEW, row=self.__row, column=self.__col)

        if alternate:
            if self.__dark:
                grey = COLORS_DARK[EMPTY]
            else:
                grey = COLORS_LIGHT[EMPTY]
            label.config(bg=grey)

        try:
            row = self.__rows[self.__row]
        except KeyError:
            row = {}
            self.__rows[self.__row] = row

        row[self.__col] = label
        self.__col += 1
        return label

    def init_button(self) -> Button:
        
        if self.__dark:
            grey = COLORS_DARK[EMPTY]
        else:
            grey = COLORS_LIGHT[EMPTY]
        button = Button(self.__frame, text=EMPTY, font=FONT, relief=FLAT, border=0, highlightthickness=0, width=5, bg=grey)
        button.grid(sticky=NSEW, row=self.__row, column=self.__col)
        self.__rows[self.__row][self.__col] = button
        self.__col += 1
        return button

    def init_active(self, day: str, text: str):

        day = int(day)
        button = self.__rows[self.__row][day]
        self.active(button, text)

    def active(self, button: Button, text: str):

        if button.cget('bg') == COLORS_LIGHT[EMPTY]:
            bg = COLORS_LIGHT.get(text, LIGHT_GREEN)
        else:
            bg = COLORS_DARK.get(text, DARK_GREEN)
        button.config(text=text, bg=bg)

    def totals(self, name: str, *args):

        row = self.__getRow(name)
        index = len(row) - 2
        for value in args:
            row[index]['text'] = value
            index -= 1

    def destroyLine(self, name: str):

        deleted = False
        for i in range(len(self.__rows)):
            row: dict = self.__rows.get(i)

            if deleted:
                self.__rows[i - 1] = self.__rows.pop(i)
                for col, val in enumerate(row.values()):
                    val: Widget
                    val.grid(row=i-1, column=col)
                    self.__invertColor(val)

            if row[0]['text'] == name:
                deleted = True
                self.__rows.pop(i)
                for val in row.values():
                    val.destroy()

    def __invertColor(self, widget):

        bg = widget['bg']
        if bg == LIGHT_GREEN:
            bg = DARK_GREEN
        elif bg == DARK_GREEN:
            bg = LIGHT_GREEN
        elif bg in COLORS_LIGHT.values():
            bg = COLORS_DARK[[k for k, v in COLORS_LIGHT.items() if v == bg][0]]
        else:
            bg = COLORS_LIGHT[[k for k, v in COLORS_DARK.items() if v == bg][0]]
        widget.config(bg=bg)

    def getButton(self, name: str, day: int) -> Button:

        for line in self.__rows.values():
            if line[0]['text'] == name:
                return line[day]

    def __getRow(self, name: str) -> dict:

        for line in self.__rows.values():
            if line[0]['text'] == name:
                return line
