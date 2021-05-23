import mysql.connector

conexao = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    port = 3306,
    password="mosegaw999",
    auth_plugin='mysql_native_password'
)

cursor = conexao.cursor()

cursor.execute('create database if not exists jogoteca')
cursor.execute('use jogoteca')
cursor.execute("""create table if not exists filme(
                id int(11) not null auto_increment,
                nome varchar(50) collate utf8_bin not null,
                ator varchar(40) collate utf8_bin not null,
                classificacao varchar(1) not null,
                primary key (id)
                )engine=innodb default charset=utf8 collate=utf8_bin"""
               )
cursor.execute("""create table if not exists usuario (
                id varchar(30) primary key not null,
                nome varchar(20) not null,
                senha varchar(8) not null
                )"""
               )

# inserindo usuarios

cursor.executemany(
    'INSERT INTO jogoteca.usuario (id, nome, senha) VALUES (%s, %s, %s)',
    [
        ('LucianMosegaw', 'Gabriel', '1221'),
        ('RodolfoHS', 'Rodolfo', '1221'),
        ('OverhaullBR', 'Brunno', '1221'),
        ('Talarico', 'Italo', '1221'),
    ])

cursor.execute('select * from jogoteca.usuario')
print(' -------------  Usuários:  -------------')
for user in cursor.fetchall():
    print(user[1])

# inserindo filmes
cursor.executemany(
    'INSERT INTO jogoteca.filme (nome, ator, classificacao) VALUES (%s, %s, %s)',
    [
        ('Harry Potter','Alguem1','1'),
        ('LOTR','Alguem2','1'),
        ('The Huntsman: Winters War','Alguem3','0'),
    ])

cursor.execute('select * from jogoteca.filme')
print(' -------------  Jogos:  -------------')
for filme in cursor.fetchall():
    print(filme[1])

# commitando senão nada tem efeito
conexao.commit()
conexao.close()