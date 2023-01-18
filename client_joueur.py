# coding: utf-8
import argparse
import random
import client
import const
import plateau
import case
import joueur
import fonction_IA as IA

def mon_IA(ma_couleur,carac_jeu, plan, les_joueurs):
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
    le_plan = plateau.Plateau(plan)
    les_joueurs = les_joueurs.split("\n")
    joueur_str = dict()
    for joueur2 in les_joueurs:  
        joueur_str[joueur2[0]] = joueur.joueur_from_str(joueur2)
    caracteristique = carac_jeu.split(";")
    caracteristique_dic = {"duree_act":caracteristique[0],"duree_tot":caracteristique[1],"reserve_init":caracteristique[2],
                        "duree_obj":caracteristique[3],"penalite":caracteristique[4],"bonus_touche":caracteristique[5],
                        "bonus_rechar":caracteristique[6],"bonus_objet":caracteristique[7]}
    position = joueur.get_pos(joueur_str[ma_couleur])
    # direction_mouvement = str(random.choice("NSEO"))
    # print(IA.mur_autour_joueur(le_plan,ma_couleur,donnees_joueurs))
    # direction_mouvement = str(random.choice(IA.mur_autour_joueur(plan,ma_couleur,les_joueurs)))
    # best_nb_case = 0
    # best_direction = 'X'
    # for direction_test in "NSEO":
    #     if IA.nb_cases_possibles_a_peindre_direction(plan,joueur.get_pos(ma_couleur),joueur.get_reserve(ma_couleur),\
    #         direction_test,ma_couleur) > best_nb_case:
    #         best_nb_case = IA.nb_cases_possibles_a_peindre_direction(plan,joueur.get_pos(ma_couleur),joueur.get_reserve(ma_couleur),\
    #             direction_test,ma_couleur):
    #         best_direction = direction_test
    try:
        #Initialisation des variables utilisées dans le programme
        the_print = "try"
        modif = False
        dic_direction = None
        #Definition des mouvements initiaux en aléatoire
        direction_mouvement = str(random.choice("NSEO"))
        direction_tir = str(random.choice("XNSEO"))
        #Si la reserve est basse, on se déplace sur nos cases et on ne tire pas
        if joueur.get_reserve(joueur_str[ma_couleur]) <= 5:
            dic_direction = plateau.directions_possibles(le_plan, position)
            for (direction1, valeur_case) in dic_direction.items():
                #On vérife qu'une case adjacente soit de notre couleur
                if valeur_case == joueur_str[ma_couleur]:
                    direction_mouvement = direction1
                    the_print = "Low_reserve + bouge dans notre couleur"
                #Sinon, on bouge dans une case qui n'est pas un mur
                else:
                    direction_mouvement = random.choice(dic_direction)
                    the_print = "Low_reserve + bouge dans autre couleur"
            return 'X' + direction_mouvement


        #Sinon, si,on tire dans une direction où la case adjacente n'est ni un mur ni de notre couleur
        elif joueur.get_reserve(joueur_str[ma_couleur]) > 5:
            dic_direction = plateau.directions_possibles(le_plan, position)
            #On vérifie si il y a une case d'une couleur autre que la notre autour de nous
            for (direction2, valeur_case) in dic_direction.items():
                #Si c'est le cas, on défini le tir et le mouvement à cette direction
                if valeur_case != ma_couleur:
                    direction_tir = direction2
                    direction_mouvement = direction_tir
                    modif = True
                    the_print = "Tir dans une autre couleur"
                #Si il n'y en as pas, alors on tir et bouge dans une case qui n'est pas un mur
            if not modif:
                direction_mouvement = random.choice(dic_direction)
                direction_tir = direction_mouvement
                the_print = "Tir 'random' dans une direction qui n'est pas un mur"
        print(the_print,dic_direction, ma_couleur)
        return direction_tir + direction_mouvement

    #Si jamais on arrive à un crash, on génère un coup aléatoire pour éviter un time-out
    except:
        direction_mouvement = random.choice(plateau.directions_possibles(le_plan, position))
        direction_tir = random.choice(plateau.directions_possibles(le_plan, position))
        print("EXCEPT !!!")
        return direction_tir + direction_mouvement

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
