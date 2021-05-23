# FlaskSiteTeste

Meu primeiro site usando o flask, ainda tem muitas coisas para serem melhoradas. 
Cada usuario tem o seu login e tem a capacidade de add filmes vistos junto com a sua classificação pessoal, indo assim para a sua tabela de filmes vistos. Caso não tenha um login, é permitido a criação de um novo usuario. Este projeto esta ligado a um banco de dados, logo as informações não se perdem, mas ao mudar de pc são perdidas, ja que esta base de dados esta no meu pc principal.
Futuramente quero usar metodos de ML para poder recomendar filmes para os usuarios do site. 


Coisas a serem melhoradas:

Por ser meu primeiro programa com esta biblioteca, eu fiquei indeciso sobre oq fazer logo tem muitas variaveis relacionadas a jogos, que era minha primeira ideia. Por culpa disso,
tenho que refatorar o codigo para que não existam variaveis com nomes estranhos.

Ao entrar em http://127.0.0.1:5000/ pela primeira vez, ele da erro, ja que ele ja considera que tem um usuario quando na verdade não tem, logo tenho que criar uma pagina inicial
ou entrar em http://127.0.0.1:5000/login primeiro.
