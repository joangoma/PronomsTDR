from Funcions.constants import VERBS_CONJUGATS
from Funcions.funcionsVariades import article_apostrofat_segons_genere, dependencies_completes, dependencies_verb, oracio_amb_de


def complement_directe(tkpar, dep, tkora):
    # funció que determina si un complement és DIRECTE, 
    # i el pronom adeqüat per pronminalitzar el complement

    cdDet = ["el", "la", "els", "les", "l'", "aquest", "aquests", 
            "aquestes", "aquesta", "aquell", "aquella", "aquells", "aquelles"]
    proDet = ["el", "la", "els", "les", "l'"]
    demostr = ["aquest", "aquesta", "aquests", "aquestes", 
               "aquell", "aquella", "aquells", "aquelles"]
    
    cdNeut = ["això", "allò"]
    
    quant = ["massa", "força", "prou", "més", "menys", "gens", 
             "bastant", "bastants", "gaire", "gaires", 
             "quant", "quanta", "quants", "quantes", "tant", "tanta", 
             "tants", "molt", "molta", "molts", 
             "moltes", "moltíssimes", "poc", "poca", "pocs", "poques"]    

    indef = ["un", "una", "uns", "unes"]

    prp = ['a', 'per']
    l = ["FER", "DIR", "ELEGIR", "NOMENAR"]
    morph = ['NOUN']

    verb = ""
    for token in tkora:
        if str(token.dep_) == "aux": verb += str(token) + " "
        if str(token.dep_) == "ROOT": verb += str(token)
    
    for e in l:
        if verb in VERBS_CONJUGATS[e] and tkpar.pos_ == "ADJ": return []

    if str(tkpar) in prp: return [] #si la paraula és una preposicó, es descarta automaticament

    ora = str(tkora)
    # 1r cas: comprovació del cd neutre + retornar pronom ho
    if str(tkpar) in cdNeut: return ['cdNeut', 'ho'] 

    #2n cas: comprovació si el cd és determinat + retorno el pronom corresponent
    if len(dep) != 0:
        if str(dep[0]) in cdDet: 
            t = False
            
            sig = ["'", "-"]
            l = ora.split()
            for e in l:
                for s in sig:
                    if s in e: 
                        l.remove(e)
                        l += e.split(s)

            if l[l.index(str(tkpar))-len(dep)-1] in prp: return []
            if str(dep[0]) in demostr: 
                if demostr.index(str(dep[0])) > 3: 
                    return ['cdDet', proDet[demostr.index(str(dep[0]))-4]]
                else: 
                    return ['cdDet', proDet[demostr.index(str(dep[0]))]]
            else:
                # es mira el gènere del nucli del complement respectiu per saber el gènere
                if str(dep[0]) == "l'" or str(dep[0]) == "L'": 
                    return ['cdDet', article_apostrofat_segons_genere(str(dep[0]), tkora)] 
                else: 
                    return ['cdDet', str(dep[0])]

    # 3r pas: comprovació si el cd és indeterminat + retornar pronom corresponent
    # + retornar numeral si es necessita
    t = 0
    if str(tkpar.pos_) == "NOUN" and dep == []: t = 1
    if str(tkpar.pos_) == "NOUN" and str(dep[0]) in indef: t = 1
    if str(tkpar.pos_) == "NOUN" and str(dep[0]) in quant: t = 1
    if str(tkpar.pos_) == "NOUN" and str(dep[0].pos_) == 'NUM': t = 1
    if t == 1: return ['cdIndet', 'en']
            
    return []


def complement_predicatiu(tkpar, dep, tkora): 
    # funció que determina si un complement és PREDICATIU, 
    # i el pronom adeqüat per pronminalitzar el complement

    # ALERTA: excepccio fer-se, dir-se, elegir, nomenar 
    # no funciona 
    
    l = ["FER", "DIR", "ELEGIR", "NOMENAR"]
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
                return ['cp', 'en'] #diria que s'ha de comprovar alguna altra cosa
            elif e == "ELEGIR" or e == "NOMENAR":
                return ['cp', 'en']

    if t == False:
        if str(tkpar.pos_) == 'ADJ' and len(dep) != 0: #comprovem que tingui antecedent
            if str(dep[0]) == 'de' or str(dep[0]) == 'd': return ['cp', 'en']
        if str(tkpar.pos_) == 'ADJ': 
            return ['cp','hi']

    
    return []


def atribut(tkpar, tkora, semb):
    # funció que determina si un complement és un ATRIBUT, 
    # i el pronom adeqüat per pronminalitzar el complement

    #estic ajustant tot el que no ha de sortir a la frase
    #va diferent si el verb és semblar (excepció del model)

    if semb == False:
        for token in tkora:
            if token.dep_ == 'ROOT':
                l = [child for child in token.children]
                l1 = []
                for i, e in enumerate(l):
                    if str(e.dep_) != 'nsubj':
                        l1.append(e)
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

    proDet = ["el", "la", "els", "les", "l'", "L'"]
    ora = str(tkora)

    sig = ["'", "-"]
    l = ora.split()
    for e in l:
        for s in sig:
            if s in e: 
                l.remove(e)
                l += e.split(s)

    p_1 = l.index(str(tkpar))+1 #posició de la següent paraula al verb

    if str(tkora[p_1]) in proDet:
        if str(tkora[p_1]) == "l'" or str(tkora[p_1]) == "L'": 
            return [atr, article_apostrofat_segons_genere(str(tkora[p_1]), tkora), dep] #mirem quin el gènere per tornar el pronom corresponent
        else: 
            return [atr, str(tkora[p_1]), dep]
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
    l = ['obj', 'iobj', 'obl', 'cop', 'amod', 'appos', 'ROOT']
    for token in tkora:
        child = [child for child in token.children]
        for i, c in enumerate(child):
            child[i] = str(c)

        if token != token1 and str(token.dep_) != 'ROOT':
            if str(token1) in child and str(token1.dep_) not in l: return False
    
    if str(token1.dep_) not in l: return False
    return True


def complement_indirecte(tkpar, dep, tkora): 
    # funció que determina si un complement és un COMPLEMENT INDIRECTE, 
    # i el pronom adeqüat per pronminalitzar el complement

    #PROBLEMA: he escrit una carta al diari != he escrit una carta al pere
    print(tkpar)
    pr = ['a', 'al', 'als', 'per a', 'per al', 'per als', 'per la', 'per les', "per l'", 'a el', 'a la', 'a els', 'a les', 'per a el', 'per a la', 'per a els', 'per a les']
    prp = ['a', 'per', 'al', 'als', 'pel', 'pels']
    
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
        if str(dep[0].dep_) != 'case': return[]

        s = ""
        for e in dep: s += str(e) + " " #estic passant a string una llista amb les dependències del ci
        s = s[:-1]

        l = str(tkpar.morph).split('|')
        print(2, l)
        
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








