#---------------------------------------------------------------------------------------------------------------------------------#
#-----------------------------------------------------Classes---------------------------------------------------------------------#

class Filme:
    def __init__(self, nome,classificacao,id=None): #contrutor
        self.id = id
        self.nome = nome
        self.classificacao = classificacao

class Usuario:
    def __init__(self,id,nome,senha):
        self.tabela = id
        self.id = id
        self.nome = nome
        self.senha = senha

class Filme_Geral:
    def __init__(self,id,title,rating,year,users_rating,votes,metascore,img_url,countries,languages,actors,genre,tagline,description,directors,runtime,imdb_url):
        self.id = id
        self.title = title
        self.rating = rating
        self.year = year
        self.users_rating = users_rating
        self.votes = votes
        self.metascore = metascore
        self.img_url = img_url
        self.countries = countries
        self.languages = languages
        self.actors = actors
        self.genre = genre
        self.tagline = tagline
        self.description = description
        self.directors = directors
        self.runtime = runtime
        self.imdb_url = imdb_url