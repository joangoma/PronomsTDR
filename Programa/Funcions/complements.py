from Funcions.constants import VERBS_CONJUGATS
from Funcions.funcionsVariades import article_apostrofat_segons_genere, dependencies_completes, dependencies_verb, oracio_amb_de


def complement_directe(par, tkpar, dep, tkora):
    # funció que determina si un complement és DIRECTE, 
    # i el pronom adeqüat per pronminalitzar el complement

    cdDet = ["el", "la", "els", "les", "l'", "aquest", "aquests", "aquestes", "aquesta", "aquell", "aquella", "aquells", "aquelles"]
    proDet = ["el", "la", "els", "les", "l'"]
    demostr = ["aquest", "aquesta", "aquests", "aquestes", "aquell", "aquella", "aquells", "aquelles"]
    
    cdNeut = ["això", "allò"]
    
    quant = ["massa", "força", "prou", "més", "menys", "gens", "bastant", "bastants", "gaire", "gaires", 
             "quant", "quanta", "quants", "quantes", "tant", "tanta", "tants", "molt", "molta", "molts", 
             "moltes", "poc", "poca", "pocs", "poques"]
    indef = ["un", "una", "uns", "unes"]
    prp = ['a', 'per']
    morph = ['NOUN']
    
    l = ["FER", "DIR", "ELEGIR", "NOMENAR"]
    
    verb = ""
    for token in tkora:
        if str(token.dep_) == "aux": verb += str(token) + " "
        if str(token.dep_) == "ROOT": verb += str(token)
    
    for e in l:
        if verb in VERBS_CONJUGATS[e] and tkpar.pos_ == "ADJ": return []

    ora = str(tkora)
    # 1r cas: comprovació del cd neutre + retornar pronom ho
    if par in cdNeut: return ['cdNeut', 'ho'] 

    #2n cas: comprovació si el cd és determinat + retorno el pronom corresponent
    if len(dep) != 0:
        if str(dep[0]) in cdDet: 
            sig = ["'", "-"]
            t = False
            l = ora.split()
            for e in l:
                for s in sig:
                    if s in e: 
                        l.remove(e)
                        l += e.split(s)
            if l[l.index(str(par))-len(dep)-1] in prp: return []
            if str(dep[0]) in demostr: 
                if demostr.index(str(dep[0])) > 3: return ['cdDet', proDet[demostr.index(str(dep[0]))-4]]
                else: return ['cdDet', proDet[demostr.index(str(dep[0]))]]
            else:
                # es mira el gènere del nucli del complement respectiu per saber el gènere
                if str(dep[0]) == "l'" or str(dep[0]) == "L'": return ['cdDet', article_apostrofat_segons_genere(str(dep[0]), ora)] 
                else: return ['cdDet', str(dep[0])]

    if str(tkpar) in prp: return [] #si la paraula és una preposicó, es descarta automaticament

    # 3r pas: comprovació si el cd és indeterminat + retornar pronom corresponent
    # + retornar numeral si es necessita
    t = 0
    if str(tkpar.pos_) in morph and dep == []: t = 1
    elif str(tkpar.pos_) in morph and str(dep[0]) in indef: t = 1
    elif str(tkpar.pos_) in morph and str(dep[0]) in quant: t = 1
    elif str(tkpar.pos_) in morph and str(dep[0].pos_) == 'NUM': t = 1
    if t == 1: return ['cdIndet', 'en']
            
    return []


def complement_predicatiu(tkpar, dep, tkora): 
    # funció que determina si un complement és PREDICATIU, 
    # i el pronom adeqüat per pronminalitzar el complement

    # ALERTA: excepccio fer-se, dir-se, elegir, nomenar 
    # no funciona 
    
    l = ["FER", "DIR", "ELEGIR", "NOMENAR"]
    pron = dependencies_completes(dep)
    verb = ""
    for token in tkora:
        if str(token.dep_) == "aux": verb += str(token) + " "
        if str(token.dep_) == "ROOT": verb += str(token)
    
    
    # això no funciona
    t = False
    for e in l:
        if verb in VERBS_CONJUGATS[e]:
            if e == "FER" or e == "DIR":
                if str(tkpar.pos_) == 'NOUN': return []
                return ['cp', 'en', pron] #diria que s'ha de comprovar alguna altra cosa
            elif e == "ELEGIR" or e == "NOMENAR":
                return ['cp', 'en', pron]

    if t == False:
        if str(tkpar.pos_) == 'ADJ' and len(dep) != 0: #comprovem que tingui antecedent
            if str(dep[0]) == 'de' or str(dep[0]) == 'd': return ['cp', 'en', pron]
        if str(tkpar.pos_) == 'ADJ': 
            return ['cp','hi', pron]

    
    return []


def atribut(par, tkpar, dep, tkora, semb):
    # funció que determina si un complement és un ATRIBUT, 
    # i el pronom adeqüat per pronminalitzar el complement

    #estic ajustant tot el que no ha de sortir a la frase
    #va diferent si el verb és semblar (excepció del model)

    if semb == False:
        for token in tkora:
            if token.dep_ == 'ROOT':
                l = [child for child in token.children]
                l1 = []
                l2 = [child for child in token.children]
                for i, e in enumerate(l):
                    if str(e.dep_) != 'nsubj':
                        l1.append(e)
                        l2.append(e)
                l = l1

    else:
        for token in tkora:
            if token.dep_ == 'ROOT':
                l = [child for child in token.children]
                l1 = []
                for i, e in enumerate(l):
                    if str(e.dep_) == 'ccomp':
                        l1.append(e)
                        for c in e.children:
                            l1.append(c) #estem afegint les dependències del ccomp

        l = l1

    dep = l
    print(dep)
    dep = dependencies_completes(dep)
    #print(dep, par)
    #miro el tipus de atr i retorno el pronom corresponent

    if semb == True: atr = "atr1"
    else : atr = "atr"

    proDet = ["el", "la", "els", "les", "l'"]
    ora = str(tkora)
    l = ora.split()
    p_1 = l.index(par)+1 #posició de la següent paraula al verb
    
    if l[p_1] in proDet:
        if l[p_1] == "l'" or l[p_1] == "L'": return [atr, article_apostrofat_segons_genere(l[p_1], ora), dep] #mirem quin el gènere per tornar el pronom corresponent
        else: return [atr, l[p_1], dep]
    else:
        return [atr, 'ho', dep]


def atribut_semblar(tkora, token): 
    #l'spacy no detecta sembla com a verb copulatiu, 
    # llavors he de fer hardcode perquè el detecti
    if str(token) in VERBS_CONJUGATS['SEMBLAR']: return True
    else: return False
    #FUNCIÓ QUE SEGURAMENT S'HAURÀ DE POLIR

def possible_complement(tkora, token1): 
    #es comprova que el complement no sigui un complement del nom 
    l = ['obj', 'iobj', 'obl', 'cop', 'amod', 'appos', 'nsubj']
    for token in tkora:
        child = [child for child in token.children]
        for i, c in enumerate(child):
            child[i] = str(c)

        if token != token1 and str(token.dep_) != 'ROOT':
            if str(token1) in child and str(token1.dep_) not in l: return False
    
    if str(token1.dep_) not in l: return False
    return True


def complement_indirecte(tkpar, dep, tkora): 
    # funció que determina si un complement és un ATRIBUT, 
    # i el pronom adeqüat per pronminalitzar el complement

    #PROBLEMA: he escrit una carta al diari != he escrit una carta al pere
    print(tkpar)
    pr = ['a', 'al', 'als', 'per a', 'per al', 'per als', 'per la', 'per les', "per l'", 'a el', 'a la', 'a els', 'a les', 'per a el', 'per a la', 'per a els', 'per a les']
    prp = ['a', 'per', 'al', 'als']
    sig = ["'", "-"]
    t = False
    l = str(tkora).split()
    for e in l:
        for s in sig:
            if s in e: 
                l.remove(e)
                l += e.split(s)

    #comprovem que no sigui un atr
    for e in tkora:
        if str(e.dep_) == "cop": return []
        elif str(e) in VERBS_CONJUGATS['SEMBLAR']: return []

    if len(dep) >= 1:
        if l.index(str(tkpar))-len(dep)-1 >= 0:
            if l[l.index(str(tkpar))-len(dep)-1] in prp: t = True
        elif str(dep[0].dep_) != 'case': return[]
        l = str(tkpar.morph).split('|')
        print(2, l)
        s = ""
        for e in dep: s += str(e) + " " #estic passant a string una llista amb les dependències del ci
        s = s[:-1]
        if str(dep[0]) in prp or t:
            for e in l:
                ml = e.split('=')
                print(1, ml)
                if ml[0] == 'Number': 
                    print(3)
                    if ml[-1] == 'Sing': return ['ci','li']
                    elif ml[-1] == 'Plur': return ['ci', 'els']
    return []

def complement_regim_verbal(tkpar, dep):
    # funció que determina si un complement és un COMPLEMENT DE RÈGIM VERBAL, 
    # i el pronom adeqüat per pronminalitzar el complement
     
    # print (tkpar, dep)
    # si va introduit per de, està programat a banda per no interferir
    
    pr = ["a", "de", "en", "amb", "per"] 
    for e in dep:
        if str(e) in pr: 
            if oracio_amb_de(dep): return ["crv", "en"]
            else: return ["crv", "hi"]

    return []

def complement_circumstancial(par):
    # funció que determina si un complement és un COMPLEMENT CIRCUMSTANCIAL, 
    # i el pronom adeqüat per pronminalitzar el complement

    #ALERTA: NO ESTÀ OPERATIVA, FALTEN MOLTES MILLORES

    l = ["advmod", "obl", "nmod"]

    if str(par.dep_) in l: return True
    else: return False






