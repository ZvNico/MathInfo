from Automate import Automate
from copy import deepcopy

if __name__ == '__main__':
    automate = Automate()
    print(automate)
    automate.determinisation_et_completion_synchrone()
    automate.ecrire_automate_sur_fichier()
    print(automate)
