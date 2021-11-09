from Funcions.constants import PRON_BINARIES, PRONOMS
from Funcions.funcionsVariades import apostrofar_article, arreglar_oracio, dependencies_verb, verb_auxiliar
from Funcions.funcionsVariades import cal_apostrofar_bin


def pron_frase(pron, ora, tkora, binari, binCdIndet, nucliComplement):
    #['cp', 'hi', [], [nucli]]
    comp = ["obj", "ROOT", "advmod", "obl", "NMOD", "aux", "amod", 'appos']
    s = ""
    pro, dep, tip = pron[0][1], pron[0][2], pron[0][0] #rebem les dades dels paràmetres
    print(1, dep)

    print(0, pro)
    
    if binari == True and cal_apostrofar_bin(tkora) and (len(pro) > 1): pro = pro[1]
    elif len(pro) > 1 and binari == True: pro = pro[0]
    elif binari == True: pro = pro[0]
    

    if binari == False: 
        pro = apostrofar_article(pro, tkora, tip)
    
    print(1, pro)

    rDep = dependencies_verb(tkora)
    per = False

    #variables per comprovar el tema d'atributs i verbs auxiliars
    cop = False
    if tip == "atr": cop = True 
    if str(rDep[-1].dep_) == 'xcomp': per = True
    
    aux = False

    depI = []
    for i, e in enumerate(dep): 
        depI.append(e.i)
        dep[i] = str(e) #passem a string perquè no sigui tipus token

    posNuclis = []

    for i, e in enumerate(nucliComplement):
        if str(e) != "": posNuclis.append(e.i)

    print(3, depI, tip)

    if verb_auxiliar(tkora): aux = True #mirem si hi ha verb auxiliar
    for i, token in enumerate(tkora): #afegim el pronom a la frase i vigilem de no posar dependències ni coses que no toquen
        if aux and str(token.dep_) == "aux": 
            s += pro + " " + str(token) + " " + str(tkora[i+1]) + " "
        elif str(token.dep_) == 'ROOT' and aux == False and cop == False:
            s += pro + " " + str(token) + " "
        elif tip == 'atr' and str(token.dep_) == 'cop':
            s += pro + " " + str(token) + " "
        elif tip == 'atr1' and str(token.dep_) == 'ROOT':
            s += pro + " " + str(token.dep_)
        else:
            #mirem que no estiguem afegint una dependència, un verb, o el complement
            if token.i not in depI and str(token.dep_) not in comp: 
                s += str(token) + " "     
            #comprovem que no s'hagi d'afegir un complement en el cas que no es puguin pronominalitzar
            # els dos alhora        
            elif (str(token.dep_) in comp) and (token.i not in posNuclis) and (token.i not in depI) and (str(token.dep_) != "ROOT") and tip != "atr" and tip != "atr1": 
                print("es cola", token)
                s += str(token) + " "

        #ajustament amb ciIndet
        if str(token.dep_) == 'ROOT' and (tip == 'cdIndet'or binCdIndet == True) and len(dep) != 0 and per == False: s += dep[0] + " "
        elif len(rDep) > 0 and str(token) == str(rDep[-1]) and per == True and len(dep) != 0 and (tip == 'cdIndet' or binCdIndet == True): s += dep[0] + " "
    
    #s += '({0})'.format(tip)   
    s = arreglar_oracio(s)            
                                                                                                                             
    print(s) 
    return s 


def bin_pron_frase(pron, tkora): 
    #funció que retorna una llista amb les quatre combinacions possibles dels pronoms
    # retorna una llista semblant a aquesta:
    # [prnom forma reforçada, pronom forma elidida, 
    # pronom forma plena, pronom forma reduïda]

    l = ['cdDet', 'cdIndet', 'cdNeut']
    m = ["es", "et", "us", "em", "ens", "li", 
    "els (ci)", "el", "els (cd)", "la", "les", "en"]
    n = ["hi", "en", "ho", "les", "la", "els (cd)", 
    "el", "els (ci)", "li", "ens", "em", "us", "et"]

    pr1, pr2 = pron[0], pron[1]  #pr1 = [tipusDeComp, pronom, [dependències], nucli]
    nucli1, nucli2 = pr1[-1][0], pr2[-1][0]
    
    indet = False
    if pr1[0] == 'cdIndet' or pr2[0] == 'cdIndet': indet = True
    
    if pr1[0] == 'cdIndet' and pr1[-2] == []: indet = False
    if pr2[0] == 'cdIndet' and pr2[-2] == []: indet = False

    if pr1[0] in l and pr1[1] == "els": pr1[1] = "els (cd)"
    if pr2[0] in l and pr2[1] == "els": pr2[1] = "els (cd)"

    if pr1[0] == "ci" and pr1[1] == "els": pr1[1] = "els (ci)"
    if pr2[0] == "ci" and pr2[1] == "els": pr2[1] = "els (ci)"  
    
    print(pr1, pr2)

    if pr1[1] == "els":
        if pr2[0] in l: pr1[1] = "els (ci)"
        elif pr2[0] == "ci": pr1[1] = "els (cd)"
    if pr2[1] == "els":
        if pr1[0] in l: pr2[1] = "els (ci)"
        elif pr1[0] == "ci": pr2[1] = "els (cd)"

    #
    # CODI QUE AJUSTA ELS PROMS "ELS"
    #


    l = ["els (cd)", "els (ci)"]

    for e in PRONOMS.keys():
        if pr1[1] in PRONOMS[e] and pr1[0] not in l:
            pr1[1] = e
        if pr2[1] in PRONOMS[e] and pr1[0] not in l:
            pr2[1] = e

    p = []
    m1, m2, n1, n2 = -1, -1, -1, -1

    #es busca la combinació binària
    if pr1[1] in m: m1 = m.index(pr1[1])
    if pr2[1] in m: m2 = m.index(pr2[1])
    
    if pr1[1] in n: n1 = n.index(pr1[1])
    if pr2[1] in n: n2 = n.index(pr2[1])

    print(m1, n2, " ", m2, n1)
    if n2 < len(PRON_BINARIES[m1]) and n2 != -1 and m1 != -1: 
        p = PRON_BINARIES[m1][n2]
    elif n1 < len(PRON_BINARIES[m2]) and n1 != -1 and m2 != -1: 
        p = PRON_BINARIES[m2][n1]
    
    #p[0] és davant el verb, i p[1] darrere
    comen = ['a', 'e', 'i', 'o', 'u','ha', 'he', 'hi', 'ho', 'hu', 'é', 'à', 'ú', 'ò', 'í', 'ó']
    depT = pr1[2] + pr2[2]
    pT = ["bin", " ", depT]

    print(p, pT)
    
    for token in tkora:
        if str(token.dep_) == 'aux' or str(token.dep_) == 'ROOT':

            if p == []:
                print(pron[0])
                return pron_frase([pron[0]], str(tkora), tkora, False, indet, [nucli1]) + "/ " + pron_frase([pron[1]], str(tkora), tkora, False, indet, [nucli2]) #cas especial que no es poden pronominalitzar els dos complements alhora

            s = str(token)
            print(1, s)
            if s[0] in comen or s[:2] in l: 
                if len(p[0]) > 1:
                    pT[1] = [p[0][-1]] 
                    print(pT)
                    return pron_frase([pT], str(tkora), tkora, True, indet, [nucli1, nucli2])
                else:
                    pT[1] = p[0] 
                    print(pT)
                    return pron_frase([pT], str(tkora), tkora, True, indet, [nucli1, nucli2])
            else: 
                pT[1] = p[0]
                print(pT)
                return pron_frase([pT], str(tkora), tkora, True, indet, [nucli1, nucli2])
