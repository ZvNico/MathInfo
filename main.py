from Automate import *

if __name__ == '__main__':
    input = ""
    while input != "O":
        automate = Automate()
        try:
            print(automate)
            print("==determinisation et completion==")
            automate.determinisation_et_completion_synchrone()
            print(automate)
            print("==minimisation==")
            automate.minimisation()
            print(automate)
            print("==complémentarisation==")
            automate.automate_complementaire()
        except:
            print(f"Erreur sur le fichier {automate.filename}")
        input = askstring_or_tk("Voulez vous arrêtez ? (O)ui (*)Non")
