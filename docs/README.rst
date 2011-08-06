VideoConvert Buildout

Arquitetura
-----------

Como pode ser visto no pacote "nsi.videoconvert" o sistema consiste em um webservice RESTful hostiado por padrão na porta 8080
na url "http://localhost:8080/". Ele responde aos verbos POST e GET. Cada verbo correspondendo a uma ação do serviço de granularização:
POST para submeter um vídeo, GET para verificar o estado da granularização. Todos os verbos recebem parâmetros no formato "json",
para melhor interoperabilidade com qualquer outra ferramenta.


POST
    Recebe em um parâmetro "video" o vídeo a ser convertido codificado em base64, para evitar problemas de encoding.
    Responde a requisição com as chaves onde estarão o vídeos e os grãos correspondentes a ele no SAM.
    É possível enviar uma URL para receber um "callback" assim que o vídeo for convertido. Caso o parêmtro "callback"
    seja fornecido, ao término da conversão, um dos workers realizará uma requisição para tal URL com o verbo
    POST, fornecendo no corpo dela uma chave "done" com valor verdadeiro e a chave "key", com a chave para acesso aos grãos.

GET
    Também é possível receber se um determinado vídeo já foi convertido fazendo uma requisição do tipo GET para o servidor,
    passando como parâmetro "key" a chave do vídeo que é retornada pelo método POST. O retorno será uma chave
    "done", com valor verdadeiro caso os grão estejam prontos, e falso para o contrário.


Bibliotecas
-----------

- Cyclone
Cyclone é um fork do Tornado, um webserver criado originalmente pelo FriendFeed,
que foi comprado pelo Facebook mais tarde e teve seu código aberto. É baseado no
Twisted e tem suporte a bancos noSQL, como MongoDB e Redis, XMLRPC e JsonRPC,
além de um cliente HTTP assíncrono.

- txredisapi
É uma API que promove acesso assíncrono ao banco de dados Redis, feita em cima do Twisted.

- nsi.multimedia
API criada pelo próprio NSI para fazer converter qual vídeo para o formato ogm.


Instalação
----------

Assumindo que o SAM já está devidamente instalado e iniciado na máquina, criar
um ambiente virtual usando Python 2.6 e sem a opção no-site-packages e com o
mesmo ativado executar “make” na pasta do buildout.


Executando
----------

Na pasta do buildout do SAM, executar: “bin/samctl start”, adicionar um usuário
para o VideoConvert com: “bin/add-user.py video convert” e na pasta do buildout
do VideoConvert executar: “bin/videoconvert_ctl start”.

É indispensável que o serviço de filas esteja ligado para que tudo funciona
perfeitamente. Para instalar o serviço de filas basta baixar o *servicequeue_buildout*
e rodar o  utilitário *make* contido nele. Depois, basta executar o comando
*bin/rabbitmq-server -detached* para ativar o serviço de filas.

Tudo deverá estar funcionando normalmente (caso contrário me mande um e-mail).



Rodando os testes
-----------------

Com o SAM em execução, adicionar o usuário “video”, com senha “convert” nele
utilizando: “bin/add-user.py video convert”. Depois na raiz do buildout do
VideoConvert executar: “make test”.

