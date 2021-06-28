import spacy
from spacy import displacy

nlp = spacy.load("ca_base_web_trf")

def apostr_El_La(obj, tkora):
    #és una funció molt incompleta falta feina
    l = ['a', 'e', 'i', 'o', 'u','ha', 'he', 'hi', 'ho', 'hu']
    pron = ["el", "la", "en", "es", "et", "em"]
    if obj in pron:
        for token in tkora:
            if str(token.dep_) == 'aux' or str(token.dep_) == 'ROOT':
                s = str(token)
                #print(s)
                if s[0] in l:
                    if obj in ["el", "la"]: return "l'"
                    elif obj == 'en': return "n'"
                    elif obj == 'es': return "s'"
                    elif obj == "et": return "t'"
                    elif obj == "em": return "m'"
                else: return obj
            
    return obj

def arreOra(s):
    pass

def pron_frase(pron, ora, tkora):
    #['cp', 'hi', []]
    s = ""
    pro, dep, tip = pron[0][1], pron[0][-1], pron[0][0] #rebem les dades dels paràmetres
    rDep = rootDep(tkora)
    per = False
    if str(rDep[-1].dep_) == 'xcomp': per = True
    pro = apostr_El_La(pro, tkora)
    for i, e in enumerate(dep): dep[i] = str(e) #passem a string perquè no sigui tipus token
    aux = False
    if vAux(ora): aux = True #mirem si hi ha verb auxiliar
    for i, token in enumerate(tkora): #afegim el pronom a la frase i vigilem de no posar dependències
        if aux and str(token.dep_) == "aux": 
            s += pro + " " + str(token) + " " + str(tkora[i+1]) + " "
        elif str(token.dep_) == 'ROOT' and aux == False:
            s += pro + " " + str(token) + " "
        else:
            if str(token) not in dep and str(token.dep_) != 'obj' and token.dep_ != 'ROOT' and token.dep_ != 'aux': s += str(token) + " " 
            #mirem que no estiguem afegint una dependència, un verb, o el complement
        
        if str(token.dep_) == 'ROOT' and tip == 'cdIndet' and len(dep) != 0 and per == False: s += dep[0] + " "
        elif len(rDep) > 0 and str(token) == str(rDep[-1]) and per == True and len(dep) != 0 and tip == 'cdIndet': s += dep[0] + " "
                                                                                                                                                    
    print(s) #falta arreglar la s perquè quedi bonica :D
         

def rootDep(tkora):
    for token in tkora:
        if token.dep_ == 'ROOT':
            return [child for child in token.children]

def vAux(s): #miro si hi ha un verb auxiliar
    pr = nlp(s)
    for i, par in enumerate(pr): 
        if par.dep_ == "aux": return True

def bin_pron_frase(pron, ora, tkora):
    pass


def ap_pron(art, ora): #si hi havia un article apostrofat, comprovem quin és el gènere
    ora = nlp(ora)
    for i, token in enumerate(ora):
        if str(token) == art:
            l = str(ora[i+1].morph).split('|')
            s = l[0].split('=')
            if s[-1] == 'Fem': return 'la'
            else: return 'el'



def cd(par, tkpar, dep, ora):
    #totes les dependències que hem de comprovar per determinar el tipus de cd :D
    cdDet = ["el", "la", "els", "les", "l'", "aquest", "aquests", "aquestes", "aquesta", "aquell", "aquella", "aquells", "aquelles"]
    proDet = ["el", "la", "els", "les", "l'"]
    demostr = ["aquest", "aquesta", "aquests", "aquestes", "aquell", "aquella", "aquells", "aquelles"]
    
    cdNeut = ["això", "allò"]
    
    quant = ["massa", "força", "prou", "més", "menys", "gens", "bastant", "bastants", "gaire", "gaires", 
             "quant", "quanta", "quants", "quantes", "tant", "tanta", "tants", "molt", "molta", "molts", 
             "moltes", "poc", "poca", "pocs", "poques"]
    indef = ["un", "una", "uns", "unes"]
    
    if par in cdNeut: return ['cdNeut', 'ho'] #1. comprovació del neutre + retornar pronom ho
    if len(dep) != 0:
        if str(dep[0]) in cdDet: #2. miro si el cd és determinat + retorno el pronom corresponent
            if str(dep[0]) in demostr: 
                if demostr.index(str(dep[0])) > 3: return ['cdDet', proDet[demostr.index(str(dep[0]))-4]]
                else: return ['cdDet', proDet[demostr.index(str(dep[0]))]]
            else:
                if str(dep[0]) == "l'" or str(dep[0]) == "L'": return ['cdDet', ap_pron(str(dep[0]), ora)] #mirem quin el gènere per tornar el pronom corresponent
                else: return ['cdDet', str(dep[0])]
    #mirem si és indeterminat
    t = 0
    if str(tkpar.pos_) == 'NOUN' and dep == []: t = 1
    elif str(tkpar.pos_) == 'NOUN' and str(dep[0]) in indef: t = 1
    elif str(tkpar.pos_) == 'NOUN' and str(dep[0]) in quant: t = 1
    elif str(tkpar.pos_) == 'NOUN' and str(dep[0].pos_) == 'NUM': t = 1
    if t == 1: return ['cdIndet', 'en']
            
    return []

def cp(tkpar, dep): #si ens ha detectat obj i és adj, serà predicatiu per força.
    #falta programar elegir, fer, dir, nomenar
    if str(tkpar.pos_) == 'ADJ' and len(dep) != 0: #comprovem que tingui antecedent
        if str(dep[0]) == 'de' or str(dep[0]) == 'De': return ['cp', 'en']
    elif str(tkpar.pos_) == 'ADJ': 
        return ['cp','hi']
    
    return []

def ci(tkpar, dep):
    if str(dep[0].dep_) != 'case': return[]
    l = str(tkpar.morph).split('|')
    for e in l:
        ml = e.split('=')
        if ml[0] == 'Number': 
            if ml[-1] == 'Sing': return ['ci','li']
            elif ml[-1] == 'Plur': return ['ci', 'els']


def obj(par, tkpar, dep, ora):
    pron = []
    pron = cd(par, tkpar, dep, ora)
    if pron == []: pron = cp(tkpar, dep)
    if pron == []: pron = ci(tkpar, dep)
    if pron == []: return "res"
    pron.append(dep)
    return pron

def main(s):
    l = []
    for token in nlp(s):
        print(token, token.morph, token.pos_, token.dep_)
        if str(token.dep_) == 'obj': l.append(obj(str(token), token, [child for child in token.children], s))
        #if str(token.dep_) == 'ROOT': print([child for child in token.children])
        #if str(token.dep_) == 'obj': print([child for child in token.children], token.morph)
    #print(l)
    if (l[0] != "res"):
        if len(l) == 1: pron_frase(l, s, nlp(s))
        elif len(l) == 2: bin_pron_frase(l, s, nlp(s))
        #print(l)

def nova_S(s):
    s1 = ""
    for e in s: s1 += e.lower()
    return s1

s = "Escriu al noi"
s = nova_S(s) #la passem a minúscules
main(s)
