# coding: utf-8
import argparse
import random
import client
import const
import plateau
import case
import joueur


def mur_autour_joueur(plan, ma_couleur, les_joueurs):
    """ Cette fonction permet de savoir dans quelle direction le joueurs peut aller en fonction des murs
    Args:
        plan (str): le plan du plateau comme comme indiqué dans le sujet
    Returns:
        list: une liste de direction où le joueur peut aller
    """
    liste_couleur = []
    for i in les_joueurs.keys():
        if i == ["couleur"]:
            liste_couleur.append(i.lower)
    liste_couleur.append("#")
    
    pos = joueur.get_pos(ma_couleur)
    direction_possible = [plan[pos[0]-1][pos[1]], plan[pos[0]+1][pos[1]], plan[pos[0]][pos[1]+1], plan[pos[0]][pos[1]-1]]
    for direction in ["N","S","E","O"]:
        if direction == "N":
            if plan[pos[0]-1][pos[1]] in liste_couleur:
                direction_possible.remove(direction)
        elif direction == "S":
            if plan[pos[0]+1][pos[1]] in liste_couleur:
                direction_possible.remove(direction)
        elif direction == "E":
            if plan[pos[0]][pos[1]+1] in liste_couleur:
                direction_possible.remove(direction)
        elif direction == "O":
            if plan[pos[0]][pos[1]-1] in liste_couleur:
                direction_possible.remove(direction)
    return direction_possible


def case_vide_direction(plan,pos,direction):
    """ Cette fonction permet d'obtenir la liste d'index des positions des cases vides
    Args:
        plan (str): le plan du plateau comme indiqué dans le sujet
        pos (tuple): la position du joueur
        direction (str): la direction où on veut regarder
    Returns:
        list: une liste d'index des cases étant incolore
    """
    distance_max = const.DIST_MAX
    case_vides = []
    pos2 = pos
    INC_DIRECTION = {'N': (-1, 0), 'E': (0, 1), 'S': (1, 0), 'O': (0, -1), 'X': (0, 0)}
    for index in range(distance_max):
        if plateau.est_sur_plateau(plan,pos2) and not plan["cases"][pos2]["mur"]:
            if plan["cases"][pos2]['couleur'] == ' ':
                case_vides.append(index+1)
        pos2 = (pos2[0] + INC_DIRECTION[direction][0], pos2[1] + INC_DIRECTION[direction][1])
    return case_vides

def case_peinte_autre_joueurs_direction(plan,pos,direction,ma_couleur):
    """ Cette fonction permet d'obtenir la liste d'index des positions des cases peintes par des autres joueur)
    Args:n
        plan (str): le plan du plateau comme indiqué dans le sujet
        pos (tuple): la position du joueur
        direction (str): la direction où on veut regarder
    Returns:
        list: une liste d'index des cases étant peintes par des joueurs autres que nous même
    """
    distance_max = const.DIST_MAX
    case_joueurs = []
    pos2 = pos
    INC_DIRECTION = {'N': (-1, 0), 'E': (0, 1), 'S': (1, 0), 'O': (0, -1), 'X': (0, 0)}
    for index in range(distance_max):
        if plateau.est_sur_plateau(plan,pos2) and not plan["cases"][pos2]["mur"]:
            if plan["cases"][pos2]['couleur'] != ' ':
                case_joueurs.append(index+1)
        pos2 = (pos2[0] + INC_DIRECTION[direction][0], pos2[1] + INC_DIRECTION[direction][1])
    return case_joueurs

def nb_cases_possibles_a_peindre_direction(plan,pos,reserve,direction,ma_couleur):
    """ Cette fonction permet d'obtenir le nombre de cases possibles à peindre dans une direction et un nombre de reserve donné
    Args:
        plan (str): le plan du plateau comme indiqué dans le sujet
        pos (tuple): la position du joueur
        reserve (int): le nombre de reserve du joueur
        direction (str): la direction où on veut regarder
    Returns:
        int: le nombre de cases possibles à peindre dans une direction et un nombre de reserve donné
    """
    nombre_case = 0
    case_vide = case_peinte_autre_joueurs_direction(plan,pos,direction,ma_couleur)
    case_peinte_autre_joueurs = case_peinte_autre_joueurs_direction(plan,pos,direction,ma_couleur)
    for i in range(1,6):
        if i in case_vide:
            if reserve >= 1:
                reserve -= 1
                nombre_case = i
        elif i in case_peinte_autre_joueurs:
            if reserve >= 2:
                reserve -= 2
                nombre_case = i
    return nombre_case

def best_direction_shoot(plan,pos,ma_couleur,reserve):
    best_nb = 0
    best_dir = 0
    directions = ["N","S","E","O"]
    for direction in directions:
        if nb_cases_possibles_a_peindre_direction(plan,pos,reserve,direction,ma_couleur) > best_nb:
            best_nb = nb_cases_possibles_a_peindre_direction(plan,pos,reserve,direction,ma_couleur)
            best_dir = dir
    return best_dir

def fabrique_le_calque(le_plateau, pos_depart):
    ''' Fabrique le calque du plateau en utilisant le principe de l'inondation.
    Args:
        le_plateau (dict): le plateau comme indiqué dans le sujet
        pos_depart (tuple): la position de départ du joueur
    Returns:    
        dict: le calque du plateau
    '''
    INC_DIRECTION = {'N': (-1, 0), 'E': (0, 1), 'S': (1, 0), 'O': (0, -1)}
    calque = {}
    calque[pos_depart] = 0
    pile = [pos_depart]
    while pile:
        pos = pile.pop()
        for voisin in plateau.directions_possibles(le_plateau, pos).keys():
            voisin = (pos[0] + INC_DIRECTION[voisin][0], pos[1] + INC_DIRECTION[voisin][1])
            if plateau.est_sur_plateau(le_plateau, voisin) and not le_plateau["cases"][voisin]["mur"] and voisin not in calque.keys():
                calque[voisin] = calque[pos] + 1
                pile.append(voisin)
        #print ("test", pile, pos)
    return calque


def fabrique_chemin(le_plateau,pos_depart,pos_arrivee):
    """Renvoie le plus court chemin entre pos_depart et pos_arrivee
    
    Args:
        le_plateau(dict) : un plateau de jeu
        position_depart (tuple) : un tuple de deux entiers de la forme (no_ligne, no_colonne)
        position_arrivee (tuple) : tuple de deux entiers de la forme (no_ligne,no_colonne)

    Returns:
        list : Une liste de positions entre position_arrivee et position_depart qui représente le plus_court chemin entre les deux positions    
    
    """
    INC_DIRECTION = {'N': (-1, 0), 'E': (0, 1), 'S': (1, 0), 'O': (0, -1)}
    calque = fabrique_le_calque(le_plateau,pos_depart)
    chemin = [pos_arrivee]
    pos = pos_arrivee
    while pos != pos_depart:
        for voisin in plateau.directions_possibles(le_plateau, pos):
            voisin = (pos[0] + INC_DIRECTION[voisin][0], pos[1] + INC_DIRECTION[voisin][1])
            if voisin in calque and calque[voisin] < calque[pos]:
                chemin.append(voisin)
                pos = voisin
                break
    chemin.reverse()
    return chemin


def get_case_vide_plus_proche(plan,pos):
    ''' Trouve la case vide la plus proche de la position pos et renvoie le chemin pour y aller.
    Args:
        plan (dict): le plan du plateau comme indiqué dans le sujet
        pos (tuple): la position du joueur
    Returns:
        list: le chemin pour aller à la case vide la plus proche
    '''
    calque = fabrique_le_calque(plan,pos)
    case_vide = []
    for case in calque:
        if plan["cases"][case]["couleur"] == ' ':
            case_vide.append(case)
    case_vide_plus_proche = case_vide[0]
    for case in case_vide:
        if calque[case] < calque[case_vide_plus_proche]:
            case_vide_plus_proche = case
    return fabrique_chemin(plan,pos,case_vide_plus_proche)


def get_case_autre_couleur_plus_proche(plan,pos,ma_couleur):
    ''' Trouve la case d'une couleur différente de notre couleur la plus proche de la position pos et renvoie le chemin pour y aller.
    Args:
        plan (dict): le plan du plateau comme indiqué dans le sujet
        pos (tuple): la position du joueur
    Returns:
        list: le chemin pour aller à la case vide la plus proche
    '''
    calque = fabrique_le_calque(plan,pos)
    case_autre_couleur = []
    for case in calque.keys():
        if plan["cases"][case]["couleur"] != ma_couleur:
            case_autre_couleur.append(case)
    if case_autre_couleur == []:
        return None
    case_vide_plus_proche = case_autre_couleur[0]
    for case in case_autre_couleur:
        if calque[case] < calque[case_vide_plus_proche]:
            case_vide_plus_proche = case
    return fabrique_chemin(plan,pos,case_vide_plus_proche)


def get_ma_couleur_plus_proche(plan,pos,ma_couleur):
    ''' Trouve la case de notre couleur la plus proche de la position pos et renvoie le chemin pour y aller.
    Args:
        plan (dict): le plan du plateau comme indiqué dans le sujet
        pos (tuple): la position du joueur
    Returns:
        list: le chemin pour aller à la case vide la plus proche
    '''
    calque = fabrique_le_calque(plan,pos)
    case_autre_couleur = []
    for case in calque.keys():
        if plan["cases"][case]["couleur"] == ma_couleur:
            case_autre_couleur.append(case)
    if case_autre_couleur == []:
        return None
    case_vide_plus_proche = case_autre_couleur[0]
    for case in case_autre_couleur:
        if calque[case] < calque[case_vide_plus_proche]:
            case_vide_plus_proche = case
    return fabrique_chemin(plan,pos,case_vide_plus_proche)


def get_case_objet_plus_proche_donne(plan, pos, objet):
    ''' Trouve la case avec l'objet le plus proche de la position pos et renvoie le chemin pour y aller.
    Args:
        plan (dict): le plan du plateau comme indiqué dans le sujet
        pos (tuple): la position du joueur
        objet (int): l'objet que l'on veut trouver
    Returns:
        list: le chemin pour aller à la case avec l'objet le plus proche
    '''
    calque = fabrique_le_calque(plan,pos)
    case_objet = []
    for case in calque.keys():
        if plan["cases"][case]["objet"] == objet:
            case_objet.append(case)
    if case_objet == []:
        return None
    case_objet_plus_proche = case_objet[0]
    for case in case_objet:
        if calque[case] < calque[case_objet_plus_proche]:
            case_objet_plus_proche = case
    return fabrique_chemin(plan,pos,case_objet_plus_proche)

def direction (pos1,pos2):
    ''' Renvoie la direction à prendre pour aller de pos1 à pos2 si pos1 est à côté de pos2.
    Args:
        pos1 (tuple): la position de départ
        pos2 (tuple): la position d'arrivée
    Returns:
        str: la direction à prendre
    '''
    if pos1[0] == pos2[0]:
        if pos1[1] < pos2[1]:
            return "E"
        else:
            return "O"
    else:
        if pos1[0] < pos2[0]:
            return "S"
        else:
            return "N"
        
def aligne_pos_avec_direction(plan, pos1, pos2):
    """"Renvoie un bouléen qui indique si pos1 et pos2 sont alignés et si oui dans quelle direction.
    Args:
        plan (dict): le plan du plateau comme indiqué dans le sujet
        pos1 (tuple): la position de départ
        pos2 (tuple): la position d'arrivée
    Returns:
        bool: True si pos1 et pos2 sont alignés, False sinon
        str: la direction dans laquelle pos1 et pos2 sont alignés
    """
    if pos1[0] == pos2[0]:
        if pos1[1] < pos2[1]:
            direction = "E"
        else:
            direction = "O"
        for i in range(pos1[1]+1,pos2[1]):
            if plan["cases"][(pos1[0],i)]["couleur"] != ' ':
                return False, None
        return True, direction
    elif pos1[1] == pos2[1]:
        if pos1[0] < pos2[0]:
            direction = "S"
        else:
            direction = "N"
        for i in range(pos1[0]+1,pos2[0]):
            if plan["cases"][(i,pos1[1])]["couleur"] != ' ':
                return False, None
        return True, direction
    else:
        return False, None


def possible_a_peindre(plan, pos, ma_couleur, direction, reserve):
    """Renvoie un bouléen qui indique si on peut peindre dans la direction donnée avec une distance maximal(reserve).
    Args:
        plan (dict): le plan du plateau comme indiqué dans le sujet
        pos (tuple): la position de départ
        ma_couleur (str): la couleur du joueur
        direction (str): la direction dans laquelle on veut peindre
        reserve (int): la distance maximal que l'on peut peindre
    Returns:
        bool: True si on peut peindre dans la direction donnée avec une distance maximal(reserve), False sinon
    """
    INC_DIRECTION = {'N': (-1, 0), 'E': (0, 1), 'S': (1, 0), 'O': (0, -1), 'X': (0, 0)}
    reserve = nb_cases_possibles_a_peindre_direction(plan,pos,reserve,direction,ma_couleur)
    for i in range(1,reserve+1):
        pos = (pos[0] + INC_DIRECTION[direction][0], pos[1] + INC_DIRECTION[direction][1])
        if plateau.est_sur_plateau(plan,pos) and plan["cases"][(pos)]["couleur"] != ma_couleur and not plan["cases"][pos]["mur"]:
            return True
    return False


def test_calque():
    with open("plans/plan1.txt") as fic:
            plan1 = fic.read()
    le_plateau = plateau.Plateau(plan1)
    # placer l'objer 4 dans la case (1,2)
    le_plateau["cases"][(2,3)]["objet"] = 4
    print(le_plateau["cases"][(3,3)]["couleur"])
    print(get_case_objet_plus_proche_donne(le_plateau,(0,1),const.BIDON))
    print(direction((1,1),(1,0)))
test_calque()