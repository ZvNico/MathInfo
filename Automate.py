from graphviz import Digraph
from string import ascii_lowercase
from prettytable import PrettyTable
from utils_display import *


class Automate:
    def __init__(self, filename=None):
        if not filename:
            if not tkinter:
                raise Exception('Both Tkinter and File are not provided')
            filename = askopenfilename(initialdir="automates/", filetypes=[('Text Files', '*.txt')])
        self.filename = filename
        self.alphabet = []
        self.etats = []
        self.initial = []
        self.terminal = []
        self.historique = []
        self.transitions = {}
        self.lire_automate_sur_fichier(self.filename)

    def __str__(self):
        """equivalent à 'afficher_automate' mais implementer joliment en python, affiche l'automate"""
        asynchrone = self.est_un_automate_asynchrone()
        if asynchrone:
            self.alphabet.insert(0, "*")
        tab = PrettyTable()
        tab.field_names = [""] + [i for i in self.alphabet]
        x = [[" " for i in range(len(self.alphabet) + 1)] for j in range(len(self.transitions))]
        for i, depart in enumerate(self.transitions):
            x[i][0] = ""
            if depart in self.initial:
                x[i][0] += "E"
            if depart in self.terminal:
                x[i][0] += "S"
            if x[i][0]:
                x[i][0] += " - "
            x[i][0] += depart
            for symbole, arriver in self.transitions[depart].items():
                if isinstance(arriver, list):
                    x[i][self.alphabet.index(symbole) + 1] = ".".join(arriver)
                else:
                    x[i][self.alphabet.index(symbole) + 1] = arriver
        tab.add_rows(x)
        if asynchrone:
            self.alphabet.pop(0)
        return str(tab)

    def lire_automate_sur_fichier(self, nom_fichier):
        """fonction pour restranscrit un automate dans la classe depuis un fichier"""
        with open(nom_fichier) as automatetxt:
            lines = automatetxt.readlines()
            n0 = lambda x: int(lines[x][0])
            n = lambda x: int(lines[x])
            for i in range(n(0)):
                self.alphabet.append(ascii_lowercase[i])
            for i in range(n(1)):
                self.etats.append(str(i))
            for i in range(n0(2)):
                self.initial.append(lines[2][2 * (1 + i)])
            for i in range(n0(3)):
                self.terminal.append(lines[3][2 * (1 + i)])
            for i in range(n(4)):
                depart = lines[5 + i][0]
                symbole = lines[5 + i][1]
                arrive = lines[5 + i][2]
                self.ajouter_transition(depart, symbole, arrive)

    def ecrire_automate_sur_fichier(self):
        """fonction pour retranscrire un automate dans un fichier depuis les attributs de cette classe"""
        i = 1
        while self.filename[-i] != "-":
            i += 1
        filename = self.filename[:-i + 1] + 'trace' + self.filename[-i + 1:]
        automate_w = open(filename, 'w')
        automate_w.write(str(len(self.alphabet)))
        automate_w.write('\n')
        automate_w.write(str(len(self.initial) + len(self.terminal) + 1))
        automate_w.write('\n')
        automate_w.write(str(len(self.initial)) + " ")
        for i in range(len(self.initial)):
            automate_w.write(str(self.initial[i]) + " ")
        automate_w.write('\n')
        automate_w.write(str(len(self.terminal)) + " ")
        for i in range(len(self.terminal)):
            automate_w.write(str(self.terminal[i]) + " ")
        automate_w.write('\n')
        somme_len_transitions = 0
        for elem_a in self.transitions.items():
            for elem_b in elem_a[1].items():
                somme_len_transitions += len(elem_b[1])
        automate_w.write(str(somme_len_transitions))
        automate_w.write('\n')

        for elem_a in self.transitions.items():
            for elem_b in elem_a[1].items():
                for elem_c in elem_b[1]:
                    automate_w.write(str(elem_a[0]))
                    automate_w.write(str(elem_b[0]))
                    automate_w.write(str(elem_c))
                    automate_w.write('\n')
        automate_w.close()

    def generer_graphe(self):
        """génération de graph, nécessite graphviz"""
        if not tkinter:
            f = Digraph(filename=f"graphes/{self.filename.split('/')[-1].replace('.txt', '.gv')}")
        else:
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

    def reconnaitre_mot(self, mot):
        """reconnaissance de mot pour automate deterministe"""
        if self.est_un_automate_deterministe():
            pos = self.initial[0]
            for lettre in mot:
                try:
                    pos = self.transitions[pos][lettre]
                except:
                    break
            return pos in self.terminal
        else:
            print_or_tk("Erreur ... l'automate n'est pas deterministe", "ERROR")

    def run(self):
        mot = askstring_or_tk(f'Saisissez un mot ("fin" pour arrêter)\nAlphabet:{", ".join(self.alphabet)}')
        while mot != "fin":
            res = self.reconnaitre_mot(mot)
            if res:
                print_or_tk(f"Le mot '{mot}' a été reconnu par l'automate :D", "INFO")
            else:
                print_or_tk(f"Le mot '{mot}' n'a été reconnu par l'automate :/", "INFO")
            mot = askstring_or_tk(f'Saisissez un mot ("fin" pour arrêter)\nAlphabet:{", ".join(self.alphabet)}')

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
        for depart in self.etats:
            if depart not in self.transitions:
                return False
            value = self.transitions[depart]
            transitions = list(value.keys())
            for symbole in self.alphabet:
                if symbole not in transitions:
                    return False
        return True

    def est_un_automate_standart(self):
        if len(self.initial) > 1:
            return False
        for value in self.transitions.values():
            for arriver in value.values():
                if arriver in self.initial:
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
        for depart in self.etats:
            if depart not in self.transitions:
                self.transitions[depart] = {}
            value = self.transitions[depart]
            transitions = list(value.keys())
            for symbole in self.alphabet:
                if symbole not in transitions:
                    complet = False
                    self.ajouter_transition(depart, symbole, 'p')
        if not complet:
            self.transitions['p'] = {symbole: 'p' for symbole in self.alphabet}
            self.etats.append('p')

    def determiniser(self):
        new_transitions = {}
        queue = []
        self.etats = []
        self.historique.append({})
        new_terminal = []
        if len(self.initial) > 1:
            new_initial = "".join(self.initial)
            self.historique[-1][new_initial] = [etat for etat in self.initial]
            self.initial = [new_initial]
        queue.append(self.initial[0])
        while queue:
            depart = queue.pop(0)
            if depart not in self.etats:
                self.etats.append(depart)
            sub_dict = {}
            for etat in depart:
                if etat in self.terminal and etat not in new_terminal:
                    new_terminal.append(depart)
                if etat in self.transitions:
                    for symbole, arriver in self.transitions[etat].items():
                        if isinstance(arriver, list):
                            arriver = "".join(arriver)
                        if symbole in sub_dict.keys():
                            if arriver not in sub_dict[symbole]:
                                sub_dict[symbole] += arriver
                        else:
                            sub_dict[symbole] = arriver
            new_transitions[depart] = sub_dict
            if depart not in self.historique[-1]:
                self.historique[-1][depart] = []
            for arriver in new_transitions[depart].values():
                self.historique[-1][depart].append(arriver)
                if arriver not in new_transitions.keys():
                    queue.append(arriver)

        self.terminal = new_terminal
        self.transitions = new_transitions

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

    def minimisation(self):
        def index_sous_partition(partition, etat):
            for i, sous_partition in enumerate(partition):
                if etat in sous_partition:
                    return i
            raise IndexError

        p = [[etat for etat in self.etats if etat not in self.terminal],
             [etat for etat in self.etats if etat in self.terminal]]

        for sous_partition in p:
            if not sous_partition:
                p.remove(sous_partition)

        minimiser = False
        while not minimiser:
            minimiser = True
            for i, sous_partition in enumerate(p):
                equivalence = {}
                for etat in sous_partition:
                    key = tuple(index_sous_partition(p, self.transitions[etat][symbole]) for symbole in self.alphabet)
                    if key not in equivalence.keys():
                        equivalence[key] = [etat]
                    else:
                        equivalence[key].append(etat)
                if len(equivalence) > 1:
                    minimiser = False
                    keys = list(equivalence.keys())
                    while len(keys) > 1:
                        min = keys[0]
                        for key in keys:
                            if len(equivalence[key]) < len(equivalence[min]):
                                min = key
                        p.append([])
                        for etat in equivalence[min]:
                            sous_partition.remove(etat)
                            p[-1].append(etat)
                        keys.remove(min)
        new_etats = []
        self.historique.append({})

        for sous_partition in p:
            temp = []
            for etat in sous_partition:
                for lettre in etat:
                    if lettre not in temp:
                        temp.append(lettre)
            temp = "".join(temp)
            new_etats.append(temp)
            self.historique[-1][temp] = [etat for etat in sous_partition]

        def find_new_key(old_key):
            for key, value in self.historique[-1].items():
                if old_key in value:
                    return key
            raise KeyError

        new_transitions = {}
        new_terminal = []
        new_initial = []

        for key, value in self.historique[-1].items():
            for old_key in value:
                if old_key in self.initial:
                    new_initial.append(key)
                if old_key in self.terminal:
                    new_terminal.append(key)

        for key, value in self.historique[-1].items():
            new_value = {}
            for symbole, arriver in self.transitions[value[0]].items():
                if arriver not in self.historique[-1]:
                    arriver = find_new_key(arriver)
                new_value[symbole] = arriver
            new_transitions[key] = new_value

        self.terminal = new_terminal
        self.initial = new_initial
        self.etats = new_etats
        self.transitions = new_transitions

    def automate_complementaire(self):
        """transformation de l'automate deterministe complet pour que celui ci reconnaisse le langage complémentaire à celui actuel"""
        self.terminal = [etat for etat in self.etats if etat not in self.terminal]

    def automate_standard(self):
        """transformation de l'automate en automate standart"""
        if len(self.initial) > 1:
            new_transitions = {}
            self.historique.append({})
            queue = []
            self.etats = []
            new_terminal = []
            if len(self.initial) > 1:
                new_initial = "".join(self.initial)
                self.historique[-1][new_initial] = [etat for etat in self.initial]
                self.initial = [new_initial]
            queue.append(self.initial[0])
            while queue:
                depart = queue.pop(0)
                if depart not in self.etats:
                    self.etats.append(depart)
                sub_dict = {}
                for etat in depart:
                    if etat in self.terminal and etat not in new_terminal:
                        new_terminal.append(depart)
                    if etat in self.transitions:
                        for symbole, arriver in self.transitions[etat].items():
                            if isinstance(arriver, list):
                                if symbole in sub_dict.keys():
                                    sub_dict[symbole] = [elt for elt in sub_dict[symbole]]
                                    sub_dict[symbole].extend(arriver)
                                else:
                                    sub_dict[symbole] = arriver
                            else:
                                if symbole in sub_dict.keys():
                                    if arriver not in sub_dict[symbole]:
                                        sub_dict[symbole] += arriver
                                else:
                                    sub_dict[symbole] = arriver
                new_transitions[depart] = sub_dict
                if depart not in self.historique[-1]:
                    self.historique[-1][depart] = []
                for arriver in new_transitions[depart].values():
                    if isinstance(arriver, list):
                        for etat in arriver:
                            self.historique[-1][depart].append(etat)
                            if etat not in new_transitions.keys():
                                queue.append(etat)
                    else:
                        if arriver not in new_transitions.keys():
                            self.historique[-1][depart].append(arriver)
                            queue.append(arriver)
            self.terminal = new_terminal
            self.transitions = new_transitions
        if not self.est_un_automate_standart():
            self.transitions['i'] = self.transitions[self.initial[0]].copy()
            if self.initial[0] in self.terminal:
                self.terminal.append('i')
            self.initial = ['i']
