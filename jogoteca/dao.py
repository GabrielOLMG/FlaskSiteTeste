from models import Filme, Usuario, Filme_Geral
from flask import flash


#----------------------------------------------------------------------------------------------------------------------------#
'''SQL_FILMES'''
SQL_PROCURA_ID_FILME = 'select id from dadosfilme where title = %s' # procura id na tabela 'dadosfilme'
SQL_PROCURA_NOME_FILME = 'select title from dadosfilme where id = %s' # procura title na tabela 'dadosfilme'
SQL_PROCURA_EXISTENCIA_ID_FILME = 'select id_filme from notafilmeusuario where id_filme = %s and id_usuario = %s'
SQL_ADD_NOTAFILMEUSUARIO = 'insert into notafilmeusuario (id_usuario,id_filme,classificacao) values (%s,%s,%s)'
SQL_DELETA_NOTAFILMEUSUARIO =  'delete from notafilmeusuario where id_filme = %s' #deleta filme da tabela notafilmeusuario
SQL_IDS_FILME_DO_USUARIO = 'select id_filme from notafilmeusuario where id_usuario = %s'
SQL_PROCURA_ID_FILME_PARA_CLASSIFICACAO = 'select classificacao from notafilmeusuario where id_filme = %s and id_usuario = %s' #Procura o id do Filme na tabela 'notafilmeusuario' com o objetivo de alterar a classificacao dada
SQL_ATUALIZA_FILME = 'update notafilmeusuario set classificacao = %s, id_filme = %s  where id_filme = %s and id_usuario = %s'
#----------------------------------------------------------------------------------------------------------------------------#
'''SQL_USUARIOS'''
SQL_USUARIO_POR_ID = 'SELECT id, nome, senha from usuario where id = %s'
SQL_CRIA_USUARIO = 'INSERT into usuario (id,nome,senha) values (%s,%s,%s)'
#----------------------------------------------------------------------------------------------------------------------------#
class FilmeDao:
    def __init__(self, db):
        self.__db = db

    def salvar(self, filme,usuarioL):
        cursor = self.__db.connection.cursor()
        cursor.execute(SQL_PROCURA_ID_FILME,(filme.nome,))
        id = cursor.fetchone()
        cursor.execute(SQL_PROCURA_EXISTENCIA_ID_FILME,(filme.id,usuarioL))
        idV = cursor.fetchone()
        
        if (idV is not None ): # Caso o filme ja exista, ele vai atualizar ele com novos dados 
            cursor.execute(SQL_ATUALIZA_FILME,(filme.classificacao,id,filme.id,usuarioL))
        else:
            cursor.execute(SQL_ADD_NOTAFILMEUSUARIO,(usuarioL,id,filme.classificacao)) #add o filme na lista

        self.__db.connection.commit()
        return filme

    def listar(self, usuarioL):
        cursor = self.__db.connection.cursor()
        cursor.execute(SQL_IDS_FILME_DO_USUARIO,(usuarioL,)) #pego os ids
        lista = cursor.fetchall()

        if len(lista) == 0: #Caso o usuario nã tenha colocado nenhum filme
            return ()
        
        lista_ids = traduz_ids(lista)
        sql_code = 'select id,title,actors,description from dadosfilme where id  = '

        for id in lista_ids: # crio um codigo com todos os ids
            sql_code = sql_code + str(id)
            if id != lista_ids[-1]:
                sql_code = sql_code + ' or id = '
        
        cursor.execute(sql_code)
        filmes = traduz_filmes(cursor.fetchall())
        return filmes

    def busca_por_id(self, id,usuarioL): 
        cursor = self.__db.connection.cursor()
        cursor.execute(SQL_PROCURA_ID_FILME_PARA_CLASSIFICACAO,(id,usuarioL))
        classificacao = cursor.fetchone()
        cursor.execute(SQL_PROCURA_NOME_FILME,(id,))
        nome = cursor.fetchone()
        return Filme(nome[0],classificacao[0],id)
    def deletar(self, id,usuarioL):
        self.__db.connection.cursor().execute(SQL_DELETA_NOTAFILMEUSUARIO, (id, ))
        self.__db.connection.commit()

#----------------------------------------------------------------------------------------------------------------------------#
class UsuarioDao:
    def __init__(self, db):
        self.__db = db

    def buscar_por_id(self, id):
        cursor = self.__db.connection.cursor()
        cursor.execute(SQL_USUARIO_POR_ID, (id,))
        dados = cursor.fetchone()
        usuario = traduz_usuario(dados) if dados else None
        return usuario
    
    
    def salvar(self, usuario):
        cursor = self.__db.connection.cursor()
        if (cursor.execute(SQL_USUARIO_POR_ID, (usuario.id,))): # Caso o usuario ja exista, ele vai retornar null
            return 'erro'
        else:
            cursor.execute(SQL_CRIA_USUARIO, (usuario.id, usuario.nome, usuario.senha))
        self.__db.connection.commit()
        return usuario
    

#----------------------------------------------------------------------------------------------------------------------------#
def traduz_filmes(filmes):
    def cria_filme_com_tupla(tupla):
        return Filme(tupla[1], tupla[3], id=tupla[0])
    return list(map(cria_filme_com_tupla, filmes))



def traduz_ids(ids):
    def cria_filme_com_tupla(tupla):
        return tupla[0]
    return list(map(cria_filme_com_tupla, ids))



def traduz_usuario(tupla):
    return Usuario(tupla[0], tupla[1], tupla[2])

