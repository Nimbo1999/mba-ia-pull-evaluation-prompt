"""
Script para fazer pull de prompts do LangSmith Prompt Hub.

Este script:
1. Conecta ao LangSmith usando credenciais do .env
2. Faz pull dos prompts do Hub
3. Salva localmente em prompts/bug_to_user_story_v1.yml

SIMPLIFICADO: Usa serialização nativa do LangChain para extrair prompts.
"""

import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from langchain import hub
from langchain_core.load import dumpd
from utils import save_yaml, check_env_vars, print_section_header

load_dotenv()

LANGSMITH_REPOSITORY = "leonanluppi/bug_to_user_story_v1"

def pull_prompts_from_langsmith(repository):
    prompt = hub.pull(repository)
    print(prompt)
    return prompt


def main():
    """Função principal"""
    print_section_header("Iniciando Pull de Prompts do LangSmith Prompt Hub")

    required_env_vars = [
        'LANGSMITH_ENDPOINT',
        'LANGSMITH_API_KEY',
        'USERNAME_LANGSMITH_HUB',
    ]
    if not check_env_vars(required_env_vars):
        print("Variáveis de ambiente necessárias não estão definidas. Verifique o .env.")
        return 1

    print_section_header(f"Fazendo pull do repositório: {LANGSMITH_REPOSITORY}")
    prompt_pull_data = pull_prompts_from_langsmith(LANGSMITH_REPOSITORY)

    if not prompt_pull_data:
        print("Falha ao obter dados do prompt.")
        return 1

    output_path = Path("prompts") / f"{LANGSMITH_REPOSITORY.split('/')[-1]}.yml"
    prompt_dict = dumpd(prompt_pull_data)
    if save_yaml(prompt_dict, output_path):
        print_section_header(f"Prompt salvo com sucesso em: {output_path}")
        return 0
    else:
        print_section_header("Falha ao salvar o prompt.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
