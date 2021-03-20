from tkinter.filedialog import askopenfilename, asksaveasfilename
import constantes
from prettytable import PrettyTable


class Automate:
    def __init__(self):
        filename = askopenfilename(initialdir="automates/", filetypes=[('Text Files', '*.txt')])
        self.alphabet = []
        self.etats = []
        self.initial = []
        self.terminal = []
        self.transition = {}
        self.lire_automate_sur_fichier(filename)

    def lire_automate_sur_fichier(self, nom_fichier):
        """fonction pour restranscrit un automate dans la classe depuis un fichier"""
        with open(nom_fichier) as automatetxt:
            lines = automatetxt.readlines()
            n = lambda x: int(lines[x][0])
            for i in range(n(0)):
                self.alphabet.append(constantes.ALPHABET[i])
            for i in range(n(1)):
                self.etats.append(str(i))
            for i in range(n(2)):
                self.initial.append(lines[2][2 * (1 + i)])
            for i in range(n(3)):
                self.terminal.append(lines[3][2 * (1 + i)])
            for i in range(int(lines[4][:-1])):
                depart = lines[5 + i][0]
                symbole = lines[5 + i][1]
                arriver = lines[5 + i][2]
                if depart not in self.transition.keys():
                    self.transition[depart] = {}
                self.transition[depart][symbole] = arriver

        print("".join("%s: %s\n" % item for item in vars(self).items()))

    def __str__(self):
        """equivalent to 'afficher_automate' but implement nicely in python"""
        res = ""
        return res

    def ecrire_automate_sur_fichier(self, nom_fichier):
        """fonction pour restranscrit un automate dans un fichier depuis les attributs de cette classe"""
        pass
