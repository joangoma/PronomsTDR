import re
import spacy
from spacy import displacy
from thinc.config import deep_merge_configs

nlp = spacy.load("ca_base_web_trf")

#DICCIONARI AMB CONJUGACIONS VERBALS NECEESSARIES PER COMPROVAR CERTS COMPLEMENTS
#SEMBLAR, ELEGIR, NOMENAR (falta), FER-SE, DIR-SE

d = {'SEMBLAR': ['semblo', 'sembles', 'sembla', 'semblem', 'sembleu', 'semblen', 'he semblat', 'has semblat', 'ha semblat', 'hem semblat', 'heu semblat', 'han semblat', 'semblava', 'semblaves', 'semblava', 'semblàvem', 'semblàveu', 'semblaven', 'havia semblat', 'havies semblat', 'havia semblat', 'havíem semblat', 'havíeu semblat', 'havien semblat', 'semblí', 'semblares', 'semblà', 'semblàrem', 'semblàreu', 'semblaren', 'haguí semblat', 'hagueres semblat', 'hagué semblat', 'haguérem semblat', 'haguéreu semblat', 'hagueren semblat', 'vaig semblar', 'vas semblar', 'va semblar', 'vam semblar', 'vau semblar', 'van semblar', 'vaig haver semblat', 'vas haver semblat', 'va haver semblat', 'vam haver semblat', 'vau haver semblat', 'van haver semblat', 'semblaré', 'semblaràs', 'semblarà', 'semblarem', 'semblareu', 'semblaran', 'hauré semblat', 'hauràs semblat', 'haurà semblat', 'haurem semblat', 'haureu semblat', 'hauran semblat', 'semblaria', 'semblaries', 'semblaria', 'semblaríem', 'semblaríeu', 'semblarien', 'hauria semblat', 'hauries semblat', 'hauria semblat', 'hauríem semblat', 'hauríeu semblat', 'haurien semblat', 'haguera semblat', 'hagueres semblat', 'haguera semblat', 'haguérem semblat', 'haguéreu semblat', 'hagueren semblat', 'sembli', 'semblis', 'sembli', 'semblem', 'sembleu', 'semblin', 'semblés', 'semblessis', 'semblés', 'sembléssim', 'sembléssiu', 'semblessin', 'hagi semblat', 'hagis semblat', 'hagi semblat', 'hàgim semblat', 'hàgiu semblat', 'hagin semblat', 'hagués semblat', 'haguessis semblat', 'hagués semblat', 'haguéssim semblat', 'haguéssiu semblat', 'haguessin semblat', 'sembla', 'sembli', 'semblem', 'sembleu', 'semblin'], 
    "ELEGIR" : ['elegeixo', 'elegeixes', 'elegeix', 'elegim', 'elegiu', 'elegeixen', 'he elegit', 'has elegit', 'ha elegit', 'hem elegit', 'heu elegit', 'han elegit', 'elegia', 'elegies', 'elegia', 'elegíem', 'elegíeu', 'elegien', 'havia elegit', 'havies elegit', 'havia elegit', 'havíem elegit', 'havíeu elegit', 'havien elegit', 'elegí', 'elegires', 'elegí', 'elegírem', 'elegíreu', 'elegiren', 'haguí elegit', 'hagueres elegit', 'hagué elegit', 'haguérem elegit', 'haguéreu elegit', 'hagueren elegit', 'vaig elegir', 'vas elegir', 'va elegir', 'vam elegir', 'vau elegir', 'van elegir', 'vaig haver elegit', 'vas haver elegit', 'va haver elegit', 'vam haver elegit', 'vau haver elegit', 'van haver elegit', 'elegiré', 'elegiràs', 'elegirà', 'elegirem', 'elegireu', 'elegiran', 'hauré elegit', 'hauràs elegit', 'haurà elegit', 'haurem elegit', 'haureu elegit', 'hauran elegit', 'elegiria', 'elegiries', 'elegiria', 'elegiríem', 'elegiríeu', 'elegirien', 'hauria elegit', 'hauries elegit', 'hauria elegit', 'hauríem elegit', 'hauríeu elegit', 'haurien elegit', 'haguera elegit', 'hagueres elegit', 'haguera elegit', 'haguérem elegit', 'haguéreu elegit', 'hagueren elegit', 'elegeixi', 'elegeixis', 'elegeixi', 'elegim', 'elegiu', 'elegeixin', 'elegís', 'elegissis', 'elegís', 'elegíssim', 'elegíssiu', 'elegissin', 'hagi elegit', 'hagis elegit', 'hagi elegit', 'hàgim elegit', 'hàgiu elegit', 'hagin elegit', 'hagués elegit', 'haguessis elegit', 'hagués elegit', 'haguéssim elegit', 'haguéssiu elegit', 'haguessin elegit', 'elegeix', 'elegeixi', 'elegim', 'elegiu', 'elegeixin'],
    "DIR": ['dic', 'dius', 'diu', 'diem', 'dieu', 'diuen', 'he dit', 'has dit', 'ha dit', 'hem dit', 'heu dit', 'han dit', 'deia', 'deias', 'deia', 'dèiem', 'dèieu', 'deien', 'havia dit', 'havies dit', 'havia dit', 'havíem dit', 'havíeu dit', 'havien dit', 'diguí', 'digueres', 'digué', 'diguérem', 'diguéreu', 'digueren', 'haguí dit', 'hagueres dit', 'hagué dit', 'haguérem dit', 'haguéreu dit', 'hagueren dit', 'vaig dir', 'vas dir', 'va dir', 'vam dir', 'vau dir', 'van dir', 'vaig haver dit', 'vas haver dit', 'va haver dit', 'vam haver dit', 'vau haver dit', 'van haver dit', 'diré', 'diràs', 'dirà', 'direm', 'direu', 'diran', 'hauré dit', 'hauràs dit', 'haurà dit', 'haurem dit', 'haureu dit', 'hauran dit', 'diria', 'diries', 'diria', 'diríem', 'diríeu', 'dirien', 'hauria dit', 'hauries dit', 'hauria dit', 'hauríem dit', 'hauríeu dit', 'haurien dit', 'haguera dit', 'hagueres dit', 'haguera dit', 'haguérem dit', 'haguéreu dit', 'hagueren dit', 'digui', 'diguis', 'digui', 'diguem', 'digueu', 'diguin', 'digués', 'diguessis', 'digués', 'diguéssim', 'diguéssiu', 'diguessin', 'hagi dit', 'hagis dit', 'hagi dit', 'hàgim dit', 'hàgiu dit', 'hagin dit', 'hagués dit', 'haguessis dit', 'hagués dit', 'haguéssim dit', 'haguéssiu dit', 'haguessin dit', 'digues', 'digui', 'diguem', 'digueu', 'diguin', 'dir', 'haver dit', 'dient', 'havent dit', 'dit', 'dita', 'dits', 'dites'],
    "FER": ['faig', 'fas', 'fa', 'fem', 'feu', 'fan', 'he fet', 'has fet', 'ha fet', 'hem fet', 'heu fet', 'han fet', 'feia', 'feies', 'feia', 'fèiem', 'fèieu', 'feien', 'havia fet', 'havies fet', 'havia fet', 'havíem fet', 'havíeu fet', 'havien fet', 'fiu', 'feres', 'féu', 'férem', 'féreu', 'feren', 'haguí fet', 'hagueres fet', 'hagué fet', 'haguérem fet', 'haguéreu fet', 'hagueren fet', 'vaig fer', 'vas fer', 'va fer', 'vam fer', 'vau fer', 'van fer', 'vaig haver fet', 'vas haver fet', 'va haver fet', 'vam haver fet', 'vau haver fet', 'van haver fet', 'faré', 'faràs', 'farà', 'farem', 'fareu', 'faran', 'hauré fet', 'hauràs fet', 'haurà fet', 'haurem fet', 'haureu fet', 'hauran fet', 'faria', 'faries', 'faria', 'faríem', 'faríeu', 'farien', 'hauria fet', 'hauries fet', 'hauria fet', 'hauríem fet', 'hauríeu fet', 'haurien fet', 'haguera fet', 'hagueres fet', 'haguera fet', 'haguérem fet', 'haguéreu fet', 'hagueren fet', 'faci', 'facis', 'faci', 'fem', 'feu', 'facin', 'fes', 'fessis', 'fes', 'féssim', 'féssiu', 'fessin', 'hagi fet', 'hagis fet', 'hagi fet', 'hàgim fet', 'hàgiu fet', 'hagin fet', 'hagués fet', 'haguessis fet', 'hagués fet', 'haguéssim fet', 'haguéssiu fet', 'haguessin fet', 'fes', 'faci', 'fem/ facem', 'feu', 'facin'],
    "NOMENAR": ['nomeno', 'nomene', 'nomèn', 'nomenes', 'nomena', 'nomenem', 'nomenam', 'nomene', 'nomenau', 'nomenen', 'he nomenat', 'has nomenat', 'ha nomenat', 'hem nomenat', 'heu nomenat', 'han nomenat', 'nomenava', 'nomenaves', 'nomenava', 'nomenàvem', 'nomenàveu', 'nomenaven', 'havia nomenat', 'havies nomenat', 'havia nomenat', 'havíem nomenat', 'havíeu nomenat', 'havien nomenat', 'nomení', 'nomenares', 'nomenà', 'nomenàrem', 'vós nomenàreu', 'nomenaren', 'vaig nomenar', 'vas nomenar', 'vares nomenar', 'va nomenar', 'vam nomenar', 'vàrem nomenar', 'vau nomenar', 'van nomenar', 'haguí nomenat', 'hagueres nomenat', 'hagué nomenat', 'haguérem nomenat', 'haguéreu nomenat', 'hagueren nomenat', 'vaig haver nomenat', 'vas haver nomenat', 'va haver nomenat', 'vam haver nomenat', 'vau haver nomenat', 'van haver nomenat', 'nomenaré', 'nomenaràs', 'nomenarà', 'nomenarem', 'nomenareu', 'nomenaran', 'hauré nomenat', 'hauràs nomenat', 'haurà nomenat', 'haurem nomenat', 'haureu nomenat', 'hauran nomenat', 'nomenaria', 'nomenaries', 'nomenaria', 'nomenaríem', 'nomenaríeu', 'nomenarien', 'hauria nomenat', 'hauries nomenat', 'hauria nomenat', 'hauríem nomenat', 'hauríeu nomenat', 'haurien nomenat']
    }

def apostr_El_La(obj, tkora, tip):
    #és una funció molt incompleta falta feina
    l = ['a', 'e', 'i', 'o', 'u','ha', 'he', 'hi', 'ho', 'hu', 'é', 'à', 'ú', 'ò', 'í', 'ó']
    pron = ["el", "la", "en", "es", "et", "em"]
    if obj in pron:
        if tip == 'atr':
            for token in tkora:
                if str(token.dep_) == 'cop':
                    print("eo", token)
                    if str(token)[0] in l or str(token)[:2] in l:
                        if obj in ["el", "la"]: return "l'"
                        elif obj == 'en': return "n'"
                        elif obj == 'es': return "s'"
                        elif obj == "et": return "t'"
                        elif obj == "em": return "m'"
                    else: return obj
        elif tip == 'atr1':
            for token in tkora:
                if str(token) in d['SEMBLAR']:
                    if str(token)[0] in l or str(token)[:2] in l:
                        if obj in ["el", "la"]: return "l'"
                        elif obj == 'en': return "n'"
                        elif obj == 'es': return "s'"
                        elif obj == "et": return "t'"
                        elif obj == "em": return "m'"
                    else: return obj
        for token in tkora:
            if str(token.dep_) == 'aux' or str(token.dep_) == 'ROOT':
                s = str(token)
                print(1, s)
                if s[0] in l or s[:2] in l:
                    if obj in ["el", "la"]: return "l'"
                    elif obj == 'en': return "n'"
                    elif obj == 'es': return "s'"
                    elif obj == "et": return "t'"
                    elif obj == "em": return "m'"
                else: return obj
            
    return obj

def arreOra(s):
    l = s.split()
    s1 = ""
    for e in l:
       s1 += e + " "
    s1[0].upper()
    return s1 

def pron_frase(pron, ora, tkora, binari):
    #['cp', 'hi', []]
    comp = ["obj", "ROOT", "advmod", "obl", "NMOD", "aux"]
    s = ""
    pro, dep, tip = pron[0][1], pron[0][-1], pron[0][0] #rebem les dades dels paràmetres
    #print(1, pro, dep, tip)
    if binari == True: pro = pro[0]
    rDep = rootDep(tkora)
    per = False

    #variables per comprovar el tema d'atributs i verbs auxiliars
    cop = False
    if tip == "atr": cop = True 
    if str(rDep[-1].dep_) == 'xcomp': per = True
    aux = False
    print(0, pro)
    if binari == False: pro = apostr_El_La(pro, tkora, tip)
    print(1, pro)
    depI = []
    for i, e in enumerate(dep): 
        depI.append(e.i)
        dep[i] = str(e) #passem a string perquè no sigui tipus token

    print(depI)

    if vAux(ora): aux = True #mirem si hi ha verb auxiliar
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
            if token.i not in depI and str(token.dep_) not in comp: s += str(token) + " " 
            #mirem que no estiguem afegint una dependència, un verb, o el complement
        

        #ajustament amb ciIndet
        if str(token.dep_) == 'ROOT' and tip == 'cdIndet' and len(dep) != 0 and per == False: s += dep[0] + " "
        elif len(rDep) > 0 and str(token) == str(rDep[-1]) and per == True and len(dep) != 0 and tip == 'cdIndet': s += dep[0] + " "
    
    s += '({0})'.format(tip)   
    s = arreOra(s)                                                                                                                                           
    print(s) #falta arreglar la s perquè quedi bonica :D
         

def rootDep(tkora):
    for token in tkora:
        if token.dep_ == 'ROOT':
            return [child for child in token.children]

def vAux(s): #miro si hi ha un verb auxiliar
    pr = nlp(s)
    for i, par in enumerate(pr): 
        if par.dep_ == "aux": return True


def bin_pron_frase(pron, ora, tkora): #funció que retorna una llista amb les quatre combinacions possibles dels pronoms
                                      #[davant apostrofat, davant sense ap, darre1, darrere 2]

    l = ['cdDet', 'cdIndet', 'cdNeut']

    m, n = [], []
    m = ["es", "et", "us", "em", "ens", "li", "els (ci)", "el", "els (cd)", "la", "les", "en"]
    n = ["hi", "en", "ho", "les", "la", "els (cd)", "el", "els (ci)", "li", "ens", "em", "us", "et"]

    comb = [[[["s'hi"], ["-s'hi"]], [["se'n", "se n'"], ["-se'n"]], [["s'ho"], ["-s'ho"]], [["se les"], ["-se-les"]], [["se la", "se l'"], ["-se-la"]], [["se'ls"], ["-se'ls"]], [["se'ls"], ["-se'ls"]], [["se'ls"], ["-se'ls"]], [["se li"], ["-se-li"]], [["se'ns"], ["-se'ns"]], [["se'm", "se m'"], ["-se'm"]], [["se us"], ["-se-us"]], [["se't", "se t'"], ["-se't"]]], 
    [[["t'hi"], ["-t'hi"]], [["te'n", "te n'"], ["te'n"]], [["t'ho"], ["-t'ho"]], [["te les"], ["-te-les"]], [["te la", "te l'"], ["-te-la"]], [["te'ls"], ["-te'ls"]], [["te'l", "te l'"], ["-te'l"]], [["te'ls"], ["-te'ls"]], [["te li"], ["-te-li"]], [["te'ns"], ["-te'ns"]], [["te'm", "te m'"], ["-te'm"]]], 
    [[["us hi"], ["-vos-hi", "-us-hi"]], [["us en", "us n'"], ["-vos-en", "-us-en"]], [["us ho"], ["-vos-ho", "-us-ho"]], [["us les"], ["-vos-les", "-us-les"]], [["us la", "us l'"], ["-vos-la", "-us-la"]], [["us els"], ["vos-els", "-us-els"]], [["us el", "us l'"], ["-vos-el", "-us-el"]], [["us els"], ["-vos-els", "-us-els"]], [["us li"], ["-vos-li", "-us-li"]], [["us ens"], ["-vos-ens", "-us-ens"]], [["us em", "us m'"], ["-vos-em", "-us-em"]]], 
    [[["m'hi"], ["-m'hi"]], [["me'n", "me n'"], ["-me'n"]], [["m'ho"], ["-m'ho"]], [["me les"], ["me-les"]], [["me la", "me l'"], ["-me-la"]], [["me'ls"], ["-me'ls"]], [["me'l", "me l'"], ["-me'l"]], [["me'ls"], ["-me'ls"]], [["me li"], ["me-li"]]], 
    [[["ens hi"], ["-nos hi", "'ns-hi"]], [["ens en", "ens n'"], ["-nos-en", "'ns-en"]], [["ens ho"], ["-nos-ho", "'ns-ho"]], [["ens les"], ["-nos-les", "'ns-les"]], [["ens la", "ens l'"], ["-nos-la", "'ns-la"]], [["ens els"], ["-nos-els", "'ns-els"]], [["ens el"], ["-nos-el", "'ns-el"]], [["ens els"], ["-nos-els", "'ns-els"]], [["ens li"], ["-nos-li", "'ns-li"]]], 
    [[["li hi"], ["-li-hi"]], [["li'n", "li n'"], ["-li'n"]], [["li ho"], ["-li-ho"]], [["les hi"], ["-les-hi"]], [["la hi"], ["-la-hi"]], [["els hi"], ["-los-hi", "'ls-hi"]], [["l'hi"], ["-l'hi"]]], 
    [[["els hi"], ["-los hi", "'ls-hi"]], [["els en", "els n'"], ["-los-en", "'ls-en"]], [["els ho"], ["-los-ho", "'ls-ho"]], [["els les"], ["-los-les", "'ls-les"]], [["els la", "els l'"], ["-los-la", "'ls-la"]], [["els els"], ["-los-els", "'ls-els"]], [["els el", "els l'"], ["-los-el", "'ls-el"]]], 
    [[["l'hi"], ["-l'hi"]], [["le'n", "el n'"], ["-l'en"]]], 
    [[["els hi"], ["-los-hi", "'ls-hi"]], [["els en", "els n'"], ["-los-en", "'ls-en"]]], 
    [[["la hi"], ["-la-hi"]], [["la'n", "la n'"], ["-la'n"]]], 
    [[["les hi"], ["-les-hi"]], [["les en", "les n'"], ["-les-en"]]], 
    [[["n'hi"], ["-n'hi"]]]]
        
    pr1, pr2 = pron[0], pron[1]  #pr1 = [tipusDeComp, pronom, [dependències]]
    
    if pr1[0] in l and pr1[1] == "els": pr1[1] = "els (cd)"
    if pr2[0] in l and pr2[1] == "els": pr2[1] = "els (cd)"

    if pr1[0] == "ci" and pr1[1] == "els": pr1[1] = "els (ci)"
    if pr2[0] == "ci" and pr2[1] == "els": pr2[1] = "els (ci)"  
    
    print(pr1, pr2)
    p = []
    m1, m2, n1, n2 = -1, -1, -1, -1

    #es busca la combinació binària
    if pr1[1] in m: m1 = m.index(pr1[1])
    if pr2[1] in m: m2 = m.index(pr2[1])
    
    if pr1[1] in n: n1 = n.index(pr1[1])
    if pr2[1] in n: n2 = n.index(pr2[1])

    depT = pr1[2] + pr2[2]

    print(m1, n2, " ", m2, n1)

    if n2 < len(comb[m1]): p = comb[m1][n2]
    elif n1 < len(comb[m2]): p = comb[m2][n1]
    
    #p[0] és davant el verb, i p[1] darrere
    comen = ['a', 'e', 'i', 'o', 'u','ha', 'he', 'hi', 'ho', 'hu', 'é', 'à', 'ú', 'ò', 'í', 'ó']

    pT = ["bin", " ", depT]

    print(p, pT)
    
    for token in tkora:
        if str(token.dep_) == 'aux' or str(token.dep_) == 'ROOT':
            s = str(token)
            print(1, s)
            if s[0] in comen or s[:2] in l: 
                if len(p[0]) > 1:
                    pT[1] = [p[0][-1]] 
                    print(pT)
                    pron_frase([pT], str(tkora), tkora, True)
                else:
                    pT[1] = p[0] 
                    print(pT)
                    pron_frase([pT], str(tkora), tkora, True)
            else: 
                pT[1] = p[0]
                print(pT)
                pron_frase([pT], str(tkora), tkora, True)
    



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

    prp = ['a', 'per']

    morph = ['NOUN']
    
    l = ["FER", "DIR", "ELEGIR", "NOMENAR"]
    
    verb = ""
    for token in nlp(ora):
        if str(token.dep_) == "aux": verb += str(token) + " "
        if str(token.dep_) == "ROOT": verb += str(token)
    
    for e in l:
        if verb in d[e] and tkpar.pos_ == "ADJ": return []

    if par in cdNeut: return ['cdNeut', 'ho'] #1. comprovació del neutre + retornar pronom ho
    if len(dep) != 0:
        if str(dep[0]) in cdDet: #2. miro si el cd és determinat + retorno el pronom corresponent
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
                if str(dep[0]) == "l'" or str(dep[0]) == "L'": return ['cdDet', ap_pron(str(dep[0]), ora)] #mirem quin el gènere per tornar el pronom corresponent
                else: return ['cdDet', str(dep[0])]
    #mirem si és indeterminat
    t = 0
    
    if str(tkpar) in prp: return [] #si la paraula és una preposicó, retornem directament ja que no ens interessa

    if str(tkpar.pos_) in morph and dep == []: t = 1
    elif str(tkpar.pos_) in morph and str(dep[0]) in indef: t = 1
    elif str(tkpar.pos_) in morph and str(dep[0]) in quant: t = 1
    elif str(tkpar.pos_) in morph and str(dep[0].pos_) == 'NUM': t = 1
    if t == 1: return ['cdIndet', 'en']
            
    return []

def cp(tkpar, dep, ora): #si ens ha detectat obj i és adj, serà predicatiu per força. pot ser que detecti appos en el cas d'elegir i nomenar
    #aquesta última implementació no acaba de funcionar
    l = ["FER", "DIR", "ELEGIR", "NOMENAR"]
    pron = fullDep(dep)
    verb = ""
    for token in nlp(ora):
        if str(token.dep_) == "aux": verb += str(token) + " "
        if str(token.dep_) == "ROOT": verb += str(token)
    
    
    t = False
    for e in l:
        if verb in d[e]:
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

def ci(tkpar, dep, ora): 
    #he escrit una carta al diari != he escrit una carta al pere
    print(tkpar)
    pr = ['a', 'al', 'als', 'per a', 'per al', 'per als', 'per la', 'per les', "per l'", 'a el', 'a la', 'a els', 'a les', 'per a el', 'per a la', 'per a els', 'per a les']
    prp = ['a', 'per', 'al', 'als']
    sig = ["'", "-"]
    t = False
    l = ora.split()
    for e in l:
        for s in sig:
            if s in e: 
                l.remove(e)
                l += e.split(s)
    print(l)
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


def cop(par, tkpar, dep, ora, semb):
    #estic ajustant tot el que no ha de sortir a la frase
    #va diferent si el verb és semblar (excepció del model)

    if semb == False:
        for token in nlp(ora):
            if token.dep_ == 'ROOT':
                l = [child for child in token.children]
                l1 = []
                l2 = [child for child in token.children]
                for i, e in enumerate(l):
                    if str(e.dep_) != 'nsubj':
                        l1.append(e)
                        l2.append(e)
                l = l1
                '''
                if par in l:
                    l2.pop(l.index(par))
                    l2.append(token)
                    l = l2
                '''

    else:
        for token in nlp(ora):
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
    dep = fullDep(dep)
    #print(dep, par)
    #miro el tipus de atr i retorno el pronom corresponent

    if semb == True: 
        atr = "atr1"
    else : atr = "atr"
    proDet = ["el", "la", "els", "les", "l'"]
    l = ora.split()
    p_1 = l.index(par)+1 #posició de la següent paraula al verb
    if l[p_1] in proDet:
        if l[p_1] == "l'" or l[p_1] == "L'": return [atr, ap_pron(l[p_1], ora), dep] #mirem quin el gènere per tornar el pronom corresponent
        else: return [atr, l[p_1], dep]
    else:
        return [atr, 'ho', dep]


def cop_semb(tkora, token): #l'spacy no detecta sembla com a verb copulatiu, llavors he de fer hardcode perquè el detecti
    if str(token) in d['SEMBLAR']: return True
    else: return False
    #FUNCIÓ QUE SEGURAMENT S'HAURÀ DE POLIR

def pos_comp(tkora, token1): #mirem que el complement no sigui un complement del nom 
    #print(tkora, token1)
    
    for token in tkora:
        child = [child for child in token.children]
        for i, c in enumerate(child):
            child[i] = str(c)

        if token != token1 and str(token.dep_) != 'ROOT':
            if str(token1) in child: return True
    return False

def fullDep(dep):
    l = []
    for e in dep:
        l.append(e)
        child = [f for f in e.children]
        if child != []:
            for el in child:
                dep.append(el)
    return l

def crv(tkpar, dep):
    print (tkpar, dep)
    pr = ["a", "de", "en", "amb", "per"]
    for e in dep:
        if str(e) in pr: 
            if str(e) == "de": return ["crv", "hi"]
            else: return ["crv", "en"]

    return []

def obj(par, tkpar, dep, ora):
    pron = []
    pron = cd(par, tkpar, dep, ora)
    if pron == []: pron = cp(tkpar, dep, ora)
    if pron == []: pron = ci(tkpar, dep, ora)
    if pron == []: pron = crv(tkpar, dep)
    if pron == []: #me l'estic jugant, (en cas que no sigui res del d'abans ha de ser cc) no estic segur que això funcioni en tots els casos
        if len(dep) >= 1:
            if str(dep[0]) == 'de': pron = ['cc', 'en'] #faltaria comprovar que fos de lloc
            else: pron = ['cc', 'hi'] 

    pron.append(fullDep(dep))
    return pron

def pos_cc(par): #funció de prova, no crec que funcioni

    l = ["advmod", "obl", "nmod"]

    if str(par.dep_) in l: return True
    else: return False

def mod_dep(tkora, child, token): 
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

def main(s):
    d = {
        'em' : ['em', "m'", '-me', "'m"],
        'et' : ['et', "t'", '-te', "'t"],
        'es' : ['es', "s'", '-se', "'s"],
        'en' : ['en', "n'", '-ne', "'n"],
        'el' : ['el', "l'", '-el', "'l"],
        'la' : ['la', "l'", '-la', "-la"], #paraula femenina primera sil·laba àtona (h, hi, u, hu)
        'ens' : ['ens', "ens", '-nos', "'ns"],
        'us' : ['us', "us", '-vos', "-us"],
        'els' : ['els', "els", '-los', "'ls"],
        'les' : ['les', "les", '-les', "-les"],
        'li' : ['li', "li", '-li', "-li"],
        'ho' : ['ho', "ho", '-ho', "-ho"],
        'hi' : ['hi', "hi", '-hi', "-hi"],
    }
    cpp = ['amod', 'appos', 'nsubj']
    l = []
    t = False
    v = False
    for token in nlp(s):
        child = [child for child in token.children]
        #print("inicial", child)
        #child = mod_dep(nlp(s), child, token)
        #print("modificat", child)
        print(token, token.morph, token.pos_, token.dep_, child)
        if pos_comp(nlp(s), token) == False:
            for e in d.keys():
                if str(token) in d[e]: 
                    l.append(['pron', str(token), child])
                    print (1)
                    v = True

            if v == False:
                if str(token.dep_) == 'obj': 
                    l.append(obj(str(token), token, child, s))
                    t = False
                elif str(token.dep_) == 'cop': 
                    l.append(cop(str(token), token, child, s, False))
                    t = False
                elif str(token.dep_) == 'ROOT' and cop_semb(nlp(s), token): 
                    l.append(cop(str(token), token, child, s, True))
                    t = False
                elif str(token.dep_) in cpp:
                    l.append(cp(token, child, s))
                    print(l)

            #si no hem afegit res en aquesta paraula, comprovem que no sigui cc
            #if t == False and pos_cc(token): l.append(['cc', 'hi', child])
        v = False


    # l = [tipusDeComp, pronom, [dependències]]

    for i, e in enumerate(l):
        if e == []: l.pop(i)
    
    print(l)
    
    if (len(l) == 1 and l[0] == "res") == False:
        if 'res' in l: l.pop(l.index('res'))
        if len(l) == 1: pron_frase(l, s, nlp(s), False)
        elif len(l) == 2: bin_pron_frase(l, s, nlp(s))
        #print(l)
    else: print("NO HE TROBAT RES A PRONOMINALITZAR EN AQUESTA FRASE")

def nova_S(s):
    s1 = ""
    for e in s: s1 += e.lower() 
    if s1[-1] == '.': s1 = s1[:-1]
    return s1
 
s = "Compra això del mercat" 
while s != "":
    s = nova_S(s) #la passem a minúscules
    main(s)
    s = input()
