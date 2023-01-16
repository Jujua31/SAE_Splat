import unittest
import const
import joueur

class test_joueur(unittest.TestCase):  
    def setUp(self):
        self.chaine1="A;15;28;0;0;12;25;le peintre"
        self.chaine2="B;-8;12;1;3;6;4;iut'o"
        self.chaine3="C;14;0;2;1;23;1;splash"
    
    def test_joueur(self):
        le_joueur=joueur.Joueur('A',"test1",10,5,(12,47),1,3)
        self.assertEqual(joueur.get_couleur(le_joueur),'A')
        self.assertEqual(joueur.get_nom(le_joueur),'test1')
        self.assertEqual(joueur.get_reserve(le_joueur),10)
        self.assertEqual(joueur.get_surface(le_joueur),5)
        self.assertEqual(joueur.get_pos(le_joueur),(12,47))
        self.assertEqual(joueur.get_objet(le_joueur),1)
        self.assertEqual(joueur.get_duree(le_joueur),3)

        le_joueur=joueur.Joueur('B',"test2",-8,45,(7,22),0,0)
        self.assertEqual(joueur.get_couleur(le_joueur),'B')
        self.assertEqual(joueur.get_nom(le_joueur),'test2')
        self.assertEqual(joueur.get_reserve(le_joueur),-8)
        self.assertEqual(joueur.get_surface(le_joueur),45)
        self.assertEqual(joueur.get_pos(le_joueur),(7,22))
        self.assertEqual(joueur.get_objet(le_joueur),0)
        self.assertEqual(joueur.get_duree(le_joueur),0)
 
    def test_joueur_from_str(self):

        le_joueur=joueur.joueur_from_str(self.chaine1)
        self.assertEqual(joueur.get_couleur(le_joueur),'A')
        self.assertEqual(joueur.get_nom(le_joueur),'le peintre')
        self.assertEqual(joueur.get_reserve(le_joueur),15)
        self.assertEqual(joueur.get_surface(le_joueur),28)
        self.assertEqual(joueur.get_pos(le_joueur),(12,25))
        self.assertEqual(joueur.get_objet(le_joueur),0)
        self.assertEqual(joueur.get_duree(le_joueur),0)

        le_joueur=joueur.joueur_from_str(self.chaine2)
        self.assertEqual(joueur.get_couleur(le_joueur),'B')
        self.assertEqual(joueur.get_nom(le_joueur),"iut'o")
        self.assertEqual(joueur.get_reserve(le_joueur),-8)
        self.assertEqual(joueur.get_surface(le_joueur),12)
        self.assertEqual(joueur.get_pos(le_joueur),(6,4))
        self.assertEqual(joueur.get_objet(le_joueur),1)
        self.assertEqual(joueur.get_duree(le_joueur),3)

        le_joueur=joueur.joueur_from_str(self.chaine3)
        self.assertEqual(joueur.get_couleur(le_joueur),'C')
        self.assertEqual(joueur.get_nom(le_joueur),"splash")
        self.assertEqual(joueur.get_reserve(le_joueur),14)
        self.assertEqual(joueur.get_surface(le_joueur),0)
        self.assertEqual(joueur.get_pos(le_joueur),(23,1))
        self.assertEqual(joueur.get_objet(le_joueur),2)
        self.assertEqual(joueur.get_duree(le_joueur),1)

    def test_modifier_reserve(self):
        le_joueur=joueur.joueur_from_str(self.chaine1)
        self.assertEqual(joueur.modifie_reserve(le_joueur,10),25)
        self.assertEqual(joueur.get_reserve(le_joueur),25)

        le_joueur=joueur.joueur_from_str(self.chaine2)
        self.assertEqual(joueur.modifie_reserve(le_joueur,10),2)
        self.assertEqual(joueur.get_reserve(le_joueur),2)

        le_joueur=joueur.joueur_from_str(self.chaine3)
        self.assertEqual(joueur.modifie_reserve(le_joueur,-20),-6)
        self.assertEqual(joueur.get_reserve(le_joueur),-6)

    def test_ajouter_objet(self):
        le_joueur=joueur.joueur_from_str(self.chaine1)
        joueur.ajouter_objet(le_joueur,1,5)
        self.assertEqual(joueur.get_objet(le_joueur),1)
        self.assertEqual(joueur.get_duree(le_joueur),5)
        self.assertEqual(joueur.get_reserve(le_joueur),15)
        
        le_joueur=joueur.joueur_from_str(self.chaine2)
        joueur.ajouter_objet(le_joueur,const.BIDON,0)
        self.assertEqual(joueur.get_objet(le_joueur),1)
        self.assertEqual(joueur.get_duree(le_joueur),3)
        self.assertEqual(joueur.get_reserve(le_joueur),0)
        
        le_joueur=joueur.joueur_from_str(self.chaine3)
        joueur.ajouter_objet(le_joueur,const.BIDON,4)
        self.assertEqual(joueur.get_objet(le_joueur),2)
        self.assertEqual(joueur.get_duree(le_joueur),1)
        self.assertEqual(joueur.get_reserve(le_joueur),14)

        le_joueur=joueur.joueur_from_str(self.chaine3)
        joueur.ajouter_objet(le_joueur,1,4)
        self.assertEqual(joueur.get_objet(le_joueur),1)
        self.assertEqual(joueur.get_duree(le_joueur),4)
        self.assertEqual(joueur.get_reserve(le_joueur),14)

    def test_mise_a_jour_duree(self):
        le_joueur=joueur.joueur_from_str(self.chaine1)
        joueur.maj_duree(le_joueur)
        self.assertEqual(joueur.get_objet(le_joueur),0)
        self.assertEqual(joueur.get_duree(le_joueur),0)
        
        le_joueur=joueur.joueur_from_str(self.chaine2)
        joueur.maj_duree(le_joueur)
        self.assertEqual(joueur.get_objet(le_joueur),1)
        self.assertEqual(joueur.get_duree(le_joueur),2)

        le_joueur=joueur.joueur_from_str(self.chaine3)
        joueur.maj_duree(le_joueur)
        self.assertEqual(joueur.get_objet(le_joueur),0)
        self.assertEqual(joueur.get_duree(le_joueur),0)

if __name__ == '__main__':
    unittest.main()       
       
        
        
        
        
        