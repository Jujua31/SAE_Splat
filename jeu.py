# -*- coding: utf-8 -*-
"""
                           Projet Splat_IUT'O

"""
import random

AUCUN = 0
BOMBE = 1
PISTOLET = 2
BOUCLIER = 3
BIDON = 4
NB_OBJETS = 4


class Obj1(object):
    def __init__(self, p1=False, p2=' ', p3=AUCUN, p4=None):
        self.prop1 = p1
        self.prop3 = p2
        self.prop9 = p3
        if p4==None:
            self.p5 = set()
        else:
            self.p5 = p4

    def meth1(self):
        return self.prop1

    def meth2(self):
        return self.prop3

    def meth3(self):
        return self.prop9

    def meth4(self):
        return self.p5

    def meth5(self):
        return len(self.p5)

    def meth6(self, p1):
        self.prop3 = p1
        return self.p5

    def meth7(self, p1):
        self.prop9 = p1

    def meth8(self):
        res = self.prop9
        self.prop9 = AUCUN
        return res

    def meth9(self):
        self.prop3 = ' '

    def meth10(self, p1):
        self.p5.add(p1)

    def meth11(self, p1):
        if p1 in self.p5:
            self.p5.remove(p1)
            return True
        return False


class Obj2(object):
    def __init__(self, p1, p2, p3=0):
        self.prop1 = p1
        self.prop2 = p2
        self.prop3 = [p3] * (p1 * p2)

    def meth1(self):
        return self.prop1

    def meth2(self):
        return self.prop2

    def meth3(self, pos):
        return self.prop3[pos[0] * self.prop2 + pos[1]]

    def meth4(self, p1, p2):
        self.prop3[p1[0] * self.prop2 + p1[1]] = p2

    def meth5(self, p1, p2):
        self.meth3(p2).meth10(p1)

    def meth6(self, p1, p2):
        return self.meth3(p2).meth11(p1)

    def meth7(self, p1, p2):
        self.meth3(p2).meth7(p1)

    def meth8(self, p1):
        return self.meth3(p1).meth8()


    def meth9(self, p1, p2=True):
        var1 = p1.split("\n")
        var2, var3 = var1[0].split(";")
        self.prop1 = int(var2)
        self.prop2 = int(var3)
        self.prop3 = []
        for ind in range(1, self.prop1+1):
            for car in var1[ind]:
                if car == '#' or car.islower():
                    if car == '#':
                        car=' '
                    self.prop3.append(Obj1(True,car.upper()))
                else:
                    self.prop3.append(Obj1(False,car))
        if not p2:
            return
        ind += 1
        var9 = int(var1[ind])
        for ind in range(ind+1, ind+var9+1):
            numj, lignej, colj = var1[ind].split(";")
            self.meth5(numj, (int(lignej), int(colj)))
        ind += 1
        var10 = int(var1[ind])
        for ind in range(ind+1, ind+var10+1):
            numo, ligneo, colo = var1[ind].split(";")
            self.meth7(int(numo), (int(ligneo), int(colo)))
        return var1[ind+1:]

    def meth10(self):
        res = str(self.prop1)+";"+str(self.prop2)+"\n"
        var1 = []
        var2 = []
        for var3 in range(self.prop1):
            ligne = ""
            for var4 in range(self.prop2):
                var5 = self.meth3((var3, var4))
                var6=var5.meth2()
                if var5.meth1():
                    if var6.isalpha():
                        ligne+=var6.lower()
                    else:
                        ligne += "#"
                else:
                    var7 = var5.meth3()
                    var8 = var5.meth4()
                    ligne += str(var6)
                    if var7 != AUCUN:
                        var2.append((var7, var3, var4))
                    for var14 in var8:
                        var1.append((var14, var3, var4))
            res += ligne+"\n"
        res += str(len(var1))+'\n'
        for var14, var3, var4 in var1:
            res += str(var14)+";"+str(var3)+";"+str(var4)+"\n"
        res += str(len(var2))+"\n"
        for var15, var3, var4 in var2:
            res += str(var15)+";"+str(var3)+";"+str(var4)+"\n"
        return res

    def meth11(self, p1, p2, p3, p4, p5, p6, p7=False):
        if p2 == 'N':
            inc = (-1, 0)
        elif p2 == 'S':
            inc = (1, 0)
        elif p2 == 'O':
            inc = (0, -1)
        elif p2 == 'E':
            inc = (0, 1)
        else:
            return 0, []
        if p5:
            var1 = p1
        else:
            var1 = (p1[0]+inc[0], p1[1]+inc[1])
        var2 = 0
        var3 = 0
        var4 = []
        var5=0
        while 0 <= var1[0] < self.prop1 and\
                0 <= var1[1] < self.prop2 and\
                var5<p6:
            var5+=1
            var6 = self.meth3(var1)
            if var6.meth1():
                if not p7:
                    return var3, var4
                
            if var6.meth2() in '# '+p3:
                cout=1
            else:
                cout=2
            if var3+cout>p4:
                return var3, var4
            jt = var6.meth6(p3)
            var2 += 1
            var3+=cout
            var4.extend(jt)
            var1 = (var1[0]+inc[0], var1[1]+inc[1])
        return var3, var4

    def meth12(self,p1,p2,p3):
        var1=self.meth3(p2)
        if p1 not in var1.meth4():
            return False,0,0,None
        if p3 == 'N':
            var2=(p2[0]-1,p2[1])
        elif p3 == 'S':
            var2 = (p2[0]+1, p2[1])
        elif p3 == 'O':
            var2 = (p2[0], p2[1]-1)
        elif p3 == 'E':
            var2 = (p2[0], p2[1]+1)
        else:
            return False,0,0,None
        if var2[0]<0 or var2[0]>=self.prop1 or \
                var2[1]<0 or var2[1]>=self.prop2:
            return False,0,0,None
        var3=self.meth3(var2)
        if var3.meth1():
            return False,0,0,None
        var1.meth11(p1)
        var3.meth10(p1)
        coul=var3.meth2()
        obj=var3.meth8()
        if coul==p1:
            return True,1,obj,var2
        if coul==0:
            return True,0,obj,var2
        return True,-1,obj,var2
        
    def meth13(self):
        objet=random.randint(1,NB_OBJETS)
        while True:
            ligne=random.randint(0,self.prop1-1)
            colonne=random.randint(0,self.prop2-1)
            case=self.meth3((ligne,colonne))
            if not case.meth1() and case.meth4() == set():
                case.meth7(objet)
                return (ligne,colonne)

    def meth14(self,p1):
        while True:
            var1=random.randint(0,self.prop1-1)
            var2=random.randint(0,self.prop2-1)
            var3=self.meth3((var1,var2))
            if not var3.meth1() and var3.meth4() == set():
                var3.meth10(p1)
                return (var1,var2)

    def meth15(self,p1):
        res={}
        for var1 in range(p1):
            res[chr(ord('A')+var1)]=0
        for var2 in self.prop3:
            coul=var2.meth2().upper()
            if coul!=' ':
                res[coul]+=1
        return res
    
class Obj3(object):
    def __init__(self,P1,p2,p3,p4,p5):
        self.prop1=P1
        self.prop2=p2.replace(';',',').replace('\n',' ')
        self.prop3=p3
        self.prop4=p4
        self.prop5=0
        self.prop6=0
        self.prop7=p5

    def meth1(self):
        return self.prop1
    def meth2(self):
        return self.prop2
    def meth3(self):
        return self.prop3
    def meth4(self):
        return self.prop4
    def meth5(self):
        return self.prop5
    def meth6(self):
        return self.prop7
    def meth7(self,pos):
        self.prop7=pos
    def meth8(self,p1):
        self.prop3+=p1
        return self.prop3
    def meth9(self,p1):
        self.prop4=p1

    def meth10(self,p1,p2):
        if p1==BIDON:
            self.prop3=max(self.prop3,0)
        else:
            self.prop5=p1
            self.prop6=p2

    def meth11(self,separateur=";"):
        return str(self.prop1)+separateur+str(self.prop3)+separateur+str(self.prop4)+\
            separateur+str(self.prop5)+separateur+str(self.prop6)+separateur+\
                str(self.prop7[0])+separateur+str(self.prop7[1])+separateur+self.prop2+'\n'
    def meth12(self,p1,separateur=";"):
        try:
            var1,var2,var3,var4,var5,var6,var7,var8=p1.split(separateur)
            self.prop1=var1
            self.prop3=int(var2)
            self.prop4=int(var3)
            self.prop5=int(var4)
            self.prop6=int(var5)
            self.prop7=(int(var6),int(var7))
            self.prop2=var8
        except Exception as ex:
            print("probleme construction joueur",p1)
            raise ex

    def meth13(self):
        if self.prop5!=0:
            self.prop6-=1
            if self.prop6==0:
                self.prop5=0


class Jeu(object):
    def __init__(self,nom_fic="",duree_totale=200,reserve_initiale=20,duree_obj=10,
                penalite=-2,bonus_recharge=3,bonus_objet=5, bonus_touche=5, distance_max=5):
        if nom_fic!="":
            with open(nom_fic) as fic:
                contenu=fic.read()
        else:
            return
        self.plateau=Obj2(0,0)
        self.plateau.meth9(contenu,False)
        self.les_joueurs={}
        self.duree_totale=duree_totale
        self.duree_actuelle=0
        self.nb_joueurs=0
        self.reserve_initiale=reserve_initiale
        self.duree_obj=duree_obj
        self.penalite=penalite
        self.bonus_touche=bonus_touche
        self.bonus_recharge=bonus_recharge
        self.bonus_objet=bonus_objet
        self.distance_max=distance_max

    def jeu_2_str(self,separateur=";"):
        res=str(self.duree_actuelle)+separateur+str(self.duree_totale)+separateur+\
            str(self.reserve_initiale)+separateur+\
            str(self.duree_obj)+separateur+str(self.penalite)+separateur+str(self.bonus_touche)+\
            separateur+str(self.bonus_recharge)+separateur+str(self.bonus_objet)+\
                separateur+str(self.distance_max)+'\n'
        res+="-"*20+'\n'+self.plateau.meth10()+"-"*20+'\n'
        for joueur in self.les_joueurs.values():
            res+=joueur.meth11(separateur)
        return res

    def jeu_from_str(self,chaine,separateur=';'):
        param,le_plateau,les_joueurs=chaine.split("-"*20+'\n')
        self.plateau=Obj2(1,1)
        self.plateau.meth9(le_plateau)
        self.les_joueurs={}
        for ligne in les_joueurs.split('\n'):
            if ligne!='':
                joueur=Obj3(0,'toto',0,0,(0,0))
                joueur.meth12(ligne)
                self.les_joueurs[joueur.prop1]=joueur
                self.plateau.meth5(joueur.prop1,joueur.prop7)
        # il faut récupérer les paramètres
        duree_actuelle,duree_totale,reserve_initiale,duree_obj,penalite,\
            bonus_touche,bonus_recharge,bonus_objet, distance_max=param.split(separateur)
        self.duree_actuelle=int(duree_actuelle)
        self.duree_totale=int(duree_totale)
        self.reserve_initiale=int(reserve_initiale)
        self.duree_obj=int(duree_obj)
        self.penalite=int(penalite)
        self.bonus_touche=int(bonus_touche)
        self.bonus_recharge=int(bonus_recharge)
        self.bonus_objet=int(bonus_objet)
        self.distance_max=int(distance_max)

    def inscrire_joueur(self,nom):
        coul=chr(ord('A')+self.nb_joueurs)
        self.nb_joueurs+=1
        pos=self.plateau.meth14(coul)
        self.les_joueurs[coul]=Obj3(coul,nom,self.reserve_initiale,0,pos)

    def ajouter_objet(self):
        self.plateau.meth13()

    def executer_peindre(self,couleur,joueur,direction):
        if direction not in 'XNSOE':
            joueur.meth8(self.penalite)
        if direction!='X':
            pos_joueur=joueur.meth6()
            reserve_joueur=joueur.meth3()
            objet_joueur=joueur.meth5()
            if objet_joueur in [AUCUN,PISTOLET,BOUCLIER]:
                nb_repeintes,joueurs_touches=self.plateau.meth11(pos_joueur,direction,
                                                    couleur,reserve_joueur, True, 
                                                    self.distance_max, objet_joueur==PISTOLET)
                joueur.meth8(-nb_repeintes)
            else:
                directions='NESO'
                ind=directions.index(direction)
                nb_repeintes=0
                joueurs_touches=[]
                debut=True
                for ind_2 in range(4):
                    nbr,jts=self.plateau.meth11(pos_joueur,directions[(ind+ind_2)%4],
                                                    couleur,reserve_joueur,debut,self.distance_max)
                    debut=False
                    nb_repeintes+=nbr
                    reserve_joueur-=nbr
                    joueurs_touches.extend(jts)
            
            for coul_j in joueurs_touches:
                if coul_j!=couleur:
                    joueur_touche=self.les_joueurs[coul_j]
                    if joueur_touche.meth5()!=BOUCLIER:
                        vol=min(self.bonus_touche,max(joueur_touche.meth3(),0))
                        joueur.meth8(vol)
                        joueur_touche.meth8(-vol)

    def executer_deplacer(self,couleur,joueur,direction):
        if direction not in "NESO":
            joueur.meth8(self.penalite)
            return
        pos_joueur=joueur.meth6()
        reussi,arrivee,objet,pos_arrivee=self.plateau.meth12(couleur,pos_joueur,direction)

        if not reussi:
            joueur.meth8(self.penalite)
            return
        joueur.meth7(pos_arrivee)
        if arrivee==-1:
            joueur.meth8(self.penalite)
        elif arrivee==0:
            joueur.meth8(0)
        else:
            joueur.meth8(self.bonus_recharge)
        if objet!=AUCUN:
            joueur.meth10(objet,self.duree_obj)
            joueur.meth8(self.bonus_objet)

    def executer_actions(self,couleur,actions):
        joueur=self.les_joueurs[couleur]
        if len(actions)!=2:
            joueur.meth8(2*self.penalite)
            return
        self.executer_peindre(couleur,joueur,actions[0])
        self.executer_deplacer(couleur,joueur,actions[1])
        self.les_joueurs[couleur].meth13()

    def maj_surface(self):
        couverture=self.plateau.meth15(self.nb_joueurs)
        for coul,nb_cases in couverture.items():
            self.les_joueurs[coul].meth9(nb_cases)

    def fin_tour(self):
        self.duree_actuelle+=1
        if self.duree_actuelle>=self.duree_totale:
            self.duree_actuelle=self.duree_totale
            return False
        if random.randint(1,10)==1:
            _,_=self.plateau.meth13()
        return True
            

    def tour_de_jeu(self,actions):
        melange=actions.items()
        random.shuffle(melange)
        for couleur,act in melange:
            self.executer_actions(couleur,act)
            couverture=self.plateau.meth15(self.nb_joueurs)
            for coul,nb_cases in couverture.items():
                self.les_joueurs[coul].meth9(nb_cases)
                self.les_joueurs[coul].meth13()
        self.duree_actuelle+=1
        if self.duree_actuelle>=self.duree_totale:
            self.duree_actuelle=self.duree_totale
            return False
        if random.randint(1,5)==1:
            _,_=self.plateau.meth13()
        return True

    def sauver_score(self,nom_fic):
        with open(nom_fic, "w") as fic:
            for ind_j in range(self.nb_joueurs):
                joueur = self.les_joueurs[chr(ord('A')+ind_j)]
                fic.write(
                joueur.meth2().replace(":", ".").replace(";", ",") + ";" + \
                            str(joueur.meth4() * 1000 + joueur.meth3()) + "\n")

    def classement(self):
        res=list(self.les_joueurs.values())
        res.sort(key=lambda x:x.prop4*1000+x.prop3,reverse=True)
        return res

    def get_duree_restante(self):
        return self.duree_totale-self.duree_actuelle
    
    def est_fini(self):
        return self.duree_actuelle==self.duree_totale
    