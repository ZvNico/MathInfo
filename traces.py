from Automate import Automate


def operation(func):
    fichier.write(f"\n{func.__name__}\n")
    n = len(automate.historique)
    func()
    if len(automate.historique) > n:
        for key, value in automate.historique[-1].items():
            if ' '.join(value) != key:
                fichier.write(f"{' '.join(value)} => {key}\n")
    fichier.write(str(automate))



for i in range(1, 45):
    file = f"automates/A4-{i}.txt"
    with open(f"automates/A4-trace{i}.txt", "w") as fichier:
        try:
            automate = Automate(file)
            fichier.write(str(automate))
            operation(automate.determinisation_et_completion_synchrone)
            operation(automate.minimisation)
            operation(automate.automate_complementaire)
            automate.generer_graphe() #necessite graphviz
        except :
            fichier.write("Erreur")

