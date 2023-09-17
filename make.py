

def criar_tabelas():
    from models import Base
    from sqlalchemy import create_engine
    from env import CONN
    engine = create_engine(CONN, echo=True)
    Base.metadata.create_all(engine)


def criar_pasta_temp():
    import os
    from env import directory_temp
    if not os.path.exists(directory_temp):
        os.makedirs(directory_temp)


def criar_arquivo_env():
    import os
    from dotenv import dotenv_values
    env_vars = {
        'key': 'sua_chave_aqui',
        'DEBUG': 'True',
        'environment': 'False'
    }

    # Caminho para o arquivo .env
    arquivo_env = '.env'

    # Se o arquivo .env já existir, faça backup das variáveis existentes
    if os.path.exists(arquivo_env):
        env_vars_existentes = dotenv_values(arquivo_env)
        env_vars.update(env_vars_existentes)

    # Escreva as variáveis no arquivo .env
    with open(arquivo_env, 'w') as env_file:
        for chave, valor in env_vars.items():
            env_file.write(f'{chave}={valor}\n')


def bootstrap():
    criar_pasta_temp()
    criar_tabelas()
    criar_arquivo_env()


if __name__ == '__main__':
    bootstrap()
