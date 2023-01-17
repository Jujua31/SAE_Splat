# coding: utf-8
import argparse
import random
import client
import const
import plateau
import case
import joueur

def mon_IA(ma_couleur,carac_jeu, plan, les_joueurs):
    def mur_autour_joueur(plan, ma_couleur, les_joueurs):
        """ Cette fonction permet de savoir dans quelle direction le joueurs peut aller en fonction des murs
        Args:
            plan (str): le plan du plateau comme comme indiqué dans le sujet
        Returns:
            list: une liste de direction où le joueur peut aller
        """
        liste_joueurs = joueur.joueur_from_str(les_joueurs)
        print(liste_joueurs)
        liste_couleur = []
        for i in liste_joueurs.keys():
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
        """ Cette fonction permet d'obtenir la liste d'index des positions des cases vides)
        Args:
            plan (str): le plan du plateau comme indiqué dans le sujet
            pos (tuple): la position du joueur
            direction (str): la direction où on veut regarder
        Returns:
            list: une liste d'index des cases étant incolore
        """
        distance_max = 5
        case_vides = []
        pos2 = pos
        INC_DIRECTION = {'N': (-1, 0), 'E': (0, 1), 'S': (1, 0), 'O': (0, -1), 'X': (0, 0)}
        for index in range(distance_max):
            if plateau.est_sur_plateau(plan,pos2) and not plan["cases"][pos2]["mur"]:
                if plan["cases"][pos2]['couleur'] == ' ':
                    case_vides.append(index+1)
            pos2 = (pos2[0] + INC_DIRECTION[direction][0], pos2[1] + INC_DIRECTION[direction][1])
        return case_vides

    def case_peinte_autre_joueurs_direction(plan,pos,direction):
        """ Cette fonction permet d'obtenir la liste d'index des positions des cases peintes par des autres joueur)
        Args:
            plan (str): le plan du plateau comme indiqué dans le sujet
            pos (tuple): la position du joueur
            direction (str): la direction où on veut regarder
        Returns:
            list: une liste d'index des cases étant peintes par des joueurs autres que nous même
        """
        distance_max = 5
        case_joueurs = []
        pos2 = pos
        INC_DIRECTION = {'N': (-1, 0), 'E': (0, 1), 'S': (1, 0), 'O': (0, -1), 'X': (0, 0)}
        for index in range(distance_max):
            if plateau.est_sur_plateau(plan,pos2) and not plan["cases"][pos2]["mur"]:
                if plan["cases"][pos2]['couleur'] != ' ':
                    if plan["cases"][pos2]['couleur'] != ma_couleur:
                        case_joueurs.append(index+1)
            pos2 = (pos2[0] + INC_DIRECTION[direction][0], pos2[1] + INC_DIRECTION[direction][1])
        return case_joueurs

    def nb_cases_possibles_a_peindre_direction(plan,pos,reserve,direction):
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
        case_vide = case_peinte_autre_joueurs_direction(plan,pos,direction)
        case_peinte_autre_joueurs = case_peinte_autre_joueurs_direction(plan,pos,direction)
        for i in range(1,6):
            if i in case_vide:
                if reserve >= 1:
                    reserve -= 1
                    nombre_case = 1+i
            elif i in case_peinte_autre_joueurs:
                if reserve >= 2:
                    reserve -= 2
                    nombre_case = 1+i
        return nombre_case

    def dico_reserve(plan,les_joueurs):
        pass

    def joueurs_plus_proche():
        pass

    def direction():
        pass

    def get_coords_objets():
        pass

    """ Cette fonction permet de calculer les deux actions du joueur de couleur ma_couleur
        en fonction de l'état du jeu décrit par les paramètres. 
        Le premier caractère est parmi XSNOE X indique pas de peinture et les autres
        caractères indique la direction où peindre (Nord, Sud, Est ou Ouest)
        Le deuxième caractère est parmi SNOE indiquant la direction où se déplacer.

    Args:
        ma_couleur (str): un caractère en majuscule indiquant la couleur du jeur
        carac_jeu (str): une chaine de caractères contenant les caractéristiques
                                de la partie séparées par des ;
            duree_act;duree_tot;reserve_init;duree_obj;penalite;bonus_touche;bonus_rechar;bonus_objet           
        plan (str): le plan du plateau comme comme indiqué dans le sujet
        les_joueurs (str): le liste des joueurs avec leur caractéristique (1 joueur par ligne)
        couleur;reserve;nb_cases_peintes;objet;duree_objet;ligne;colonne;nom_complet
    
    Returns:
        str: une chaine de deux caractères en majuscules indiquant la direction de peinture
            et la direction de déplacement
    """
    # IA complètement légitime et très forte (et extrêmement recherchée)
    direction_mouvement = str(random.choice("NSEO"))
    direction_mouvement = str(random.choice(mur_autour_joueur(plan,ma_couleur,les_joueurs)))
    best_nb_case = 0
    best_direction = 'X'
    for direction_test in "NSEO":
        if nb_cases_possibles_a_peindre_direction(plan,joueur.get_pos(ma_couleur),joueur.get_reserve(ma_couleur),direction_test) > best_nb_case:
            best_nb_case = nb_cases_possibles_a_peindre_direction(plan,joueur.get_pos(ma_couleur),joueur.get_reserve(ma_couleur),direction_test)
            best_direction = direction_test
    return best_direction + direction_mouvement

if __name__=="__main__":
    parser = argparse.ArgumentParser()  
    parser.add_argument("--equipe", dest="nom_equipe", help="nom de l'équipe", type=str, default='Non fournie')
    parser.add_argument("--serveur", dest="serveur", help="serveur de jeu", type=str, default='localhost')
    parser.add_argument("--port", dest="port", help="port de connexion", type=int, default=1111)
    
    args = parser.parse_args()
    le_client=client.ClientCyber()
    le_client.creer_socket(args.serveur,args.port)
    le_client.enregistrement(args.nom_equipe,"joueur")
    ok=True
    while ok:
        ok,id_joueur,le_jeu=le_client.prochaine_commande()
        if ok:
            carac_jeu,le_plateau,les_joueurs=le_jeu.split("--------------------\n")
            actions_joueur=mon_IA(id_joueur,carac_jeu,le_plateau,les_joueurs[:-1])
            le_client.envoyer_commande_client(actions_joueur)
            # le_client.afficher_msg("sa reponse  envoyée "+str(id_joueur)+args.nom_equipe)
    le_client.afficher_msg("terminé")
