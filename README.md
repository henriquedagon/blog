# Desafio SuperSim - Blog

Está em desenvolvimento um blog com as seguintes funcionalidades:
- Como adminstrador, quero criar novas postagens com título, categorias e conteúdo, além de uma foto de capa;
- Como leitor, quero ver as postagens existentes;
- Como leitor, quero compartilhar os conteúdos em mídias sociais ou através de links;
- Como leitor, quero filtrar postagens por categoria;

------------------------------------------------------------------------------------

As tecnologias:
- O front-end está sendo desenvolvido em React
- O back-end está sendo desenvolvido em Python por ser uma linguagem que contém diversos frameworks e uma ampla possibilidade bibliotecas. 
- A API foi desenvolvida em Flask por ser um framework bem leve, assim muito boa para aplicações pequenas.
- O banco de dados escolhido foi o Postgres por ser um banco leve, bom para pequenos projetos.

-----------------------------------------------------------------------------------

O desenvolvimento até o momento:
- Uma tela com cabeçalho e botão de login na parte superior e os post já criados.
- Uma tela com cabeçalho e botão de login na parte superior e formulário de adicionar posts.

- A API contém um swagger em http:localhost:5000/api/ e foram criadas as view:
    - add_post - view para adicionar posts
    - files - view para retornar arquivos
    - get_token - view para retorna o token de autenticação
    - posts - view para retornar arquivos

- O banco de dados contém 3 tabelas:
    - Tabela de posts com as colunas: id, title, post, categories, img_filename, image_name, author, date
    - Tabela de usuário com as colunas: usr, pass, grp
    - Essa tabela contém os usuários: "usuario" (senha: 1234, grupo:1) e "administrador" (senha: 12345, grupo:2)
    - tabela descritora de grupos com as colunas: grp, descrition
    
 -----------------------------------------------------------------------------------

Próximos passos:
- Terminar o roteamento das páginas.
- Criar os containers Docker com Dockerfile e docker-compose.
- Adicionar links de compartilhameto.
- Fazer filtros das postagens por categoria.
