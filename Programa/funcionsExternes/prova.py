import spacy
from spacy import displacy
#import numpy as np
#import pandas as pd

nlp = spacy.load("ca_base_web_trf")

#llegint totes les frases del fitxer txt i afegint-les a un diccionari
dic = {}
l = []
r = open('c:/JOAN/TDR/Pronominalització/Part pràctica/Gramatica/Programa/main.txt', 'r')
for line in r:
  for token in nlp(line):
    print (token, '||', token.dep_, '||', [child for child in token.children], '||' , token.morph)
'''
i, maxL = 0, 0
for line in r:
    line.rstrip()
    line.lstrip()
    if line[0] == '-':
      dic[i] = line
    else:
      s = nlp(line)
      l = []
      for token in s:
          l += [str(token) + " | " + str(token.dep_)]
          print (token, '||', token.dep_, '||', [child for child in token.children], '||' , token.morph)
      l = l[:-1] #elimino el salt de linia
      dic[i] = l
      if len(l) > maxL: maxL = len(l)
      i += 1

#aquí estic ajustant les llargades de les llistes per poder fer el dataframe
d1 = {}
i = 0
for e in dic.values():
    if len(e) < maxL:
        for i in range(len(e), maxL): e.append('----')
'''
