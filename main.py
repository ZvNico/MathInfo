from Automate import Automate
from tkinter.filedialog import askopenfilename, asksaveasfilename

if __name__ == '__main__':
    automate = Automate()
    if (automate.est_un_automate_asynchrone(askopenfilename(initialdir="automates/", filetypes=[('Text Files', '*.txt')])) == True):
        print("Cet automate est asynchrone")
    else: 
        print("Cet automate n'est pas asynchrone")

