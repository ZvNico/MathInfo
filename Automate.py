from tkinter.filedialog import askopenfilename, asksaveasfilename
from graphviz import Digraph
from string import ascii_lowercase
from prettytable import PrettyTable


class Automate:
    def __init__(self):
        filename = askopenfilename(initialdir="automates/", filetypes=[('Text Files', '*.txt')])
        self.alphabet = []
        self.etats = []
        self.initial = []
        self.terminal = []
        self.transitions = {}
        self.lire_automate_sur_fichier(filename)

    def lire_automate_sur_fichier(self, nom_fichier):
        """fonction pour restranscrit un automate dans la classe depuis un fichier"""
        with open(nom_fichier) as automatetxt:
            lines = automatetxt.readlines()
            n = lambda x: int(lines[x][0])
            for i in range(n(0)):
                self.alphabet.append(ascii_lowercase[i])
            for i in range(n(1)):
                self.etats.append(str(i))
            for i in range(n(2)):
                self.initial.append(lines[2][2 * (1 + i)])
            for i in range(n(3)):
                self.terminal.append(lines[3][2 * (1 + i)])
            for i in range(int(lines[4])):
                depart = lines[5 + i][0]
                symbole = lines[5 + i][1]
                arrive = lines[5 + i][2]
                self.ajouter_transition(depart, symbole, arrive)

    def __str__(self):
        """equivalent à 'afficher_automate' mais implementer joliment en python, affiche l'automate"""
        res = "".join("%s: %s\n" % item for item in vars(self).items())
        # TODO le tableau ne prend pas encore les automates asynchrones
        if not self.est_un_automate_asynchrone():
            tab = PrettyTable()
            tab.field_names = [""] + [i for i in self.alphabet]
            x = [[" " for i in range(len(self.alphabet) + 1)] for j in range(len(self.transitions))]
            for i, depart in enumerate(self.transitions):
                x[i][0] = depart
                for symbole, arriver in self.transitions[depart].items():
                    if isinstance(arriver, list):
                        x[i][self.alphabet.index(symbole) + 1] = ",".join(arriver)
                    else:
                        x[i][self.alphabet.index(symbole) + 1] = arriver
            tab.add_rows(x)
            res += str(tab)
        return res

    def ajouter_transition(self, depart, symbole, arriver):
        if depart not in self.transitions:
            self.transitions[depart] = {}

        if symbole not in self.transitions[depart]:
            self.transitions[depart][symbole] = arriver
        elif isinstance(self.transitions[depart][symbole], list):
            self.transitions[depart][symbole].append(arriver)
        else:
            self.transitions[depart][symbole] = [self.transitions[depart][symbole], arriver]

    def est_un_automate_asynchrone(self):
        """Vérifie si un automate est asynchrone ou non"""
        for depart in self.transitions:
            for key in self.transitions[depart].keys():
                if key == "*":
                    return True
        return False

    def est_un_automate_deterministe(self):
        if len(self.initial) > 1:
            return False
        for value in self.transitions.values():
            for arriver in value.values():
                if isinstance(arriver, list):
                    return False
        return True

    def est_un_automate_complet(self):
        for value in self.transitions.values():
            transitions = list(value.keys())
            for symbole in self.alphabet:
                if symbole not in transitions:
                    return False
        return True

    def elimination_epsilon(self):
        """"""
        supprimer = []
        chercher_depuis_etat_a = lambda etat_a: [(key1, key2) for key1, value1 in self.transitions.items() for
                                                 key2, value2 in value1.items() if key2 == etat_a]
        for depart, value in self.transitions.items():
            for symbole in value.keys():
                if symbole == "*":
                    fermeture_epsilon = value[symbole]
                    supprimer.append(depart)
                    for depart, transition2 in chercher_depuis_etat_a(fermeture_epsilon):
                        self.ajouter_transition(depart, symbole, fermeture_epsilon)
        for etat in supprimer:
            del self.transitions[etat]['*']

    def completion(self):
        """Construction  de  l’automate  déterministe  et  complet  à  partir  de  l’automate synchrone et déterministe AF"""
        complet = True
        for depart, value in self.transitions.items():
            transitions = list(value.keys())
            for symbole in self.alphabet:
                if symbole not in transitions:
                    complet = False
                    self.ajouter_transition(depart, symbole, 'p')
        if not complet:
            self.transitions['p'] = {symbole: 'p' for symbole in self.alphabet}
            self.etats.append('p')

    def determiniser(self):
        new_dict = {}
        queue = []
        self.etats = []
        if len(self.initial) > 1:
            self.initial = ["".join(self.initial)]
        queue.append(self.initial[0])
        while queue:
            depart = queue.pop(0)
            sub_dict = {}
            for etat in depart:
                for symbole, arriver in self.transitions[etat].items():
                    if isinstance(arriver, list):
                        arriver = "".join(arriver)
                    if symbole in sub_dict.keys():
                        sub_dict[symbole] += arriver
                    else:
                        sub_dict[symbole] = arriver
            new_dict[depart] = sub_dict
            for arriver in new_dict[depart].values():
                if arriver not in new_dict.keys():
                    queue.append(arriver)

        self.transitions = new_dict

    def determinisation_et_completion_asynchrone(self):
        if self.est_un_automate_asynchrone():
            self.elimination_epsilon()
        self.determinisation_et_completion_synchrone()

    def determinisation_et_completion_synchrone(self):
        if self.est_un_automate_asynchrone():
            self.determinisation_et_completion_asynchrone()
        else:
            if self.est_un_automate_deterministe():
                if not self.est_un_automate_complet():
                    self.completion()
            else:
                self.determiniser()
                self.completion()
        print(self)

    def ecrire_automate_sur_fichier(self, nom_fichier):
        """fonction pour retranscrire un automate dans un fichier depuis les attributs de cette classe"""
        pass

    def generer_graphe(self):
        """génération de graph, nécessite graphviz"""
        f = Digraph(filename=asksaveasfilename(initialdir="graphes/", filetypes=[('Graphviz Files', '*.gv')]))
        f.attr(rankdir="LR")
        for depart, value in self.transitions.items():
            if depart in self.initial:
                f.node(depart, color="blue")
            elif depart in self.terminal:
                f.node(depart, color="red")
            else:
                f.node(depart)

            for symbole, arriver in value.items():
                if isinstance(arriver, list):
                    for etat in arriver:
                        f.edge(depart, etat, label=symbole)
                else:
                    f.edge(depart, arriver, label=symbole)
        f.render()
