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
        ma_couleur (str): un caractère en majuscule indiquant la couleur du joueur
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

    #Initialisation des variables utilisées dans le programme
    modif = False
    dic_direction = None
    liste_direction_not_mur = []
    position = joueur.get_pos(joueur_str[ma_couleur])
    for dir in (plateau.directions_possibles(le_plan, position)).keys():
        liste_direction_not_mur.append(dir)
    reserve = joueur.get_reserve(joueur_str[ma_couleur])
    #Definition des mouvements initiaux en aléatoire
    direction_mouvement = str(random.choice(liste_direction_not_mur))
    direction_tir = str(random.choice(liste_direction_not_mur))
    
    if reserve < 0:
        direction_tir = "X"
        if IA.get_case_objet_plus_proche_donne(le_plan,position,const.BIDON) != None:
                if IA.get_case_objet_plus_proche_donne(le_plan,position,const.BIDON)[1] != position:
                    if len(IA.get_case_objet_plus_proche_donne(le_plan,position,const.BIDON)) == 2:
                        direction_mouvement = str(IA.direction(position,IA.get_case_objet_plus_proche_donne(le_plan,position,const.BIDON)[1]))
                        direction_tir = random.choice(liste_direction_not_mur)
        elif (plateau.surfaces_peintes(le_plan,len(joueur_str)))[ma_couleur] <= 0:
            print("jai plus d'énergie", direction_mouvement)
            if IA.get_case_objet_plus_proche_donne(le_plan,position,const.BIDON) != None:
                print("jai plus de case")
                if IA.get_case_objet_plus_proche_donne(le_plan,position,const.BIDON)[1] != position:
                    direction_mouvement = str(IA.direction(position,IA.get_case_objet_plus_proche_donne(le_plan,position,const.BIDON)[1]))
                    print("OMG 1 BIDON?????!!!! J V 2 SE PAS")
        
        elif IA.get_ma_couleur_plus_proche(le_plan,position,ma_couleur) != None:
            if IA.get_case_objet_plus_proche_donne(le_plan,position,const.BIDON) != None:
                if IA.get_case_objet_plus_proche_donne(le_plan,position,const.BIDON)[1] != position:
                    if len(IA.get_case_objet_plus_proche_donne(le_plan,position,const.BIDON)[1]) < 5 :
                        direction_mouvement = str(IA.direction(position,IA.get_case_objet_plus_proche_donne(le_plan,position,const.BIDON)[1]))
        
    #Si la reserve est basse, on se déplace sur nos cases et on ne tire pas
    elif reserve <= 5:
        # dic_nb_case_possible_peindre = {}
        # for direction in "NSEO":
        #     dic_nb_case_possible_peindre[direction] = IA.nb_cases_possibles_a_peindre_direction(le_plan,position,reserve,direction,ma_couleur) == 0:
        #     if dic_nb_case_possible != 0:
        #         modif = True
        # if modif = False:
        direction_tir = "X"
        dic_direction = plateau.directions_possibles(le_plan, position)
        for (direction1, valeur_case) in dic_direction.items():
            #On vérife qu'une case adjacente soit de notre couleur
            if valeur_case == ma_couleur:
                direction_mouvement = direction1
            #Sinon, on bouge vers la case de notre couleur la plus proche
            elif IA.get_ma_couleur_plus_proche(le_plan,position,ma_couleur) != None:
                if len(IA.get_ma_couleur_plus_proche(le_plan,position,ma_couleur)) > 1:
                    print(IA.get_ma_couleur_plus_proche(le_plan,position,ma_couleur))
                    direction_mouvement = IA.direction(position,IA.get_ma_couleur_plus_proche(le_plan,position,ma_couleur)[1])
            
        print("Je suis low !", direction_mouvement)
        # else:
        #   best_dir = None
        #   best_nb = 0
        #   for (direction4, val) in dic_nb_case_possible_peindre.items():
        #       if val > best_nb:
        #           best_nb = val
        #           best_dir = direction4
        #   direction_tir = best_dir
        #   direction_mouvement = best_tir

    #Sinon, si,on tire dans une direction où la case adjacente n'est ni un mur ni de notre couleur
    elif reserve > 5:
        dic_direction = plateau.directions_possibles(le_plan, position)
        #On vérifie si il y a une case d'une couleur autre que la notre autour de nous
        for (direction2, valeur_case) in dic_direction.items():
            #Si c'est le cas, on défini le tir et le mouvement à cette direction
            if valeur_case != ma_couleur:
                direction_tir = direction2
                direction_mouvement = direction_tir
                modif = True
        #Si il n'y en as pas, alors on tir et on bouge vers la case la plus proche qui n'est pas de notre couleur
        if not modif:
            if IA.get_case_autre_couleur_plus_proche(le_plan,position,ma_couleur) != None:
                if position != IA.get_case_autre_couleur_plus_proche(le_plan,position,ma_couleur)[1]:
                    if IA.possible_a_peindre(le_plan,position,ma_couleur,direction_tir,reserve):
                        direction_tir = IA.direction(position,IA.get_case_autre_couleur_plus_proche(le_plan,position,ma_couleur)[1])
                    else:
                        direction_tir = "X"
                else:
                    direction_tir = random.choice(liste_direction_not_mur)
            else:
                direction_tir = random.choice(liste_direction_not_mur)
            direction_mouvement = direction_tir
        print("Je suis normal !", direction_mouvement, direction_tir)
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
