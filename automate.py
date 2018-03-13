# -*- coding: utf-8 -*-
from transition import Transition
from state import State
import os
import copy
import sp
from sp import *
from parser import Parser
from itertools import product
from automateBase import AutomateBase



class Automate(AutomateBase):
        
        def succElem(self, state, lettre):
                """State x str -> list[State]
                rend la liste des états accessibles à partir d'un état
                state par l'étiquette lettre
                """
                # successeurs : list[State]
                successeurs = []
                # t: Transitions
                for t in self.getListTransitionsFrom(state):
                        if t.etiquette == lettre and t.stateDest not in successeurs:
                                successeurs.append(t.stateDest)
                return successeurs

        def succ (self, listStates, lettre):
                """list[State] x str -> list[State]
                rend la liste des états accessibles à partir de la liste d'états
                listStates par l'étiquette lettre
                """
                #print "DEBUT succ1"
                successeurs = []
                for state in listStates:# on recupere chaque etat de cet automate
                        for t in self.succElem(state, lettre) :#on recupere toutes les lettres qui vont de cet etat
                                if (t in successeurs) == False:# On le stock dans une liste s'il n'est pas deja dedant on le met
                                        successeurs.append(t)#t.etiquette nous donne la lettre/t.stateDest nous donne vers quel etat enmène cette lettre
                return successeurs #On retourne la liste finale
               

        def acc(self):
                """ -> list[State]
                rend la liste des états accessibles
                """#verifie s'il passe par tout les etats, donc s'il n'y a pas d'etat isolé
                successeurs = []
                
                for i in self.getListTransitionFrom(self):
                        if not(i.stateDest in successeurs) :#PAS SUR QUE SA MARCHE
                                states.append(i.stateDest)
                
                return successeurs

        @staticmethod
        def accepte(auto,mot) :
                """ Automate x str -> bool
                rend True si auto accepte mot, False sinon
                """
                #succElem(self, state, lettre):
                res=auto.getListInitialStates()
                for i in mot:
     
                        res = auto.succ(res,i)
                        
                return State.isFinalIn(res)
                
        """Fonction renvoyant True si l'automate auto est complet vis-à-vis de l'alphabet alphabet,False sinon."""
        @staticmethod
        def estComplet(auto,alphabet) :
                """ Automate x str -> bool
                rend True si auto est complet pour alphabet, False sinon
                """
                #Complet si a partir de chaque etat on peux donner n'importe quel lettre du langage
                for i in auto.getListStates():#On recupere la liste des etat de l'automate
                        
                        h = auto.getListTransitionsFrom(i)#On recupere les transitions de chaque etat
                        a=[]
                        for mot in h:
                                a.append(mot.etiquette)
                        for j in alphabet :#On teste si chaque mot de l'alphabet est present sur les transitions des etats
                                
                                if j not in a :
                                        return False #Dés qu'il n'est pas present on sort du programme
                return True

        @staticmethod
        def estDeterministe(auto) :
                """ Automate  -> bool
                rend True si auto est déterministe, False sinon
                """
                #Un automate est deterministe s’il n’a qu’un seul etat initial et si, pour tout etat p, toute lettre a, il y a, au plus, une transition partant de p ´etiquet´ee par a.
                etatinit =[]
                etatinit = auto.getListInitialStates()
                
                if len(etatinit) != 1:
                        return False
                
                for state in auto.getListStates():
                        List_eti = []
                        for trans in auto.getListTransitionsFrom(state):#On met les etiquette de chaque etat dans une liste, s'il y est deja sa veut dire qu'il n'est pas deterministe, donc return false
                                if trans.etiquette in List_eti:
                                        return False
                                List_eti.append(trans.etiquette)#On ajoute les lettre si on vient de la rencontrer
                return True


       
        @staticmethod
        def completeAutomate(auto,alphabet) :
                """ Automate x str -> Automate
                rend l'automate complété d'auto, par rapport à alphabet
                """
               
                if auto.estComplet(auto, alphabet) == True :#Si l'automate est deja complet pas besoin de le completer :p 
                        return auto
                var1 = 0#on cree la variable qui va rajouter un nouvelle etat, plutot le nouveau id 
                for etat in auto.listStates :#on l'incremente jusqu'au dernier etat
                        var1 = var1 + int(etat.id)
                Netat = State(var1, False, False, "etat puit")#on crée le nouveau etat qui sera placé a la fin
                auto.addState(Netat)#on l'ajoute a l'automate
                for etat in auto.listStates :#Mnt on parcour tout les etats
                        etiquettes = []#liste poubelles pour recuperer les etiquettes
                        for transiotioon in auto.getListTransitionsFrom(etat) :#si on trouve une transition qui ne possède pas une etiquette 
                                if transiotioon.etiquette not in etiquettes:#alors on l'ajoute a la liste des etiquettes
                                        etiquettes.append(transiotioon.etiquette)
                        for lettre in alphabet :
                                if lettre not in etiquettes:#ici on cherche les lettres qui manque puis on les ajoute 
                                        auto.addTransition(Transition(etat, lettre, Netat))

                return auto
        
        @staticmethod
        def determinisation(auto) :
                """ Automate  -> Automate
                rend l'automate déterminisé d'auto
                """
                alphabet = auto.getAlphabetFromTransitions()#alphabet = la liste de mots
                finalstate = auto.getListFinalStates()
                transitions = []#liste des transitions a remplir
                Q = []#Liste des etats
                E = [[auto.getListInitialStates()]]#list des etats initiaux
                while len(E) > 0 :#tant qu'on a des etats initaux
                        S = E[0]#on prend le premier
                        E.remove(S)
                        Q.append(S)
                        for l in alphabet :
                                temp = []
                                for k in S :#pour chaque etat on parcour les transitions pour voir la lettre qui manque
                                        for t in auto.getListTransitionsFrom(k) :
                                                if t.etiquette == l and not(t.stateDest in temp) :
                                                        temp.append(t.stateDest)

                                if not(temp in Q) and not(temp in E) :#on voit si on est entrer dans le if, du coup on l'joute a E
                                        E.append(temp)

                                transitions.append(Transition(S, l, temp))#on crée une nouvelle transition et on la liste

                states = []#liste d'etat
                cpt = 0#compteur pour le nb d'etat

                
                for o in Q:#au final Q c'est tout l'automate
                        flag = False
                        for p in o :
                                if p:
                                        flag = True
                        s = State(cpt, cpt == 0, flag)
                        cpt += 1
                        states.append(s)
                transitionsFinales = []
                for m in transitions :
                        t = Transition(states[auto.indexOf(Q, m.stateSrc)], m.etiquette, states[auto.indexOf(Q, m.stateDest)])
                        transitionsFinales.append(t)
                        
                for i in finalstate:
                        auto.addState(i)

                auto = Automate(transitionsFinales)

                return auto

        @staticmethod
        def complementaire(auto, alphabet):
                """ Automate x str -> Automate
                rend  l'automate acceptant pour langage le complémentaire du langage de auto
                """
                auto_dc = auto.completeAutomate(auto, auto.getAlphabetFromTransitions())#on utilise les fonctions faites avant pour completer puisdeterminiser le programme
                auto_dc = auto.determinisation(auto_dc)
                for state in auto_dc.getListStates() :
                        if state.fin :#Tout les etat finaux deviennent non finaux, et inversement
                                state.fin = False
                        else:
                                state.fin = True
                return auto_dc


     
        @staticmethod
        def intersection (auto1, auto2):
                """ Automate x Automate -> Automate
                rend l'automate acceptant pour langage l'intersection des langages des deux automates
                """
                L = [] #liste de couples
                listeStates = [] # liste des états
                listeTrans = []
                L.append((auto1.getListInitialStates()[0] , auto2.getListInitialStates()[0] )) #couple initial
                isFinal = L[0][0].fin and L[0][1].fin
                listeStates.append(State(0 , True , isFinal)) 
                alpha1 = auto1.getAlphabetFromTransitions()
                alpha2 = auto2.getAlphabetFromTransitions()
                alpha = []
                for a  in alpha2 :
                        if a in alpha1 :
                                alpha.append(a) 
                i = 0
                j = 0
                while(i < len(L) ) :
                        for c in L[i:] :
                                for l in alpha :
                                        if len(auto1.succElem(c[0] , l)) > 0 and len(auto2.succElem(c[1], l)) > 0 :
                                                couple = (auto1.succElem(c[0] , l)[0] ,auto2.succElem(c[1], l)[0] )
                                                if couple not in L :
                                                        L.append(couple)
                                                        j = j + 1
                                                        isFinal = couple[0].fin and couple[1].fin
                                                        listeStates.append(State(j , False , isFinal ))
                                                        trans = Transition(listeStates[i] , l , listeStates[j])
                                                else :
                                                        trans = Transition(listeStates[i] , l , listeStates[L.index(couple)])
                                                if trans not in listeTrans :
                                                        listeTrans.append(trans)
                        i = i + 1
                autoInter = Automate(listeTrans)
                
                return autoInter


        @staticmethod
        def union (auto1, auto2):
                """ Automate x Automate -> Automate
                rend l'automate acceptant pour langage l'union des langages des deux automates
                """
                if not(Automate.estDeterministe(auto1)) or not(Automate.estDeterministe(auto2)) :
                        print ("Les deux automates ne sont pas déterministes donc impossible de faire l'union !")
                        return None

                alphabet = auto1.getAlphabetFromTransitions()
                alphabet.append(auto2.getAlphabetFromTransitions())#alphabet = la liste de mots

                

                
                transitions = []

                Q = []
                E = [[auto1.getListInitialStates(), auto2.getListInitialStates()]]

                zero = State(len(auto1.getListStates())+ len(auto2.getListStates()), False, False)

                while len(E) > 0 :
                        print (E)
                        S = E[0]
                        E.remove(S)
                        Q.append(S)

                        for l in alphabet :
                                temp = []
                                for t in auto1.getListTransitionsFrom(S[0]) :
                                        if t.etiquette == l and not(t.stateDest in temp) :
                                                temp.append(t.stateDest)
                                if len(temp) == 0 :
                                        temp.append(zero)

                                for t in auto2.getListTransitionsFrom(S[1]) :
                                        if t.etiquette == l and not(t.stateDest in temp) :
                                                temp.append(t.stateDest)
                                if len(temp) == 1 :
                                        temp.append(zero)

                                if not(temp in Q) and not(temp in E) and len(temp) == 2 :
                                        E.append(temp)

                                transitions.append(Transition(S, l, temp))

                states = []
                i = 0

                for o in Q :
                        
                        s = State(i, o[0] or o[1], o[0] or o[1])
                        i += 1
                        states.append(s)

                transitionsFinales = []

                for m in transitions :
                        
                        t = Transition(states[auto1.indexOf(Q, m.stateSrc)], m.etiquette, states[auto1.indexOf(Q, m.stateDest)])
                        transitionsFinales.append(t)

                auto = Automate(transitionsFinales)

                return auto


        
       
        @staticmethod
        def concatenation (auto1, auto2):
                """ Automate x Automate -> Automate
                rend l'automate acceptant pour langage la concaténation des langages des deux automates
                """
                listTrans1 = []#auto1.listTransitions()
                listState1 = []#auto1.getListStates()
                for s in auto1.getListStates():
                      listTrans1.append(auto1.getListTransitionsFrom(s))
                      listState1.append(s)

                
                initStates2 = auto2.getListInitialStates()
                
                autoC = Automate(auto1.listTransitions)# nouvel automate
                listStateC = autoC.getListStates()

                for trans1 in listTrans1:
                        
                        if (trans1 in autoC.getListFinalStates()) :
                                for state in initStates2:
                                        newTrans = (trans1[0], trans1[1], state)
                                        autoC.addTransition(newTrans)

                for stateC in listStateC :
                        if stateC.fin :
                                stateC.fin = False
                return autoC

       
        @staticmethod
        def etoile (auto):
                """ Automate  -> Automate
                rend l'automate acceptant pour langage l'étoile du langage de a
                """
                auto2 = copy.deepcopy(auto)
                alpha = auto2.getAlphabetFromTransitions()
                I = auto2.getListInitialStates()
                for s in auto2.getListStates() :
                        for e in alpha :
                                A = auto.succElem(s , e)
                                for elem in A :
                                        if elem.fin :
                                                for i in I :
                                                        auto2.addTransition(Transition(s,e,i))


                motvide = State(-1 , True , True , "eps")
                auto2.addState(motvide)
                return auto2












        
        def indexOf(self, T, S) :
                i = 0
                for t in T :
                        if t == S :
                                return i
                        i += 1
                return -1 





