from flask import Flask,render_template, request, redirect, session, flash, url_for
from models import Filme, Usuario,Filme_Geral
from dao import FilmeDao, UsuarioDao
from flask_mysqldb import MySQL

app = Flask(__name__)
app.secret_key = 'brisingr' #chave que o flask usa para criptografar de forma q ninguem consiga alterar as informaçoes do usuario

app.config['MYSQL_HOST'] = "127.0.0.1"
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = "mosegaw999"
app.config['MYSQL_DB'] = "jogoteca"
app.config['MYSQL_PORT'] = 3306



#---------------------------------------------------------------------------------------------------------------------------------#
#---------------------------------------------------------------------------------------------------------------------------------#
db = MySQL(app)
filme_dao = FilmeDao(db)
usuario_dao = UsuarioDao(db)

#---------------------------------------------------------------------------------------------------------------------------------#
#-----------------------------------------------------ROTAS-----------------------------------------------------------------------#

@app.route('/') #configuração da rota(https://www.dominio/rota)
def index(): #Esta função esta ligada com a rota definida acima
    usuarioL = session['usuario_logado']
    if usuarioL == None:
        return redirect(url_for('login', proxima = url_for('index')))
    else:
        lista_filmes = filme_dao.listar(usuarioL)
        msg = "Proprietario/a da tabela: " + usuarioL
    return render_template('index.html',
                            titulo = 'Filmes', 
                            Filmes = lista_filmes,
                            Us = msg) # chama o html

@app.route('/addFilme')
def addF():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima = url_for('addF'))) #diz que  a pagina que queremos ir apos logar é addFilme|com o url_for, deixamos dinamico d forma que n temos q alterar o codigo caso a root mude, então apenas colocamos o nome da função da root e as coisas q serão enviadas(igual ao render_template)

    return render_template('add.html',
                            titulo = 'Novo Filme')

@app.route('/criar', methods = ['POST']) #com o methods eu estou dizendo que tipo de metodo ele vai receber
def criar():
    nome = request.form['nome']
    classificacao = request.form['classificacao']
    filme = Filme(nome,classificacao)
    usuarioL = session['usuario_logado']
    filme_dao.salvar(filme,usuarioL)
    return redirect(url_for('index')) #ao criar o filme, ele vai redirecionar para a pagina inicial

@app.route('/registro')
def registro():
    return render_template('registro.html')

@app.route('/cadastrar', methods = ['POST'])
def cadastrar():
    nome = request.form['nome']
    id = request.form['id']
    senha = request.form['senha']
    novoUsuario = Usuario(id,nome,senha)
    if usuario_dao.salvar(novoUsuario) == 'erro':
        flash('Usuario Já Cadastrado antes!!!')
        return redirect(url_for('registro'))
    else:
        return redirect(url_for('login'))

@app.route('/login')
def login():
    proxima = request.args.get('proxima') #pegamos as informaçoes q  ficam visíveis junto com a URL na barra de endereços do browser.
    return render_template('login.html', proxima=proxima)

@app.route('/autenticar', methods = ['POST',])
def autenticar():
    usuario = usuario_dao.buscar_por_id(request.form['usuario'])
    if usuario:
        if request.form['senha'] == usuario.senha:
            session['usuario_logado'] = usuario.id
            flash('Ola {0}!!!'.format( usuario.nome) ) #vai mostrar uma msg rapida dizendo q foi logado
            proxima_pagina =  request.form['proxima']
            if proxima_pagina ==  'None':
                return redirect(url_for('index'))
            else:
                return redirect(proxima_pagina)    
        else:
            flash('Senha incorreta')
            return redirect(url_for('login'))
    else:
        flash('Usuario não cadastrado no sistema')
        return redirect(url_for('registro'))

@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Nenhum usuario logado')
    return redirect(url_for('index'))

@app.route('/edit/<int:id>') #estou recebendo o id do jogo 
def edit(id):
    usuarioL = session['usuario_logado']
    if 'usuario_logado' not in session or usuarioL == None:
        return redirect(url_for('login', proxima = url_for('edit',id= id))) 
    filme = filme_dao.busca_por_id(id,usuarioL)
    return render_template('edit.html', titulo = "Editando Jogo", filme = filme)

@app.route('/atualizar', methods = ['POST']) #com o methods eu estou dizendo que tipo de metodo ele vai receber
def atualizar():
    usuarioL = session['usuario_logado']
    nome = request.form['nome']
    classificacao = request.form['classificacao']
    filme = Filme(nome,classificacao, id=request.form['id'])
    filme_dao.salvar(filme,usuarioL)
    return redirect(url_for('index')) #ao criar o filme, ele vai redirecionar para a pagina inicial

@app.route('/delet/<int:id>')
def delet(id):
    usuarioL = session['usuario_logado']
    if 'usuario_logado' not in session or usuarioL == None:
        return redirect(url_for('login')) 
    filme_dao.deletar(id,usuarioL)
    flash('O jogo foi removido com sucesso!')
    return redirect(url_for('index'))

#---------------------------------------------------------------------------------------------------------------------------------#
#-----------------------------------------------------DandoStart------------------------------------------------------------------#


app.run(debug = True) #com debug = True, eu n preciso ficar executando o codigo toda hora, basta salvar e pronto