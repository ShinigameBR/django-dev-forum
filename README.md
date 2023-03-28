DevForum
==========================

Este é um fórum para desenvolvedores construído em Django que permite a criação de salas de conversas e discussão de tópicos relacionados ao desenvolvimento de software. A aplicação também possui uma API para acesso às salas de conversas.

Funcionalidades
---------------

-   Criação de salas de conversas;
-   Criação de tópicos;
-   Discussão com outros usuários;
-   API para visualização das salas de conversas.

Pré-requisitos
--------------

-   Python 3.6 ou superior
-   Django 3.0 ou superior

Como utilizar
-------------

1.  Clone o repositório:

`git clone https://github.com/seu_usuario/nome_do_repositorio.git`

1.  Crie e ative um ambiente virtual:


`python -m venv venv
source venv/bin/activate`

1.  Instale as dependências do projeto:


`pip install -r requirements.txt`

1.  Execute as migrações do banco de dados:

`python manage.py migrate`

1.  Inicie o servidor:

`python manage.py runserver`

1.  Acesse o fórum em seu navegador em:

`http://localhost:8000/`

API
---

Para visualizar as salas de conversas através da API, acesse:

`http://localhost:8000/api/`

A API retorna dados em formato JSON.

Contribuindo
------------

Contribuições são sempre bem-vindas! Se você deseja contribuir com este projeto, siga os passos abaixo:

1.  Faça um fork deste repositório;
2.  Crie uma nova branch com a sua feature: `git checkout -b minha-feature`;
3.  Faça as alterações necessárias no código;
4.  Adicione suas alterações: `git add .`;
5.  Faça o commit das suas alterações: `git commit -m "Minha nova feature"`;
6.  Faça o push para a branch: `git push origin minha-feature`;
7.  Abra um Pull Request para este repositório.
