# Projeto de Autenticação com Flask

Este é um projeto de exemplo focado exclusivamente em autenticação de usuários utilizando o microframework Flask. O projeto implementa funcionalidades de registro, login e logout, além de utilizar criptografia de senhas para garantir a segurança dos dados e MySQL com Docker.

## Funcionalidades

- **CRUD de Usuário**: Cadastro de novos usuários com verificação de dados e controle de permissões.
- **Login**: Autenticação de usuários cadastrados.
- **Logout**: Encerramento de sessão de forma segura.
- **Hashing de Senhas**: Senhas são armazenadas com hash (bcrypt) para segurança.
- **Proteção de Rotas**: Algumas rotas são acessíveis apenas para usuários autenticados.

## Tecnologias Utilizadas

- **Flask:** Framework principal para desenvolvimento da aplicação web.
- **Flask-SQLAlchemy:** ORM (Object-Relational Mapper) para gerenciamento do banco de dados.
- **Flask-Login:** Biblioteca para gerenciar a autenticação de usuários.
- **Docker e Docker Compose:** Ferramenta de containerização para fácil configuração e deploy.
- **pymysql:** Driver para conexão com bancos de dados MySQL.
- **bcrypt:** Biblioteca para hashing de senhas, garantindo a segurança das credenciais dos usuários.

## Notas Técnicas
- **Hashing de Senhas:** Senhas são criptografadas com `bcrypt` antes de serem armazenadas.
- **Gerenciamento de Sessões:** `Flask-Login` controla o status de autenticação do usuário.
- **Banco de Dados MySQL:** O projeto utiliza `Flask-SQLAlchemy` para conectar-se ao MySQL com o driver `pymysql`.

## Configuração do Ambiente
### Pré-requisitos
- **Docker** e **Docker Compose** instalados.

### Instalação

1. **Clone o repositório**:
   ```bash
   git clone https://github.com/matheusfd3/tasks-flask-crud.git
   
   cd sample-flask-auth
   ```
2. **Instale as dependências:**:
    ```bash
    pip install -r requirements.txt
    ```
3. **Configurações**:
- Configure o arquivo `docker-compose.yml`
- Lembre-se de mudar o `path`
    ```yml
    volumes:
      - (Seu path aqui)/mysql:/var/lib/mysql
    ```
4. **Inicie o container docker com nosso MySQL:**
    ```bash
    docker-compose up
    ```
5. **Use o flask shell para criar suas tabelas:**
- Na raiz do projeto
    ```bash
    flask shell
    ```
    ```bash
    db.create_all()
    ```
    ```bash
    db.session.commit()
    ```
    ```bash
    exit()
    ```
6. **Inicie o servidor:**
    ```bash
    python app.py
    ```

## Endpoints

Você pode testar esses endpoints usando o [Postman](https://www.postman.com/) ou outra ferramenta de sua preferência. Usuário possuem os campos `id`, `username`, `password` e `role`("user" ou "admin"):

| Método | Endpoint              | Descrição                          |
|--------|-----------------------|------------------------------------|
| POST   | `/login`              | Realiza o login do usuário         |
| GET    | `/logout`             | Realiza o logout do usuário        |
| POST   | `/user`               | Cria um novo usuário               |
| GET    | `/user/<int:user_id>` | Retorna informações de um usuário  |
| PUT    | `/user/<int:user_id>` | Atualiza informações de um usuário |
| DELETE | `/user/<int:user_id>` | Deleta um usuário                  |

