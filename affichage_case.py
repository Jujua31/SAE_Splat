import pygame
import os
import const
import case

class JeuGraphique(object):
    """Classe simple d'affichage d'une case."""

    def __init__(self, la_case, titre="Splat'IUT'O", size=(500, 500),
                 couleur=(209, 238, 238),
                 prefixe_image="./images"):
        """Method docstring."""
        self.la_case=la_case
        self.couleur_texte = couleur
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
        self.hauteur = round(self.surface.get_height() * 1)
        self.largeur = self.hauteur
        self.deltah = max(self.hauteur,self.largeur) 
        self.deltal = self.deltah 
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


    def demarrer(self):
        self.surface.blit(self.surface_carte(self.la_case),(0,0))
        pygame.display.flip()
        while (True):
            ev = pygame.event.wait()
            if ev.type == pygame.QUIT:
                break
            if ev.type == pygame.KEYDOWN:
                if ev.__dict__["unicode"].upper()=='Q':
                    break
            if ev.type == pygame.VIDEORESIZE:
                pygame.display.set_mode(ev.size, pygame.RESIZABLE | pygame.DOUBLEBUF)
                self.maj_parametres()
                self.surface.blit(self.surface_carte(self.la_case),(0,0))
                pygame.display.flip()
        pygame.quit()

if __name__ == '__main__':
    la_case=case.Case(False,' ',const.BOMBE,{'A','F'})
    affichage=JeuGraphique(la_case)
    affichage.demarrer()
