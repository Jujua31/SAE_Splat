import unittest
import const
import plateau
import case
class test_case(unittest.TestCase):  
    def setUp(self):
        with open("plans/plan1.txt") as fic:
            self.plan1=fic.read()
        with open("plans/plan2.txt") as fic:
            self.plan1=fic.read()
    
    def verif(self,plan,le_plateau):
        les_lignes=plan.split("\n")
        [nb_lignes,nb_colonnes]=les_lignes[0].split(";")
        nb_lignes=int(nb_lignes)
        nb_colonnes=int(nb_colonnes)
        nblo=plateau.get_nb_lignes(le_plateau)
        if nb_lignes!=nblo:
            return "Le nombre de lignes est incorrect. Attendu: "+str(nb_lignes)+\
                "Obtenu: "+ str(nblo)
        nbco=plateau.get_nb_colonnes(le_plateau)
        if nb_colonnes!=nbco:
            return "Le nombre de colonnes est incorrect. Attendu: "+str(nb_colonnes)+\
                "Obtenu: "+ str(nbco)
        for lin in range(nb_lignes):
            la_ligne=les_lignes[lin+1]
            for col in range(nb_colonnes):
                la_case=plateau.get_case(le_plateau,(lin,col))
                if la_ligne[col]==' ':
                    if case.est_mur(la_case):
                        return "La case "+str(lin)+","+str(col)+\
                            " devrait être un couloir alors que c'est un mur dans votre plateau"
                    coul=case.get_couleur(la_case)
                    if coul!=' ':
                        return "La case "+str(lin)+","+str(col)+\
                            " devrait être non peinte alors qu'elle a la couleur "+\
                                str(coul)+" dans votre plateau"
                elif la_ligne[col]=='#':
                    if not case.est_mur(la_case):
                        return "La case "+str(lin)+","+str(col)+\
                            " devrait être un mur alors que c'est un couloir dans votre plateau"
                    coul=case.get_couleur(la_case)
                    if coul!=' ':
                        return "La case "+str(lin)+","+str(col)+\
                            " devrait être non peinte alors qu'elle a la couleur "+\
                                str(coul)+" dans votre plateau"
                elif la_ligne[col].islower():
                    if not case.est_mur(la_case):
                        return "La case "+str(lin)+","+str(col)+\
                            " devrait être un mur alors que c'est un couloir dans votre plateau"
                    coul=case.get_couleur(la_case)
                    if coul.lower()!=la_ligne[col]:
                        return "La case "+str(lin)+","+str(col)+\
                            " devrait être peinte en "+la_ligne[col]+" alors qu'elle a la couleur "+\
                                str(coul)+" dans votre plateau"
                elif la_ligne[col].isupper():
                    if case.est_mur(la_case):
                        return "La case "+str(lin)+","+str(col)+\
                            " devrait être un couloir alors que c'est un mur dans votre plateau"
                    coul=case.get_couleur(la_case)
                    if coul.upper()!=la_ligne[col]:
                        return "La case "+str(lin)+","+str(col)+\
                            " devrait être peinte en "+la_ligne[col]+" alors qu'elle a la couleur "+\
                                str(coul)+" dans votre plateau"
        nb_joueurs=int(les_lignes[nb_lignes+1])
        for ind in range(nb_lignes+2,nb_lignes+2+nb_joueurs):
            joueur,lin,col=les_lignes[ind].split(';')
            lin=int(lin)
            col=int(col)
            joueurs=case.get_joueurs(plateau.get_case(le_plateau,(lin,col)))
            if joueur not in joueurs:
                return "La case "+str(lin)+","+str(col)+\
                            " devrait contenir le joueur "+joueur+\
                            " alors qu'elle contient cet ensemble de joueurs "+\
                            str(joueurs)
        nb_objets=int(les_lignes[nb_lignes+2+nb_joueurs])
        for ind in range(nb_lignes+3+nb_joueurs,nb_lignes+3+nb_joueurs+nb_objets):
            obj,lin,col=les_lignes[ind].split(';')
            obj=int(obj)
            lin=int(lin)
            col=int(col)
            objo=case.get_objet(plateau.get_case(le_plateau,(lin,col)))
            if objo != obj:
                return "La case "+str(lin)+","+str(col)+\
                            " devrait contenir l'objet "+obj+\
                            " alors qu'elle contient l'objet "+\
                            str(objo)
        return None

    def test_Plateau(self):
        res=self.verif(self.plan1,plateau.Plateau(self.plan1))
        self.assertIsNone(res,res)
        res=self.verif(self.plan2,plateau.Plateau(self.plan2))
        self.assertIsNone(res,res)

    def test_enlever_joueur(self):
        p1=plateau.Plateau(self.plan1)
        res=plateau.enlever_joueur(p1,'A',(1,1))
        self.assertTrue(res,"Le joueur A devrait être sur la case (1,1) du plateau 1")
        self.assertFalse('A' in case.get_joueurs(plateau.get_case(p1,(1,1))),
                        "après avoir enlevé le joueur A de la case (1,1) il ne devrait"+\
                         "plus être sur cette case (plateau 2)")
        p2=plateau.Plateau(self.plan2)
        res=plateau.enlever_joueur(p2,'C',(17,1))
        self.assertTrue(res,"Le joueur C devrait être sur la case (17,1) du plateau 2")
        self.assertFalse('C' in case.get_joueurs(plateau.get_case(p2,(17,1))),
                        "après avoir enlevé le joueur C de la case (17,1) il ne devrait"+\
                         "plus être sur cette case (plateau 2)")
        self.assertFalse(plateau.enlever_joueur(p1,'B',(1,1)),
                    "Le joueur ne se trouve pas sur la case (1,1) du plateau 1 or vous le détectez")
        self.assertFalse(plateau.enlever_joueur(p2,'B',(17,8)),
                    "Le joueur ne se trouve pas sur la case (17,8) du plateau 2 or vous le détecter")

    def test_poser_joueur(self):
        p1=plateau.Plateau(self.plan1)
        plateau.poser_joueur(p1,"Z",(3,0))
        self.assertTrue("Z" in case.get_joueurs(plateau.get_case(p1,(3,0))))
        p2=plateau.Plateau(self.plan2)
        plateau.poser_joueur(p2,"Z",(18,1))
        self.assertTrue("Z" in case.get_joueurs(plateau.get_case(p2,(18,1))))

    def test_poser_tresor(self):
        p1=plateau.Plateau(self.plan1)
        plateau.poser_objet(p1,3,(3,1))
        self.assertEqual(case.get_objet(plateau.get_case(p1,(3,1))),3)
        p2=plateau.Plateau(self.plan2)
        plateau.poser_objet(p2,2,(6,5))
        self.assertEqual(case.get_objet(plateau.get_case(p2,(6,5))),2)

    def test_prendre_objet(self):
        p1=plateau.Plateau(self.plan1)
        self.assertEqual(plateau.prendre_objet(p1,(1,1)),const.AUCUN)
        p2=plateau.Plateau(self.plan2)
        self.assertEqual(plateau.prendre_objet(p2,(0,2)),1)
        self.assertEqual(plateau.prendre_objet(p2,(0,2)),const.AUCUN,
                "Après avoir pris un objet en (0,2) cette case devrait être vide")
        self.assertEqual(plateau.prendre_objet(p2,(18,5)),3)
        self.assertEqual(plateau.prendre_objet(p2,(18,5)),const.AUCUN,
                "Après avoir pris un objet en (18,5) cette case devrait être vide")
        self.assertEqual(plateau.prendre_objet(p2,(10,11)),4)
        self.assertEqual(plateau.prendre_objet(p2,(10,11)),const.AUCUN,
                "Après avoir pris un objet en (10,11) cette case devrait être vide")
    
    def test_deplacer_joueur(self):
        p1=plateau.Plateau(self.plan1)
        self.assertEqual(plateau.deplacer_joueur(p1,'A',(1,1),'N'),
                            (True,0,const.AUCUN,(0,1)))
        self.assertTrue('A' in case.get_joueurs(plateau.get_case(p1,(0,1))))
        self.assertFalse('A' in case.get_joueurs(plateau.get_case(p1,(1,1))))

        p1=plateau.Plateau(self.plan1)
        self.assertEqual(plateau.deplacer_joueur(p1,'A',(1,1),'E'),
                            (True,1,const.AUCUN,(1,2)))
        self.assertTrue('A' in case.get_joueurs(plateau.get_case(p1,(1,2))))
        self.assertFalse('A' in case.get_joueurs(plateau.get_case(p1,(1,1))))


        p1=plateau.Plateau(self.plan1)
        reussi,_,_,_=plateau.deplacer_joueur(p1,'A',(1,1),'S')
        self.assertFalse(reussi,"Le déplacement du joueur A vers le sud n'est pas possible."+
                        "deplacer_joueur devrait retourner False en premier élement")
        self.assertTrue('A' in case.get_joueurs(plateau.get_case(p1,(1,1))))

        p1=plateau.Plateau(self.plan1)
        reussi,_,_,_=plateau.deplacer_joueur(p1,'A',(0,1),'S')
        self.assertFalse(reussi,"Le joueur A ne se trouve pas en (0,1)."+
                        "deplacer_joueur devrait retourner False en premier élement")


        p2=plateau.Plateau(self.plan2)
        self.assertEqual(plateau.deplacer_joueur(p2,'A',(0,1),'E'),
                            (True,0,1,(0,2)))
        self.assertTrue('A' in case.get_joueurs(plateau.get_case(p2,(0,2))))
        self.assertFalse('A' in case.get_joueurs(plateau.get_case(p2,(0,1))))
        self.assertEqual(case.get_objet(plateau.get_case(p2,(0,2))),const.AUCUN)

        p2=plateau.Plateau(self.plan2)
        self.assertEqual(plateau.deplacer_joueur(p2,'E',(2,2),'O'),
                            (True,-1,const.AUCUN,(2,1)))
        self.assertTrue('E' in case.get_joueurs(plateau.get_case(p2,(2,1))))
        self.assertFalse('E' in case.get_joueurs(plateau.get_case(p2,(2,2))))

    def test_directions_possibles(self):
        p1=plateau.Plateau(self.plan1)
        self.assertEqual(plateau.directions_possibles(p1,(0,1)),{'S':' ','E':' '})
        self.assertEqual(plateau.directions_possibles(p1,(0,2)),{'S':'A','O':' '})
        self.assertEqual(plateau.directions_possibles(p1,(1,2)),{'N':' ','S':'A','O':' '})
        self.assertEqual(plateau.directions_possibles(p1,(2,5)),{'N':' ','O':' '})


    def test_joueurs_direction(self):
        p1=plateau.Plateau(self.plan1)
        self.assertEqual(plateau.nb_joueurs_direction(p1, (0,1), 'N', 3),0)
        self.assertEqual(plateau.nb_joueurs_direction(p1, (0,1), 'S', 3),1)
        self.assertEqual(plateau.nb_joueurs_direction(p1, (0,1), 'O', 3),0)
        self.assertEqual(plateau.nb_joueurs_direction(p1, (0,1), 'E', 3),0)
        self.assertEqual(plateau.nb_joueurs_direction(p1, (3,2), 'N', 3),0)
        self.assertEqual(plateau.nb_joueurs_direction(p1, (3,2), 'S', 3),0)
        self.assertEqual(plateau.nb_joueurs_direction(p1, (3,2), 'O', 3),1)
        self.assertEqual(plateau.nb_joueurs_direction(p1, (3,2), 'E', 3),0)
        p2=plateau.Plateau(self.plan2)
        self.assertEqual(plateau.nb_joueurs_direction(p2, (2,1), 'N', 10),0)
        self.assertEqual(plateau.nb_joueurs_direction(p2, (2,1), 'S', 10),0)
        self.assertEqual(plateau.nb_joueurs_direction(p2, (2,1), 'O', 10),0)
        self.assertEqual(plateau.nb_joueurs_direction(p2, (2,1), 'E', 10),1)

        self.assertEqual(plateau.nb_joueurs_direction(p2, (9,1), 'N', 10),0)
        self.assertEqual(plateau.nb_joueurs_direction(p2, (9,1), 'S', 10),0)
        self.assertEqual(plateau.nb_joueurs_direction(p2, (9,1), 'O', 10),0)
        self.assertEqual(plateau.nb_joueurs_direction(p2, (9,1), 'E', 10),0)
        
        self.assertEqual(plateau.nb_joueurs_direction(p2, (12,1), 'N', 10),0)
        self.assertEqual(plateau.nb_joueurs_direction(p2, (12,1), 'S', 10),2)
        self.assertEqual(plateau.nb_joueurs_direction(p2, (12,1), 'O', 10),0)
        self.assertEqual(plateau.nb_joueurs_direction(p2, (12,1), 'E', 10),0)

        self.assertEqual(plateau.nb_joueurs_direction(p2, (10,13), 'N', 10),1)
        self.assertEqual(plateau.nb_joueurs_direction(p2, (10,13), 'S', 10),1)
        self.assertEqual(plateau.nb_joueurs_direction(p2, (10,13), 'O', 10),1)
        self.assertEqual(plateau.nb_joueurs_direction(p2, (10,13), 'E', 10),1)

    def test_surfaces_peintes(self):
        p1=plateau.Plateau(self.plan1)
        self.assertEqual(plateau.surfaces_peintes(p1,2),{'A':4,'B':1})
        p2=plateau.Plateau(self.plan2)
        self.assertEqual(plateau.surfaces_peintes(p2,5),
                    {'A':68,'B': 7, 'C': 7, 'D': 0, 'E': 8})


    def test_peindre(self):
        p1=plateau.Plateau(self.plan1)
        self.assertEqual(plateau.peindre(p1,(1,1),'N','A',10,5,False),
                {"cout": 2, "nb_repeintes": 2,
           "nb_murs_repeints": 0, "joueurs_touches": {'A'}})
        self.assertEqual(case.get_couleur(plateau.get_case(p1,(1,1))).upper(),'A')
        self.assertEqual(case.get_couleur(plateau.get_case(p1,(0,1))).upper(),'A')
        

        p1=plateau.Plateau(self.plan1)
        self.assertEqual(plateau.peindre(p1,(1,1),'E','A',10,5,False),
                {"cout": 2, "nb_repeintes": 1,
           "nb_murs_repeints": 0, "joueurs_touches": {'A'}})
        self.assertEqual(case.get_couleur(plateau.get_case(p1,(1,1))).upper(),'A')

        p1=plateau.Plateau(self.plan1)
        self.assertEqual(plateau.peindre(p1,(1,1),'E','A',10,5,True),
                {"cout": 5, "nb_repeintes": 4,
           "nb_murs_repeints": 2, "joueurs_touches": {'A'}})
        self.assertEqual(case.get_couleur(plateau.get_case(p1,(1,1))).upper(),'A')
        self.assertEqual(case.get_couleur(plateau.get_case(p1,(1,2))).upper(),'A')
        self.assertEqual(case.get_couleur(plateau.get_case(p1,(1,3))).upper(),'A')
        self.assertEqual(case.get_couleur(plateau.get_case(p1,(1,4))).upper(),'A')

        p2=plateau.Plateau(self.plan2)
        self.assertEqual(plateau.peindre(p2,(0,1),'S','A',50,25,True),
                {"cout": 22, "nb_repeintes": 20,
           "nb_murs_repeints": 2, "joueurs_touches": {'A','B','C'}})
        for i in range(20):
            self.assertEqual(case.get_couleur(plateau.get_case(p2,(i,1))).upper(),'A',
                'Problème couleur avec la case ('+str(i)+',1)')
        
        p2=plateau.Plateau(self.plan2)
        self.assertEqual(plateau.peindre(p2,(0,1),'S','A',10,25,True),
                {"cout": 10, "nb_repeintes": 9,
           "nb_murs_repeints": 1, "joueurs_touches": {'A'}})
        for i in range(9):
            self.assertEqual(case.get_couleur(plateau.get_case(p2,(i,1))).upper(),'A',
                'Problème couleur avec la case ('+str(i)+',1)')
        
        p2=plateau.Plateau(self.plan2)
        self.assertEqual(plateau.peindre(p2,(0,1),'S','A',50,10,True),
                {"cout": 11, "nb_repeintes": 10,
           "nb_murs_repeints": 1, "joueurs_touches": {'A'}})
        for i in range(10):
            self.assertEqual(case.get_couleur(plateau.get_case(p2,(i,1))).upper(),'A',
                'Problème couleur avec la case ('+str(i)+',1)')

        p2=plateau.Plateau(self.plan2)
        self.assertEqual(plateau.peindre(p2,(10,13),'N','D',9,10,True),
                {"cout": 8, "nb_repeintes": 4,
           "nb_murs_repeints": 0, "joueurs_touches": {'D'}})
        for i in range(4):
            self.assertEqual(case.get_couleur(plateau.get_case(p2,(10-i,13))).upper(),'D',
                'Problème couleur avec la case ('+str(10-i)+',13)')

        
if __name__ == '__main__':
    unittest.main()       
        
