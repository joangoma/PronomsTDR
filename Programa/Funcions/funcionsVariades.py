from Funcions.constants import VERBS_CONJUGATS

def apostrofar (obj):
    if obj in ["el", "la"]: return "l'"
    elif obj == 'en': return "n'"
    elif obj == 'es': return "s'"
    elif obj == "et": return "t'"
    elif obj == "em": return "m'"

def apostrofar_article (obj, tkora, tip):
    #és una funció molt incompleta falta feina
    l = ['a', 'e', 'i', 'o', 'u','ha', 'he', 'hi', 'ho', 'hu', 'é', 'à', 'ú', 'ò', 'í', 'ó']
    pron = ["el", "la", "en", "es", "et", "em"]
    if obj in pron:
        if tip == 'atr':
            for token in tkora:
                if str(token.dep_) == 'cop':
                    print("eo", token)
                    if str(token)[0] in l or str(token)[:2] in l:
                        return apostrofar(obj)
                    else: return obj
        elif tip == 'atr1':
            for token in tkora:
                if str(token) in VERBS_CONJUGATS['SEMBLAR']:
                    if str(token)[0] in l or str(token)[:2] in l:
                        return apostrofar(obj)
                    else: return obj
        for token in tkora:
            if str(token.dep_) == 'aux' or str(token.dep_) == 'ROOT':
                s = str(token)
                print(1, s)
                if s[0] in l or s[:2] in l:
                    return apostrofar(obj)
                else: return obj
            
    return obj

def arreglar_oracio (s):
    c = s[0].upper()
    s = s[1:]
    l = s.split()
    s1 = c
    for e in l:
        if e[-1] == "'": s1 += e 
        else: s1 += e + " "
    return s1 

def dependencies_verb (tkora):
    for token in tkora:
        if token.dep_ == 'ROOT':
            return [child for child in token.children]

def verb_auxiliar (tkora): #miro si hi ha un verb auxiliar
    for token in tkora:
        if str(token.dep_) == "aux": return True

    return False

def article_apostrofat_segons_genere(art, tkora): 
    #si hi ha un article apostrofat, comprovem quin és el gènere

    for i, token in enumerate(tkora):
        if str(token) == art:
            l = str(tkora[i+1].morph).split('|')
            s = l[0].split('=')
            if s[-1] == 'Fem': return 'la'
            else: return 'el'

def dependencies_completes (dep):
    l = []
    for e in dep:
        l.append(e)
        child = [f for f in e.children]
        if child != []:
            for el in child:
                dep.append(el)
    return l

def oracio_amb_de (child):
    child = dependencies_completes(child)
    print(child)
    l = ["de", "d'", "del"]
    for e in child:
        # print(type(str(e)), l, e.pos_)
        if str(e) in l and str(e.pos_) == "ADP": 
            print("eo")
            return True

    return False

def modificar_dependencies (tkora, child, token): 
    #funció que modifica les dependències en cas que siguin errònies.
    #majoritàriament afegeix preposicions que no s'inclouen.
    #cal revisar que no faci que alguns CD no funcionin.

    prp = ['a', 'per', 'al', 'als', 'pel', 'pels']
    #print(type(token))

    l = str(tkora).split()
    l1 = []
    for e in child:
        l1.append(str(e))

    if token.dep_ == "obj":
        i = 0
        for paraula in l:
            if (i + len(child)) < len(l):
                if str(paraula) == str(child[0]) and l1 == l[i:i+len(child)]:
                    if str(l[i-1]) in prp: 
                        for p in range(len(tkora)):
                            if p == i-1:
                                return [tkora[p]] + child

            i += 1

    return child
