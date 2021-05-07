from Automate import Automate
from copy import deepcopy
import os
import tkinter as tk

root = tk.Tk()
root.withdraw()

if __name__ == '__main__':
    plusde10 = []
    for i in range(1, 44):
        file = os.path.abspath(f"automates/A4-{i}.txt")
        print(file)
        automate = Automate()
        if len(automate.etats) < 9:
            print(automate.etats)
            print(automate.initial)
            print(automate.terminal)
            print(automate)
            print("==determinisation et completion==")
            automate.determinisation_et_completion_synchrone()
            print(automate.etats)
            print(automate.initial)
            print(automate.terminal)
            print(automate)
            print("==minimisation==")
            automate.minimisation()
            print(automate.etats)
            print(automate.initial)
            print(automate.terminal)
            print(automate)
            print("==complémentarisation==")
            automate.automate_complementaire()
            print(automate)
            automate.run()
        else:
            plusde10.append(i)
    print(plusde10)
