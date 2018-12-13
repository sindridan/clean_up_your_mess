#the window app of main.py
from tkinter import *
from main import *

HEIGHT=500
WIDTH=500

window = Tk()
window.title('Sort your torrents!')
Frame(width=WIDTH, height=HEIGHT).pack()

Button(text='Clean download folder', command=sort_to_new_folder('from_folder', 'to_folder')).pack()

window.mainloop()