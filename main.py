from Automate import Automate
from copy import deepcopy
from utils_display import askstring_or_tk

if __name__ == '__main__':
    for i in range(1, 44):
        file = f"automates/A4-{i}.txt"
        automate = Automate(file)
        print("==standardisation==")
        automate.automate_standard()
        print("==determinisation et completion==")
        automate.determinisation_et_completion_synchrone()
        print("==minimisation==")
        automate.minimisation()
        print("==complémentarisation==")
        automate.automate_complementaire()
        automate.ecrire_automate_sur_fichier()
        automate.generer_graphe()
