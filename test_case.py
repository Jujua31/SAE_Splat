import unittest
import const
import case

class test_case(unittest.TestCase):  
    def setUp(self):
        self.case_par_defaut=case.Case()
        self.case_mur=case.Case(True)
        self.case_jA=case.Case(False,' ',const.AUCUN,{"A"})
        self.case_pB=case.Case(False,'B',const.AUCUN)
        self.case_o1=case.Case(False,' ',1)
        self.case_jB_o1=case.Case(False,' ',1,{"B"})
        self.case_jB_pA_o2=case.Case(False,'A',2,{"B"})
        self.case_jBA=case.Case(False,' ',1,{'B','A'})
        
    def test_est_mur(self):
        self.assertFalse(case.est_mur(self.case_par_defaut))
        self.assertFalse(case.est_mur(self.case_jA))
        self.assertFalse(case.est_mur(self.case_pB))
        self.assertFalse(case.est_mur(self.case_o1))
        self.assertFalse(case.est_mur(self.case_jB_o1))
        self.assertFalse(case.est_mur(self.case_jB_pA_o2))
        self.assertTrue(case.est_mur(self.case_mur))

    def test_get_couleur(self):
        self.assertEqual(case.get_couleur(self.case_par_defaut)," ")
        self.assertEqual(case.get_couleur(self.case_jA)," ")
        self.assertEqual(case.get_couleur(self.case_pB),"B")
        self.assertEqual(case.get_couleur(self.case_o1)," ")
        self.assertEqual(case.get_couleur(self.case_jB_o1)," ")
        self.assertEqual(case.get_couleur(self.case_jB_pA_o2),"A")
        self.assertEqual(case.get_couleur(self.case_mur), " ")

    def test_get_objet(self):
        self.assertEqual(case.get_objet(self.case_par_defaut),const.AUCUN)
        self.assertEqual(case.get_objet(self.case_jA),const.AUCUN)
        self.assertEqual(case.get_objet(self.case_pB),const.AUCUN)
        self.assertEqual(case.get_objet(self.case_o1),1)
        self.assertEqual(case.get_objet(self.case_jB_o1),1)
        self.assertEqual(case.get_objet(self.case_jB_pA_o2),2)
        self.assertEqual(case.get_objet(self.case_mur), const.AUCUN)

    def test_get_joueurs(self):
        self.assertEqual(case.get_joueurs(self.case_par_defaut),set())
        self.assertEqual(case.get_joueurs(self.case_jA),{"A"})
        self.assertEqual(case.get_joueurs(self.case_pB),set())
        self.assertEqual(case.get_joueurs(self.case_o1),set())
        self.assertEqual(case.get_joueurs(self.case_jB_o1),{"B"})
        self.assertEqual(case.get_joueurs(self.case_jB_pA_o2),{"B"})
        self.assertEqual(case.get_joueurs(self.case_mur), set())

    def test_get_nb_joueurs(self):
        self.assertEqual(case.get_nb_joueurs(self.case_par_defaut),0)
        self.assertEqual(case.get_nb_joueurs(self.case_jA),1)
        self.assertEqual(case.get_nb_joueurs(self.case_pB),0)
        self.assertEqual(case.get_nb_joueurs(self.case_o1),0)
        self.assertEqual(case.get_nb_joueurs(self.case_jB_o1),1)
        self.assertEqual(case.get_nb_joueurs(self.case_jB_pA_o2),1)
        self.assertEqual(case.get_nb_joueurs(self.case_mur), 0)
        self.assertEqual(case.get_nb_joueurs(self.case_jBA), 2)

    def test_peindre(self):
        self.assertEqual(case.peindre(self.case_par_defaut,"A"),set())
        self.assertEqual(case.get_couleur(self.case_par_defaut),"A")
        self.assertEqual(case.peindre(self.case_jA,"B"),{"A"})
        self.assertEqual(case.get_couleur(self.case_jA),"B")
        self.assertEqual(case.peindre(self.case_pB,"C"),set())
        self.assertEqual(case.get_couleur(self.case_pB),"C")
        self.assertEqual(case.peindre(self.case_o1,"A"),set())
        self.assertEqual(case.get_couleur(self.case_o1),"A")
        self.assertEqual(case.peindre(self.case_jB_o1,"B"),{"B"})
        self.assertEqual(case.get_couleur(self.case_jB_o1),"B")
        self.assertEqual(case.peindre(self.case_jB_pA_o2,"C"),{"B"})
        self.assertEqual(case.get_couleur(self.case_jB_pA_o2),"C")
        self.assertEqual(case.peindre(self.case_jBA,"A"),{"A","B"})
        self.assertEqual(case.get_couleur(self.case_jBA),"A")

    def test_laver(self):
        case.laver(self.case_par_defaut)
        self.assertEqual(case.get_couleur(self.case_par_defaut)," ")
        case.laver(self.case_jA)
        self.assertEqual(case.get_couleur(self.case_jA)," ")
        case.laver(self.case_pB)
        self.assertEqual(case.get_couleur(self.case_pB)," ")
        case.laver(self.case_o1)
        self.assertEqual(case.get_couleur(self.case_o1)," ")
        case.laver(self.case_jB_o1)
        self.assertEqual(case.get_couleur(self.case_jB_o1)," ")
        case.laver(self.case_jB_pA_o2)
        self.assertEqual(case.get_couleur(self.case_jB_pA_o2)," ")

    def test_poser_objet(self):
        case.poser_objet(self.case_par_defaut,1)
        self.assertEqual(case.get_objet(self.case_par_defaut),1)
        case.poser_objet(self.case_jA,2)
        self.assertEqual(case.get_objet(self.case_jA),2)
        case.poser_objet(self.case_pB,3)
        self.assertEqual(case.get_objet(self.case_pB),3)
        case.poser_objet(self.case_o1,const.AUCUN)
        self.assertEqual(case.get_objet(self.case_o1),const.AUCUN)
        case.poser_objet(self.case_jB_o1,2)
        self.assertEqual(case.get_objet(self.case_jB_o1),2)
        case.poser_objet(self.case_jB_pA_o2,2)
        self.assertEqual(case.get_objet(self.case_jB_pA_o2),2)

    def test_prendre_objet(self):
        self.assertEqual(case.prendre_objet(self.case_par_defaut),const.AUCUN)
        self.assertEqual(case.get_objet(self.case_par_defaut),const.AUCUN)
        self.assertEqual(case.prendre_objet(self.case_jA),const.AUCUN)
        self.assertEqual(case.get_objet(self.case_jA),const.AUCUN)
        self.assertEqual(case.prendre_objet(self.case_pB),const.AUCUN)
        self.assertEqual(case.get_objet(self.case_pB),const.AUCUN)
        self.assertEqual(case.prendre_objet(self.case_o1),1)
        self.assertEqual(case.get_objet(self.case_o1),const.AUCUN)
        self.assertEqual(case.prendre_objet(self.case_jB_o1),1)
        self.assertEqual(case.get_objet(self.case_jB_o1),const.AUCUN)
        self.assertEqual(case.prendre_objet(self.case_jB_pA_o2),2)
        self.assertEqual(case.get_objet(self.case_jB_pA_o2),const.AUCUN)

    def test_poser_joueur(self):
        case.poser_joueur(self.case_par_defaut,'A')
        self.assertTrue('A' in case.get_joueurs(self.case_par_defaut))
        self.assertFalse('B' in case.get_joueurs(self.case_par_defaut))
        case.poser_joueur(self.case_jA,'B')
        self.assertTrue('A' in case.get_joueurs(self.case_jA))
        self.assertTrue('B' in case.get_joueurs(self.case_jA))
        case.poser_joueur(self.case_pB,'B')
        self.assertEqual(case.get_joueurs(self.case_pB),{'B'})
        case.poser_joueur(self.case_o1,'A')
        self.assertEqual(case.get_joueurs(self.case_o1),{'A'})
        case.poser_joueur(self.case_jB_o1,'C')
        self.assertEqual(case.get_joueurs(self.case_jB_o1),{'B','C'})
        case.poser_joueur(self.case_jB_pA_o2,'A')
        self.assertEqual(case.get_joueurs(self.case_jB_pA_o2),{'A','B'})
        case.poser_joueur(self.case_jBA,'C')
        self.assertEqual(case.get_joueurs(self.case_jBA),{'A','B','C'})
        

    def test_prendre_joueur(self):
        self.assertFalse(case.prendre_joueur(self.case_par_defaut,'A'))
        self.assertEqual(case.get_joueurs(self.case_par_defaut),set())
        self.assertTrue(case.prendre_joueur(self.case_jA,'A'))
        self.assertEqual(case.get_joueurs(self.case_jA),set())
        self.assertFalse(case.prendre_joueur(self.case_pB,'C'))
        self.assertEqual(case.get_joueurs(self.case_pB),set())
        self.assertFalse(case.prendre_joueur(self.case_o1,'C'))
        self.assertEqual(case.get_joueurs(self.case_o1),set())
        self.assertTrue(case.prendre_joueur(self.case_jB_o1,'B'))
        self.assertEqual(case.get_joueurs(self.case_jB_o1),set())
        self.assertFalse(case.prendre_joueur(self.case_jB_pA_o2,'A'))
        self.assertEqual(case.get_joueurs(self.case_jB_pA_o2),{'B'})
        self.assertTrue(case.prendre_joueur(self.case_jBA,'B'))
        self.assertEqual(case.get_joueurs(self.case_jBA),{'A'})

if __name__ == '__main__':
    unittest.main()       
        
        
        
        