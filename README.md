# Install Deps

In order to run the pipenv is necessary. To install it just executa `pip install pipenv`
After installed it shoud be run the install of dependencies with the following command.

`pipenv install`

# Run

`pipenv run start`

# Routes

- [POST]"/user" (open)
- [POST]"/user/auth" (open)
- [GET]"/language/<language>/namespace/<namespaceName>" (authenticated)
- [POST]"/language/<language>/namespace/<namespaceName>" (authenticated)
- [POST]"/language/<language>/namespace" (authenticated)
- [GET]"/language/<language>/namespaces" (authenticated)

# MVP 

API feita em python com flask para projeto de MVP do curso de pós graduacão em engenharia de software PUC-RIO

# Descricao: 

Trata-se de uma API MVP para um CRM de gerenciamento de entradas de configuracao para internacionalizacão. Ao internacionalizar um aplicativo ha duas formas de gerenciar o texto, a primeira utilizando um arquivo local junto ao App internacionalizado no formato JSON e a outra e ter um CRM que sirva o JSON através de uma API. 

Caso voce abra a pagina `main.html` automaticamente sera redirecionado para pagina de login onde devera criar uma senha com email + senha de 6 digitos.