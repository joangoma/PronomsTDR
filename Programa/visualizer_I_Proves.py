import spacy
from spacy import displacy
import sys
#import numpy as np
#import pandas as pd


nlp = spacy.load("ca_base_web_trf")
doc = nlp("el nen va a comprar tres pomes al mercat")

#FUNCIÓ QUE M'AJUDA A VEURE L'ESTROCUTRA DE L'ANÀLISI
def frases():
    line = "El joan sembla un bon noi"
    while line != "":
        for token in nlp(line):
            print(token, token.dep_, token.pos_, [child for child in token.children])
        line = input()
        line = line.rstrip()
        line = line.lstrip()

    #displacy.serve(nlp(line), style="dep")
#frases()


#FUNCIONS QUE M'AJUDEN A FICAR CONJUGACIONS VERBALS A LLISTES DE MANERA FÀCIL
def inputV():
    l = []
    s = ""
    s = str(input())
    while s != "":
        s = s.rstrip()
        s = s.lstrip()
        l.append(s)
        s = str(input())
    print(l)
    
#inputV()

