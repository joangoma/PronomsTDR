import spacy
from spacy import displacy

nlp = spacy.load("ca_base_web_trf")

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

def main(s):
    l = []
    for token in nlp(s):
        print(token, token.morph, token.pos_, token.dep_)
        #if str(token.dep_) == 'obj': l.append(obj(str(token), token, [child for child in token.children], s))
        #if str(token.dep_) == 'ROOT': print([child for child in token.children])

    #print(l)

s = "el pere compra patates"
main(s)