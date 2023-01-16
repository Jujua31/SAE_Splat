import pygame
import os
import case
import plateau

class JeuGraphique(object):
    """Classe simple d'affichage et d'interaction pour le labyrinthe."""

    def __init__(self, le_plateau, titre="Splat'IUT'O", size=(3000, 1600),
                 couleur=(209, 238, 238),
                 prefixe_image="./images"):
        """Method docstring."""
        self.plateau = le_plateau
        self.couleur_texte = couleur
        self.nb_colonnes = plateau.get_nb_colonnes(le_plateau)
        self.nb_lignes = plateau.get_nb_lignes(le_plateau)
        self.titre = titre
        self.images_cartes = {}
        self.images_pions = {}
        self.images_objets = {}
        self.images_murs={}
        self.icone = None
        self.hauteur = 0
        self.largeur = 0
        self.deltah = 0
        self.deltal = 0
        self.finh = 0
        self.finl = 0
        self.taille_font = 0
        self.get_images(prefixe_image)
        pygame.init()
        pygame.display.set_icon(self.icone)
        pygame.display.set_mode(size, pygame.RESIZABLE | pygame.DOUBLEBUF)
        pygame.display.set_caption(titre)
        self.surface = pygame.display.get_surface()
        self.maj_parametres()
        self.affiche_plateau()

    def get_images(self, prefixe_image="./images"):
        codage="_abcdefghijklmnopqrstuvwxyz"
        for i in range(7):
            if os.path.isfile(os.path.join(prefixe_image, 'mur' + codage[i] + '.jpeg')):
                s = pygame.image.load(os.path.join(prefixe_image, 'mur' + codage[i] + '.jpeg'))
            else:
                s = None
            self.images_murs[codage[i]]=s
            if os.path.isfile(os.path.join(prefixe_image, 'peinture' + codage[i] + '.jpg')):
                s = pygame.image.load(os.path.join(prefixe_image, 'peinture' + codage[i] + '.jpg'))
            else:
                s = None
            self.images_cartes[codage[i]]=s
            if i>0:
                s = pygame.image.load(os.path.join(prefixe_image, 'pion'+codage[i]+'.png'))
            self.images_pions[codage[i]] = s
        # lecture des différents objets dans les fichiers de la forme objetxxx.png où xxx va de 0 à 3
        i = 1
        while os.path.isfile(os.path.join(prefixe_image, 'objet' + str(i) + '.png')):
            s = pygame.image.load(os.path.join(prefixe_image, 'objet' + str(i) + '.png'))
            self.images_objets[i] = s
            i += 1

        # lecture du logo de l'IUT'O
        icone_img = pygame.image.load(os.path.join(prefixe_image, 'logo.jpeg'))
        self.icone = pygame.transform.smoothscale(icone_img, (50, 50))

    def maj_parametres(self):
        """
        permet de mettre à jour les paramètre d'affichage en cas de redimensionnement de la fenêtre
        """
        self.surface = pygame.display.get_surface()
        self.hauteur = round(self.surface.get_height() *1)
        self.largeur = self.hauteur
        self.deltah = self.hauteur // (self.nb_lignes + 2)
        self.deltal = self.largeur // (self.nb_colonnes + 2)
        self.finh = self.deltah * (self.nb_lignes + 2)
        self.finl = self.deltal * (self.nb_colonnes + 2)
        self.taille_font = min(self.deltah, self.deltal) * 1 // 2

    def surface_carte(self, la_carte):
        """
        transforme une carte en une surface (image 2D) avec les pions et trésor associés
        """
        couleur = case.get_couleur(la_carte).lower()
        if couleur==' ':
            couleur='_'
        if case.est_mur(la_carte):
            surf_carte=pygame.transform.smoothscale(self.images_murs[couleur], (self.deltal, self.deltah))
            return surf_carte
        objet = case.get_objet(la_carte)
        pions = case.get_joueurs(la_carte)
        img = self.images_cartes[couleur]
        if img is None:
            return None

        surf_carte = pygame.transform.smoothscale(img, (self.deltal, self.deltah))
        dist = 5
        coord = [(dist, dist), (dist, self.deltah - (self.deltah // 2 +dist)),
                 (self.deltal - (self.deltal // 2 +dist), self.deltah - (self.deltah // 2 +dist)),
                 (self.deltal - (self.deltal // 2 +dist), dist), (self.deltal//4+dist,dist),
                 (self.deltal//4+dist,self.deltah - (self.deltah // 2 +dist))]
        for pion in pions:
            surf_pion = pygame.transform.smoothscale(
                self.surface_pion(pion.lower(), True),
                (self.deltal // 2, self.deltah // 2))
            surf_carte.blit(surf_pion, coord.pop(0))
        if objet != 0:
            surf_objet = pygame.transform.smoothscale(self.images_objets[objet],
                                                      (self.deltal // 4, self.deltah // 4))
            surf_carte.blit(surf_objet, (self.deltah // 4 + dist, self.deltah // 4 + dist))
        return surf_carte

    
    def surface_pion(self, couleur, affiche_objet=False):
        """
        transforme un numéro de pion en son image
        """
        res = pygame.Surface((self.deltal, self.deltah), pygame.SRCALPHA)
        surf_pion = pygame.transform.smoothscale(self.images_pions[couleur], (self.deltal // 2, self.deltah // 2))
        res.blit(surf_pion, (self.deltal // 4, self.deltah // 4))
        return res

    def surface_objet(self, objet):
        """
        produit l'image de l'objet dont le numéro est passé en paramètre
        """
        res = pygame.Surface((self.deltal, self.deltah))
        surf_objet = pygame.transform.smoothscale(self.images_objets[objet], (self.deltal // 2, self.deltah // 2))
        res.blit(surf_objet, (self.deltal // 4, self.deltah // 4))
        return res


    def affiche_plateau(self):
        """
        affiche le labyrinthe
        """
        self.surface.fill((0, 0, 0))
        font = pygame.font.Font(None, self.taille_font)
        for i in range(self.nb_lignes):
            for j in range(self.nb_colonnes):
                try:
                    carte = plateau.get_case(self.plateau,(i, j))
                    s = self.surface_carte(carte)
                    if s is None:
                        self.surface.fill((0, 0, 0),
                                          ((j + 1) * self.deltal, (i + 1) * self.deltah, self.deltal, self.deltah))
                    else:
                        self.surface.blit(s, ((j + 1) * self.deltal, (i + 1) * self.deltah))
                except Exception as ex:
                    print(ex, i, j)
                    pass
        pygame.display.flip()

    def demarrer(self):
        """
        démarre l'environnement graphique et la boucle d'écoute des événements
        """
        self.affiche_plateau()
        done=False
        while (True):
            ev = pygame.event.wait()
            if ev.type == pygame.QUIT:
                break
            if ev.type == pygame.KEYDOWN:
                if ev.__dict__["unicode"].upper()=='Q':
                    break
                if ev.__dict__["unicode"].upper()=='A' and not done:
                    print("action")
                    actions(self.plateau)
                    self.affiche_plateau()
                    done=True
            if ev.type == pygame.VIDEORESIZE:
                pygame.display.set_mode(ev.size, pygame.RESIZABLE | pygame.DOUBLEBUF)
                self.maj_parametres()
                self.affiche_plateau()
        pygame.quit()

# utilisez cette fonction pour voir l'effet de vos fonctions
#  sur les plateaux
def actions(le_plateau):
    plateau.peindre(le_plateau,(1,1),'S','A',10,True)

if __name__ == '__main__':
    plan1="4;6\n"+\
                    "#  b# \n"+\
                    "  A## \n"+\
                    "##A   \n"+\
                    "  Aa##\n"+\
                    "2\nA;1;1\nB;3;0\n"+\
                    "0\n"
    plan2="20;16\n"+\
                    "b   #AA##   #AA#\n"+\
                    "b## #CABBB# #CA#\n"+\
                    "#C EE ###  EE ##\n"+\
                    "#   #AA##   #AA#\n"+\
                    "#   #AA##   #AA#\n"+\
                    "#   #AA##   #AA#\n"+\
                    "#   #AA##   #AA#\n"+\
                    "#   #AA##   #AA#\n"+\
                    "#   #AA##   #AA#\n"+\
                    "#   #AA##   #AA#\n"+\
                    "#   #AA##   #AA#\n"+\
                    "#cc #CA BB# #CA#\n"+\
                    "#   EE###   EE##\n"+\
                    "#   #AA##   #AA#\n"+\
                    "#   #AA##   #AA#\n"+\
                    "#   #AA##   #AA#\n"+\
                    "#   #AA##   #AA#\n"+\
                    "#   #AA##   #AA#\n"+\
                    "#   #AA##   #AA#\n"+\
                    "#   #AA##   #AA#\n"+\
                    "5\nA;0;1\nB;18;1\nC;17;1\nD;10;13\nE;2;2\n"+\
                    "3\n1;0;2\n3;18;5\n4;10;11\n"

    plan3="9;9\n"+\
                    "b   #AA# \n"+\
                    "b## #CABB\n"+\
                    "#C EE ###\n"+\
                    "#   #AA##\n"+\
                    "#   #AA##\n"+\
                    "#   #AA##\n"+\
                    "#   #AA##\n"+\
                    "#   #AA##\n"+\
                    "#   #AA##\n"+\
            "5\nA;0;1\nB;8;1\nC;5;1\nD;0;1\nE;2;2\n"+\
                    "3\n1;0;2\n3;8;5\n3;4;3\n"
    plan4="9;9\n"+\
                    "#AAAa  ##\n"+\
                    "    #B#  \n"+\
                    "#    B## \n"+\
                    "#   #B # \n"+\
                    "#   #B   \n"+\
                    "#        \n"+\
                    "#   #  # \n"+\
                    "# #    ##\n"+\
                    "#   #AA##\n"+\
            "2\nA;0;1\nB;5;5\n"+\
                    "1\n3;3;1\n"
    
    le_plateau=plateau.Plateau(plan1)
    affichage=JeuGraphique(le_plateau)
    affichage.demarrer()