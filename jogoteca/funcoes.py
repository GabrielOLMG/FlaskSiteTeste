import pandas as pd
import numpy as np

#---------------------------------------------------------------------------------------------------------------------------------------#
#---------------------------------------------------------AberturaDeArquivos------------------------------------------------------------#

class Filme_geral:
    def __init__(self, nome, atores,classificacao): #contrutor
        self.nome = nome
        self.atores = atores
        self.classificacao = classificacao

def arq_carrega():
    arquivo_completo = pd.read_csv("arquivos/movie.csv",encoding = "utf-8")
    arq = arquivo_completo[['title','description','actors']]

    lista_filmes_completa = []

    for title,actors,desc in zip(arq['title'],arq['actors'],arq['description']):
        nv_filme = Filme_geral(title,actors,desc)
        lista_filmes_completa.append(nv_filme)
    return lista_filmes_completa