from Tkinter import *
'''
class Application(Frame):

    def __init__(self, master = None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()

    def createWidgets(self):
        self.helloLable = Label(self, text = 'Hello world.')
        self.helloLable.pack()
        self.quitButton = Button(self, text = 'Quit', command = self.quit)
        self.quitButton.pack()


app = Application()
app.master.title('\tHello World!\t\n')
app.mainloop()
'''

import Tkinter.messagebox as messagebox
class Application(Frame):
    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.pack()
        self.createWidgets()

    def createWidgets(self):
        self.nameInput = Entry(self)
        self.nameInput.pack()
        self.alertButton = Button(self, text='Hello', command=self.hello)
        self.alertButton.pack()

    def hello(self):
        name = self.nameImput.get() or 'world'
        messagebox.showinfo('Message', 'Hello, %s' % name)
