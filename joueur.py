"""Module de gestion des joueurs
"""
import const


def Joueur(couleur, nom, reserve, surface, position, objet, duree_objet):
    """Créer un nouveau joueur à partir de ses caractéristiques

    Args:
        couleur (str): une lettre majuscule indiquant la couleur du joueur
        nom (str): un nom de joueur
        reserve (int): un entier qui indique la réserve de peinture du joueur
        surface (int): un entier inquant le nombre de cases peintes par le joueur
        position (tuple): une pair d'entier indiquant sur quelle case se trouve le joueur
        objet (int): un entier indiquant l'objet posédé par le joueur (case.AUCUN si pas d'objet)
        duree_objet (int): un entier qui indique pour combier de temps le joueur a l'objet

    Returns:
        dict: un dictionnaire représentant le joueur
    """
    joueur_dict = {'couleur':couleur,'nom_joueur':nom,'reserve':reserve,'surface':surface,'position':position,'objet':objet,'duree_objet':duree_objet}
    return joueur_dict
   
    

    
def joueur_from_str(description):
    """créer un joueur à partir d'un chaine de caractères qui contient
        ses caractéristiques séparées par des ; dans l'ordre suivant:
        "couleur;reserve;surface;objet;duree_objet;lin;col;nom_joueur"

    Args:
        description (str): la chaine de caractères contenant les caractéristiques
                            du joueur

    Returns:
        dict: le joueur ayant les caractéristiques décrite dans la chaine.
    """
    liste = description.split(";")
    res = {"couleur": liste[0], "reserve": int(liste[1]), "surface": int(liste[2]), "objet": int(liste[3]),"duree_objet": int(liste[4]),"position": (int(liste[5]),int(liste[6])),"nom_joueur": liste[7]}
    return res

def get_couleur(joueur):
    """retourne la couleur du joueur

    Args:
        joueur (dict): le joueur considéré

    Returns:
        str: une lettre indiquant la couleur du joueur
    """
    return joueur['couleur']


def get_nom(joueur):
    """retourne le nom du joueur

    Args:
        joueur (dict): le joueur considéré

    Returns:
        str: le nom du joueur
    """
    return joueur['nom_joueur']


def get_reserve(joueur):
    """retourne la valeur de la réserve du joueur
    joueur (dict): le joueur considéré

    Returns:
        int: la réserve du joueur
    """
    return joueur['reserve']


def get_surface(joueur):
    """retourne le nombre de cases peintes par le joueur
        Attention on ne calcule pas ce nombre on retourne juste la valeur
        stockée dans le joueur
    joueur (dict): le joueur considéré

    Returns:
        int: le nombre de cases peintes du joueur
    """
    return joueur['surface']


def get_objet(joueur):
    """retourne l'objet possédé par le joueur (case.AUCUN pour aucun objet)
    joueur (dict): le joueur considéré

    Returns:
        int: un entier indiquant l'objet possédé par le joueur
    """
    return joueur['objet']
    

def get_duree(joueur):
    """retourne la duree de vie de l'objet possédé par le joueur
    joueur (dict): le joueur considéré

    Returns:
        int: un entier indiquant la durée de vie l'objet possédé par le joueur
    """
    return joueur['duree_objet']

    
def get_pos(joueur):
    """retourne la position du joueur. ATTENTION c'est la position stockée dans le
        joueur. On ne la calcule pas
    joueur (dict): le joueur considéré

    Returns:
        tuple: une paire d'entiers indiquant la position du joueur.
    """
    return joueur['position']


def set_pos(joueur, pos):
    """met à jour la position du joueur

    Args:
        joueur (dict): le joueur considéré
        pos (tuple): une paire d'entier (lin,col) indiquant la position du joueur
    """
    joueur['position'] = pos
    return


def modifie_reserve(joueur, quantite):
    """ modifie la réserve du joueur.
        ATTENTION! La quantité peut être négative et la réserve peut devenir négative

    Args:
        joueur (dict): le joueur considéré
        quantite (int)): un entier positif ou négatif inquant la variation de la réserve

    Returns:
        int: la nouvelle valeur de la réserve
    """
    joueur['reserve'] = quantite
    return

def set_surface(joueur, surface):
    """met à jour la surface du joueur

    Args:
        joueur (dict): le joueur considéré
        surface (int): la nouvelle valeur de la surface
    """
    joueur['surface'] = surface
    return


def ajouter_objet(joueur, objet, duree):
    """ajoute un objet au joueur (celui-ci ne peut en avoir qu'un à la fois).
        Si l'objet est const.BIDON on change pas l'objet mais on remet à 0 la
        réserve du joueur si celle ci est négative
    Args:
        joueur (dict): le joueur considéré
        objet (int): l'objet considéré
        duree (int): la durée de vie de l'objet
    """
    if objet == const.BIDON:
        if get_reserve(joueur) < 0:
            joueur["reserve"] = 0
    else:
        joueur['objet'] = objet
        joueur['duree_objet'] = duree

    
def maj_duree(joueur):
    """décrémente la durée de vie de l'objet du joueur (si celui-ci en a un).
        Si la durée arrive à 0 l'objet disparait

    Args:
        joueur (dict): le joueur considéré
    """
    ...