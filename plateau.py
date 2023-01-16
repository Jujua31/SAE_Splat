"""module de gestion du plateau de jeu
"""
import const
import case


# dictionnaire permettant d'associer une direction et la position relative
# de la case qui se trouve dans cette direction
INC_DIRECTION = {'N': (-1, 0), 'E': (0, 1), 'S': (1, 0),
                 'O': (0, -1), 'X': (0, 0)}


def get_nb_lignes(plateau):
    """retourne le nombre de lignes du plateau

    Args:
        plateau (dict): le plateau considéré

    Returns:
        int: le nombre de lignes du plateau
    """
    return plateau["nb_lignes"]


def get_nb_colonnes(plateau):
    """retourne le nombre de colonnes du plateau

    Args:
        plateau (dict): le plateau considéré

    Returns:
        int: le nombre de colonnes du plateau
    """
    return plateau["nb_colonnes"]


def get_case(plateau, pos):
    """retourne la case qui se trouve à la position pos du plateau

    Args:
        plateau (dict): le plateau considéré
        pos (tuple): une paire (lig,col) de deux int

    Returns:
        dict: La case qui se situe à la position pos du plateau
    """
    return plateau["cases"][pos]


def poser_joueur(plateau, joueur, pos):
    """pose un joueur en position pos sur le plateau

    Args:
        plateau (dict): le plateau considéré
        joueur (str): la lettre représentant le joueur
        pos (tuple): une paire (lig,col) de deux int
    """
    plateau["cases"][pos]["joueurs_presents"] = joueur
    return plateau


def poser_objet(plateau, objet, pos):
    """Pose un objet en position pos sur le plateau. Si cette case contenait déjà
        un objet ce dernier disparait

    Args:
        plateau (dict): le plateau considéré
        objet (int): un entier représentant l'objet. const.AUCUN indique aucun objet
        pos (tuple): une paire (lig,col) de deux int
    """
    plateau["cases"][pos]["objet"] = int(objet)
    return plateau


def plateau_from_str(la_chaine):
    """Construit un plateau à partir d'une chaine de caractère contenant les informations
        sur le contenu du plateau (voir sujet)

    Args:
        la_chaine (str): la chaine de caractères décrivant le plateau

    Returns:
        dict: le plateau correspondant à la chaine. None si l'opération a échoué
    """
    ...

def Plateau(plan):
    """Créer un plateau en respectant le plan donné en paramètre.
        Le plan est une chaine de caractères contenant
            '#' (mur)
            ' ' (couloir non peint)
            une lettre majuscule (un couloir peint par le joueur représenté par la lettre)

    Args:
        plan (str): le plan sous la forme d'une chaine de caractères

    Returns:
        dict: Le plateau correspondant au plan
    """
    plateau = {}

    les_lignes = plan.split("\n")
    [nb_lignes, nb_colonnes] = les_lignes[0].split(";")
    nb_lignes = int(nb_lignes)
    nb_colonnes = int(nb_colonnes)
    plateau["nb_lignes"] = nb_lignes
    plateau["nb_colonnes"] = nb_colonnes
    plateau["cases"] = {}
    for lig in range(nb_lignes):
        for col in range(nb_colonnes):
            if les_lignes[lig + 1][col] == '#':
                plateau["cases"][(lig, col)] = case.Case(True, ' ')
            elif les_lignes[lig + 1][col] == ' ':
                plateau["cases"][(lig, col)] = case.Case(False, ' ')
            else:
                if not les_lignes[lig + 1][col].isupper():
                    plateau["cases"][(lig, col)] = case.Case(True, les_lignes[lig + 1][col])
                else:
                    plateau["cases"][(lig, col)] = case.Case(False, les_lignes[lig + 1][col])

    debut_def_joueur = nb_lignes + 2
    fin_def_joueur = nb_lignes+int(les_lignes[nb_lignes+1])+2
    for lig in les_lignes[debut_def_joueur:fin_def_joueur]:
        [joueur, ligne, colonne] = lig.split(";")
        pos = (int(ligne), int(colonne))
        poser_joueur(plateau, joueur, pos)

    debut_def_objet = fin_def_joueur + 1
    fin_def_objet = fin_def_joueur + int(les_lignes[fin_def_joueur]) + 1
    for lig in les_lignes[debut_def_objet:fin_def_objet]:
        [objet, ligne, colonne] = lig.split(";")
        pos = (int(ligne), int(colonne))
        poser_objet(plateau, objet, pos)

    return plateau


def set_case(plateau, pos, une_case):
    """remplace la case qui se trouve en position pos du plateau par une_case

    Args:
        plateau (dict): le plateau considéré
        pos (tuple): une paire (lig,col) de deux int
        une_case (dict): la nouvelle case
    """
    plateau["cases"][pos] = une_case
    return plateau


def enlever_joueur(plateau, joueur, pos):
    """enlève un joueur qui se trouve en position pos sur le plateau

    Args:
        plateau (dict): le plateau considéré
        joueur (str): la lettre représentant le joueur
        pos (tuple): une paire (lig,col) de deux int

    Returns:
        bool: True si l'opération s'est bien déroulée, False sinon
    """
    if plateau["cases"][pos]["joueurs_presents"] == joueur:
        plateau["cases"][pos]["joueurs_presents"] = None
        return True
    else:
        return False


def prendre_objet(plateau, pos):
    """Prend l'objet qui se trouve en position pos du plateau et retourne l'entier
        représentant cet objet. const.AUCUN indique qu'aucun objet se trouve sur case

    Args:
        plateau (dict): Le plateau considéré
        pos (tuple): une paire (lig,col) de deux int

    Returns:
        int: l'entier représentant l'objet qui se trouvait sur la case.
        const.AUCUN indique aucun objet
    """
    objet = plateau["cases"][pos]["objet"]
    plateau["cases"][pos]["objet"] = const.AUCUN
    return objet


def deplacer_joueur(plateau, joueur, pos, direction):
    """Déplace dans la direction indiquée un joueur se trouvant en position pos
        sur le plateau

    Args:
        plateau (dict): Le plateau considéré
        joueur (str): La lettre identifiant le joueur à déplacer
        pos (tuple): une paire (lig,col) d'int
        direction (str): une lettre parmie NSEO indiquant la direction du déplacement

    Returns:
        tuple: un tuple contenant 4 informations
            - un bool indiquant si le déplacement a pu se faire ou non
            - un int valeur une des 3 valeurs suivantes:
                *  1 la case d'arrivée est de la couleur du joueur
                *  0 la case d'arrivée n'est pas peinte
                * -1 la case d'arrivée est d'une couleur autre que celle du joueur
            - un int indiquant si un objet se trouvait sur la case d'arrivée (dans ce
                cas l'objet est pris de la case d'arrivée)
            - une paire (lig,col) indiquant la position d'arrivée du joueur (None si
                le joueur n'a pas pu se déplacer)
    """
    def est_sur_plateau(plateau, pos):
        """Indique si une position est sur le plateau

        Args:
            plateau (dict): le plateau considéré
            pos (tuple): une paire (lig,col) de deux int

        Returns:
            bool: True si la position est sur le plateau, False sinon
        """
        if pos[0] < 0 or pos[0] >= plateau["nb_lignes"]:
            return False
        if pos[1] < 0 or pos[1] >= plateau["nb_colonnes"]:
            return False
        return True

    pos = (pos[0]+INC_DIRECTION[direction][0], pos[1]+INC_DIRECTION[direction][1])

    if case.est_mur(plateau["cases"][pos]) or not est_sur_plateau(plateau, pos):
        return False



#-----------------------------
# fonctions d'observation du plateau
#-----------------------------

def surfaces_peintes(plateau, nb_joueurs):
    """retourne un dictionnaire indiquant le nombre de cases peintes pour chaque joueur.

    Args:
        plateau (dict): le plateau considéré
        nb_joueurs (int): le nombre de joueurs total participant à la partie

    Returns:
        dict: un dictionnaire dont les clées sont les identifiants joueurs et les
            valeurs le nombre de cases peintes par le joueur
    """
    cases_peintes = dict()
    joueurs = set()

    for cases in plateau['cases'].values():
        if cases['couleur'] in cases_peintes.keys():
            cases_peintes[cases['couleur']] += 1
        elif cases['couleur'] != ' ':
            cases_peintes[cases['couleur']] = 1    
            
        for joueur in case.get_joueurs(cases):
            joueurs.add(joueur)

    if nb_joueurs != len(cases_peintes.keys()):
        for joueur in joueurs:
            if joueur not in cases_peintes.keys():
                cases_peintes[joueur] = 0        
        
    return cases_peintes                

    
def directions_possibles(plateau,pos):
    """ retourne les directions vers où il est possible de se déplacer à partir
        de la position pos

    Args:
        plateau (dict): le plateau considéré
        pos (tuple): un couple d'entiers (ligne,colonne) indiquant la position de départ
    
    Returns:
        dict: un dictionnaire dont les clés sont les directions possibles et les valeurs la couleur
              de la case d'arrivée si on prend cette direction
              à partir de pos
    """
    ...

    
def nb_joueurs_direction(plateau, pos, direction, distance_max):
    """indique combien de joueurs se trouve à portée sans protection de mur.
        Attention! il faut compter les joueurs qui sont sur la case pos

    Args:
        plateau (dict): le plateau considéré
        pos (_type_): la position à partir de laquelle on fait le recherche
        direction (str): un caractère 'N','O','S','E' indiquant dans quelle direction on regarde
    Returns:
        int: le nombre de joueurs à portée de peinture (ou qui risque de nous peindre)
    """
    counter = 0
    if direction == "N":
        for i in range(distance_max):
            if not case.est_mur((pos[0]-1*(i+1),pos[1])) and not Stop:
                if (pos[0]-1*(i+1),pos[1]) not in case.get_joueurs(pos[0]-1*(i+1),pos[1]):
                    counter += 1
            else:
                Stop = True
    elif direction == "S":
        for i in range(distance_max):
            if not case.est_mur((pos[0]+1*(i+1),pos[1])) and not Stop:
                if (pos[0]+1*(i+1),pos[1]) not in case.get_joueurs(pos[0]+1*(i+1),pos[1]):
                    counter += 1
            else:
                Stop = True
    elif direction == "E":
        for i in range(distance_max):
            if not case.est_mur((pos[0],pos[1]+1*(i+1))) and not Stop:
                if (pos[0],pos[1]+1*(i+1)) not in case.get_joueurs(pos[0],pos[1]+1*(i+1)):
                    counter += 1
            else:
                Stop = True
    elif direction == "O":
        for i in range(distance_max):
            if not case.est_mur((pos[0],pos[1]-1*(i+1))) and not Stop:
                if (pos[0],pos[1]-1*(i+1)) not in case.get_joueurs(pos[0],pos[1]-1*(i+1)):
                    counter += 1
            else:
                Stop = True

    
def peindre(plateau, pos, direction, couleur, reserve, distance_max, peindre_murs=False):
    """ Peint avec la couleur les cases du plateau à partir de la position pos dans
        la direction indiquée en s'arrêtant au premier mur ou au bord du plateau ou
        lorsque que la distance maximum a été atteinte.

    Args:
        plateau (dict): le plateau considéré
        pos (tuple): une paire (lig,col) de int
        direction (str): un des caractères 'N','S','E','O' indiquant la direction de peinture
        couleur (str): une lettre indiquant l'idenfiant du joueur qui peint (couleur de la peinture)
        reserve (int): un entier indiquant la taille de la reserve de peinture du joueur
        distance_max (int): un entier indiquant la portée maximale du pistolet à peinture
        peindre_mur (bool): un booléen indiquant si on peint aussi les murs ou non

    Returns:
        dict: un dictionnaire avec 4 clés
                "cout": un entier indiquant le cout en unités de peinture de l'action
                "nb_repeintes": un entier indiquant le nombre de cases qui ont changé de couleur
                "nb_murs_repeints": un entier indiquant le nombre de murs qui ont changé de couleur
                "joueurs_touches": un ensemble (set) indiquant les joueurs touchés lors de l'action
    """
    ...