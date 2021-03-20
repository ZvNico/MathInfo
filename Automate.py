from tkinter.filedialog import askopenfilename, asksaveasfilename


class Automate:
    def __init__(self):
        filename = askopenfilename(initialdir="automates/", filetypes=[('Text Files', '*.txt')])
        self.lire_automate_sur_fichier(filename)

    def lire_automate_sur_fichier(self, nom_fichier):
        """fonction pour restranscrit un automate depuis un fichier"""
        with open(nom_fichier) as automatetxt:
            for line in automatetxt.readlines():
                print(line, end="")

    def ecrire_automate_sur_fichier(self, nom_fichier):
        """fonction pour restranscrit un automate dans un fichier depuis les attributs de cette classe"""
        pass
