from transition import Transition
from state import State
import os
import copy
import sp
from sp import *
from parser import Parser
from itertools import product
from automateBase import AutomateBase
from automate import *


s_a3_0 = State(0,True,False)
s_a3_1 = State(1,False,False)
s_a3_2 = State(2,False,False)
s_a3_3 = State(3,False,True)

t_a3_1 = Transition(s_a3_0,"a",s_a3_1)
t_a3_2 = Transition(s_a3_0,"a",s_a3_2)
t_a3_3 = Transition(s_a3_0,"b",s_a3_0)
t_a3_4 = Transition(s_a3_0,"b",s_a3_3)
t_a3_5 = Transition(s_a3_1,"a",s_a3_3)
t_a3_6 = Transition(s_a3_1,"b",s_a3_1)
t_a3_7 = Transition(s_a3_2,"a",s_a3_3)
t_a3_8 = Transition(s_a3_2,"a",s_a3_0)
t_a3_9 = Transition(s_a3_2,"b",s_a3_2)
t_a3_10 = Transition(s_a3_2,"b",s_a3_1)
t_a3_11 = Transition(s_a3_3,"b",s_a3_3)
t_a3_12 = Transition(s_a3_3,"a",s_a3_2)


lt_a3 = [t_a3_1,t_a3_2,t_a3_3,t_a3_4,t_a3_5,t_a3_6,t_a3_7,t_a3_8,t_a3_9,t_a3_10,t_a3_11,t_a3_12]
aut3 = Automate(lt_a3)


b1 = aut3.accepte(aut3, "babaa")
print (b1)

b2 = aut3.accepte(aut3, "abbaaa")
print (b2)

b3 = aut3.estComplet(aut3, aut3.getAlphabetFromTransitions())
print (b3)

b4 = aut3.estDeterministe(aut3)
print (b4)
