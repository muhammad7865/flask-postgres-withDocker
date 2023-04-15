# flask-postgres-boilerplate

a flask api boilerplate with authentication backed by postgres

## app dependencies

- [flask](https://pypi.org/project/Flask/): python web framework
- [flask-sqlalchemy](https://pypi.org/project/Flask-SQLAlchemy/): sql toolkit / ORM
- [flask-migrate](https://pypi.org/project/Flask-Migrate/): sql migrations
- [flask-login](https://pypi.org/project/Flask-Login/): authentication helpers for flask
- [flasgger](https://github.com/flasgger/flasgger): used to generate the swagger documentation
- [apispec](https://apispec.readthedocs.io/en/latest/): required for the integration between marshmallow and flasgger
- [postgres](https://www.postgresql.org/): database

### system dependencies

you should only need to install or set these up once

#### python environment

- `brew install pipenv`
- `brew install pyenv`
- `brew install pyenv-virtualenv`
- optional for `oh-my-zsh`:
  - `git clone https://github.com/mattberther/zsh-pyenv ~/.oh-my-zsh/custom/plugins/zsh-pyenv`
  - update `.zshrc`

    ```shell
    plugins=(
        ...
        zsh-pyenv
        pipenv
    )
    ```

#### postgres

- install with homebrew

    ```shell
    brew install postgresql@14
    ```

- start

    ```shell
    brew services start postgresql@14
    ```

- run config script

    ```shell
    make db-setup
    ```

## starting the application

0. checkout lastest from remote repository

1. install/update requirements

    ```shell
    pipenv install
    ```

2. check for and run migrations

    ```shell
    pipenv run pythom -m flask db check
    pipenv run python -m flask db upgrade # only if necessary
    ```

3. start the server

    ```shell
    pipenv run python -m flask run
    ```

## Tests

The code is covered by tests, to run the tests please execute

```shell
pipenv run python -m unittest
```
