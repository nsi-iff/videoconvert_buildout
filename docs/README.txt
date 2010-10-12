VideoConvert Buildout

Arquitetura

Como pode ser visto no pacote nsi.videoconvert o sistema consiste em um
webservice (xmlrpc) hostiado por padrão na porta 8080 na url
http://usuario:senha@localhost:8080/xmlrpc. O serviço contém uma função
“convert” que é reponsável por colocar o vídeo em uma fila para ser convertido e
retorna para o usuário o UID onde o vídeo convertido se encontrará.
Então os slaves iniciados retiram o UID da fila, procuram pelo vídeo
correspondente no SAM, recuperam, convertem e guardam novamente o vídeo
convertido no SAM naquele UID.
O usuário então pergunta ao servidor se o vídeo daquele UID já está convertido
usando a função "done". Caso positivo ela retorna True, caso contrário, False.
--------------------
Bibliotecas

- Cyclone
Cyclone é um fork do Tornado, um webserver criado originalmente pelo FriendFeed,
que foi comprado pelo Facebook mais tarde e teve seu código aberto. É baseado no
Twisted e tem suporte a bancos noSQL, como MongoDB e Redis, XMLRPC e JsonRPC,
além de um cliente HTTP assíncrono.

- txredisapi
É uma API que promove acesso assíncrono ao banco de dados Redis, feita em cima do Twisted.

- nsi.multimedia
API criada pelo próprio NSI para fazer converter qual vídeo para o formato ogm.
--------------------
Instalação

Assumindo que o SAM já está devidamente instalado e iniciado na máquina, criar
 um ambiente virtual usando Python 2.6 e sem a opção no-site-packages e com o
 mesmo ativado executar “make” na pasta do buildout.
--------------------
Executando

Na pasta do buildout do SAM, executar: “bin/samctl start”, adicionar um usuário
para o VideoConvert com: “bin/add-user.py video convert” e na pasta do buildout
do VideoConvert executar: “bin/videoconvert_ctl start” e "bin/restmq". Tudo deverá estar
funcionando normalmente (caso contrário me mande um e-mail).

Lembrando que estes passos somente colocam o webservice e a fila de conversão
online. Para rodar uma instância do slave de conversão, executar "etc/slave.py".
--------------------
Rodando os testes

Com o SAM em execução, adicionar o usuário “video”, com senha “convert” nele
utilizando: “bin/add-user.py video convert”. Depois na raiz do buildout do
VideoConvert executar: “make test”.
--------------------
Consumindo o serviço manualmente (usando Python)

Com os dois serviços devidamente iniciados (SAM e VideoConvert), abrir um
terminal Python. Da biblioteca “xmlrpclib” importar a classe “Server” e da
classe “base64” importar “b64encode” e “decodestring”. Criar uma instância da
classe “Server”, passando como parâmetro o endereço do serviço
(http://video:convert@localhost:8080/xmlrpc, e lembrar de adicionar o usuário).
Ler um arquivo de vídeo do disco e codifiça-lo usando a função “b64encode”.
Chamar a função “convert” do objeto criada anteriormente passando como parâmetro
o vídeo codificado em base 64. A função retornará um uid (id único) onde se
encontrará o vídeo convertido. Se algum slave estiver sendo executado, ele
converterá o vídeo automaticamente. Chamar a função "done" passando o UID para
o saber se o vídeo já foi convertido com sucesso.
Para recuperar o vídeo, criar um novo objeto da classe "Server" passando como
parâmetro o endereço do servidor de armazenamento e chamar a função "get" para
obter o dicionário com os dados do vídeo como string. Aplicar a função "eval"
nele para transformá-lo em um objeto Python.

