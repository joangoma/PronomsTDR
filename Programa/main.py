import re
import spacy
from Funcions.constants import *
from thinc.config import deep_merge_configs
from Funcions.complements import *
from Funcions.funcionsVariades import arreglar_oracio
from Funcions.colocarPronoms import *
from Funcions.constants import PRONOMS

nlp = spacy.load("ca_base_web_trf")

def posiblitat_comp_obj(par, tkpar, dep, ora, tkora):
    pron = []
    pron = complement_directe(par, tkpar, dep, tkora)
    if pron == []: pron = complement_predicatiu(tkpar, dep, tkora)
    if pron == []: pron = complement_indirecte(tkpar, dep, tkora)
    if pron == []: pron = complement_regim_verbal(tkpar, dep)
    if pron == []: #me l'estic jugant, (en cas que no sigui res del d'abans ha de ser cc) no estic segur que això funcioni en tots els casos
        if len(dep) >= 1:
            if oracio_amb_de(dep): pron = ['cc', 'en'] #faltaria comprovar que fos de lloc
            else: pron = ['cc', 'hi'] 

    pron.append(dependencies_completes(dep))
    return pron

def main(s):
    cpp = ['amod', 'appos', 'nsubj']
    l = []
    t, v = True, False 
    tkora = nlp(s)
    for i, token in enumerate(tkora):
        child = [child for child in token.children]
        #print("inicial", child)
        #child = mod_dep(nlp(s), child, token)
        #print("modificat", child)
        print(token, token.morph, token.pos_, token.dep_, child)

        #comprovació si el pronom està darrere el verb
        for e in PRONOMS.keys():
            pron =  str(tkora[i-1]) + str(token)
            if pron in PRONOMS[e]: l.append(['pron', str(e), child]) 

        if possible_complement(nlp(s), token) == False:
            for e in PRONOMS.keys():
                if str(token) in PRONOMS[e]: 
                    l.append(['pron', str(token), child])
                    print (1)
                    v = True
            l_inicial = l
            if v == False:
                if str(token.dep_) == 'obj': 
                    l.append(posiblitat_comp_obj(str(token), token, child, s, tkora))
                    print(1, l)
                    if l != l_inicial: t = False
                elif str(token.dep_) == 'cop': 
                    l.append(atribut(str(token), token, child, tkora, False))
                    if l != l_inicial: t = False
                elif str(token.dep_) == 'ROOT' and atribut_semblar(nlp(s), token): 
                    l.append(atribut(str(token), token, child, tkora, True))
                    if l != l_inicial: t = False
                elif str(token.dep_) in cpp:
                    l.append(complement_predicatiu(token, child, tkora))
                    print(l)
                    if l != l_inicial: t = False
                elif str(token.dep_) == "obl":
                    l.append(complement_indirecte(token, child, s) + [child])
                    if l != l_inicial: t = False
                else:
                    pass
                    # if hi_ha_de(child):
                    #     print(1, token)
                    #     l.append(["-", "de", child])
                    #     print(l)
                    #cosa random per mirar si el complement està introduit per de substituir en
                    
            if t == False:
                l[-1].append([token])


            #si no hem afegit res en aquesta paraula, comprovem que no sigui cc
            #if t == True and pos_cc(token): l.append(['cc', 'hi', child])
            
        t = True
        v = False


    # l = [tipusDeComp, pronom, [dependències]]

    print(l)
    for i, e in enumerate(l):
        if e == [] or e == [[]] or e == [[[]]]: l.pop(i)

    frase=""
    if len(l) == 1 and l[0][0] == "pron": 
        frase = arreglar_oracio(s)
    else:
        if (len(l) == 1 and l[0] == "res") == False:
            if 'res' in l: l.pop(l.index('res'))
            if len(l) == 1: frase = pron_frase(l, s, nlp(s), False, False, l[0][-1])
            elif len(l) == 2: frase = bin_pron_frase(l, s, nlp(s))
            else: frase = s
            #print(l)
        else: print("NO HE TROBAT RES A PRONOMINALITZAR EN AQUESTA FRASE")

    return frase

def nova_S(s):
    s1 = ""
    for e in s: s1 += e.lower() 
    if s1[-1] == '.': s1 = s1[:-1]
    return s1


def entrada(s):
    if str(s) == "None": return "None"
    l = s.split()
    if len(l) > 1:
        s = nova_S(s) #la passem a minúscules
        frase = main(s)
        return frase
    else: return "None"
    # print(frase, 1)

s = "."
while s != "":
    print(entrada(str(input())))

    #falta arregalr ultima implemtació que està feta a la pàgina web